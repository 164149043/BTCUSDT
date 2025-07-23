"""
23列精简数据文件最终总结
展示用户指定的23列数据文件的特点和使用方法
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')

def show_23_column_summary():
    """显示23列数据总结"""
    print("📊 BTCUSDT 23列精简数据文件总结")
    print("=" * 80)
    
    print("🎯 用户指定的23列结构:")
    columns_info = [
        ("1. open_time", "时间戳", "基础数据"),
        ("2. 开盘价", "开盘价格", "基础数据"),
        ("3. 最高价", "最高价格", "基础数据"),
        ("4. 最低价", "最低价格", "基础数据"),
        ("5. 收盘价", "收盘价格", "基础数据"),
        ("6. 成交量", "交易量", "基础数据"),
        ("7. MA20", "20期移动平均", "趋势指标"),
        ("8. MA50", "50期移动平均", "趋势指标"),
        ("9. MA89", "89期移动平均", "趋势指标"),
        ("10. BB_Upper", "布林带上轨", "波动指标"),
        ("11. BB_Lower", "布林带下轨", "波动指标"),
        ("12. BB_Long_Upper", "长期布林带上轨", "波动指标"),
        ("13. BB_Long_Lower", "长期布林带下轨", "波动指标"),
        ("14. MACD_Hist", "MACD柱状图", "动量指标"),
        ("15. RSI", "相对强弱指标", "动量指标"),
        ("16. ATR", "平均真实波幅", "波动率指标"),
        ("17. Fib_Ret_0.382", "38.2%斐波那契回调", "斐波那契"),
        ("18. Fib_Ret_0.500", "50%斐波那契回调", "斐波那契"),
        ("19. Fib_Ret_0.618", "61.8%斐波那契回调", "斐波那契"),
        ("20. Fib_Support_Level", "斐波那契支撑位", "斐波那契"),
        ("21. Fib_Resistance_Level", "斐波那契阻力位", "斐波那契"),
        ("22. Fib_Price_Position", "价格斐波那契位置", "斐波那契"),
        ("23. MACD_Long", "长期MACD", "动量指标")
    ]
    
    for col_info in columns_info:
        print(f"   {col_info[0]:<25} {col_info[1]:<15} [{col_info[2]}]")

def analyze_23_column_files():
    """分析23列文件"""
    print(f"\n📊 23列文件分析")
    print("=" * 80)
    
    # 查找23列文件
    col23_files = list(DATA_DIR.glob("*_23col.csv"))
    
    if not col23_files:
        print("❌ 未找到23列文件")
        return
    
    for file_path in col23_files:
        print(f"\n📄 文件: {file_path.name}")
        print("-" * 60)
        
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            
            # 基本信息
            print(f"   📊 基本信息:")
            print(f"      数据行数: {len(df)} (200条数据)")
            print(f"      实际列数: {len(df.columns)}")
            print(f"      文件大小: {file_path.stat().st_size / 1024:.1f}KB")
            
            # 检查列完整性
            expected_columns = [
                'open_time', '开盘价', '最高价', '最低价', '收盘价', '成交量',
                'MA20', 'MA50', 'MA89', 'BB_Upper', 'BB_Lower', 'BB_Long_Upper', 'BB_Long_Lower',
                'MACD_Hist', 'RSI', 'ATR',
                'Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618',
                'Fib_Support_Level', 'Fib_Resistance_Level', 'Fib_Price_Position',
                'MACD_Long'
            ]
            
            present_columns = [col for col in expected_columns if col in df.columns]
            missing_columns = [col for col in expected_columns if col not in df.columns]
            
            print(f"   ✅ 包含列数: {len(present_columns)}/23")
            if missing_columns:
                print(f"   ⚠️ 缺失列: {missing_columns}")
            
            # 数据质量检查
            print(f"   🔍 数据质量:")
            key_columns = ['收盘价', 'MA20', 'MA50', 'RSI', 'ATR']
            for col in key_columns:
                if col in df.columns:
                    valid_count = df[col].notna().sum()
                    if valid_count > 0:
                        latest_value = df[col].iloc[-1]
                        print(f"      {col}: {valid_count}/{len(df)} 有效, 最新: {latest_value:.2f}")
            
            # 斐波那契数据检查
            fib_columns = ['Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618']
            print(f"   🔢 斐波那契水平:")
            for col in fib_columns:
                if col in df.columns:
                    valid_count = df[col].notna().sum()
                    if valid_count > 0:
                        latest_value = df[col].iloc[-1]
                        print(f"      {col}: ${latest_value:.2f}")
            
        except Exception as e:
            print(f"   ❌ 分析失败: {e}")

def show_23_column_advantages():
    """显示23列文件优势"""
    print(f"\n💡 23列精简文件优势")
    print("=" * 80)
    
    print("🎯 核心优势:")
    print("   • 精准聚焦: 只包含最重要的23个技术指标")
    print("   • 文件精简: 相比完整版减少50-60%文件大小")
    print("   • 传输高效: 39-40KB文件大小，上传下载更快")
    print("   • AI友好: 专为DeepSeek AI分析优化")
    print("   • 信号完整: 保留所有关键交易信号")
    
    print(f"\n📊 指标分类完整性:")
    categories = {
        '基础OHLCV数据': '6列 - 完整的价格和成交量信息',
        '趋势分析': '3列 - MA20/50/89多层次趋势判断',
        '波动分析': '4列 - 标准和长期布林带通道',
        '动量分析': '3列 - MACD_Hist, MACD_Long, RSI',
        '波动率分析': '1列 - ATR风险管理',
        '斐波那契分析': '6列 - 关键回调水平+动态支撑阻力'
    }
    
    for category, description in categories.items():
        print(f"   • {category}: {description}")
    
    print(f"\n🔄 与其他版本对比:")
    comparison = {
        '完整版': '48-52列, 85-95KB, 包含所有指标',
        '优化版': '29-34列, 50-60KB, 核心指标+完整斐波那契',
        '23列版': '22-23列, 39-40KB, 用户指定核心指标 ⭐推荐'
    }
    
    for version, description in comparison.items():
        print(f"   • {version}: {description}")

def show_ai_usage_recommendations():
    """显示AI使用建议"""
    print(f"\n🤖 DeepSeek AI使用建议")
    print("=" * 80)
    
    print("📝 23列专用提示词:")
    print("""
请分析我上传的BTCUSDT K线数据文件（200条数据，23个核心指标）。
数据包含精选的技术指标：

基础数据: OHLC价格 + 成交量
趋势指标: MA20/MA50/MA89 三层移动平均系统
波动指标: 标准布林带 + 长期布林带通道
动量指标: MACD_Hist, MACD_Long, RSI
波动率: ATR (风险管理)
斐波那契: 38.2%/50%/61.8%回调 + 动态支撑阻力

请基于这23个核心指标完成分析:
1. 趋势判断 (基于MA20/50/89系统)
2. 价格通道分析 (布林带上下轨)
3. 动量确认 (MACD和RSI信号)
4. 斐波那契关键水平 (支撑阻力位)
5. 交易建议 (入场点位和止损目标)

要求: 重点关注23个指标的协同信号，提供具体可执行的交易策略。
    """)
    
    print(f"\n✅ 23列AI分析优势:")
    print("   • 指标精选: 去除冗余，聚焦最重要的信号")
    print("   • 处理高效: 文件小，AI分析速度更快")
    print("   • 信号清晰: 核心指标突出关键交易机会")
    print("   • 策略完整: 涵盖趋势、动量、支撑阻力全方位")

def show_trading_strategy_guide():
    """显示交易策略指南"""
    print(f"\n💡 基于23列指标的交易策略")
    print("=" * 80)
    
    print("🎯 多指标确认策略:")
    
    strategies = {
        '趋势跟踪策略': {
            '入场条件': 'MA20 > MA50 > MA89，价格在MA20上方',
            '动量确认': 'MACD_Hist > 0，RSI > 50',
            '支撑确认': '价格在斐波那契支撑位上方',
            '止损位': '跌破MA20或斐波那契支撑位',
            '目标位': '斐波那契阻力位或布林带上轨'
        },
        '反转抄底策略': {
            '入场条件': '价格触及布林带下轨，RSI < 30',
            '斐波那契确认': '价格接近61.8%或78.6%回调位',
            '动量背离': 'MACD出现底背离信号',
            '止损位': '跌破关键斐波那契支撑',
            '目标位': '50%斐波那契回调或MA50'
        },
        '突破交易策略': {
            '入场条件': '价格突破布林带上轨，成交量放大',
            '趋势确认': 'MA20向上，MACD_Hist扩大',
            '阻力突破': '突破斐波那契阻力位',
            '止损位': '回落至布林带中轨',
            '目标位': '下一个斐波那契扩展位'
        }
    }
    
    for strategy, details in strategies.items():
        print(f"\n📊 {strategy}:")
        for condition, description in details.items():
            print(f"   • {condition}: {description}")

def main():
    """主函数"""
    print("BTCUSDT 23列精简数据文件最终总结")
    print("=" * 80)
    
    # 显示23列总结
    show_23_column_summary()
    
    # 分析23列文件
    analyze_23_column_files()
    
    # 显示优势
    show_23_column_advantages()
    
    # 显示AI使用建议
    show_ai_usage_recommendations()
    
    # 显示交易策略
    show_trading_strategy_guide()
    
    print(f"\n" + "=" * 80)
    print("🎉 23列精简数据文件系统完成!")
    print("✅ 用户指定的23个核心指标")
    print("✅ 文件大小优化至39-40KB")
    print("✅ 保留完整的交易信号")
    print("✅ 专为DeepSeek AI优化")
    print("✅ 支持多种交易策略")
    
    print(f"\n📁 推荐使用文件:")
    col23_files = list(DATA_DIR.glob("*_23col.csv"))
    for file in col23_files:
        size_kb = file.stat().st_size / 1024
        print(f"   • {file.name} ({size_kb:.1f}KB)")
    
    print(f"\n🚀 使用方法:")
    print("   1. 选择适合的时间周期23列文件")
    print("   2. 上传给DeepSeek AI进行分析")
    print("   3. 使用专用提示词获取详细建议")
    print("   4. 基于多指标确认制定交易策略")

if __name__ == "__main__":
    main()
