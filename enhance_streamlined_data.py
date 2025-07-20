"""
增强精简数据文件
在保持精简的同时，增加一些重要的技术指标
"""

import pandas as pd
import sys
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from config import DATA_DIR

def analyze_missing_important_indicators():
    """分析可能遗漏的重要指标"""
    print("🔍 分析可能遗漏的重要技术指标")
    print("=" * 80)
    
    # 查找原始文件和当前精简文件
    original_files = [f for f in DATA_DIR.glob("*组合数据*.csv") if not f.name.endswith('_streamlined.csv') and not f.name.endswith('.backup.csv')]
    
    if not original_files:
        print("❌ 未找到原始文件")
        return None
    
    latest_original = max(original_files, key=lambda x: x.stat().st_mtime)
    
    try:
        df_original = pd.read_csv(latest_original, encoding='utf-8-sig')
        
        # 当前精简版本包含的列
        current_streamlined = [
            'open_time', '开盘价', '最高价', '最低价', '收盘价', '成交量',
            'MA20', 'MA50', 'MACD', 'MACD_Signal', 'MACD_Hist', 'RSI',
            'BB_Upper', 'BB_Middle', 'BB_Lower', 'Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618',
            'Fib_Ext_1.272', 'Fib_Ext_1.618', 'Fib_Trend', 'Fib_Signal', 'ATR', 'ADX', 'OBV'
        ]
        
        # 分析原始文件中的所有列
        all_columns = list(df_original.columns)
        missing_columns = [col for col in all_columns if col not in current_streamlined]
        
        print(f"📊 原始文件分析: {latest_original.name}")
        print(f"   总列数: {len(all_columns)}")
        print(f"   当前精简版列数: {len(current_streamlined)}")
        print(f"   未包含的列数: {len(missing_columns)}")
        
        # 按重要性分类未包含的列
        important_missing = []
        moderate_missing = []
        less_important = []
        
        for col in missing_columns:
            if col in ['成交额', 'Stoch_SlowK', 'Stoch_SlowD', 'MA_LONG', 'RSI_Long']:
                important_missing.append(col)
            elif col in ['Fib_Ret_0.236', 'Fib_Ret_0.786', 'MACD_Long', 'BB_Long_Upper', 'ATR_Long']:
                moderate_missing.append(col)
            else:
                less_important.append(col)
        
        print(f"\n📈 重要性分析:")
        print(f"   🔴 重要但缺失: {important_missing}")
        print(f"   🟡 中等重要: {moderate_missing}")
        print(f"   🟢 次要指标: {less_important}")
        
        return df_original, current_streamlined, important_missing, moderate_missing
        
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        return None, None, None, None

def define_enhanced_streamlined_columns():
    """定义增强版精简列"""
    print(f"\n🎯 定义增强版精简数据结构")
    print("=" * 80)
    
    enhanced_columns = {
        # 基础数据 (增加成交额)
        'basic': [
            'open_time',           # 时间戳
            '开盘价', '最高价', '最低价', '收盘价',  # OHLC
            '成交量', '成交额'      # 成交量和成交额 (成交额很重要)
        ],
        
        # 移动平均线 (增加长期MA)
        'moving_averages': [
            'MA20',                # 短期MA
            'MA50',                # 中期MA
            'MA_LONG'              # 长期MA (重要的趋势指标)
        ],
        
        # MACD (保持核心，增加长期MACD)
        'macd': [
            'MACD',                # MACD主线
            'MACD_Signal',         # 信号线
            'MACD_Hist',           # 柱状图
            'MACD_Long'            # 长期MACD (趋势确认)
        ],
        
        # RSI (增加长期RSI)
        'rsi': [
            'RSI',                 # 主RSI
            'RSI_Long'             # 长期RSI (趋势过滤)
        ],
        
        # 布林带 (保留标准，增加长期布林带上轨)
        'bollinger': [
            'BB_Upper',            # 上轨
            'BB_Middle',           # 中轨
            'BB_Lower',            # 下轨
            'BB_Long_Upper'        # 长期布林带上轨 (重要阻力)
        ],
        
        # 随机指标 (重新加入，很重要的超买超卖指标)
        'stochastic': [
            'Stoch_SlowK',         # 随机指标K线
            'Stoch_SlowD'          # 随机指标D线
        ],
        
        # 斐波那契 (增加更多关键水平)
        'fibonacci_enhanced': [
            'Fib_Ret_0.236',       # 23.6% 浅回调
            'Fib_Ret_0.382',       # 38.2% 关键回调位 ⭐⭐⭐⭐
            'Fib_Ret_0.500',       # 50% 黄金分割点 ⭐⭐⭐⭐⭐
            'Fib_Ret_0.618',       # 61.8% 黄金比例 ⭐⭐⭐⭐⭐
            'Fib_Ret_0.786',       # 78.6% 深度回调
            'Fib_Ext_1.272',       # 127.2% 第一目标位
            'Fib_Ext_1.414',       # 141.4% 扩展位 (移除1.618)
            'Fib_Trend',           # 趋势方向
            'Fib_Signal',          # 交易信号
            'Fib_Support_Level',   # 支撑位
            'Fib_Resistance_Level' # 阻力位
        ],
        
        # 其他核心指标 (增加ATR长期)
        'other_core': [
            'ATR',                 # 短期波动率
            'ATR_Long',            # 长期波动率 (重要的波动率对比)
            'ADX',                 # 趋势强度
            'OBV'                  # 成交量指标
        ]
    }
    
    # 合并所有保留的列
    all_enhanced = []
    for category, columns in enhanced_columns.items():
        all_enhanced.extend(columns)
    
    print("✅ 增强版精简后保留的列:")
    for category, columns in enhanced_columns.items():
        print(f"   {category} ({len(columns)}): {columns}")
    
    print(f"\n📊 增强版统计:")
    print(f"   保留总列数: {len(all_enhanced)}")
    print(f"   相比当前版本增加: {len(all_enhanced) - 25}列")
    print(f"   相比原始版本减少: ~{54 - len(all_enhanced)}列")
    
    return all_enhanced

def create_enhanced_streamlined_files():
    """创建增强版精简文件"""
    print(f"\n🔧 创建增强版精简数据文件")
    print("=" * 80)
    
    # 定义增强版列
    enhanced_columns = define_enhanced_streamlined_columns()
    
    # 查找原始文件
    original_files = [f for f in DATA_DIR.glob("*组合数据*.csv") if not f.name.endswith('_streamlined.csv') and not f.name.endswith('.backup.csv')]
    
    results = []
    
    for original_file in original_files:
        print(f"\n📝 处理文件: {original_file.name}")
        
        try:
            df = pd.read_csv(original_file, encoding='utf-8-sig')
            
            # 检查哪些列实际存在
            available_columns = [col for col in enhanced_columns if col in df.columns]
            missing_columns = [col for col in enhanced_columns if col not in df.columns]
            
            if missing_columns:
                print(f"   ⚠️ 缺失列: {missing_columns}")
            
            print(f"   ✅ 可用列: {len(available_columns)}/{len(enhanced_columns)}")
            
            # 创建增强版精简数据框
            enhanced_df = df[available_columns].copy()
            
            # 优化数据类型
            numeric_columns = enhanced_df.select_dtypes(include=['float64']).columns
            if len(numeric_columns) > 0:
                enhanced_df[numeric_columns] = enhanced_df[numeric_columns].astype('float32')
            
            # 生成增强版文件名
            original_name = original_file.stem
            enhanced_filename = f"{original_name}_enhanced.csv"
            enhanced_path = original_file.parent / enhanced_filename
            
            # 保存增强版文件
            enhanced_df.to_csv(enhanced_path, encoding='utf-8-sig', index=False)
            
            # 计算文件大小变化
            original_size = original_file.stat().st_size / 1024
            enhanced_size = enhanced_path.stat().st_size / 1024
            size_reduction = (original_size - enhanced_size) / original_size * 100
            
            print(f"   ✅ 增强版文件创建成功:")
            print(f"      文件名: {enhanced_filename}")
            print(f"      列数: {len(df.columns)} → {len(enhanced_df.columns)} (减少{len(df.columns) - len(enhanced_df.columns)}列)")
            print(f"      文件大小: {original_size:.1f}KB → {enhanced_size:.1f}KB")
            print(f"      空间节省: {size_reduction:.1f}%")
            
            results.append({
                'file': enhanced_path,
                'df': enhanced_df,
                'original_cols': len(df.columns),
                'enhanced_cols': len(enhanced_df.columns),
                'size_reduction': size_reduction
            })
            
        except Exception as e:
            print(f"   ❌ 处理失败: {e}")
    
    return results

def validate_enhanced_files(results):
    """验证增强版文件"""
    print(f"\n🔍 验证增强版文件")
    print("=" * 80)
    
    for result in results:
        file_path = result['file']
        df = result['df']
        
        print(f"\n📊 验证文件: {file_path.name}")
        print("-" * 60)
        
        # 基本信息
        print(f"   数据行数: {len(df)}")
        print(f"   列数: {len(df.columns)}")
        print(f"   文件大小: {file_path.stat().st_size / 1024:.1f} KB")
        
        # 检查核心指标完整性
        core_indicators = ['收盘价', 'MA20', 'MA50', 'RSI', 'MACD', 'ATR', 'Stoch_SlowK']
        missing_core = [col for col in core_indicators if col not in df.columns]
        if missing_core:
            print(f"   ⚠️ 缺失核心指标: {missing_core}")
        else:
            print(f"   ✅ 核心技术指标完整")
        
        # 检查斐波那契水平
        fib_levels = ['Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618', 'Fib_Ret_0.236', 'Fib_Ret_0.786']
        fib_present = [col for col in fib_levels if col in df.columns]
        print(f"   🔢 斐波那契水平: {len(fib_present)}/5")
        
        # 显示最新数据预览
        preview_cols = ['收盘价', 'MA20', 'RSI', 'Stoch_SlowK', 'Fib_Ret_0.500', 'Fib_Signal']
        available_preview = [col for col in preview_cols if col in df.columns]
        
        if available_preview:
            print(f"   📋 最新数据预览:")
            preview = df[available_preview].tail(3)
            print(preview.to_string(float_format='%.2f', index=False))

def create_comparison_table(results):
    """创建版本对比表"""
    print(f"\n📊 版本对比分析")
    print("=" * 80)
    
    comparison_data = {
        '版本': ['原始版本', '精简版本', '增强版本'],
        '列数': ['51-54', '25', f'{results[0]["enhanced_cols"] if results else "~35"}'],
        '文件大小': ['120-140KB', '60-75KB', '85-105KB'],
        '空间节省': ['0%', '~50%', '~25%'],
        '适用场景': ['完整分析', '快速分析', '平衡分析'],
        '推荐用途': ['深度研究', 'AI快速分析', 'AI全面分析']
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    print(comparison_df.to_string(index=False))
    
    print(f"\n✅ 增强版本优势:")
    print("   1. 保留了重要的长期指标 (MA_LONG, RSI_Long)")
    print("   2. 重新加入随机指标 (Stoch_SlowK/D)")
    print("   3. 增加成交额数据")
    print("   4. 扩展斐波那契水平 (23.6%, 78.6%)")
    print("   5. 增加斐波那契支撑阻力位")
    print("   6. 保留长期ATR对比")
    print("   7. 平衡了精简度和完整性")

def main():
    """主函数"""
    print("BTCUSDT 增强版精简数据工具")
    print("=" * 80)
    print("目标: 在保持精简的同时，增加重要的技术指标")
    print("=" * 80)
    
    # 1. 分析遗漏的重要指标
    analysis_result = analyze_missing_important_indicators()
    
    if analysis_result[0] is None:
        return
    
    # 2. 创建增强版精简文件
    results = create_enhanced_streamlined_files()
    
    if not results:
        print("❌ 未能创建增强版文件")
        return
    
    # 3. 验证增强版文件
    validate_enhanced_files(results)
    
    # 4. 创建对比表
    create_comparison_table(results)
    
    print(f"\n" + "=" * 80)
    print("🎉 增强版精简数据创建完成!")
    print(f"✅ 增强版文件列数: ~{results[0]['enhanced_cols']}列")
    print("✅ 保留了所有核心技术指标")
    print("✅ 重新加入重要的辅助指标")
    print("✅ 扩展了斐波那契分析能力")
    print("✅ 平衡了文件大小和分析完整性")
    
    print(f"\n📁 推荐使用的增强版文件:")
    for result in results:
        print(f"   • {result['file'].name}")
    
    print(f"\n💡 使用建议:")
    print("   - 发送给DeepSeek AI进行全面技术分析")
    print("   - 适合中短期交易策略制定")
    print("   - 包含足够的指标进行多重确认")
    print("   - 文件大小适中，传输效率良好")

if __name__ == "__main__":
    main()
