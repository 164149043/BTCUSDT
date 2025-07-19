"""
技术指标计算模块
功能：加载原始K线数据，使用TA-Lib计算技术指标，并保存结果
依赖：pandas, numpy, TA-Lib
"""
import pandas as pd
import numpy as np
import talib
import os
import sys
from pathlib import Path
from datetime import datetime

# ===== 路径修复 =====
# 确保可以导入config模块
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from config import DATA_DIR, RAW_DATA_FILENAME, INDICATORS_FILENAME, \
        MA_SHORT_TERM, MA_LONG_TERM, MACD_FAST, MACD_SLOW, MACD_SIGNAL, \
        RSI_PERIOD, BB_PERIOD, BB_STD_DEV, ATR_PERIOD, \
        get_filenames, get_indicator_params

    print("✅ 成功导入 config 模块")
except ImportError as e:
    print(f"❌ 导入 config 模块失败: {e}")
    # 尝试直接定义变量（备选方案）
    DATA_DIR = Path('data')
    RAW_DATA_FILENAME = 'BTCUSDT_日线原始数据_.csv'
    INDICATORS_FILENAME = 'BTCUSDT_技术指标分析_.csv'
    MA_SHORT_TERM = 20
    MA_LONG_TERM = 50
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    RSI_PERIOD = 14
    BB_PERIOD = 20
    BB_STD_DEV = 2
    print("⚠️ 使用默认配置继续运行")


# ===== 主函数 =====
def calculate_indicators(raw_filename=None, indicators_filename=None, timeframe_name=None):
    """
    主函数：加载原始数据，计算技术指标，保存结果
    参数:
        raw_filename: 原始数据文件名
        indicators_filename: 指标数据文件名
        timeframe_name: 时间周期名称
    """
    print("\n" + "=" * 50)
    print(f"开始计算技术指标 - {timeframe_name or '日线'}")
    print("=" * 50)

    # 获取针对当前时间周期优化的参数
    if timeframe_name:
        params = get_indicator_params(timeframe_name)
        print(f"📊 使用{timeframe_name}优化参数: {params['description']}")
    else:
        # 使用默认参数
        params = {
            'MA_SHORT_TERM': MA_SHORT_TERM,
            'MA_LONG_TERM': MA_LONG_TERM,
            'MACD_FAST': MACD_FAST,
            'MACD_SLOW': MACD_SLOW,
            'MACD_SIGNAL': MACD_SIGNAL,
            'RSI_PERIOD': RSI_PERIOD,
            'BB_PERIOD': BB_PERIOD,
            'BB_STD_DEV': BB_STD_DEV
        }

    # 1. 确定文件路径
    if raw_filename:
        raw_data_path = DATA_DIR / raw_filename
    else:
        raw_data_path = DATA_DIR / RAW_DATA_FILENAME

    if not raw_data_path.exists():
        print(f"❌ 错误: 原始数据文件不存在 - {raw_data_path}")
        return None

    try:
        # 读取CSV文件，正确处理中文列名
        df = pd.read_csv(raw_data_path, encoding='utf-8-sig')

        # 检查必要的列是否存在
        required_columns = ['开盘价', '最高价', '最低价', '收盘价', '成交量']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"❌ 错误: 数据文件缺少必要的列 - {missing_cols}")
            return None

        print(f"✅ 成功加载原始数据, 共 {len(df)} 条记录")
    except Exception as e:
        print(f"❌ 加载数据失败: {e}")
        return None

    # 2. 转换数据类型
    df = convert_data_types(df)

    # 3. 计算技术指标
    df = compute_ta_indicators(df, params)

    # 4. 添加信号分析
    df = add_signal_analysis(df, params)

    # 5. 保存结果
    if indicators_filename:
        indicators_path = DATA_DIR / indicators_filename
    else:
        indicators_path = DATA_DIR / INDICATORS_FILENAME

    save_indicators(df, indicators_path)

    print(f"✅ 技术指标计算完成! 文件保存至: {indicators_path}")

    return indicators_path


def convert_data_types(df):
    """
    转换数据类型为适合TA-Lib计算
    """
    # 转换时间列为datetime类型
    if 'open_time' in df.columns:
        df['open_time'] = pd.to_datetime(df['open_time'])
        df.set_index('open_time', inplace=True)
    elif 'open_time' not in df.index.name:
        # 如果open_time不在索引中，尝试设置第一列为索引
        df.set_index(df.columns[0], inplace=True)

    # 确保数值列是浮点数类型
    numeric_cols = ['开盘价', '最高价', '最低价', '收盘价', '成交量']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 移除可能的NaN值
    df.dropna(subset=['收盘价'], inplace=True)

    return df


def compute_ta_indicators(df, params=None):
    """
    使用TA-Lib计算技术指标
    参数:
        df: 数据框
        params: 技术指标参数字典
    """
    print("🔧 计算技术指标中...")

    # 使用传入的参数或默认参数
    if params is None:
        params = {
            'MA_SHORT_TERM': MA_SHORT_TERM,
            'MA_LONG_TERM': MA_LONG_TERM,
            'MACD_FAST': MACD_FAST,
            'MACD_SLOW': MACD_SLOW,
            'MACD_SIGNAL': MACD_SIGNAL,
            'RSI_PERIOD': RSI_PERIOD,
            'BB_PERIOD': BB_PERIOD,
            'BB_STD_DEV': BB_STD_DEV
        }

    # 提取价格序列
    close = df['收盘价'].values
    high = df['最高价'].values
    low = df['最低价'].values
    volume = df['成交量'].values

    # 1. 移动平均线
    ma_short = params.get('MA_SHORT_TERM', MA_SHORT_TERM)
    ma_long = params.get('MA_LONG_TERM', MA_LONG_TERM)
    df[f'MA{ma_short}'] = talib.MA(close, timeperiod=ma_short)
    df[f'MA{ma_long}'] = talib.MA(close, timeperiod=ma_long)

    # 为了保持向后兼容，也保留MA20和MA50列名
    df['MA20'] = df[f'MA{ma_short}']
    df['MA50'] = df[f'MA{ma_long}']

    # 2. MACD
    macd_fast = params.get('MACD_FAST', MACD_FAST)
    macd_slow = params.get('MACD_SLOW', MACD_SLOW)
    macd_signal = params.get('MACD_SIGNAL', MACD_SIGNAL)
    macd, macd_signal_line, macd_hist = talib.MACD(
        close,
        fastperiod=macd_fast,
        slowperiod=macd_slow,
        signalperiod=macd_signal
    )
    df['MACD'] = macd
    df['MACD_Signal'] = macd_signal_line
    df['MACD_Hist'] = macd_hist

    # 3. RSI
    rsi_period = params.get('RSI_PERIOD', RSI_PERIOD)
    df['RSI'] = talib.RSI(close, timeperiod=rsi_period)

    # 4. 布林带
    bb_period = params.get('BB_PERIOD', BB_PERIOD)
    bb_std_dev = params.get('BB_STD_DEV', BB_STD_DEV)
    upper, middle, lower = talib.BBANDS(
        close,
        timeperiod=bb_period,
        nbdevup=bb_std_dev,
        nbdevdn=bb_std_dev
    )
    df['BB_Upper'] = upper
    df['BB_Middle'] = middle
    df['BB_Lower'] = lower

    # 5. 随机指标
    stoch_fastk = params.get('STOCH_FASTK', 14)
    stoch_slowk = params.get('STOCH_SLOWK', 3)
    stoch_slowd = params.get('STOCH_SLOWD', 3)
    slowk, slowd = talib.STOCH(
        high, low, close,
        fastk_period=stoch_fastk,
        slowk_period=stoch_slowk,
        slowk_matype=0,
        slowd_period=stoch_slowd,
        slowd_matype=0
    )
    df['Stoch_SlowK'] = slowk
    df['Stoch_SlowD'] = slowd

    # 6. 成交量指标
    df['OBV'] = talib.OBV(close, volume)

    # 7. ATR（平均真实波幅）
    atr_period = params.get('ATR_PERIOD', ATR_PERIOD)
    df['ATR'] = talib.ATR(high, low, close, timeperiod=atr_period)

    # 8. ADX（平均趋向指数）
    adx_period = params.get('ADX_PERIOD', 14)
    df['ADX'] = talib.ADX(high, low, close, timeperiod=adx_period)

    # 添加计算时间戳
    df['计算时间'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return df


def add_signal_analysis(df, params=None):
    """
    添加基于指标的交易信号分析
    参数:
        df: 数据框
        params: 技术指标参数字典
    """
    print("🔍 添加信号分析...")

    # 使用传入的参数或默认参数
    if params is None:
        params = {
            'MA_SHORT_TERM': MA_SHORT_TERM,
            'MA_LONG_TERM': MA_LONG_TERM
        }

    ma_short = params.get('MA_SHORT_TERM', MA_SHORT_TERM)
    ma_long = params.get('MA_LONG_TERM', MA_LONG_TERM)

    # 1. 移动平均线交叉信号
    # 使用动态列名，但保持MA20和MA50作为标准输出
    df['MA_Signal'] = np.where(
        df['MA20'] > df['MA50'],
        '金叉',
        np.where(df['MA20'] < df['MA50'], '死叉', '中性')
    )

    # 2. MACD信号
    df['MACD_Signal_Analysis'] = np.where(
        df['MACD'] > df['MACD_Signal'],
        '看涨',
        np.where(df['MACD'] < df['MACD_Signal'], '看跌', '中性')
    )

    # 3. RSI信号
    df['RSI_Signal'] = np.select(
        [
            df['RSI'] >= 70,
            df['RSI'] <= 30,
            (df['RSI'] > 50) & (df['RSI'] < 70),
            (df['RSI'] > 30) & (df['RSI'] <= 50)
        ],
        ['超买', '超卖', '看涨区域', '看跌区域'],
        default='中性'
    )

    # 4. 布林带信号
    df['BB_Signal'] = np.select(
        [
            df['收盘价'] > df['BB_Upper'],
            df['收盘价'] < df['BB_Lower'],
            (df['收盘价'] > df['BB_Middle']) & (df['收盘价'] <= df['BB_Upper']),
            (df['收盘价'] < df['BB_Middle']) & (df['收盘价'] >= df['BB_Lower'])
        ],
        ['突破上轨', '突破下轨', '上轨区域', '下轨区域'],
        default='中轨附近'
    )

    # 5. 随机指标信号
    df['Stoch_Signal'] = np.select(
        [
            (df['Stoch_SlowK'] > 80) & (df['Stoch_SlowD'] > 80),
            (df['Stoch_SlowK'] < 20) & (df['Stoch_SlowD'] < 20),
            (df['Stoch_SlowK'] > df['Stoch_SlowD']),
            (df['Stoch_SlowK'] < df['Stoch_SlowD'])
        ],
        ['超买交叉', '超卖交叉', '看涨交叉', '看跌交叉'],
        default='中性'
    )

    # 6. 综合信号强度（简单加权）
    conditions = [
        (df['MA_Signal'] == '金叉') & (df['MACD_Signal_Analysis'] == '看涨') & (df['RSI_Signal'] == '看涨区域'),
        (df['MA_Signal'] == '死叉') & (df['MACD_Signal_Analysis'] == '看跌') & (df['RSI_Signal'] == '看跌区域'),
    ]
    choices = ['强烈看涨', '强烈看跌']
    df['综合信号'] = np.select(conditions, choices, default='中性')

    return df


def save_indicators(df, file_path):
    """
    保存技术指标数据到CSV文件
    """
    # 确保目录存在
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # 保存数据，使用utf-8-sig编码支持Excel中文
    df.to_csv(file_path, encoding='utf-8-sig')

    # 打印文件信息
    print(f"💾 指标数据已保存: {file_path}")
    print(f"📊 包含 {len(df.columns)} 列技术指标和分析信号")


def get_latest_indicators_path():
    """获取最新的技术指标文件路径"""
    indicators_path = DATA_DIR / INDICATORS_FILENAME
    return indicators_path if indicators_path.exists() else None


if __name__ == "__main__":
    print("=" * 50)
    print("技术指标计算模块测试")
    print("=" * 50)

    try:
        # 执行指标计算
        result_path = calculate_indicators()

        if result_path:
            # 加载并预览结果
            df = pd.read_csv(result_path, encoding='utf-8-sig')
            print("\n技术指标数据预览:")
            # 显示最后5行的重要列
            preview_cols = ['开盘价', '收盘价', 'MA20', 'MA50', 'RSI', 'MACD', '综合信号']
            available_cols = [col for col in preview_cols if col in df.columns]
            print(df[available_cols].tail(5))

            # 显示信号分布
            if '综合信号' in df.columns:
                print("\n信号分布统计:")
                print(df['综合信号'].value_counts())
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback

        traceback.print_exc()