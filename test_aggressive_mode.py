"""
激进模式测试脚本
用于验证激进化修改是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def test_config_changes():
    """测试配置文件的激进化修改"""
    print("=" * 50)
    print("测试配置文件激进化修改")
    print("=" * 50)
    
    try:
        from config import (
            RSI_OVERBOUGHT, RSI_OVERSOLD, RSI_STRONG_BUY, RSI_STRONG_SELL,
            SIGNAL_WEIGHTS, AGGRESSIVE_MODE, ATR_STOP_MULTIPLIER, ATR_TARGET_MULTIPLIER,
            TIMEFRAME_INDICATOR_PARAMS
        )
        
        print("✅ RSI阈值修改:")
        print(f"   超买阈值: {RSI_OVERBOUGHT} (原70)")
        print(f"   超卖阈值: {RSI_OVERSOLD} (原30)")
        print(f"   强买入阈值: {RSI_STRONG_BUY}")
        print(f"   强卖出阈值: {RSI_STRONG_SELL}")
        
        print("\n✅ 信号权重修改:")
        for key, value in SIGNAL_WEIGHTS.items():
            print(f"   {key}: {value}")
            
        print(f"\n✅ 激进模式: {'启用' if AGGRESSIVE_MODE else '禁用'}")
        print(f"✅ ATR止损倍数: {ATR_STOP_MULTIPLIER}")
        print(f"✅ ATR目标倍数: {ATR_TARGET_MULTIPLIER}")
        
        print("\n✅ 15分钟线激进参数:")
        params_15m = TIMEFRAME_INDICATOR_PARAMS['15分钟线']
        print(f"   MA短期: {params_15m['MA_SHORT_TERM']} (原10)")
        print(f"   MACD快线: {params_15m['MACD_FAST']} (原8)")
        print(f"   RSI周期: {params_15m['RSI_PERIOD']} (原9)")
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")

def test_aggressive_config():
    """测试激进模式配置文件"""
    print("\n" + "=" * 50)
    print("测试激进模式配置文件")
    print("=" * 50)
    
    try:
        from aggressive_config import (
            AGGRESSIVE_MODE_ENABLED, AGGRESSIVE_TRADING, AGGRESSIVE_THRESHOLDS,
            AGGRESSIVE_SIGNAL_WEIGHTS, MULTI_TIMEFRAME_CONFIRMATION
        )
        
        print(f"✅ 激进模式状态: {'启用' if AGGRESSIVE_MODE_ENABLED else '禁用'}")
        print(f"✅ 最大杠杆: {AGGRESSIVE_TRADING['MAX_LEVERAGE']}倍")
        print(f"✅ 剥头皮模式: {'启用' if AGGRESSIVE_TRADING['SCALPING_MODE'] else '禁用'}")
        print(f"✅ 紧止损倍数: {AGGRESSIVE_TRADING['STOP_LOSS_ATR_MULTIPLIER']}")
        
        print("\n✅ 激进RSI阈值:")
        print(f"   极度超买: {AGGRESSIVE_THRESHOLDS['RSI_EXTREME_OVERBOUGHT']}")
        print(f"   极度超卖: {AGGRESSIVE_THRESHOLDS['RSI_EXTREME_OVERSOLD']}")
        
        print("\n✅ 激进信号权重:")
        for key, value in AGGRESSIVE_SIGNAL_WEIGHTS.items():
            print(f"   {key}: {value}")
            
        print(f"\n✅ 多时间框架确认: {'启用' if MULTI_TIMEFRAME_CONFIRMATION['DIVERGENCE_DETECTION'] else '禁用'}")
        
    except Exception as e:
        print(f"❌ 激进配置测试失败: {e}")

def test_ta_calculator_changes():
    """测试技术指标计算的激进化修改"""
    print("\n" + "=" * 50)
    print("测试技术指标计算激进化修改")
    print("=" * 50)
    
    try:
        # 创建测试数据
        import pandas as pd
        import numpy as np
        
        # 模拟价格数据
        test_data = pd.DataFrame({
            '收盘价': np.random.uniform(100000, 120000, 100),
            '最高价': np.random.uniform(100000, 120000, 100),
            '最低价': np.random.uniform(100000, 120000, 100),
            '成交量': np.random.uniform(1000, 5000, 100),
            'RSI': np.random.uniform(20, 80, 100),
            'BB_Upper': np.random.uniform(110000, 125000, 100),
            'BB_Lower': np.random.uniform(95000, 110000, 100),
            'BB_Middle': np.random.uniform(100000, 120000, 100),
        })
        
        # 测试RSI信号逻辑
        from ta_calculator import add_signal_analysis
        
        # 创建一个包含激进RSI值的测试案例
        test_data.loc[0, 'RSI'] = 76  # 极度超买
        test_data.loc[1, 'RSI'] = 24  # 极度超卖
        test_data.loc[2, 'RSI'] = 68  # 强卖出
        test_data.loc[3, 'RSI'] = 32  # 强买入
        
        # 添加必要的列
        test_data['MA20'] = test_data['收盘价']
        test_data['MA50'] = test_data['收盘价'] * 0.99
        test_data['MACD'] = np.random.uniform(-100, 100, 100)
        test_data['MACD_Signal'] = np.random.uniform(-100, 100, 100)
        test_data['Stoch_SlowK'] = np.random.uniform(20, 80, 100)
        test_data['Stoch_SlowD'] = np.random.uniform(20, 80, 100)
        test_data['BB_Width'] = np.random.uniform(0.01, 0.05, 100)
        test_data['BB_Squeeze'] = np.random.choice([True, False], 100)
        
        # 应用信号分析
        result = add_signal_analysis(test_data)
        
        print("✅ RSI信号测试:")
        print(f"   RSI=76 -> {result.loc[0, 'RSI_Signal']} (应为'极度超买')")
        print(f"   RSI=24 -> {result.loc[1, 'RSI_Signal']} (应为'极度超卖')")
        print(f"   RSI=68 -> {result.loc[2, 'RSI_Signal']} (应为'强卖出')")
        print(f"   RSI=32 -> {result.loc[3, 'RSI_Signal']} (应为'强买入')")
        
        # 测试综合信号
        print(f"\n✅ 综合信号测试:")
        unique_signals = result['综合信号'].unique()
        print(f"   可能的信号类型: {list(unique_signals)}")
        
    except Exception as e:
        print(f"❌ 技术指标测试失败: {e}")

def test_report_generator_changes():
    """测试报告生成器的激进化修改"""
    print("\n" + "=" * 50)
    print("测试报告生成器激进化修改")
    print("=" * 50)
    
    try:
        from report_generator import trading_recommendation_section, comprehensive_analysis_section
        
        # 创建测试数据
        test_latest_data = {
            '收盘价': 118000,
            'ATR': 1500,
            'RSI': 76,
            'RSI_Signal': '极度超买',
            'BB_Signal': '强力突破上轨',
            '综合信号': '极强看涨',
            'MACD': 50,
            'MACD_Signal': 30
        }
        
        # 测试交易建议
        trading_section = trading_recommendation_section(test_latest_data)
        print("✅ 激进交易建议生成成功")
        print("预览:")
        print(trading_section[:200] + "...")
        
        # 测试综合分析
        analysis_section = comprehensive_analysis_section(test_latest_data)
        print("\n✅ 激进综合分析生成成功")
        print("预览:")
        print(analysis_section[:200] + "...")
        
    except Exception as e:
        print(f"❌ 报告生成器测试失败: {e}")

def main():
    """主测试函数"""
    print("BTCUSDT激进模式测试")
    print("=" * 60)
    
    test_config_changes()
    test_aggressive_config()
    test_ta_calculator_changes()
    test_report_generator_changes()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("如果所有测试都显示✅，说明激进化修改成功")
    print("如果有❌，请检查对应的文件修改")

if __name__ == "__main__":
    main()
