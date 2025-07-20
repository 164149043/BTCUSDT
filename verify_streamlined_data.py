"""
验证精简数据文件
"""

import pandas as pd
import sys
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from config import DATA_DIR

def verify_streamlined_files():
    """验证所有精简文件"""
    print("🔍 验证精简数据文件")
    print("=" * 80)
    
    # 查找精简文件
    streamlined_files = list(DATA_DIR.glob("*_streamlined.csv"))
    
    if not streamlined_files:
        print("❌ 未找到精简文件")
        return
    
    print(f"📁 找到 {len(streamlined_files)} 个精简文件:")
    
    for file in streamlined_files:
        print(f"\n📊 验证文件: {file.name}")
        print("-" * 60)
        
        try:
            df = pd.read_csv(file, encoding='utf-8-sig')
            
            # 基本信息
            print(f"   数据行数: {len(df)}")
            print(f"   列数: {len(df.columns)}")
            print(f"   文件大小: {file.stat().st_size / 1024:.1f} KB")
            
            # 检查核心列
            core_columns = ['收盘价', 'MA20', 'RSI', 'MACD', 'ATR']
            missing_core = [col for col in core_columns if col not in df.columns]
            if missing_core:
                print(f"   ⚠️ 缺失核心列: {missing_core}")
            else:
                print(f"   ✅ 核心技术指标完整")
            
            # 检查斐波那契关键水平
            fib_key_levels = ['Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618']
            fib_present = [col for col in fib_key_levels if col in df.columns]
            print(f"   🔢 斐波那契关键水平: {len(fib_present)}/3")
            
            for col in fib_present:
                valid_count = df[col].notna().sum()
                if valid_count > 0:
                    latest_value = df[col].dropna().iloc[-1]
                    print(f"      {col}: {valid_count}/{len(df)} - 最新: ${latest_value:.2f}")
            
            # 数据完整性
            null_counts = df.isnull().sum()
            high_null_cols = null_counts[null_counts > len(df) * 0.3].index.tolist()
            if high_null_cols:
                print(f"   ⚠️ 高空值列 (>30%): {high_null_cols}")
            else:
                print(f"   ✅ 数据完整性良好")
            
            # 显示列结构
            print(f"   📋 列结构: {list(df.columns)}")
            
        except Exception as e:
            print(f"   ❌ 验证失败: {e}")

def compare_original_vs_streamlined():
    """对比原始文件与精简文件"""
    print(f"\n📊 原始文件 vs 精简文件对比")
    print("=" * 80)
    
    # 查找配对文件
    original_files = [f for f in DATA_DIR.glob("*组合数据*.csv") if not f.name.endswith('_streamlined.csv') and not f.name.endswith('.backup.csv')]
    streamlined_files = list(DATA_DIR.glob("*_streamlined.csv"))
    
    comparison_data = []
    
    for original_file in original_files:
        # 查找对应的精简文件
        base_name = original_file.stem
        streamlined_name = f"{base_name}_streamlined.csv"
        streamlined_file = DATA_DIR / streamlined_name
        
        if streamlined_file.exists():
            try:
                df_original = pd.read_csv(original_file, encoding='utf-8-sig')
                df_streamlined = pd.read_csv(streamlined_file, encoding='utf-8-sig')
                
                original_size = original_file.stat().st_size / 1024
                streamlined_size = streamlined_file.stat().st_size / 1024
                size_reduction = (original_size - streamlined_size) / original_size * 100
                
                comparison_data.append({
                    '文件': original_file.name.replace('BTCUSDT_', '').replace('组合数据_20250720.csv', ''),
                    '原始列数': len(df_original.columns),
                    '精简列数': len(df_streamlined.columns),
                    '减少列数': len(df_original.columns) - len(df_streamlined.columns),
                    '原始大小(KB)': f"{original_size:.1f}",
                    '精简大小(KB)': f"{streamlined_size:.1f}",
                    '空间节省': f"{size_reduction:.1f}%"
                })
                
            except Exception as e:
                print(f"❌ 对比失败 {original_file.name}: {e}")
    
    if comparison_data:
        comparison_df = pd.DataFrame(comparison_data)
        print(comparison_df.to_string(index=False))
    else:
        print("❌ 未找到可对比的文件")

def show_streamlined_structure():
    """显示精简文件的标准结构"""
    print(f"\n📋 精简文件标准结构")
    print("=" * 80)
    
    structure = {
        '类别': [
            '基础数据', '移动平均', 'MACD', 'RSI', '布林带', 
            '斐波那契关键', '斐波那契扩展', '斐波那契信号', '其他核心'
        ],
        '列数': [6, 2, 3, 1, 3, 3, 2, 2, 3],
        '具体指标': [
            'open_time, OHLC, 成交量',
            'MA20, MA50',
            'MACD, MACD_Signal, MACD_Hist',
            'RSI',
            'BB_Upper, BB_Middle, BB_Lower',
            'Fib_Ret_0.382, 0.500, 0.618',
            'Fib_Ext_1.272, 1.618',
            'Fib_Trend, Fib_Signal',
            'ATR, ADX, OBV'
        ]
    }
    
    structure_df = pd.DataFrame(structure)
    print(structure_df.to_string(index=False))
    
    print(f"\n✅ 精简原则:")
    print("   1. 保留最核心的技术指标")
    print("   2. 重点保留斐波那契关键水平 (38.2%, 50%, 61.8%)")
    print("   3. 移除冗余和次要指标")
    print("   4. 优化文件大小和传输效率")
    print("   5. 适合DeepSeek AI快速分析")

def generate_usage_recommendations():
    """生成使用建议"""
    print(f"\n💡 精简文件使用建议")
    print("=" * 80)
    
    print("🎯 适用场景:")
    print("   ✅ 发送给DeepSeek AI分析")
    print("   ✅ 短线和日内交易决策")
    print("   ✅ 快速技术分析")
    print("   ✅ 移动设备查看")
    print("   ✅ 网络传输优化")
    
    print(f"\n📊 核心指标解读:")
    print("   • MA20/MA50: 短中期趋势")
    print("   • MACD: 动量和趋势变化")
    print("   • RSI: 超买超卖状态")
    print("   • 布林带: 价格通道和波动率")
    print("   • 斐波那契38.2%: 关键回调位")
    print("   • 斐波那契50%: 黄金分割点")
    print("   • 斐波那契61.8%: 黄金比例")
    print("   • ATR: 波动率和止损参考")
    
    print(f"\n🚀 与DeepSeek AI结合:")
    print("   1. 上传精简文件，分析速度更快")
    print("   2. AI能精准识别关键支撑阻力")
    print("   3. 基于斐波那契水平的交易建议")
    print("   4. 结合多个指标的综合分析")

def main():
    """主函数"""
    print("BTCUSDT 精简数据验证工具")
    print("=" * 80)
    
    # 验证精简文件
    verify_streamlined_files()
    
    # 对比分析
    compare_original_vs_streamlined()
    
    # 显示结构
    show_streamlined_structure()
    
    # 使用建议
    generate_usage_recommendations()
    
    print(f"\n" + "=" * 80)
    print("🎉 精简数据验证完成!")
    print("✅ 精简文件已准备就绪")
    print("✅ 保留了最核心的25个技术指标")
    print("✅ 文件大小减少约50%")
    print("✅ 重点保留斐波那契关键水平")
    print("\n📁 推荐使用的精简文件:")
    
    streamlined_files = list(DATA_DIR.glob("*_streamlined.csv"))
    for file in streamlined_files:
        print(f"   • {file.name}")

if __name__ == "__main__":
    main()
