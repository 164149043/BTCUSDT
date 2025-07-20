"""
组合数据文件精简工具
移除不必要的数据，保留核心技术指标
"""

import pandas as pd
import sys
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from config import DATA_DIR

def analyze_current_data_structure():
    """分析当前数据结构"""
    print("📊 分析当前组合数据结构")
    print("=" * 80)
    
    # 查找最新的组合数据文件
    csv_files = [f for f in DATA_DIR.glob("*组合数据*.csv") if not f.name.endswith('.backup.csv') and not f.name.endswith('_streamlined.csv')]
    
    if not csv_files:
        print("❌ 未找到组合数据文件")
        return None
    
    latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)
    print(f"📁 分析文件: {latest_file.name}")
    
    try:
        df = pd.read_csv(latest_file, encoding='utf-8-sig')
        
        print(f"📈 当前数据结构:")
        print(f"   数据行数: {len(df)}")
        print(f"   总列数: {len(df.columns)}")
        print(f"   文件大小: {latest_file.stat().st_size / 1024:.1f} KB")
        
        # 按类别分析列
        basic_cols = []
        ma_cols = []
        macd_cols = []
        rsi_cols = []
        bb_cols = []
        fib_retracement_cols = []
        fib_extension_cols = []
        fib_signal_cols = []
        other_cols = []
        
        for col in df.columns:
            if col in ['open_time', '开盘价', '最高价', '最低价', '收盘价', '成交量', '成交额', '成交笔数', '主动买入量', '主动买入额']:
                basic_cols.append(col)
            elif 'MA' in col and 'MACD' not in col:
                ma_cols.append(col)
            elif 'MACD' in col:
                macd_cols.append(col)
            elif 'RSI' in col:
                rsi_cols.append(col)
            elif 'BB_' in col:
                bb_cols.append(col)
            elif col.startswith('Fib_Ret_'):
                fib_retracement_cols.append(col)
            elif col.startswith('Fib_Ext_'):
                fib_extension_cols.append(col)
            elif col.startswith('Fib_'):
                fib_signal_cols.append(col)
            else:
                other_cols.append(col)
        
        print(f"\n📋 列分类统计:")
        print(f"   基础数据 ({len(basic_cols)}): {basic_cols}")
        print(f"   移动平均 ({len(ma_cols)}): {ma_cols}")
        print(f"   MACD ({len(macd_cols)}): {macd_cols}")
        print(f"   RSI ({len(rsi_cols)}): {rsi_cols}")
        print(f"   布林带 ({len(bb_cols)}): {bb_cols}")
        print(f"   斐波那契回调 ({len(fib_retracement_cols)}): {fib_retracement_cols}")
        print(f"   斐波那契扩展 ({len(fib_extension_cols)}): {fib_extension_cols}")
        print(f"   斐波那契信号 ({len(fib_signal_cols)}): {fib_signal_cols}")
        print(f"   其他指标 ({len(other_cols)}): {other_cols}")
        
        return latest_file, df
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        return None, None

def define_streamlined_columns():
    """定义精简后保留的列"""
    print(f"\n🎯 定义精简数据结构")
    print("=" * 80)
    
    # 核心必需列 (基于重要性和实用性)
    streamlined_columns = {
        # 基础数据 (必需)
        'basic': [
            'open_time',           # 时间戳
            '开盘价', '最高价', '最低价', '收盘价',  # OHLC
            '成交量'               # 成交量 (移除成交额等次要数据)
        ],
        
        # 核心移动平均线 (保留最重要的)
        'moving_averages': [
            'MA20',                # 短期MA
            'MA50',                # 中期MA
            # 移除: MA_LONG (长期MA，对短线交易意义不大)
        ],
        
        # MACD (保留核心)
        'macd': [
            'MACD',                # MACD主线
            'MACD_Signal',         # 信号线
            'MACD_Hist'            # 柱状图
            # 移除: MACD_Long系列 (长期MACD对短线意义不大)
        ],
        
        # RSI (保留主要的)
        'rsi': [
            'RSI',                 # 主RSI
            # 移除: RSI_Secondary, RSI_Long (多重RSI造成冗余)
        ],
        
        # 布林带 (保留标准布林带)
        'bollinger': [
            'BB_Upper',            # 上轨
            'BB_Middle',           # 中轨
            'BB_Lower'             # 下轨
            # 移除: BB_Long系列 (长期布林带)
        ],
        
        # 斐波那契 (保留最关键的)
        'fibonacci_key': [
            'Fib_Ret_0.382',       # 38.2% 关键回调位 ⭐⭐⭐⭐
            'Fib_Ret_0.500',       # 50% 黄金分割点 ⭐⭐⭐⭐⭐
            'Fib_Ret_0.618',       # 61.8% 黄金比例 ⭐⭐⭐⭐⭐
            'Fib_Ext_1.272',       # 127.2% 第一目标位
            'Fib_Ext_1.618',       # 161.8% 黄金扩展
            'Fib_Trend',           # 趋势方向
            'Fib_Signal'           # 交易信号
            # 移除: 其他斐波那契水平 (23.6%, 78.6%, 100%等次要水平)
        ],
        
        # 其他核心指标
        'other_core': [
            'ATR',                 # 波动率
            'ADX',                 # 趋势强度
            'OBV'                  # 成交量指标
            # 移除: Stoch系列, ATR_Long, ATR_Ratio等
        ]
    }
    
    # 合并所有保留的列
    all_streamlined = []
    for category, columns in streamlined_columns.items():
        all_streamlined.extend(columns)
    
    print("✅ 精简后保留的列:")
    for category, columns in streamlined_columns.items():
        print(f"   {category} ({len(columns)}): {columns}")
    
    print(f"\n📊 精简统计:")
    print(f"   保留总列数: {len(all_streamlined)}")
    print(f"   预计减少: ~{51 - len(all_streamlined)}列")
    
    return all_streamlined

def create_streamlined_file(original_file, df, streamlined_columns):
    """创建精简的组合数据文件"""
    print(f"\n🔧 创建精简数据文件")
    print("=" * 80)
    
    try:
        # 检查哪些列实际存在
        available_columns = [col for col in streamlined_columns if col in df.columns]
        missing_columns = [col for col in streamlined_columns if col not in df.columns]
        
        if missing_columns:
            print(f"⚠️ 缺失列: {missing_columns}")
        
        print(f"✅ 可用列: {len(available_columns)}/{len(streamlined_columns)}")
        
        # 创建精简数据框
        streamlined_df = df[available_columns].copy()
        
        # 优化数据类型
        numeric_columns = streamlined_df.select_dtypes(include=['float64']).columns
        if len(numeric_columns) > 0:
            streamlined_df[numeric_columns] = streamlined_df[numeric_columns].astype('float32')
        
        # 生成精简文件名
        original_name = original_file.stem
        streamlined_filename = f"{original_name}_streamlined.csv"
        streamlined_path = original_file.parent / streamlined_filename
        
        # 保存精简文件
        streamlined_df.to_csv(streamlined_path, encoding='utf-8-sig', index=False)
        
        # 计算文件大小变化
        original_size = original_file.stat().st_size / 1024
        streamlined_size = streamlined_path.stat().st_size / 1024
        size_reduction = (original_size - streamlined_size) / original_size * 100
        
        print(f"✅ 精简文件创建成功:")
        print(f"   文件名: {streamlined_filename}")
        print(f"   列数: {len(df.columns)} → {len(streamlined_df.columns)} (减少{len(df.columns) - len(streamlined_df.columns)}列)")
        print(f"   文件大小: {original_size:.1f}KB → {streamlined_size:.1f}KB")
        print(f"   空间节省: {size_reduction:.1f}%")
        
        return streamlined_path, streamlined_df
        
    except Exception as e:
        print(f"❌ 创建精简文件失败: {e}")
        return None, None

def validate_streamlined_data(streamlined_df):
    """验证精简数据的完整性"""
    print(f"\n🔍 验证精简数据完整性")
    print("=" * 80)
    
    # 检查数据完整性
    total_rows = len(streamlined_df)
    
    print("📊 数据完整性检查:")
    
    # 检查基础数据
    basic_cols = ['收盘价', '成交量', 'MA20', 'RSI']
    for col in basic_cols:
        if col in streamlined_df.columns:
            valid_count = streamlined_df[col].notna().sum()
            print(f"   {col}: {valid_count}/{total_rows} ({valid_count/total_rows*100:.1f}%)")
    
    # 检查斐波那契关键水平
    fib_key_cols = ['Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618']
    print(f"\n🔢 斐波那契关键水平:")
    for col in fib_key_cols:
        if col in streamlined_df.columns:
            valid_count = streamlined_df[col].notna().sum()
            latest_value = streamlined_df[col].dropna().iloc[-1] if valid_count > 0 else 'N/A'
            print(f"   {col}: {valid_count}/{total_rows} ({valid_count/total_rows*100:.1f}%) - 最新: ${latest_value:.2f}" if latest_value != 'N/A' else f"   {col}: 无数据")
    
    # 显示最新数据预览
    print(f"\n📋 精简数据预览 (最新5行):")
    preview_cols = ['收盘价', 'MA20', 'RSI', 'Fib_Ret_0.500', 'Fib_Signal']
    available_preview_cols = [col for col in preview_cols if col in streamlined_df.columns]
    
    if available_preview_cols:
        preview = streamlined_df[available_preview_cols].tail(5)
        print(preview.to_string(float_format='%.2f'))

def create_streamlined_comparison():
    """创建精简前后对比"""
    print(f"\n📊 精简效果对比")
    print("=" * 80)
    
    # 对比表格
    comparison_data = {
        '项目': ['总列数', '基础数据', '技术指标', '斐波那契', '文件大小', '适用场景'],
        '原始文件': ['51列', '10列', '22列', '19列', '~90KB', '完整分析'],
        '精简文件': ['~25列', '6列', '12列', '7列', '~45KB', '核心交易'],
        '减少比例': ['~51%', '40%', '45%', '63%', '50%', '聚焦核心']
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    print(comparison_df.to_string(index=False))
    
    print(f"\n✅ 精简优势:")
    print("   1. 文件大小减少50%，上传更快")
    print("   2. 数据更聚焦，DeepSeek分析更精准")
    print("   3. 保留最关键的斐波那契水平")
    print("   4. 移除冗余指标，突出核心信号")
    print("   5. 适合快速决策和短线交易")

def main():
    """主函数"""
    print("BTCUSDT 组合数据精简工具")
    print("=" * 80)
    print("目标: 保留核心技术指标，移除不必要数据")
    print("=" * 80)
    
    # 1. 分析当前数据结构
    original_file, df = analyze_current_data_structure()
    
    if original_file is None:
        return
    
    # 2. 定义精简列
    streamlined_columns = define_streamlined_columns()
    
    # 3. 创建精简文件
    streamlined_path, streamlined_df = create_streamlined_file(original_file, df, streamlined_columns)
    
    if streamlined_path is None:
        return
    
    # 4. 验证精简数据
    validate_streamlined_data(streamlined_df)
    
    # 5. 显示对比
    create_streamlined_comparison()
    
    print(f"\n" + "=" * 80)
    print("🎉 数据精简完成!")
    print(f"✅ 精简文件: {streamlined_path.name}")
    print("✅ 保留了最核心的技术指标")
    print("✅ 重点保留斐波那契关键水平: 38.2%, 50%, 61.8%")
    print("✅ 文件大小减少约50%")
    print("\n💡 建议:")
    print("   - 使用精简文件发送给DeepSeek AI")
    print("   - 适合短线和日内交易分析")
    print("   - 聚焦最重要的技术信号")

if __name__ == "__main__":
    main()
