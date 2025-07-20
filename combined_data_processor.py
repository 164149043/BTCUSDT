"""
组合数据处理模块
功能：合并原始数据和技术指标数据，生成包含完整信息的CSV文件
输出：包含日线原始数据和技术指标的合并数据集
"""

import pandas as pd
import os
import sys
from pathlib import Path
from datetime import datetime
from config import DATA_DIR, RAW_DATA_FILENAME, INDICATORS_FILENAME, COMBINED_FILENAME, SYMBOL, get_filenames

def combine_data(raw_filename=None, indicators_filename=None, combined_filename=None, timeframe_name=None):
    """
    主函数：合并原始数据和技术指标数据
    参数:
        raw_filename: 原始数据文件名
        indicators_filename: 指标数据文件名
        combined_filename: 组合数据文件名
        timeframe_name: 时间周期名称
    返回:
        Path: 合并后文件的路径对象
        None: 如果合并失败
    """
    print("\n" + "=" * 50)
    print(f"开始合并原始数据和技术指标数据 - {timeframe_name or '日线'}")
    print("=" * 50)

    # 1. 确定文件路径
    raw_path = DATA_DIR / (raw_filename or RAW_DATA_FILENAME)
    if not raw_path.exists():
        print(f"❌ 错误: 原始数据文件不存在 - {raw_path}")
        return None

    try:
        raw_df = pd.read_csv(raw_path, encoding='utf-8-sig')
        print(f"✅ 成功加载原始数据, 共 {len(raw_df)} 条记录")
    except Exception as e:
        print(f"❌ 加载原始数据失败: {e}")
        return None

    # 2. 加载技术指标数据
    indicators_path = DATA_DIR / (indicators_filename or INDICATORS_FILENAME)
    if not indicators_path.exists():
        print(f"❌ 错误: 技术指标文件不存在 - {indicators_path}")
        return None

    try:
        indicators_df = pd.read_csv(indicators_path, encoding='utf-8-sig')
        print(f"✅ 成功加载技术指标数据, 共 {len(indicators_df)} 条记录")
    except Exception as e:
        print(f"❌ 加载技术指标数据失败: {e}")
        return None

    # 3. 数据预处理
    print("🔄 数据预处理中...")

    # 查找时间列（兼容不同列名）
    time_col = None
    for col in ['open_time', '日期', '时间', 'timestamp']:
        if col in raw_df.columns and col in indicators_df.columns:
            time_col = col
            break

    if not time_col:
        print("❌ 错误: 无法找到共同的时间列")
        return None

    # 统一时间格式
    for df in [raw_df, indicators_df]:
        df[time_col] = pd.to_datetime(df[time_col])
        df.sort_values(time_col, inplace=True)
        df.reset_index(drop=True, inplace=True)

    # 4. 合并数据
    print("🔀 合并数据中...")

    # 识别重复列（除了时间列）
    duplicate_cols = [col for col in indicators_df.columns
                     if col in raw_df.columns and col != time_col]

    if duplicate_cols:
        print(f"➖ 移除重复列: {', '.join(duplicate_cols)}")
        indicators_df = indicators_df.drop(columns=duplicate_cols)

    # 执行合并（内连接确保数据一致性）
    try:
        combined_df = pd.merge(
            raw_df,
            indicators_df,
            on=time_col,
            how='inner',
            validate='one_to_one'
        )

        # 定义要移除的列 (清理多余和中间计算数据)
        columns_to_remove = [
            # 信号分析列 (文本信号，非数值数据)
            '计算时间',
            'MA_Signal',
            'MACD_Signal_Analysis',
            'RSI_Signal',
            'BB_Signal',
            'Stoch_Signal',
            '综合信号',

            # 中间计算数据 (非核心指标)
            'BB_Squeeze',           # 布林带挤压标志 (您要求移除)
            'BB_Width',             # 布林带宽度 (中间计算数据)

            # 重复的MA列 (保留标准命名)
            'MA8', 'MA21', 'MA55',  # 移除动态命名的MA，保留MA20, MA50, MA_LONG

            # 其他可能的多余列
            'MACD_Long_Hist',       # 如果存在长期MACD柱状图
            'RSI_Extra_Long',       # 如果存在超长期RSI且不需要
        ]

        # 移除不需要的列（如果存在的话）
        existing_columns_to_remove = [col for col in columns_to_remove if col in combined_df.columns]
        if existing_columns_to_remove:
            combined_df = combined_df.drop(columns=existing_columns_to_remove)
            print(f"🗑️ 已移除列: {', '.join(existing_columns_to_remove)}")

        # 数据清理和验证
        combined_df = clean_and_validate_data(combined_df)

        # 按时间排序
        combined_df.sort_values(time_col, ascending=True, inplace=True)
        combined_df.reset_index(drop=True, inplace=True)
    except Exception as e:
        print(f"❌ 数据合并失败: {e}")
        return None

    # 5. 保存结果
    combined_path = DATA_DIR / (combined_filename or COMBINED_FILENAME)

    try:
        # 确保目录存在
        combined_path.parent.mkdir(parents=True, exist_ok=True)

        # 保存为CSV（兼容中文Excel）
        combined_df.to_csv(combined_path, encoding='utf-8-sig', index=False)

        print(f"✅ 数据合并完成! 文件保存至: {combined_path}")
        print(f"📊 合并后数据维度: {len(combined_df)} 行 × {len(combined_df.columns)} 列")

        return combined_path
    except Exception as e:
        print(f"❌ 文件保存失败: {e}")
        return None

def clean_and_validate_data(df):
    """
    清理和验证组合数据
    参数:
        df: 组合后的DataFrame
    返回:
        DataFrame: 清理后的数据
    """
    print("🧹 数据清理和验证中...")

    # 1. 检查重复列
    duplicate_columns = df.columns[df.columns.duplicated()].tolist()
    if duplicate_columns:
        print(f"⚠️ 发现重复列名: {duplicate_columns}")
        df = df.loc[:, ~df.columns.duplicated()]
        print("✅ 已移除重复列")

    # 2. 检查空值过多的列 (超过50%为空值的列)
    null_percentage = df.isnull().sum() / len(df)
    high_null_columns = null_percentage[null_percentage > 0.5].index.tolist()
    if high_null_columns:
        print(f"⚠️ 发现高空值列 (>50%): {high_null_columns}")
        # 可选择移除或保留，这里选择保留但给出警告

    # 3. 标准化列名顺序 (将重要列放在前面)
    preferred_order = [
        'open_time',           # 时间
        '开盘价', '最高价', '最低价', '收盘价',  # OHLC
        '成交量', '成交额', '成交笔数',          # 成交量数据
        '主动买入量', '主动买入额',             # 买入数据
        'MA20', 'MA50', 'MA_LONG',            # 移动平均线
        'MACD', 'MACD_Signal', 'MACD_Hist',   # MACD
        'RSI', 'RSI_Secondary', 'RSI_Long',   # RSI系列
        'BB_Upper', 'BB_Middle', 'BB_Lower',  # 布林带
        'BB_Long_Upper', 'BB_Long_Middle', 'BB_Long_Lower',  # 长期布林带
        'Stoch_SlowK', 'Stoch_SlowD',         # 随机指标
        'OBV',                                # 成交量指标
        'ATR', 'ATR_Long', 'ATR_Ratio',       # ATR系列
        'ADX',                                # 趋势指标
        # 斐波那契水平 (按重要性排序)
        'Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618',  # 关键回调水平
        'Fib_Ret_0.236', 'Fib_Ret_0.786', 'Fib_Ret_0.000', 'Fib_Ret_1.000',  # 其他回调水平
        'Fib_Ext_1.272', 'Fib_Ext_1.414',    # 保留的扩展水平 (移除1.618, 2.0, 2.618)
        'Fib_Trend', 'Fib_High', 'Fib_Low',  # 斐波那契趋势和关键点
        'Fib_Signal', 'Fib_Support_Level', 'Fib_Resistance_Level', 'Fib_Price_Position'  # 斐波那契信号
    ]

    # 重新排列列顺序
    existing_preferred = [col for col in preferred_order if col in df.columns]
    other_columns = [col for col in df.columns if col not in preferred_order]
    new_column_order = existing_preferred + other_columns

    df = df[new_column_order]
    print(f"✅ 列顺序已优化，核心指标前置")

    # 4. 数据类型优化
    numeric_columns = df.select_dtypes(include=['float64']).columns
    if len(numeric_columns) > 0:
        # 将float64转换为float32以节省内存，但保留时间列为原始类型
        time_columns = ['open_time']
        numeric_columns_to_convert = [col for col in numeric_columns if col not in time_columns]
        if numeric_columns_to_convert:
            df[numeric_columns_to_convert] = df[numeric_columns_to_convert].astype('float32')
            print(f"✅ 已优化{len(numeric_columns_to_convert)}个数值列的数据类型 (float64→float32)")

    # 5. 最终验证
    print(f"✅ 数据清理完成: {len(df)}行 × {len(df.columns)}列")

    return df

def display_combined_data_preview(file_path, num_rows=5):
    """
    显示合并数据的预览信息
    参数:
        file_path (Path): 数据文件路径
        num_rows (int): 显示的行数（首尾各显示num_rows行）
    """
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return

    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')

        print("\n" + "=" * 50)
        print(f"合并数据预览 ({file_path.name})")
        print("=" * 50)

        # 显示基本信息
        print(f"● 时间范围: {df.iloc[0, 0]} 至 {df.iloc[-1, 0]}")
        print(f"● 总记录数: {len(df)}")
        print(f"● 数据列数: {len(df.columns)}")

        # 选择关键列显示
        key_columns = [
            col for col in [
                'open_time', '日期', '时间', 'timestamp',
                '开盘价', '收盘价', '最高价', '最低价', '成交量',
                'MA20', 'MA50', 'RSI', 'MACD', 'MACD_Signal', 'BB_Upper', 'BB_Lower'
            ] if col in df.columns
        ]

        # 显示首尾数据
        if len(df) > num_rows * 2:
            preview = pd.concat([df.head(num_rows), df.tail(num_rows)])
            print(f"\n【首{num_rows}行 + 尾{num_rows}行】:")
        else:
            preview = df
            print("\n【全部数据】:")

        print(preview[key_columns].to_string(index=False))

        # 显示列名清单
        print("\n【全部列名】:")
        print(", ".join(df.columns))

    except Exception as e:
        print(f"❌ 数据预览失败: {e}")

def get_latest_combined_path():
    """获取最新的组合数据文件路径"""
    combined_path = DATA_DIR / COMBINED_FILENAME
    return combined_path if combined_path.exists() else None

if __name__ == "__main__":
    print("=" * 50)
    print("组合数据处理模块测试")
    print("=" * 50)

    try:
        # 执行数据合并
        result_path = combine_data()

        # 显示预览
        if result_path:
            display_combined_data_preview(result_path)

            # 验证数据完整性
            df = pd.read_csv(result_path, encoding='utf-8-sig')
            required_cols = ['开盘价', '收盘价', 'MA20', 'MA50', 'RSI']
            missing_cols = [col for col in required_cols if col not in df.columns]

            if missing_cols:
                print(f"\n⚠️ 警告: 缺少关键列 - {missing_cols}")
            else:
                print("\n✅ 数据验证通过")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()