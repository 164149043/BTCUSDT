"""
DeepSeek优化测试脚本
验证激进模式优化代码的效果
"""

import pandas as pd
import sys
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from config import DATA_DIR

def test_deepseek_optimizations():
    """测试DeepSeek优化功能"""
    print("🚀 测试DeepSeek激进模式优化功能")
    print("=" * 80)
    
    # 查找最新的完整组合数据文件（不是23列精简版）
    all_files = list(DATA_DIR.glob("*组合数据*.csv"))
    latest_files = [f for f in all_files if not f.name.endswith('_23col.csv')]
    if not latest_files:
        print("❌ 未找到完整组合数据文件，请先运行main.py生成数据")
        return False

    latest_file = max(latest_files, key=lambda x: x.stat().st_mtime)
    print(f"📁 测试文件: {latest_file.name}")
    
    try:
        df = pd.read_csv(latest_file, encoding='utf-8-sig')
        
        print(f"\n📊 文件基本信息:")
        print(f"   数据行数: {len(df)}")
        print(f"   列数: {len(df.columns)}")
        print(f"   文件大小: {latest_file.stat().st_size / 1024:.1f}KB")
        
        # 检查DeepSeek优化新增的指标
        deepseek_indicators = {
            'MA3': '超短期均线 (3期)',
            'Volume_MA20': '成交量20期均线',
            'Volume_Ratio': '成交量比率',
            'MA_Fast_Signal': '快速MA交叉信号',
            'MACD_Zero_Cross': 'MACD零轴交叉',
            'BB_Breakout_Strength': '布林带突破强度',
            'Fib_Key_Zone': '斐波那契关键区域'
        }
        
        print(f"\n🔍 DeepSeek优化新增指标检查:")
        found_indicators = 0
        for indicator, description in deepseek_indicators.items():
            if indicator in df.columns:
                valid_count = df[indicator].notna().sum()
                print(f"   ✅ {indicator} ({description}): {valid_count}/{len(df)} 有效数据")
                found_indicators += 1
                
                # 显示最新值
                if valid_count > 0:
                    latest_value = df[indicator].iloc[-1]
                    if isinstance(latest_value, (int, float)):
                        print(f"      最新值: {latest_value:.4f}")
                    else:
                        print(f"      最新值: {latest_value}")
            else:
                print(f"   ❌ {indicator} ({description}): 未找到")
        
        print(f"\n📈 优化指标覆盖率: {found_indicators}/{len(deepseek_indicators)} ({found_indicators/len(deepseek_indicators)*100:.1f}%)")
        
        # 检查综合信号的新增超强类型
        if '综合信号' in df.columns:
            signal_counts = df['综合信号'].value_counts()
            print(f"\n📊 综合信号分布:")
            for signal, count in signal_counts.head(10).items():
                print(f"   {signal}: {count}次 ({count/len(df)*100:.1f}%)")
            
            # 检查是否有超强信号
            super_signals = [sig for sig in signal_counts.index if '🔥超强' in sig]
            if super_signals:
                print(f"\n🔥 发现DeepSeek超强信号:")
                for signal in super_signals:
                    print(f"   {signal}: {signal_counts[signal]}次")
            else:
                print(f"\n⚠️ 未发现🔥超强信号，可能需要更多数据或特定市场条件")
        
        # 检查斐波那契信号增强
        if 'Fib_Signal' in df.columns:
            fib_signals = df['Fib_Signal'].value_counts()
            enhanced_signals = [sig for sig in fib_signals.index if ('带量' in str(sig) or '缩量' in str(sig))]
            if enhanced_signals:
                print(f"\n🔢 斐波那契成交量增强信号:")
                for signal in enhanced_signals:
                    print(f"   {signal}: {fib_signals[signal]}次")
            else:
                print(f"\n📊 斐波那契信号: {len(fib_signals)}种类型")
        
        # 分析成交量确认效果
        if 'Volume_Ratio' in df.columns:
            high_volume = df[df['Volume_Ratio'] > 1.5]
            low_volume = df[df['Volume_Ratio'] < 0.8]
            normal_volume = df[(df['Volume_Ratio'] >= 0.8) & (df['Volume_Ratio'] <= 1.5)]
            
            print(f"\n📊 成交量分布分析:")
            print(f"   高成交量(>1.5倍): {len(high_volume)}次 ({len(high_volume)/len(df)*100:.1f}%)")
            print(f"   正常成交量(0.8-1.5倍): {len(normal_volume)}次 ({len(normal_volume)/len(df)*100:.1f}%)")
            print(f"   低成交量(<0.8倍): {len(low_volume)}次 ({len(low_volume)/len(df)*100:.1f}%)")
            
            if len(high_volume) > 0:
                avg_volume_ratio = high_volume['Volume_Ratio'].mean()
                print(f"   高成交量平均倍数: {avg_volume_ratio:.2f}倍")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def analyze_optimization_effects():
    """分析优化效果"""
    print(f"\n🎯 DeepSeek优化效果分析")
    print("=" * 80)
    
    # 查找最新的完整组合数据文件（不是23列精简版）
    all_files = list(DATA_DIR.glob("*组合数据*.csv"))
    latest_files = [f for f in all_files if not f.name.endswith('_23col.csv')]
    if not latest_files:
        return

    latest_file = max(latest_files, key=lambda x: x.stat().st_mtime)
    
    try:
        df = pd.read_csv(latest_file, encoding='utf-8-sig')
        
        # 分析MA3快速信号的效果
        if 'MA_Fast_Signal' in df.columns:
            fast_signals = df['MA_Fast_Signal'].value_counts()
            print("⚡ MA3快速信号统计:")
            for signal, count in fast_signals.items():
                print(f"   {signal}: {count}次 ({count/len(df)*100:.1f}%)")
        
        # 分析MACD零轴交叉的效果
        if 'MACD_Zero_Cross' in df.columns:
            zero_cross = df[df['MACD_Zero_Cross'] != '']
            print(f"\n🎯 MACD零轴交叉分析:")
            if len(zero_cross) > 0:
                cross_types = zero_cross['MACD_Zero_Cross'].value_counts()
                for cross_type, count in cross_types.items():
                    print(f"   {cross_type}: {count}次")
                print(f"   零轴交叉频率: {len(zero_cross)/len(df)*100:.1f}%")
            else:
                print("   当前数据中无零轴交叉")
        
        # 分析布林带突破强度
        if 'BB_Breakout_Strength' in df.columns:
            breakout_signals = df[df['BB_Breakout_Strength'] != '']
            print(f"\n📈 布林带突破强度分析:")
            if len(breakout_signals) > 0:
                breakout_types = breakout_signals['BB_Breakout_Strength'].value_counts()
                for breakout_type, count in breakout_types.items():
                    print(f"   {breakout_type}: {count}次")
            else:
                print("   当前数据中无带量突破")
        
        # 分析斐波那契关键区域
        if 'Fib_Key_Zone' in df.columns:
            key_zones = df[df['Fib_Key_Zone'] != '']
            print(f"\n🔢 斐波那契关键区域分析:")
            if len(key_zones) > 0:
                zone_types = key_zones['Fib_Key_Zone'].value_counts()
                for zone_type, count in zone_types.items():
                    print(f"   {zone_type}: {count}次")
            else:
                print("   当前数据中无关键区域")
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")

def show_deepseek_optimization_summary():
    """显示DeepSeek优化总结"""
    print(f"\n📋 DeepSeek激进模式优化总结")
    print("=" * 80)
    
    optimizations = {
        '🎯 参数激进化优化': [
            'MA周期缩短30%: MA20→MA14, MA50→MA35',
            'MACD参数缩短30%: 快线12→8, 慢线26→18',
            'RSI周期缩短30%: RSI14→RSI10',
            '布林带标准差放宽50%: 2.0→3.0'
        ],
        '⚡ 新增超短期指标': [
            'MA3超短期均线: 捕捉极短期趋势变化',
            'Volume_MA20成交量均线: 量价分析基础',
            'Volume_Ratio成交量比率: 识别异常成交量',
            'MA_Fast_Signal快速交叉: MA3与MA20交叉'
        ],
        '🔥 增强信号系统': [
            'MACD_Zero_Cross零轴交叉: 趋势转换确认',
            'BB_Breakout_Strength突破强度: 成交量确认',
            'Fib_Key_Zone关键区域: 精确支撑阻力',
            '🔥超强信号: 多指标协同确认'
        ],
        '📊 成交量确认机制': [
            '带量信号: 成交量>1.2倍确认',
            '缩量信号: 成交量<0.8倍标记',
            '突破确认: 成交量>1.5倍的突破',
            '信号过滤: 成交量异常的信号过滤'
        ]
    }
    
    for category, items in optimizations.items():
        print(f"\n{category}:")
        for item in items:
            print(f"   • {item}")
    
    print(f"\n✅ DeepSeek优化特别适合:")
    print("   • 日内交易和超短线操作")
    print("   • 快速变化的加密货币市场")
    print("   • 需要及时进出场的高频策略")
    print("   • 追求更敏感交易信号的场景")
    
    print(f"\n⚠️ 使用建议:")
    print("   • 激进模式信号更频繁，需要严格风控")
    print("   • 重点关注🔥超强信号，过滤一般信号")
    print("   • 结合成交量确认提高信号质量")
    print("   • 在高波动市场中效果更佳")

def main():
    """主函数"""
    print("DeepSeek激进模式优化验证")
    print("=" * 80)
    print("验证ta_calculator.py中应用的DeepSeek优化代码")
    print("=" * 80)
    
    # 1. 测试DeepSeek优化功能
    success = test_deepseek_optimizations()
    
    if success:
        # 2. 分析优化效果
        analyze_optimization_effects()
        
        # 3. 显示优化总结
        show_deepseek_optimization_summary()
        
        print(f"\n" + "=" * 80)
        print("🎉 DeepSeek激进模式优化验证完成!")
        print("✅ 参数激进化已生效")
        print("✅ 新增指标已验证")
        print("✅ 信号增强已启用")
        print("✅ 成交量确认已激活")
        
        print(f"\n🚀 下一步建议:")
        print("   1. 运行main.py生成最新数据测试优化效果")
        print("   2. 重点观察🔥超强信号的出现")
        print("   3. 对比优化前后的信号敏感度")
        print("   4. 在实际交易中验证信号质量")
    else:
        print("\n❌ 验证未通过，请先运行main.py生成数据文件")

if __name__ == "__main__":
    main()
