"""
小数点精度对技术指标计算影响分析
分析2位小数精度对BTCUSDT技术分析的影响
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from config import DATA_DIR

def analyze_current_precision():
    """分析当前数据的精度情况"""
    print("🔍 当前数据精度分析")
    print("=" * 80)
    
    # 查找组合数据文件
    csv_files = [f for f in DATA_DIR.glob("*组合数据*.csv") if not f.name.endswith('.backup.csv')]
    
    if not csv_files:
        print("❌ 未找到组合数据文件")
        return
    
    for csv_file in csv_files:
        print(f"\n📊 分析文件: {csv_file.name}")
        print("-" * 60)
        
        try:
            df = pd.read_csv(csv_file, encoding='utf-8-sig')
            
            # 分析不同类型数据的精度需求
            price_columns = ['开盘价', '最高价', '最低价', '收盘价']
            volume_columns = ['成交量', '成交额', '主动买入量', '主动买入额']
            indicator_columns = ['MA20', 'MA50', 'MACD', 'RSI', 'BB_Upper', 'ATR']
            
            print("💰 价格数据精度分析:")
            for col in price_columns:
                if col in df.columns:
                    sample_values = df[col].dropna().tail(5)
                    print(f"   {col}: {sample_values.iloc[-1]:.8f}")
                    
                    # 分析小数位数
                    decimal_places = []
                    for val in sample_values:
                        str_val = f"{val:.10f}".rstrip('0')
                        if '.' in str_val:
                            decimal_places.append(len(str_val.split('.')[1]))
                        else:
                            decimal_places.append(0)
                    
                    avg_decimals = np.mean(decimal_places)
                    print(f"      平均小数位数: {avg_decimals:.1f}")
            
            print("\n📈 技术指标精度分析:")
            for col in indicator_columns:
                if col in df.columns:
                    sample_values = df[col].dropna().tail(5)
                    if len(sample_values) > 0:
                        print(f"   {col}: {sample_values.iloc[-1]:.8f}")
                        
                        # 计算指标的变化幅度
                        if len(sample_values) >= 2:
                            change = abs(sample_values.iloc[-1] - sample_values.iloc[-2])
                            print(f"      最近变化: {change:.8f}")
            
        except Exception as e:
            print(f"❌ 分析失败: {e}")

def test_precision_impact():
    """测试不同精度对指标计算的影响"""
    print(f"\n🧪 精度影响测试")
    print("=" * 80)
    
    # 创建测试数据 (模拟BTCUSDT价格)
    np.random.seed(42)
    base_price = 100000.0
    price_changes = np.random.normal(0, 500, 100)  # 标准差500美元
    prices = base_price + np.cumsum(price_changes)
    
    # 创建测试DataFrame
    test_df = pd.DataFrame({
        '收盘价': prices,
        '最高价': prices + np.random.uniform(0, 200, 100),
        '最低价': prices - np.random.uniform(0, 200, 100),
        '成交量': np.random.uniform(1000, 5000, 100)
    })
    
    print("📊 测试不同精度对MA20计算的影响:")
    
    # 原始精度
    ma20_original = test_df['收盘价'].rolling(20).mean()
    
    # 2位小数精度
    prices_2decimal = test_df['收盘价'].round(2)
    ma20_2decimal = prices_2decimal.rolling(20).mean()
    
    # 4位小数精度
    prices_4decimal = test_df['收盘价'].round(4)
    ma20_4decimal = prices_4decimal.rolling(20).mean()
    
    # 比较最后几个值
    comparison_df = pd.DataFrame({
        '原始精度': ma20_original.tail(5),
        '2位小数': ma20_2decimal.tail(5),
        '4位小数': ma20_4decimal.tail(5)
    })
    
    print(comparison_df.to_string())
    
    # 计算误差
    error_2decimal = abs(ma20_original - ma20_2decimal).dropna()
    error_4decimal = abs(ma20_original - ma20_4decimal).dropna()
    
    print(f"\n📈 MA20计算误差统计:")
    print(f"   2位小数 - 平均误差: {error_2decimal.mean():.6f}")
    print(f"   2位小数 - 最大误差: {error_2decimal.max():.6f}")
    print(f"   4位小数 - 平均误差: {error_4decimal.mean():.6f}")
    print(f"   4位小数 - 最大误差: {error_4decimal.max():.6f}")
    
    return error_2decimal.mean(), error_2decimal.max()

def test_rsi_precision_impact():
    """测试RSI指标的精度影响"""
    print(f"\n🎯 RSI指标精度影响测试")
    print("=" * 80)
    
    try:
        import talib
        
        # 创建测试数据
        np.random.seed(42)
        base_price = 100000.0
        price_changes = np.random.normal(0, 500, 100)
        prices = base_price + np.cumsum(price_changes)
        
        # 原始精度RSI
        rsi_original = talib.RSI(prices, timeperiod=14)
        
        # 2位小数精度RSI
        prices_2decimal = np.round(prices, 2)
        rsi_2decimal = talib.RSI(prices_2decimal, timeperiod=14)
        
        # 比较最后几个值
        comparison_df = pd.DataFrame({
            '原始RSI': rsi_original[-5:],
            '2位小数RSI': rsi_2decimal[-5:]
        })
        
        print("📊 RSI计算对比:")
        print(comparison_df.to_string())
        
        # 计算误差
        error_rsi = abs(rsi_original - rsi_2decimal)
        valid_errors = error_rsi[~np.isnan(error_rsi)]
        
        print(f"\n📈 RSI计算误差统计:")
        print(f"   平均误差: {valid_errors.mean():.6f}")
        print(f"   最大误差: {valid_errors.max():.6f}")
        
        # 检查信号影响
        original_signals = np.where(rsi_original > 70, 'overbought', 
                                  np.where(rsi_original < 30, 'oversold', 'neutral'))
        decimal_signals = np.where(rsi_2decimal > 70, 'overbought',
                                 np.where(rsi_2decimal < 30, 'oversold', 'neutral'))
        
        signal_differences = np.sum(original_signals != decimal_signals)
        print(f"   信号差异数量: {signal_differences}/{len(original_signals)} ({signal_differences/len(original_signals)*100:.1f}%)")
        
        return valid_errors.mean(), signal_differences
        
    except ImportError:
        print("❌ 需要安装TA-Lib库进行RSI测试")
        return 0, 0

def analyze_deepseek_impact():
    """分析对DeepSeek分析的影响"""
    print(f"\n🤖 DeepSeek分析影响评估")
    print("=" * 80)
    
    print("📋 DeepSeek AI对数据精度的要求分析:")
    
    print("\n✅ 2位小数精度的优势:")
    print("   1. 文件大小更小，上传更快")
    print("   2. 数据更易读，DeepSeek更容易理解")
    print("   3. 减少噪音，突出主要趋势")
    print("   4. 符合金融市场显示习惯")
    print("   5. 计算速度更快")
    
    print("\n⚠️ 2位小数精度的潜在影响:")
    print("   1. 微小价格变动信息丢失")
    print("   2. 技术指标计算精度略降")
    print("   3. 高频交易信号可能受影响")
    print("   4. 累积误差可能影响长期指标")
    
    print("\n🎯 针对BTCUSDT的具体分析:")
    print("   • BTCUSDT价格通常在$20,000-$100,000+范围")
    print("   • 2位小数精度 = $0.01，相对误差极小")
    print("   • 对于$100,000的价格，0.01的误差仅为0.0001%")
    print("   • DeepSeek主要关注趋势和模式，不是精确数值")
    
    print("\n📊 建议的数据精度策略:")
    print("   • 价格数据: 2位小数 (足够精确)")
    print("   • 成交量: 整数 (无需小数)")
    print("   • 技术指标: 2-4位小数 (平衡精度和可读性)")
    print("   • 百分比指标(RSI): 2位小数")

def create_precision_optimized_csv():
    """创建精度优化的CSV文件"""
    print(f"\n🔧 创建精度优化的CSV文件")
    print("=" * 80)
    
    csv_files = [f for f in DATA_DIR.glob("*组合数据*.csv") if not f.name.endswith('.backup.csv')]
    
    for csv_file in csv_files:
        print(f"\n📝 处理文件: {csv_file.name}")
        
        try:
            df = pd.read_csv(csv_file, encoding='utf-8-sig')
            
            # 定义不同类型列的精度要求
            price_columns = ['开盘价', '最高价', '最低价', '收盘价']
            volume_columns = ['成交量', '成交额', '成交笔数', '主动买入量', '主动买入额']
            percentage_indicators = ['RSI', 'RSI_Secondary', 'RSI_Long']
            price_indicators = ['MA20', 'MA50', 'MA_LONG', 'BB_Upper', 'BB_Middle', 'BB_Lower', 
                              'BB_Long_Upper', 'BB_Long_Middle', 'BB_Long_Lower', 'ATR', 'ATR_Long']
            ratio_indicators = ['MACD', 'MACD_Signal', 'MACD_Hist', 'MACD_Long', 'MACD_Long_Signal',
                              'Stoch_SlowK', 'Stoch_SlowD', 'ATR_Ratio', 'ADX']
            
            # 应用精度设置
            for col in df.columns:
                if col in price_columns:
                    df[col] = df[col].round(2)  # 价格: 2位小数
                elif col in volume_columns:
                    df[col] = df[col].round(0).astype('int64')  # 成交量: 整数
                elif col in percentage_indicators:
                    df[col] = df[col].round(2)  # 百分比指标: 2位小数
                elif col in price_indicators:
                    df[col] = df[col].round(2)  # 价格类指标: 2位小数
                elif col in ratio_indicators:
                    df[col] = df[col].round(4)  # 比率指标: 4位小数
                elif col == 'OBV':
                    df[col] = df[col].round(0).astype('int64')  # OBV: 整数
            
            # 保存优化后的文件
            optimized_filename = csv_file.stem + '_optimized.csv'
            optimized_path = csv_file.parent / optimized_filename
            
            df.to_csv(optimized_path, encoding='utf-8-sig', index=False)
            
            # 比较文件大小
            original_size = csv_file.stat().st_size / 1024
            optimized_size = optimized_path.stat().st_size / 1024
            size_reduction = (original_size - optimized_size) / original_size * 100
            
            print(f"   ✅ 已创建优化文件: {optimized_filename}")
            print(f"   📊 文件大小: {original_size:.1f}KB → {optimized_size:.1f}KB")
            print(f"   💾 大小减少: {size_reduction:.1f}%")
            
        except Exception as e:
            print(f"   ❌ 处理失败: {e}")

def main():
    """主函数"""
    print("BTCUSDT 数据精度影响分析")
    print("=" * 80)
    print("分析小数点位数对技术指标计算和DeepSeek分析的影响")
    print("=" * 80)
    
    # 1. 分析当前数据精度
    analyze_current_precision()
    
    # 2. 测试精度影响
    ma_error_avg, ma_error_max = test_precision_impact()
    rsi_error_avg, rsi_signal_diff = test_rsi_precision_impact()
    
    # 3. DeepSeek影响分析
    analyze_deepseek_impact()
    
    # 4. 创建优化文件
    create_precision_optimized_csv()
    
    # 5. 总结建议
    print(f"\n" + "=" * 80)
    print("🎯 精度设置建议总结")
    print("=" * 80)
    
    print("✅ 推荐的精度设置:")
    print("   • 价格数据 (OHLC): 2位小数")
    print("   • 成交量数据: 整数")
    print("   • RSI等百分比指标: 2位小数")
    print("   • MA、布林带等价格指标: 2位小数")
    print("   • MACD等比率指标: 4位小数")
    
    print(f"\n📊 影响评估结果:")
    print(f"   • MA20计算误差: 平均{ma_error_avg:.6f}, 最大{ma_error_max:.6f}")
    print(f"   • RSI计算误差: 平均{rsi_error_avg:.6f}")
    print(f"   • RSI信号差异: {rsi_signal_diff}个")
    
    print(f"\n🤖 DeepSeek分析建议:")
    if ma_error_avg < 1.0 and rsi_error_avg < 0.1:
        print("   ✅ 2位小数精度对DeepSeek分析影响极小")
        print("   ✅ 建议使用2位小数以提高可读性和传输效率")
    else:
        print("   ⚠️ 建议保持更高精度以确保分析准确性")
    
    print(f"\n💡 最终建议:")
    print("   1. 对于DeepSeek分析，2位小数精度完全足够")
    print("   2. 可以显著减少文件大小，提高上传速度")
    print("   3. 不会影响DeepSeek对趋势和模式的识别")
    print("   4. 建议使用 *_optimized.csv 文件发送给DeepSeek")

if __name__ == "__main__":
    main()
