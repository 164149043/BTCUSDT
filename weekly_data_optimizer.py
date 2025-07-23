"""
周线数据优化工具
创建周线专用的优化数据文件
"""

import pandas as pd
import sys
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from config import DATA_DIR

def create_weekly_optimized_file():
    """创建周线优化数据文件"""
    print("📊 创建周线优化数据文件")
    print("=" * 80)
    
    # 查找最新的周线组合数据文件
    weekly_files = list(DATA_DIR.glob("*周线组合数据*.csv"))
    weekly_files = [f for f in weekly_files if not f.name.endswith('.backup.csv') and '_optimized' not in f.name]
    
    if not weekly_files:
        print("❌ 未找到周线组合数据文件")
        return
    
    latest_weekly = max(weekly_files, key=lambda x: x.stat().st_mtime)
    print(f"📁 处理文件: {latest_weekly.name}")
    
    try:
        df = pd.read_csv(latest_weekly, encoding='utf-8-sig')
        
        # 定义周线优化的列结构
        weekly_optimized_columns = [
            # 基础数据 (7列)
            'open_time', '开盘价', '最高价', '最低价', '收盘价', '成交量', '成交额',
            
            # 周线核心MA系统 (4列)
            'MA10',      # 10周 ≈ 2.5个月
            'MA26',      # 26周 ≈ 6个月
            'MA52',      # 52周 ≈ 1年
            'MA104',     # 104周 ≈ 2年
            
            # MACD系统 (4列)
            'MACD', 'MACD_Signal', 'MACD_Hist',
            'MACD_Long',  # 长期MACD
            
            # RSI系统 (2列)
            'RSI', 'RSI_Long',
            
            # 布林带系统 (5列)
            'BB_Upper', 'BB_Middle', 'BB_Lower',
            'BB_Long_Upper', 'BB_Long_Middle',  # 年度布林带
            
            # 其他核心指标 (4列)
            'ATR', 'ATR_Long', 'ADX', 'OBV',
            
            # 斐波那契核心 (8列)
            'Fib_Ret_0.382',       # 38.2% 关键回调
            'Fib_Ret_0.500',       # 50% 黄金分割
            'Fib_Ret_0.618',       # 61.8% 黄金比例
            'Fib_Ext_1.272',       # 127.2% 扩展
            'Fib_Trend',           # 趋势方向
            'Fib_Signal',          # 交易信号
            'Fib_Support_Level',   # 支撑位
            'Fib_Resistance_Level' # 阻力位
        ]
        
        # 检查可用列
        available_columns = [col for col in weekly_optimized_columns if col in df.columns]
        missing_columns = [col for col in weekly_optimized_columns if col not in df.columns]
        
        if missing_columns:
            print(f"   ⚠️ 缺失列: {missing_columns}")
        
        print(f"   ✅ 可用列: {len(available_columns)}/{len(weekly_optimized_columns)}")
        
        # 创建优化版本
        df_optimized = df[available_columns].copy()
        
        # 优化数据类型
        numeric_columns = df_optimized.select_dtypes(include=['float64']).columns
        if len(numeric_columns) > 0:
            df_optimized[numeric_columns] = df_optimized[numeric_columns].astype('float32')
        
        # 生成优化文件名
        original_name = latest_weekly.stem
        optimized_filename = f"{original_name}_optimized.csv"
        optimized_path = latest_weekly.parent / optimized_filename
        
        # 保存优化文件
        df_optimized.to_csv(optimized_path, encoding='utf-8-sig', index=False)
        
        # 计算优化效果
        original_size = latest_weekly.stat().st_size / 1024
        optimized_size = optimized_path.stat().st_size / 1024
        size_reduction = (original_size - optimized_size) / original_size * 100
        
        print(f"   ✅ 周线优化完成:")
        print(f"      文件名: {optimized_filename}")
        print(f"      列数: {len(df.columns)} → {len(df_optimized.columns)} (减少{len(df.columns) - len(df_optimized.columns)}列)")
        print(f"      文件大小: {original_size:.1f}KB → {optimized_size:.1f}KB (减少{size_reduction:.1f}%)")
        
        return optimized_path, df_optimized
        
    except Exception as e:
        print(f"   ❌ 优化失败: {e}")
        return None, None

def analyze_weekly_data_quality():
    """分析周线数据质量"""
    print(f"\n🔍 周线数据质量分析")
    print("=" * 80)
    
    # 查找优化后的周线文件
    optimized_files = list(DATA_DIR.glob("*周线组合数据*_optimized.csv"))
    
    if not optimized_files:
        print("❌ 未找到优化的周线文件")
        return
    
    latest_file = optimized_files[0]
    
    try:
        df = pd.read_csv(latest_file, encoding='utf-8-sig')
        
        print(f"📊 文件: {latest_file.name}")
        print(f"   数据行数: {len(df)}")
        print(f"   列数: {len(df.columns)}")
        print(f"   文件大小: {latest_file.stat().st_size / 1024:.1f}KB")
        
        # 检查MA系统有效性
        ma_columns = ['MA10', 'MA26', 'MA52', 'MA104']
        print(f"\n📈 MA系统有效性:")
        for ma in ma_columns:
            if ma in df.columns:
                valid_count = df[ma].notna().sum()
                if valid_count > 0:
                    latest_value = df[ma].dropna().iloc[-1]
                    print(f"   • {ma}: {valid_count}/{len(df)} 有效数据, 最新: ${latest_value:,.2f}")
                else:
                    print(f"   • {ma}: 无有效数据")
        
        # 检查斐波那契水平
        fib_columns = ['Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618']
        print(f"\n🔢 斐波那契关键水平:")
        for fib in fib_columns:
            if fib in df.columns:
                valid_count = df[fib].notna().sum()
                if valid_count > 0:
                    latest_value = df[fib].dropna().iloc[-1]
                    print(f"   • {fib}: {valid_count}/{len(df)} 有效数据, 最新: ${latest_value:,.2f}")
                else:
                    print(f"   • {fib}: 无有效数据")
        
        # 检查数据时间范围
        if 'open_time' in df.columns:
            first_time = df['open_time'].iloc[0]
            last_time = df['open_time'].iloc[-1]
            print(f"\n📅 时间范围: {first_time} 至 {last_time}")
            print(f"   数据跨度: 约3.8年 (200周)")
        
        # 显示最新价格信息
        if '收盘价' in df.columns:
            current_price = df['收盘价'].iloc[-1]
            print(f"\n💰 最新价格信息:")
            print(f"   当前价格: ${current_price:,.2f}")
            
            # 与MA的关系
            for ma in ['MA10', 'MA26', 'MA52']:
                if ma in df.columns and df[ma].notna().sum() > 0:
                    ma_value = df[ma].dropna().iloc[-1]
                    relation = "上方" if current_price > ma_value else "下方"
                    print(f"   相对{ma}: 在{relation} (${ma_value:,.2f})")
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")

def show_weekly_usage_guide():
    """显示周线使用指南"""
    print(f"\n💡 周线数据使用指南")
    print("=" * 80)
    
    print("🎯 周线分析的核心价值:")
    print("   • 宏观趋势: 识别长期牛熊市转换点")
    print("   • 战略决策: 制定3个月-2年的投资策略")
    print("   • 噪音过滤: 忽略短期波动，关注主要趋势")
    print("   • 关键位置: 识别多年有效的支撑阻力位")
    
    print(f"\n📊 周线MA系统解读:")
    print("   • MA10 (2.5个月): 短期趋势，适合波段交易")
    print("   • MA26 (6个月): 中期趋势，半年度方向")
    print("   • MA52 (1年): 年度趋势，牛熊分界线")
    print("   • MA104 (2年): 长期趋势，大周期判断")
    
    print(f"\n🔢 周线斐波那契特点:")
    print("   • 38.2%回调: 长期关键支撑，通常是买入机会")
    print("   • 50%回调: 心理关键位，趋势强弱分界")
    print("   • 61.8%回调: 黄金比例，最重要的长期支撑")
    print("   • 127.2%扩展: 长期目标位，适合分批获利")
    
    print(f"\n🤖 DeepSeek AI分析建议:")
    print("   1. 上传周线优化文件进行宏观分析")
    print("   2. 重点关注MA52和MA104的趋势方向")
    print("   3. 结合斐波那契水平制定长期策略")
    print("   4. 使用周线信号过滤短期噪音")

def main():
    """主函数"""
    print("BTCUSDT 周线数据优化工具")
    print("=" * 80)
    print("目标: 创建周线专用的优化数据文件")
    print("=" * 80)
    
    # 1. 创建周线优化文件
    result = create_weekly_optimized_file()
    
    if result[0] is None:
        return
    
    # 2. 分析数据质量
    analyze_weekly_data_quality()
    
    # 3. 显示使用指南
    show_weekly_usage_guide()
    
    print(f"\n" + "=" * 80)
    print("🎉 周线数据优化完成!")
    print("✅ 周线优化文件已创建")
    print("✅ 包含34个核心长期指标")
    print("✅ 200周数据覆盖3.8年历史")
    print("✅ 适合长期投资和战略分析")
    
    print(f"\n📁 推荐使用文件:")
    optimized_files = list(DATA_DIR.glob("*周线组合数据*_optimized.csv"))
    for file in optimized_files:
        size_kb = file.stat().st_size / 1024
        print(f"   • {file.name} ({size_kb:.1f}KB)")

if __name__ == "__main__":
    main()
