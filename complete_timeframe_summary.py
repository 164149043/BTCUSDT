"""
完整时间周期总结
展示所有5个时间周期的特点和使用建议
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')

def show_complete_timeframe_overview():
    """显示完整时间周期概览"""
    print("📊 BTCUSDT 完整时间周期技术分析系统")
    print("=" * 80)
    
    print("🎯 系统特点:")
    print("   • 5个时间周期: 15分钟线 → 1小时线 → 4小时线 → 日线 → 周线")
    print("   • 200条数据: 统一优化，平衡效率与质量")
    print("   • 智能参数: 每个时间周期专门优化的技术指标参数")
    print("   • 完整覆盖: 从超短线到长期投资全覆盖")
    print("   • AI优化: 专为DeepSeek AI分析优化")

def show_timeframe_comparison_table():
    """显示时间周期对比表"""
    print(f"\n📊 时间周期详细对比")
    print("=" * 80)
    
    timeframes = {
        '15分钟线': {
            '数据跨度': '2.1天',
            '适用交易': '超短线/剥头皮',
            '持仓周期': '几分钟-几小时',
            '信号频率': '极高',
            '噪音水平': '高',
            '核心MA': 'MA20/MA50/MA55',
            '适合人群': '日内交易者',
            '文件大小': '~53KB'
        },
        '1小时线': {
            '数据跨度': '8.3天',
            '适用交易': '短线交易',
            '持仓周期': '几小时-2天',
            '信号频率': '高',
            '噪音水平': '中等',
            '核心MA': 'MA20/MA50/MA89',
            '适合人群': '短线交易者',
            '文件大小': '~55KB'
        },
        '4小时线': {
            '数据跨度': '33.3天',
            '适用交易': '中短期交易',
            '持仓周期': '1-7天',
            '信号频率': '中等',
            '噪音水平': '低',
            '核心MA': 'MA20/MA50/MA144',
            '适合人群': '波段交易者',
            '文件大小': '~52KB'
        },
        '日线': {
            '数据跨度': '6.7个月',
            '适用交易': '中长期投资',
            '持仓周期': '1周-3个月',
            '信号频率': '中等',
            '噪音水平': '低',
            '核心MA': 'MA21/MA55/MA100/MA150',
            '适合人群': '投资者',
            '文件大小': '~50KB'
        },
        '周线': {
            '数据跨度': '3.8年',
            '适用交易': '长期投资',
            '持仓周期': '3个月-2年',
            '信号频率': '低',
            '噪音水平': '极低',
            '核心MA': 'MA10/MA26/MA52/MA104',
            '适合人群': '长期投资者',
            '文件大小': '~49KB'
        }
    }
    
    # 创建对比表
    headers = ['时间周期', '数据跨度', '适用交易', '持仓周期', '信号频率', '核心MA', '适合人群', '文件大小']
    print(f"{'时间周期':<8} {'数据跨度':<8} {'适用交易':<12} {'持仓周期':<12} {'信号频率':<8} {'适合人群':<10} {'文件大小':<8}")
    print("-" * 80)
    
    for timeframe, info in timeframes.items():
        print(f"{timeframe:<8} {info['数据跨度']:<8} {info['适用交易']:<12} {info['持仓周期']:<12} {info['信号频率']:<8} {info['适合人群']:<10} {info['文件大小']:<8}")

def show_ma_system_comparison():
    """显示MA系统对比"""
    print(f"\n📈 各时间周期MA系统对比")
    print("=" * 80)
    
    ma_systems = {
        '15分钟线': {
            'MA20': '20×15分钟 = 5小时',
            'MA50': '50×15分钟 = 12.5小时',
            'MA55': '55×15分钟 = 13.75小时'
        },
        '1小时线': {
            'MA20': '20小时',
            'MA50': '50小时 ≈ 2天',
            'MA89': '89小时 ≈ 3.7天'
        },
        '4小时线': {
            'MA20': '80小时 ≈ 3.3天',
            'MA50': '200小时 ≈ 8.3天',
            'MA144': '576小时 ≈ 24天'
        },
        '日线': {
            'MA21': '21天 ≈ 3周',
            'MA55': '55天 ≈ 2个月',
            'MA100': '100天 ≈ 3.3个月',
            'MA150': '150天 ≈ 5个月'
        },
        '周线': {
            'MA10': '10周 ≈ 2.5个月',
            'MA26': '26周 ≈ 6个月',
            'MA52': '52周 ≈ 1年',
            'MA104': '104周 ≈ 2年'
        }
    }
    
    for timeframe, mas in ma_systems.items():
        print(f"\n📊 {timeframe}:")
        for ma, period in mas.items():
            print(f"   • {ma}: {period}")

def show_fibonacci_analysis_comparison():
    """显示斐波那契分析对比"""
    print(f"\n🔢 各时间周期斐波那契分析特点")
    print("=" * 80)
    
    fib_analysis = {
        '15分钟线': {
            '回看周期': '30个15分钟 ≈ 7.5小时',
            '适用场景': '日内支撑阻力',
            '信号特点': '频繁但短期有效',
            '主要用途': '日内交易的进出场点'
        },
        '1小时线': {
            '回看周期': '60个1小时 ≈ 2.5天',
            '适用场景': '短期波段支撑阻力',
            '信号特点': '中等频率，1-3天有效',
            '主要用途': '短线交易的关键位置'
        },
        '4小时线': {
            '回看周期': '60个4小时 ≈ 10天',
            '适用场景': '中期趋势支撑阻力',
            '信号特点': '较稳定，1-2周有效',
            '主要用途': '波段交易的重要参考'
        },
        '日线': {
            '回看周期': '70天 ≈ 2.3个月',
            '适用场景': '中长期支撑阻力',
            '信号特点': '稳定可靠，月度有效',
            '主要用途': '投资决策的关键水平'
        },
        '周线': {
            '回看周期': '100周 ≈ 2年',
            '适用场景': '长期战略支撑阻力',
            '信号特点': '极其稳定，年度有效',
            '主要用途': '长期投资的核心参考'
        }
    }
    
    for timeframe, fib_info in fib_analysis.items():
        print(f"\n📊 {timeframe}:")
        for aspect, info in fib_info.items():
            print(f"   • {aspect}: {info}")

def show_trading_strategy_recommendations():
    """显示交易策略建议"""
    print(f"\n💡 多时间周期交易策略建议")
    print("=" * 80)
    
    print("🎯 单一时间周期策略:")
    
    single_strategies = {
        '超短线策略 (15分钟线)': {
            '目标': '日内快速获利',
            '持仓': '几分钟到几小时',
            '关键指标': 'MA20, RSI, MACD短期',
            '风险控制': 'ATR×1.5止损',
            '适合人群': '专业日内交易者'
        },
        '短线策略 (1小时线)': {
            '目标': '1-3天波段获利',
            '持仓': '几小时到2天',
            '关键指标': 'MA50, 布林带, 斐波那契',
            '风险控制': 'ATR×2止损',
            '适合人群': '短线交易者'
        },
        '中线策略 (日线)': {
            '目标': '1-3个月趋势获利',
            '持仓': '1周到3个月',
            '关键指标': 'MA100, MA150, 长期MACD',
            '风险控制': 'ATR×3止损',
            '适合人群': '投资者'
        },
        '长线策略 (周线)': {
            '目标': '长期价值投资',
            '持仓': '3个月到2年',
            '关键指标': 'MA52, MA104, 周线斐波那契',
            '风险控制': '重要支撑位止损',
            '适合人群': '长期投资者'
        }
    }
    
    for strategy, details in single_strategies.items():
        print(f"\n📊 {strategy}:")
        for aspect, info in details.items():
            print(f"   • {aspect}: {info}")
    
    print(f"\n🔄 多时间周期确认策略:")
    print("   1. 周线确定大方向 (牛市/熊市)")
    print("   2. 日线确定中期趋势 (上涨/下跌/盘整)")
    print("   3. 4小时线寻找入场时机")
    print("   4. 1小时线精确入场点位")
    print("   5. 15分钟线优化进出场")

def show_ai_analysis_recommendations():
    """显示AI分析建议"""
    print(f"\n🤖 DeepSeek AI多时间周期分析建议")
    print("=" * 80)
    
    print("📝 不同时间周期的AI分析重点:")
    
    ai_focus = {
        '15分钟线': '重点关注短期动量，RSI超买超卖，MACD短期背离',
        '1小时线': '关注短期趋势，MA20/50关系，布林带突破',
        '4小时线': '分析中期趋势，多重指标确认，关键支撑阻力',
        '日线': '判断长期趋势，MA100/150方向，月度策略制定',
        '周线': '宏观趋势分析，年度投资策略，长期支撑阻力'
    }
    
    for timeframe, focus in ai_focus.items():
        print(f"   • {timeframe}: {focus}")
    
    print(f"\n🎯 推荐的AI分析流程:")
    print("   1. 先分析周线，确定大趋势和长期策略")
    print("   2. 再看日线，制定中期交易计划")
    print("   3. 用4小时线寻找具体入场时机")
    print("   4. 用1小时线精确入场点位")
    print("   5. 用15分钟线优化执行细节")

def main():
    """主函数"""
    print("BTCUSDT 完整时间周期技术分析系统总结")
    print("=" * 80)
    
    # 显示系统概览
    show_complete_timeframe_overview()
    
    # 显示时间周期对比
    show_timeframe_comparison_table()
    
    # 显示MA系统对比
    show_ma_system_comparison()
    
    # 显示斐波那契分析对比
    show_fibonacci_analysis_comparison()
    
    # 显示交易策略建议
    show_trading_strategy_recommendations()
    
    # 显示AI分析建议
    show_ai_analysis_recommendations()
    
    print(f"\n" + "=" * 80)
    print("🎉 完整时间周期系统已就绪!")
    print("✅ 5个时间周期全覆盖")
    print("✅ 200条数据统一优化")
    print("✅ 智能参数配置")
    print("✅ 完整斐波那契分析")
    print("✅ AI分析友好")
    
    print(f"\n🚀 使用建议:")
    print("   • 新手: 从日线开始，逐步扩展到其他时间周期")
    print("   • 短线: 重点使用15分钟线和1小时线")
    print("   • 投资: 重点使用日线和周线")
    print("   • 专业: 结合多个时间周期进行确认")
    
    print(f"\n📁 所有优化文件:")
    optimized_files = list(DATA_DIR.glob("*_optimized.csv"))
    for file in optimized_files:
        size_kb = file.stat().st_size / 1024
        print(f"   • {file.name} ({size_kb:.1f}KB)")

if __name__ == "__main__":
    main()
