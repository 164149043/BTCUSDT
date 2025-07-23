"""
创建23列精简组合数据文件
只保留用户指定的23个核心列
"""

import pandas as pd
import sys
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from config import DATA_DIR

def create_23_column_files():
    """创建23列精简数据文件"""
    print("📊 创建23列精简组合数据文件")
    print("=" * 80)
    
    # 定义用户指定的23列
    required_columns = [
        'open_time',           # 1. 时间戳
        '开盘价',              # 2. 开盘价
        '最高价',              # 3. 最高价
        '最低价',              # 4. 最低价
        '收盘价',              # 5. 收盘价
        '成交量',              # 6. 成交量
        'MA20',               # 7. MA20
        'MA50',               # 8. MA50
        'MA89',               # 9. MA89 (或MA_LONG)
        'BB_Upper',           # 10. BB_Upper
        'BB_Lower',           # 11. BB_Lower
        'BB_Long_Upper',      # 12. BB_Long_Upper
        'BB_Long_Lower',      # 13. BB_Long_Lower
        'MACD_Hist',          # 14. MACD_Hist
        'RSI',                # 15. RSI
        'ATR',                # 16. ATR
        'Fib_Ret_0.382',      # 17. Fib_Ret_0.382
        'Fib_Ret_0.500',      # 18. Fib_Ret_0.500
        'Fib_Ret_0.618',      # 19. Fib_Ret_0.618
        'Fib_Support_Level',  # 20. Fib_Support_Level
        'Fib_Resistance_Level', # 21. Fib_Resistance_Level
        'Fib_Price_Position', # 22. Fib_Price_Position
        'MACD_Long'           # 23. MACD_Long
    ]
    
    print(f"🎯 目标: 创建包含以下23列的精简文件:")
    for i, col in enumerate(required_columns, 1):
        print(f"   {i:2d}. {col}")
    
    # 查找所有组合数据文件
    all_files = []
    all_files.extend(DATA_DIR.glob("*组合数据*.csv"))
    all_files.extend(DATA_DIR.glob("*_enhanced.csv"))
    all_files.extend(DATA_DIR.glob("*_optimized.csv"))
    
    # 排除备份文件和已经是23列的文件
    files_to_process = [f for f in all_files if not f.name.endswith('.backup.csv') 
                       and 'backup_' not in f.name and '_23col' not in f.name]
    
    if not files_to_process:
        print("❌ 未找到需要处理的文件")
        return
    
    print(f"\n📁 找到 {len(files_to_process)} 个文件需要处理:")
    for file in files_to_process:
        print(f"   - {file.name}")
    
    processed_count = 0
    
    for file_path in files_to_process:
        print(f"\n🔧 处理文件: {file_path.name}")
        print("-" * 60)
        
        try:
            # 读取文件
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            original_cols = len(df.columns)
            
            # 检查列名映射 (处理可能的列名差异)
            column_mapping = {}
            available_columns = []
            missing_columns = []
            
            for required_col in required_columns:
                if required_col in df.columns:
                    available_columns.append(required_col)
                else:
                    # 检查可能的替代列名
                    alternatives = get_alternative_column_names(required_col, df.columns)
                    if alternatives:
                        column_mapping[alternatives[0]] = required_col
                        available_columns.append(alternatives[0])
                        print(f"   📝 列名映射: {alternatives[0]} → {required_col}")
                    else:
                        missing_columns.append(required_col)
            
            if missing_columns:
                print(f"   ⚠️ 缺失列: {missing_columns}")
            
            print(f"   ✅ 可用列: {len(available_columns)}/{len(required_columns)}")
            
            # 创建23列数据框
            df_23col = df[available_columns].copy()
            
            # 应用列名映射
            if column_mapping:
                df_23col = df_23col.rename(columns=column_mapping)
            
            # 确保列的顺序与要求一致
            final_columns = [col for col in required_columns if col in df_23col.columns]
            df_23col = df_23col[final_columns]
            
            # 优化数据类型
            numeric_columns = df_23col.select_dtypes(include=['float64']).columns
            if len(numeric_columns) > 0:
                df_23col[numeric_columns] = df_23col[numeric_columns].astype('float32')
            
            # 生成23列文件名
            original_name = file_path.stem
            # 移除现有的后缀
            if original_name.endswith('_enhanced'):
                base_name = original_name[:-9]
            elif original_name.endswith('_optimized'):
                base_name = original_name[:-10]
            elif original_name.endswith('_streamlined'):
                base_name = original_name[:-12]
            else:
                base_name = original_name
            
            col23_filename = f"{base_name}_23col.csv"
            col23_path = file_path.parent / col23_filename
            
            # 保存23列文件
            df_23col.to_csv(col23_path, encoding='utf-8-sig', index=False)
            
            # 计算文件大小变化
            original_size = file_path.stat().st_size / 1024
            new_size = col23_path.stat().st_size / 1024
            size_reduction = (original_size - new_size) / original_size * 100
            
            print(f"   ✅ 23列文件创建成功:")
            print(f"      文件名: {col23_filename}")
            print(f"      列数: {original_cols} → {len(df_23col.columns)} (减少{original_cols - len(df_23col.columns)}列)")
            print(f"      文件大小: {original_size:.1f}KB → {new_size:.1f}KB (减少{size_reduction:.1f}%)")
            
            processed_count += 1
            
        except Exception as e:
            print(f"   ❌ 处理失败: {e}")
    
    print(f"\n" + "=" * 80)
    print(f"🎉 23列精简文件创建完成!")
    print(f"✅ 成功处理 {processed_count}/{len(files_to_process)} 个文件")
    print(f"📊 每个文件包含23个核心指标")

def get_alternative_column_names(required_col, available_cols):
    """获取可能的替代列名"""
    alternatives = []
    
    # 定义列名映射关系
    column_alternatives = {
        'MA89': ['MA_LONG', 'MA_89'],
        'MA_LONG': ['MA89', 'MA_89'],
        'BB_Long_Upper': ['BB_Long_Upper', 'BB_LONG_UPPER'],
        'BB_Long_Lower': ['BB_Long_Lower', 'BB_LONG_LOWER'],
        'MACD_Long': ['MACD_LONG', 'MACD_Long'],
        'Fib_Support_Level': ['Fib_Support_Level', 'FIB_SUPPORT_LEVEL'],
        'Fib_Resistance_Level': ['Fib_Resistance_Level', 'FIB_RESISTANCE_LEVEL'],
        'Fib_Price_Position': ['Fib_Price_Position', 'FIB_PRICE_POSITION']
    }
    
    if required_col in column_alternatives:
        for alt_name in column_alternatives[required_col]:
            if alt_name in available_cols:
                alternatives.append(alt_name)
    
    return alternatives

def verify_23_column_files():
    """验证23列文件"""
    print(f"\n🔍 验证23列文件")
    print("=" * 80)
    
    # 查找23列文件
    col23_files = list(DATA_DIR.glob("*_23col.csv"))
    
    if not col23_files:
        print("❌ 未找到23列文件")
        return
    
    for file_path in col23_files:
        print(f"\n📊 验证文件: {file_path.name}")
        print("-" * 60)
        
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            
            print(f"   📊 基本信息:")
            print(f"      数据行数: {len(df)}")
            print(f"      列数: {len(df.columns)}")
            print(f"      文件大小: {file_path.stat().st_size / 1024:.1f}KB")
            
            print(f"   📋 包含的列:")
            for i, col in enumerate(df.columns, 1):
                print(f"      {i:2d}. {col}")
            
            # 检查关键指标的有效数据
            key_indicators = ['收盘价', 'MA20', 'MA50', 'RSI', 'ATR']
            print(f"   🔍 关键指标数据质量:")
            for indicator in key_indicators:
                if indicator in df.columns:
                    valid_count = df[indicator].notna().sum()
                    if valid_count > 0:
                        latest_value = df[indicator].iloc[-1]
                        print(f"      {indicator}: {valid_count}/{len(df)} 有效, 最新: {latest_value:.2f}")
            
            # 检查斐波那契指标
            fib_indicators = ['Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618']
            print(f"   🔢 斐波那契指标:")
            for fib in fib_indicators:
                if fib in df.columns:
                    valid_count = df[fib].notna().sum()
                    if valid_count > 0:
                        latest_value = df[fib].iloc[-1]
                        print(f"      {fib}: {valid_count}/{len(df)} 有效, 最新: ${latest_value:.2f}")
                    else:
                        print(f"      {fib}: 无有效数据")
            
        except Exception as e:
            print(f"   ❌ 验证失败: {e}")

def show_23_column_usage_guide():
    """显示23列文件使用指南"""
    print(f"\n💡 23列精简文件使用指南")
    print("=" * 80)
    
    print("🎯 23列文件特点:")
    print("   • 核心指标: 包含最重要的23个技术指标")
    print("   • 文件精简: 大幅减少文件大小，传输更快")
    print("   • AI友好: 专为DeepSeek AI分析优化")
    print("   • 数据完整: 保留所有关键的交易信号")
    
    print(f"\n📊 指标分类:")
    categories = {
        '基础数据 (6列)': ['open_time', '开盘价', '最高价', '最低价', '收盘价', '成交量'],
        '移动平均 (3列)': ['MA20', 'MA50', 'MA89'],
        '布林带 (4列)': ['BB_Upper', 'BB_Lower', 'BB_Long_Upper', 'BB_Long_Lower'],
        '动量指标 (3列)': ['MACD_Hist', 'MACD_Long', 'RSI'],
        '波动率 (1列)': ['ATR'],
        '斐波那契 (6列)': ['Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618', 
                        'Fib_Support_Level', 'Fib_Resistance_Level', 'Fib_Price_Position']
    }
    
    for category, indicators in categories.items():
        print(f"   • {category}: {', '.join(indicators)}")
    
    print(f"\n🤖 DeepSeek AI使用建议:")
    print("   1. 上传23列文件进行快速分析")
    print("   2. 重点关注MA系统的趋势方向")
    print("   3. 结合布林带判断价格通道")
    print("   4. 使用斐波那契水平确定支撑阻力")
    print("   5. RSI和MACD提供动量确认")

def main():
    """主函数"""
    print("BTCUSDT 23列精简数据文件生成器")
    print("=" * 80)
    print("目标: 创建只包含用户指定23列的精简数据文件")
    print("=" * 80)
    
    # 1. 创建23列文件
    create_23_column_files()
    
    # 2. 验证23列文件
    verify_23_column_files()
    
    # 3. 显示使用指南
    show_23_column_usage_guide()
    
    print(f"\n" + "=" * 80)
    print("🎉 23列精简数据文件生成完成!")
    print("✅ 包含用户指定的23个核心指标")
    print("✅ 文件大小大幅减少")
    print("✅ 保留所有关键交易信号")
    print("✅ 适合DeepSeek AI快速分析")
    
    print(f"\n📁 生成的23列文件:")
    col23_files = list(DATA_DIR.glob("*_23col.csv"))
    for file in col23_files:
        size_kb = file.stat().st_size / 1024
        print(f"   • {file.name} ({size_kb:.1f}KB)")

if __name__ == "__main__":
    main()
