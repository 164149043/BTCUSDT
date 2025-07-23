"""
周线分析指南
介绍周线技术分析的特点和使用方法
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')

def show_weekly_analysis_introduction():
    """显示周线分析介绍"""
    print("📊 BTCUSDT 周线技术分析指南")
    print("=" * 80)
    
    print("🎯 周线分析的独特价值:")
    print("   • 宏观趋势判断: 识别长期牛熊市转换")
    print("   • 战略投资决策: 适合长期持有策略")
    print("   • 噪音过滤: 过滤短期市场波动")
    print("   • 关键支撑阻力: 识别重要的历史价格水平")
    print("   • 周期性分析: 发现市场的周期性规律")

def show_weekly_parameters():
    """显示周线技术指标参数"""
    print(f"\n⚙️ 周线技术指标参数配置")
    print("=" * 80)
    
    parameters = {
        '移动平均线系统': {
            'MA10 (短期)': '10周 ≈ 2.5个月 - 短期趋势',
            'MA26 (中期)': '26周 ≈ 6个月 - 中期趋势',
            'MA52 (长期)': '52周 ≈ 1年 - 年度趋势',
            'MA104 (超长期)': '104周 ≈ 2年 - 长期牛熊'
        },
        'MACD系统': {
            '标准MACD': '(12,26,9) - 经典参数',
            '长期MACD': '(8,21,5) - 周线优化'
        },
        'RSI系统': {
            'RSI14': '标准相对强弱指标',
            'RSI21': '长期RSI',
            'RSI30': '超长期RSI (周线特有)'
        },
        '布林带系统': {
            'BB20': '标准布林带 (20周)',
            'BB52': '年度布林带 (52周)'
        },
        '斐波那契分析': {
            '回看周期': '100周 ≈ 2年历史数据',
            '分析深度': '识别长期支撑阻力位'
        }
    }
    
    for category, params in parameters.items():
        print(f"\n📊 {category}:")
        for param, description in params.items():
            print(f"   • {param}: {description}")

def show_weekly_data_coverage():
    """显示周线数据覆盖范围"""
    print(f"\n📅 200周数据覆盖分析")
    print("=" * 80)
    
    coverage_info = {
        '时间跨度': '200周 ≈ 3.8年历史数据',
        '有效MA52后': '约148周 ≈ 2.8年有效分析数据',
        '有效MA104后': '约96周 ≈ 1.8年超长期分析',
        '斐波那契分析': '100周回看 ≈ 2年价格波动分析',
        '数据质量': '足够识别完整的市场周期'
    }
    
    print("📊 数据覆盖详情:")
    for aspect, info in coverage_info.items():
        print(f"   • {aspect}: {info}")
    
    print(f"\n🎯 周线分析优势:")
    print("   • 完整周期: 覆盖多个完整的市场周期")
    print("   • 趋势稳定: 长期移动平均线更稳定可靠")
    print("   • 信号质量: 减少假突破，提高信号质量")
    print("   • 战略价值: 适合制定长期投资策略")

def show_weekly_trading_strategies():
    """显示周线交易策略"""
    print(f"\n💡 周线交易策略指南")
    print("=" * 80)
    
    strategies = {
        '长期投资策略': {
            '适用人群': '长期投资者，机构投资者',
            '持仓周期': '3个月 - 2年',
            '关键指标': 'MA52, MA104, 长期MACD',
            '入场信号': 'MA52上穿MA104，MACD金叉',
            '止损策略': '跌破MA52或关键斐波那契支撑',
            '目标设定': '斐波那契扩展1.618或历史高点'
        },
        '趋势跟踪策略': {
            '适用人群': '趋势交易者',
            '持仓周期': '1-6个月',
            '关键指标': 'MA26, MA52, RSI周线',
            '入场信号': '价格站上MA26，RSI>50',
            '止损策略': '跌破MA26',
            '目标设定': '下一个斐波那契阻力位'
        },
        '反转抄底策略': {
            '适用人群': '价值投资者',
            '持仓周期': '6个月 - 2年',
            '关键指标': 'RSI30, 布林带下轨, 斐波那契支撑',
            '入场信号': 'RSI30<30，价格触及布林带下轨',
            '止损策略': '跌破关键斐波那契支撑',
            '目标设定': '回到MA52或斐波那契61.8%'
        }
    }
    
    for strategy, details in strategies.items():
        print(f"\n🎯 {strategy}:")
        for aspect, info in details.items():
            print(f"   • {aspect}: {info}")

def show_weekly_vs_other_timeframes():
    """显示周线与其他时间周期的对比"""
    print(f"\n📊 时间周期对比分析")
    print("=" * 80)
    
    comparison = {
        '15分钟线': {
            '数据跨度': '2.1天',
            '适用交易': '日内交易',
            '信号频率': '极高',
            '噪音水平': '高',
            '适合人群': '日内交易者'
        },
        '1小时线': {
            '数据跨度': '8.3天',
            '适用交易': '短线交易',
            '信号频率': '高',
            '噪音水平': '中等',
            '适合人群': '短线交易者'
        },
        '日线': {
            '数据跨度': '6.7个月',
            '适用交易': '中期交易',
            '信号频率': '中等',
            '噪音水平': '低',
            '适合人群': '波段交易者'
        },
        '周线': {
            '数据跨度': '3.8年',
            '适用交易': '长期投资',
            '信号频率': '低',
            '噪音水平': '极低',
            '适合人群': '长期投资者'
        }
    }
    
    print(f"{'时间周期':<10} {'数据跨度':<12} {'适用交易':<12} {'信号频率':<8} {'噪音水平':<8} {'适合人群'}")
    print("-" * 80)
    
    for timeframe, info in comparison.items():
        print(f"{timeframe:<10} {info['数据跨度']:<12} {info['适用交易']:<12} {info['信号频率']:<8} {info['噪音水平']:<8} {info['适合人群']}")

def show_weekly_fibonacci_analysis():
    """显示周线斐波那契分析特点"""
    print(f"\n🔢 周线斐波那契分析特点")
    print("=" * 80)
    
    print("🎯 周线斐波那契的独特价值:")
    print("   • 长期支撑阻力: 识别多年有效的关键价格水平")
    print("   • 牛熊转换点: 发现长期趋势的转折点")
    print("   • 战略买卖点: 提供长期投资的最佳时机")
    print("   • 风险管理: 设定长期持仓的止损位")
    
    print(f"\n📊 周线斐波那契水平意义:")
    fib_levels = {
        '23.6%回调': '浅度调整，趋势延续概率高',
        '38.2%回调': '中度调整，关键支撑位',
        '50%回调': '深度调整，心理关键位',
        '61.8%回调': '黄金比例，强力支撑/阻力',
        '78.6%回调': '极深调整，趋势可能反转',
        '127.2%扩展': '第一目标位，获利了结点',
        '161.8%扩展': '黄金扩展，主要目标位'
    }
    
    for level, meaning in fib_levels.items():
        print(f"   • {level}: {meaning}")

def show_weekly_ai_analysis_tips():
    """显示周线AI分析建议"""
    print(f"\n🤖 周线DeepSeek AI分析建议")
    print("=" * 80)
    
    print("📝 周线专用提示词:")
    print("""
请分析我上传的BTCUSDT周线数据文件（200周≈3.8年数据）。
数据包含长期技术指标：
- MA系统: MA10(2.5月)/MA26(6月)/MA52(1年)/MA104(2年)
- 长期MACD: 适配周线的参数配置
- RSI系统: 包含RSI30超长期指标
- 布林带: BB20标准 + BB52年度布林带
- 斐波那契: 100周回看，识别长期支撑阻力

请基于周线特点完成宏观分析:
1. 长期趋势判断 (基于MA52/MA104系统)
2. 牛熊市周期分析 (结合历史价格波动)
3. 关键斐波那契水平 (长期支撑阻力位)
4. 战略投资建议 (3个月-2年持仓策略)
5. 风险管理建议 (长期止损和目标位)

要求: 重点关注长期趋势，提供战略性投资建议。
    """)
    
    print(f"\n✅ 周线AI分析优势:")
    print("   • 宏观视角: 3.8年数据提供完整市场周期视角")
    print("   • 趋势稳定: 长期指标减少噪音，信号更可靠")
    print("   • 战略价值: 适合制定长期投资和资产配置策略")
    print("   • 风险控制: 长期止损位更加稳定可靠")

def main():
    """主函数"""
    print("BTCUSDT 周线技术分析完整指南")
    print("=" * 80)
    
    # 显示周线分析介绍
    show_weekly_analysis_introduction()
    
    # 显示周线参数配置
    show_weekly_parameters()
    
    # 显示数据覆盖范围
    show_weekly_data_coverage()
    
    # 显示交易策略
    show_weekly_trading_strategies()
    
    # 显示时间周期对比
    show_weekly_vs_other_timeframes()
    
    # 显示斐波那契分析
    show_weekly_fibonacci_analysis()
    
    # 显示AI分析建议
    show_weekly_ai_analysis_tips()
    
    print(f"\n" + "=" * 80)
    print("🎉 周线分析系统已就绪!")
    print("✅ 200周数据覆盖3.8年历史")
    print("✅ 专门优化的长期技术指标")
    print("✅ 完整的斐波那契分析体系")
    print("✅ 适合长期投资和战略决策")
    
    print(f"\n🚀 使用方法:")
    print("   1. 运行 python main.py")
    print("   2. 选择选项 1 (执行完整分析流程)")
    print("   3. 选择选项 5 (周线)")
    print("   4. 等待生成周线组合数据和分析报告")
    print("   5. 将文件发送给DeepSeek AI进行宏观分析")

if __name__ == "__main__":
    main()
