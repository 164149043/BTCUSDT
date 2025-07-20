"""
分析220条数据对技术指标计算的影响
评估是否需要调整指标参数
"""

import pandas as pd
import sys
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from config import TIMEFRAME_INDICATOR_PARAMS

def analyze_indicator_requirements():
    """分析各指标对数据量的要求"""
    print("📊 技术指标数据量需求分析")
    print("=" * 80)
    
    # 基础指标最小数据需求
    basic_requirements = {
        'MA20': 20,
        'MA50': 50,
        'MA200': 200,
        'MA300': 300,
        'MACD(12,26,9)': 35,  # 26 + 9
        'RSI(14)': 15,        # 14 + 1 for calculation
        'BB(20,2)': 20,
        'ATR(14)': 14,
        'ADX(14)': 28,        # 需要更多数据计算DI
        'Stoch(14,3,3)': 17,  # 14 + 3
        'OBV': 1,             # 只需要前一天数据
        '斐波那契': 30        # 最少需要30个点找高低点
    }
    
    print("📋 基础指标最小数据需求:")
    for indicator, min_data in basic_requirements.items():
        status = "✅" if min_data <= 220 else "⚠️"
        print(f"   {status} {indicator}: 最少需要 {min_data} 条数据")
    
    return basic_requirements

def analyze_timeframe_parameters():
    """分析各时间周期参数对220条数据的适应性"""
    print(f"\n🔍 各时间周期参数适应性分析")
    print("=" * 80)
    
    for timeframe, params in TIMEFRAME_INDICATOR_PARAMS.items():
        print(f"\n📈 {timeframe}:")
        print(f"   描述: {params['description']}")
        
        # 检查可能有问题的参数
        problematic_params = []
        
        # 检查MA参数
        for ma_key in ['MA_LONG_TERM', 'MA_EXTRA_LONG']:
            if ma_key in params and params[ma_key] >= 220:
                problematic_params.append(f"{ma_key}: {params[ma_key]}")
        
        # 检查布林带长期参数
        if 'BB_LONG_PERIOD' in params and params['BB_LONG_PERIOD'] >= 220:
            problematic_params.append(f"BB_LONG_PERIOD: {params['BB_LONG_PERIOD']}")
        
        # 检查斐波那契回看周期
        if 'FIB_LOOKBACK_PERIOD' in params and params['FIB_LOOKBACK_PERIOD'] >= 220:
            problematic_params.append(f"FIB_LOOKBACK_PERIOD: {params['FIB_LOOKBACK_PERIOD']}")
        
        if problematic_params:
            print(f"   ⚠️ 需要调整的参数: {', '.join(problematic_params)}")
        else:
            print(f"   ✅ 所有参数适合220条数据")

def suggest_parameter_adjustments():
    """建议参数调整方案"""
    print(f"\n🔧 参数调整建议")
    print("=" * 80)
    
    adjustments = {
        '日线': {
            'current_issues': [
                'MA_LONG_TERM: 200 → 建议调整为 150',
                'MA_EXTRA_LONG: 300 → 建议调整为 200',
                'BB_LONG_PERIOD: 100 → 建议调整为 89'
            ],
            'reasoning': '日线数据220条约7.3个月，长期指标需要适当缩短'
        },
        '4小时线': {
            'current_issues': [
                'MA_LONG_TERM: 144 → 可保持，但接近上限',
                'BB_LONG_PERIOD: 89 → 可保持'
            ],
            'reasoning': '4小时线220条约36.7天，大部分参数合适'
        },
        '1小时线': {
            'current_issues': [
                'MA_LONG_TERM: 89 → 可保持',
                'BB_LONG_PERIOD: 50 → 可保持'
            ],
            'reasoning': '1小时线220条约9.2天，参数设置合理'
        },
        '15分钟线': {
            'current_issues': [
                'MA_LONG_TERM: 55 → 可保持',
                'BB_LONG_PERIOD: 30 → 可保持'
            ],
            'reasoning': '15分钟线220条约2.3天，参数设置合理'
        }
    }
    
    for timeframe, adjustment in adjustments.items():
        print(f"\n📊 {timeframe}:")
        print(f"   理由: {adjustment['reasoning']}")
        print(f"   调整建议:")
        for issue in adjustment['current_issues']:
            print(f"      • {issue}")

def calculate_effective_data_coverage():
    """计算有效数据覆盖范围"""
    print(f"\n📅 220条数据的有效覆盖范围")
    print("=" * 80)
    
    coverage = {
        '15分钟线': {
            'total_time': '2.3天',
            'effective_after_ma200': '不适用',
            'effective_after_ma150': '不适用',
            'recommendation': '短线交易，参数设置合理'
        },
        '1小时线': {
            'total_time': '9.2天',
            'effective_after_ma200': '不适用',
            'effective_after_ma150': '不适用',
            'recommendation': '短中期交易，参数设置合理'
        },
        '4小时线': {
            'total_time': '36.7天',
            'effective_after_ma200': '不适用',
            'effective_after_ma150': '约13天有效数据',
            'recommendation': '中期分析，需要调整长期MA'
        },
        '日线': {
            'total_time': '7.3个月',
            'effective_after_ma200': '约0.7个月有效数据',
            'effective_after_ma150': '约2.3个月有效数据',
            'recommendation': '长期分析，建议调整长期指标参数'
        }
    }
    
    for timeframe, info in coverage.items():
        print(f"\n📈 {timeframe}:")
        print(f"   总时间跨度: {info['total_time']}")
        print(f"   MA150后有效数据: {info['effective_after_ma150']}")
        print(f"   MA200后有效数据: {info['effective_after_ma200']}")
        print(f"   建议: {info['recommendation']}")

def generate_optimized_parameters():
    """生成220条数据优化的参数配置"""
    print(f"\n⚙️ 220条数据优化参数配置")
    print("=" * 80)
    
    optimized_params = {
        '日线': {
            'MA_SHORT_TERM': 21,
            'MA_MEDIUM_TERM': 55,
            'MA_LONG_TERM': 150,      # 从200调整为150
            'MA_EXTRA_LONG': 200,     # 从300调整为200
            'BB_LONG_PERIOD': 89,     # 从100调整为89
            'FIB_LOOKBACK_PERIOD': 80, # 从100调整为80
            'ATR_LONG_PERIOD': 50,    # 保持不变
            'RSI_EXTRA_LONG': 50,     # 保持不变
            'description': '长期分析，220条数据优化版'
        },
        '4小时线': {
            'MA_LONG_TERM': 144,      # 保持不变，但接近上限
            'BB_LONG_PERIOD': 89,     # 保持不变
            'FIB_LOOKBACK_PERIOD': 60, # 保持不变
            'description': '中期分析，220条数据适配版'
        }
    }
    
    print("建议的参数调整:")
    for timeframe, params in optimized_params.items():
        print(f"\n📊 {timeframe} - {params['description']}:")
        for param, value in params.items():
            if param != 'description':
                print(f"   {param}: {value}")

def assess_indicator_quality_impact():
    """评估指标质量影响"""
    print(f"\n📈 指标质量影响评估")
    print("=" * 80)
    
    quality_impact = {
        '短期指标 (MA20, RSI14, MACD)': {
            'impact': '无影响',
            'reason': '220条数据远超最小需求',
            'quality': '✅ 优秀'
        },
        '中期指标 (MA50, BB20, ATR14)': {
            'impact': '无影响',
            'reason': '数据量充足',
            'quality': '✅ 优秀'
        },
        '长期指标 (MA150, MA200)': {
            'impact': '轻微影响',
            'reason': 'MA200需要调整为MA150',
            'quality': '⚠️ 良好'
        },
        '超长期指标 (MA300)': {
            'impact': '需要调整',
            'reason': '数据不足，建议调整为MA200',
            'quality': '⚠️ 需要优化'
        },
        '斐波那契分析': {
            'impact': '轻微影响',
            'reason': '回看周期需要适当缩短',
            'quality': '✅ 良好'
        }
    }
    
    for indicator, assessment in quality_impact.items():
        print(f"\n📊 {indicator}:")
        print(f"   影响程度: {assessment['impact']}")
        print(f"   原因: {assessment['reason']}")
        print(f"   质量评级: {assessment['quality']}")

def main():
    """主函数"""
    print("BTCUSDT 220条数据技术指标影响分析")
    print("=" * 80)
    print("目标: 评估220条数据对技术指标计算的影响")
    print("=" * 80)
    
    # 1. 分析指标数据需求
    analyze_indicator_requirements()
    
    # 2. 分析时间周期参数
    analyze_timeframe_parameters()
    
    # 3. 建议参数调整
    suggest_parameter_adjustments()
    
    # 4. 计算有效数据覆盖
    calculate_effective_data_coverage()
    
    # 5. 生成优化参数
    generate_optimized_parameters()
    
    # 6. 评估质量影响
    assess_indicator_quality_impact()
    
    print(f"\n" + "=" * 80)
    print("📊 分析结论:")
    print("✅ 大部分技术指标适合220条数据")
    print("⚠️ 日线长期指标需要适当调整")
    print("✅ 短中期指标质量不受影响")
    print("✅ 斐波那契分析仍然有效")
    
    print(f"\n🔧 建议操作:")
    print("1. 调整日线MA_LONG_TERM: 200 → 150")
    print("2. 调整日线MA_EXTRA_LONG: 300 → 200")
    print("3. 调整日线BB_LONG_PERIOD: 100 → 89")
    print("4. 其他时间周期参数保持不变")
    print("5. 220条数据足够进行有效的技术分析")

if __name__ == "__main__":
    main()
