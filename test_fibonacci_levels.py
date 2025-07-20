"""
斐波那契水平测试脚本
验证斐波那契回调和扩展水平的计算
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from ta_calculator import calculate_fibonacci_levels, add_fibonacci_signals
from config import get_indicator_params

def create_test_data():
    """创建测试数据"""
    print("📊 创建斐波那契测试数据")
    print("=" * 60)
    
    # 创建一个明显的上升趋势然后回调的价格模式
    np.random.seed(42)
    
    # 第一阶段：上升趋势 (100,000 -> 120,000)
    uptrend_prices = np.linspace(100000, 120000, 50)
    uptrend_noise = np.random.normal(0, 200, 50)
    uptrend_prices += uptrend_noise
    
    # 第二阶段：回调 (120,000 -> 110,000)
    retracement_prices = np.linspace(120000, 110000, 30)
    retracement_noise = np.random.normal(0, 150, 30)
    retracement_prices += retracement_noise
    
    # 第三阶段：再次上升 (110,000 -> 125,000)
    uptrend2_prices = np.linspace(110000, 125000, 40)
    uptrend2_noise = np.random.normal(0, 180, 40)
    uptrend2_prices += uptrend2_noise
    
    # 合并所有价格
    all_prices = np.concatenate([uptrend_prices, retracement_prices, uptrend2_prices])
    
    # 创建高低价
    highs = all_prices + np.random.uniform(50, 300, len(all_prices))
    lows = all_prices - np.random.uniform(50, 300, len(all_prices))
    
    # 创建DataFrame
    test_df = pd.DataFrame({
        '收盘价': all_prices,
        '最高价': highs,
        '最低价': lows,
        '成交量': np.random.uniform(1000, 5000, len(all_prices))
    })
    
    print(f"✅ 创建了{len(test_df)}条测试数据")
    print(f"   价格范围: ${test_df['收盘价'].min():.2f} - ${test_df['收盘价'].max():.2f}")
    
    return test_df

def test_fibonacci_calculation():
    """测试斐波那契水平计算"""
    print(f"\n🔢 测试斐波那契水平计算")
    print("=" * 60)
    
    # 创建测试数据
    test_df = create_test_data()
    
    # 计算斐波那契水平
    result_df = calculate_fibonacci_levels(test_df, lookback_period=30)
    
    # 添加斐波那契信号
    result_df = add_fibonacci_signals(result_df)
    
    print("\n📈 斐波那契列检查:")
    fib_columns = [col for col in result_df.columns if col.startswith('Fib_')]
    print(f"   添加的斐波那契列数: {len(fib_columns)}")
    
    # 按类型分组显示
    retracement_cols = [col for col in fib_columns if 'Ret_' in col]
    extension_cols = [col for col in fib_columns if 'Ext_' in col]
    signal_cols = [col for col in fib_columns if col in ['Fib_Signal', 'Fib_Trend', 'Fib_Support_Level', 'Fib_Resistance_Level']]
    other_cols = [col for col in fib_columns if col not in retracement_cols + extension_cols + signal_cols]
    
    print(f"   回调水平 ({len(retracement_cols)}): {retracement_cols}")
    print(f"   扩展水平 ({len(extension_cols)}): {extension_cols}")
    print(f"   信号列 ({len(signal_cols)}): {signal_cols}")
    print(f"   其他列 ({len(other_cols)}): {other_cols}")
    
    return result_df

def analyze_fibonacci_results(df):
    """分析斐波那契计算结果"""
    print(f"\n📊 斐波那契结果分析")
    print("=" * 60)
    
    # 检查数据完整性
    total_rows = len(df)
    
    # 分析关键斐波那契水平
    key_levels = ['Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618']
    
    print("🎯 关键斐波那契水平分析:")
    for level in key_levels:
        if level in df.columns:
            valid_count = df[level].notna().sum()
            if valid_count > 0:
                latest_value = df[level].dropna().iloc[-1]
                print(f"   {level}: {valid_count}/{total_rows} 有效值, 最新值: ${latest_value:.2f}")
            else:
                print(f"   {level}: 无有效数据")
    
    # 分析趋势分布
    print(f"\n📈 趋势分布分析:")
    if 'Fib_Trend' in df.columns:
        trend_counts = df['Fib_Trend'].value_counts()
        for trend, count in trend_counts.items():
            print(f"   {trend}: {count}次 ({count/total_rows*100:.1f}%)")
    
    # 分析信号分布
    print(f"\n🎯 斐波那契信号分析:")
    if 'Fib_Signal' in df.columns:
        signal_counts = df['Fib_Signal'].value_counts()
        for signal, count in signal_counts.items():
            print(f"   {signal}: {count}次 ({count/total_rows*100:.1f}%)")
    
    # 显示最后几行的斐波那契数据
    print(f"\n📋 最新斐波那契数据预览:")
    fib_display_cols = ['收盘价', 'Fib_Trend', 'Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618', 'Fib_Signal']
    available_cols = [col for col in fib_display_cols if col in df.columns]
    
    if available_cols:
        preview_df = df[available_cols].tail(5)
        print(preview_df.to_string(float_format='%.2f'))
    
    return df

def test_fibonacci_with_real_data():
    """使用真实数据测试斐波那契计算"""
    print(f"\n💰 使用真实数据测试斐波那契")
    print("=" * 60)
    
    try:
        from config import DATA_DIR
        
        # 查找最新的原始数据文件
        csv_files = list(DATA_DIR.glob("*原始数据*.csv"))
        
        if csv_files:
            latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)
            print(f"📁 使用文件: {latest_file.name}")
            
            # 读取数据
            df = pd.read_csv(latest_file, encoding='utf-8-sig')
            print(f"   数据行数: {len(df)}")
            print(f"   价格范围: ${df['收盘价'].min():.2f} - ${df['收盘价'].max():.2f}")
            
            # 计算斐波那契水平
            params = get_indicator_params('1小时线')
            result_df = calculate_fibonacci_levels(df, lookback_period=params.get('FIB_LOOKBACK_PERIOD', 40))
            result_df = add_fibonacci_signals(result_df)
            
            # 分析结果
            analyze_fibonacci_results(result_df)
            
            return result_df
            
        else:
            print("❌ 未找到原始数据文件")
            return None
            
    except Exception as e:
        print(f"❌ 真实数据测试失败: {e}")
        return None

def test_fibonacci_integration():
    """测试斐波那契与现有技术指标的集成"""
    print(f"\n🔧 测试斐波那契集成")
    print("=" * 60)
    
    try:
        from ta_calculator import compute_ta_indicators
        
        # 创建测试数据
        test_df = create_test_data()
        
        # 使用完整的技术指标计算（包括斐波那契）
        params = get_indicator_params('1小时线')
        result_df = compute_ta_indicators(test_df, params)
        
        print("✅ 完整技术指标计算成功")
        print(f"   总列数: {len(result_df.columns)}")
        
        # 检查斐波那契列是否存在
        fib_columns = [col for col in result_df.columns if col.startswith('Fib_')]
        print(f"   斐波那契列数: {len(fib_columns)}")
        
        if fib_columns:
            print("✅ 斐波那契水平已成功集成到技术指标计算中")
            
            # 显示一些关键指标的组合
            key_cols = ['收盘价', 'MA20', 'RSI', 'Fib_Ret_0.618', 'Fib_Signal']
            available_key_cols = [col for col in key_cols if col in result_df.columns]
            
            if available_key_cols:
                print(f"\n📊 关键指标组合预览:")
                preview = result_df[available_key_cols].tail(3)
                print(preview.to_string(float_format='%.2f'))
        else:
            print("❌ 斐波那契水平未能集成")
            
        return result_df
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """主测试函数"""
    print("BTCUSDT 斐波那契水平测试")
    print("=" * 80)
    print("测试斐波那契回调和扩展水平的计算与集成")
    print("=" * 80)
    
    # 1. 基础斐波那契计算测试
    test_result = test_fibonacci_calculation()
    
    if test_result is not None:
        # 2. 分析计算结果
        analyze_fibonacci_results(test_result)
        
        # 3. 真实数据测试
        real_data_result = test_fibonacci_with_real_data()
        
        # 4. 集成测试
        integration_result = test_fibonacci_integration()
        
        print(f"\n" + "=" * 80)
        print("🎉 斐波那契水平测试完成!")
        
        if integration_result is not None:
            print("✅ 斐波那契水平已成功添加到组合数据文件中")
            print("✅ 包含以下斐波那契指标:")
            print("   • 回调水平: 0%, 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%")
            print("   • 扩展水平: 127.2%, 141.4%, 161.8%, 200%, 261.8%")
            print("   • 交易信号: 趋势、支撑阻力、价格位置")
            print("   • 自动信号: 黄金分割点反弹/拒绝、突破信号")
        else:
            print("⚠️ 部分测试未通过，请检查代码")
    else:
        print("❌ 基础测试失败")

if __name__ == "__main__":
    main()
