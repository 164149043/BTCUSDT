"""
清理现有CSV文件脚本
移除BB_Squeeze和其他多余数据，优化组合数据文件
"""

import pandas as pd
import os
import sys
from pathlib import Path
from datetime import datetime

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from config import DATA_DIR

def analyze_csv_columns(file_path):
    """分析CSV文件的列结构"""
    print(f"\n📊 分析文件: {file_path.name}")
    print("=" * 60)
    
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        
        print(f"数据维度: {len(df)}行 × {len(df.columns)}列")
        print(f"时间范围: {df.iloc[0, 0]} 至 {df.iloc[-1, 0]}")
        
        # 分类显示列名
        basic_columns = []
        ma_columns = []
        indicator_columns = []
        redundant_columns = []
        
        for col in df.columns:
            if col in ['open_time', '开盘价', '最高价', '最低价', '收盘价', '成交量', '成交额', '成交笔数', '主动买入量', '主动买入额']:
                basic_columns.append(col)
            elif 'MA' in col:
                ma_columns.append(col)
            elif col in ['BB_Squeeze', 'BB_Width', 'MA8', 'MA21', 'MA55']:
                redundant_columns.append(col)
            else:
                indicator_columns.append(col)
        
        print(f"\n📈 基础数据列 ({len(basic_columns)}): {basic_columns}")
        print(f"📊 移动平均线列 ({len(ma_columns)}): {ma_columns}")
        print(f"🔧 技术指标列 ({len(indicator_columns)}): {indicator_columns}")
        print(f"🗑️ 多余数据列 ({len(redundant_columns)}): {redundant_columns}")
        
        return df, redundant_columns
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        return None, []

def clean_csv_file(file_path, backup=True):
    """清理单个CSV文件"""
    print(f"\n🧹 清理文件: {file_path.name}")
    print("=" * 60)
    
    try:
        # 读取原始数据
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        original_columns = len(df.columns)
        
        # 定义要移除的列
        columns_to_remove = [
            # 中间计算数据
            'BB_Squeeze',           # 布林带挤压标志
            'BB_Width',             # 布林带宽度
            
            # 重复的MA列 (保留标准命名MA20, MA50, MA_LONG)
            'MA8', 'MA21', 'MA55',  # 移除动态命名的MA
            
            # 其他可能的多余列
            'MACD_Long_Hist',       # 长期MACD柱状图
            'RSI_Extra_Long',       # 超长期RSI
            
            # 信号分析列 (如果存在)
            '计算时间',
            'MA_Signal',
            'MACD_Signal_Analysis',
            'RSI_Signal', 
            'BB_Signal',
            'Stoch_Signal',
            '综合信号'
        ]
        
        # 检查哪些列实际存在
        existing_columns_to_remove = [col for col in columns_to_remove if col in df.columns]
        
        if existing_columns_to_remove:
            # 创建备份
            if backup:
                backup_path = file_path.with_suffix('.backup.csv')
                df.to_csv(backup_path, encoding='utf-8-sig', index=False)
                print(f"💾 已创建备份: {backup_path.name}")
            
            # 移除多余列
            df_cleaned = df.drop(columns=existing_columns_to_remove)
            print(f"🗑️ 已移除列 ({len(existing_columns_to_remove)}): {existing_columns_to_remove}")
            
            # 优化列顺序
            df_cleaned = optimize_column_order(df_cleaned)
            
            # 数据类型优化
            df_cleaned = optimize_data_types(df_cleaned)
            
            # 保存清理后的文件
            df_cleaned.to_csv(file_path, encoding='utf-8-sig', index=False)
            
            print(f"✅ 清理完成: {original_columns}列 → {len(df_cleaned.columns)}列")
            print(f"💾 已保存: {file_path.name}")
            
            return True
        else:
            print("ℹ️ 未发现需要移除的列")
            return False
            
    except Exception as e:
        print(f"❌ 清理失败: {e}")
        return False

def optimize_column_order(df):
    """优化列顺序"""
    preferred_order = [
        'open_time',           # 时间
        '开盘价', '最高价', '最低价', '收盘价',  # OHLC
        '成交量', '成交额', '成交笔数',          # 成交量数据
        '主动买入量', '主动买入额',             # 买入数据
        'MA20', 'MA50', 'MA_LONG',            # 移动平均线
        'MACD', 'MACD_Signal', 'MACD_Hist',   # MACD
        'MACD_Long', 'MACD_Long_Signal',      # 长期MACD
        'RSI', 'RSI_Secondary', 'RSI_Long',   # RSI系列
        'BB_Upper', 'BB_Middle', 'BB_Lower',  # 布林带
        'BB_Long_Upper', 'BB_Long_Middle', 'BB_Long_Lower',  # 长期布林带
        'Stoch_SlowK', 'Stoch_SlowD',         # 随机指标
        'OBV',                                # 成交量指标
        'ATR', 'ATR_Long', 'ATR_Ratio',       # ATR系列
        'ADX'                                 # 趋势指标
    ]
    
    # 重新排列列顺序
    existing_preferred = [col for col in preferred_order if col in df.columns]
    other_columns = [col for col in df.columns if col not in preferred_order]
    new_column_order = existing_preferred + other_columns
    
    return df[new_column_order]

def optimize_data_types(df):
    """优化数据类型"""
    # 将float64转换为float32以节省内存
    numeric_columns = df.select_dtypes(include=['float64']).columns
    if len(numeric_columns) > 0:
        df[numeric_columns] = df[numeric_columns].astype('float32')
        print(f"🔧 已优化{len(numeric_columns)}个数值列的数据类型")
    
    return df

def clean_all_csv_files():
    """清理所有组合数据CSV文件"""
    print("🧹 批量清理组合数据CSV文件")
    print("=" * 80)
    
    # 查找所有组合数据文件
    csv_files = list(DATA_DIR.glob("*组合数据*.csv"))
    
    if not csv_files:
        print("❌ 未找到组合数据CSV文件")
        return
    
    print(f"📁 找到 {len(csv_files)} 个组合数据文件:")
    for file in csv_files:
        print(f"   - {file.name}")
    
    cleaned_count = 0
    
    for csv_file in csv_files:
        # 分析文件
        df, redundant_cols = analyze_csv_columns(csv_file)
        
        if df is not None and redundant_cols:
            # 清理文件
            if clean_csv_file(csv_file, backup=True):
                cleaned_count += 1
        else:
            print(f"ℹ️ {csv_file.name} 无需清理")
    
    print(f"\n✅ 批量清理完成: {cleaned_count}/{len(csv_files)} 个文件已清理")

def verify_cleaned_files():
    """验证清理后的文件"""
    print("\n🔍 验证清理结果")
    print("=" * 60)
    
    csv_files = list(DATA_DIR.glob("*组合数据*.csv"))
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, encoding='utf-8-sig')
            
            # 检查是否还有多余列
            unwanted_columns = ['BB_Squeeze', 'BB_Width', 'MA8', 'MA21', 'MA55']
            found_unwanted = [col for col in unwanted_columns if col in df.columns]
            
            if found_unwanted:
                print(f"⚠️ {csv_file.name}: 仍包含多余列 {found_unwanted}")
            else:
                print(f"✅ {csv_file.name}: 清理完成 ({len(df.columns)}列)")
                
        except Exception as e:
            print(f"❌ {csv_file.name}: 验证失败 - {e}")

def show_column_comparison():
    """显示清理前后的列对比"""
    print("\n📊 列结构对比")
    print("=" * 60)
    
    csv_files = list(DATA_DIR.glob("*组合数据*.csv"))
    backup_files = list(DATA_DIR.glob("*组合数据*.backup.csv"))
    
    for csv_file in csv_files:
        backup_file = csv_file.with_suffix('.backup.csv')
        
        if backup_file.exists():
            try:
                df_original = pd.read_csv(backup_file, encoding='utf-8-sig')
                df_cleaned = pd.read_csv(csv_file, encoding='utf-8-sig')
                
                print(f"\n📁 {csv_file.name}:")
                print(f"   清理前: {len(df_original.columns)}列")
                print(f"   清理后: {len(df_cleaned.columns)}列")
                print(f"   减少: {len(df_original.columns) - len(df_cleaned.columns)}列")
                
                # 显示被移除的列
                removed_cols = set(df_original.columns) - set(df_cleaned.columns)
                if removed_cols:
                    print(f"   移除的列: {list(removed_cols)}")
                    
            except Exception as e:
                print(f"❌ 对比失败: {e}")

def main():
    """主函数"""
    print("BTCUSDT 组合数据CSV清理工具")
    print("=" * 80)
    print("功能: 移除BB_Squeeze和其他多余数据，优化文件结构")
    print("=" * 80)
    
    # 1. 清理所有CSV文件
    clean_all_csv_files()
    
    # 2. 验证清理结果
    verify_cleaned_files()
    
    # 3. 显示对比结果
    show_column_comparison()
    
    print("\n" + "=" * 80)
    print("清理总结:")
    print("✅ 已移除 BB_Squeeze 列 (布林带挤压标志)")
    print("✅ 已移除 BB_Width 列 (布林带宽度)")
    print("✅ 已移除重复的MA列 (MA8, MA21, MA55)")
    print("✅ 已优化列顺序 (核心指标前置)")
    print("✅ 已优化数据类型 (节省内存)")
    print("✅ 已创建备份文件 (*.backup.csv)")
    print("\n建议: 如果清理结果满意，可以删除备份文件以节省空间")

if __name__ == "__main__":
    main()
