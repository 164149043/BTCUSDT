"""
验证组合数据文件中的斐波那契水平
"""

import pandas as pd
import sys
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from config import DATA_DIR

def verify_fibonacci_in_combined_data():
    """验证组合数据文件中的斐波那契水平"""
    print("🔍 验证组合数据文件中的斐波那契水平")
    print("=" * 80)
    
    # 查找最新的组合数据文件
    csv_files = [f for f in DATA_DIR.glob("*组合数据*.csv") if not f.name.endswith('.backup.csv')]
    
    if not csv_files:
        print("❌ 未找到组合数据文件")
        return
    
    # 按修改时间排序，获取最新文件
    latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)
    
    print(f"📁 验证文件: {latest_file.name}")
    print("-" * 60)
    
    try:
        df = pd.read_csv(latest_file, encoding='utf-8-sig')
        
        print(f"📊 文件基本信息:")
        print(f"   数据行数: {len(df)}")
        print(f"   总列数: {len(df.columns)}")
        
        # 查找斐波那契列
        fib_columns = [col for col in df.columns if col.startswith('Fib_')]
        
        print(f"\n🔢 斐波那契水平验证:")
        print(f"   斐波那契列数: {len(fib_columns)}")
        
        if fib_columns:
            print("✅ 斐波那契水平已成功添加到组合数据文件中!")
            
            # 按类型分组显示
            retracement_cols = [col for col in fib_columns if 'Ret_' in col]
            extension_cols = [col for col in fib_columns if 'Ext_' in col]
            signal_cols = [col for col in fib_columns if col in ['Fib_Signal', 'Fib_Trend']]
            level_cols = [col for col in fib_columns if 'Level' in col or col in ['Fib_High', 'Fib_Low', 'Fib_Price_Position']]
            
            print(f"\n📈 斐波那契指标分类:")
            print(f"   回调水平 ({len(retracement_cols)}): {retracement_cols}")
            print(f"   扩展水平 ({len(extension_cols)}): {extension_cols}")
            print(f"   交易信号 ({len(signal_cols)}): {signal_cols}")
            print(f"   支撑阻力 ({len(level_cols)}): {level_cols}")
            
            # 显示最新的斐波那契数据
            print(f"\n📋 最新斐波那契数据预览:")
            
            # 选择关键列进行显示
            key_cols = ['收盘价', 'Fib_Trend', 'Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618', 'Fib_Signal']
            available_key_cols = [col for col in key_cols if col in df.columns]
            
            if available_key_cols:
                preview_df = df[available_key_cols].tail(5)
                print(preview_df.to_string(float_format='%.2f'))
            
            # 数据完整性检查
            print(f"\n🔍 数据完整性检查:")
            for col in retracement_cols[:3]:  # 检查前3个回调水平
                if col in df.columns:
                    valid_count = df[col].notna().sum()
                    print(f"   {col}: {valid_count}/{len(df)} 有效值 ({valid_count/len(df)*100:.1f}%)")
            
            # 信号分布统计
            if 'Fib_Signal' in df.columns:
                print(f"\n🎯 斐波那契信号分布:")
                signal_counts = df['Fib_Signal'].value_counts()
                for signal, count in signal_counts.head(5).items():
                    print(f"   {signal}: {count}次 ({count/len(df)*100:.1f}%)")
            
            # 趋势分布统计
            if 'Fib_Trend' in df.columns:
                print(f"\n📈 趋势分布:")
                trend_counts = df['Fib_Trend'].value_counts()
                for trend, count in trend_counts.items():
                    print(f"   {trend}: {count}次 ({count/len(df)*100:.1f}%)")
            
        else:
            print("❌ 未找到斐波那契水平数据")
            print("   可能的原因:")
            print("   1. 斐波那契计算未正确集成")
            print("   2. 数据在组合过程中被意外移除")
            print("   3. 需要重新生成组合数据文件")
        
        # 显示所有列名（用于调试）
        print(f"\n📋 完整列名列表:")
        for i, col in enumerate(df.columns, 1):
            marker = "🔢" if col.startswith('Fib_') else "📊"
            print(f"   {i:2d}. {marker} {col}")
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()

def compare_with_previous_version():
    """与之前版本对比"""
    print(f"\n📊 与之前版本对比")
    print("=" * 80)
    
    csv_files = [f for f in DATA_DIR.glob("*组合数据*.csv") if not f.name.endswith('.backup.csv')]
    
    if len(csv_files) >= 2:
        # 按修改时间排序
        sorted_files = sorted(csv_files, key=lambda x: x.stat().st_mtime, reverse=True)
        
        latest_file = sorted_files[0]
        previous_file = sorted_files[1]
        
        try:
            df_latest = pd.read_csv(latest_file, encoding='utf-8-sig')
            df_previous = pd.read_csv(previous_file, encoding='utf-8-sig')
            
            print(f"📁 最新文件: {latest_file.name} ({len(df_latest.columns)}列)")
            print(f"📁 之前文件: {previous_file.name} ({len(df_previous.columns)}列)")
            
            # 找出新增的列
            new_columns = set(df_latest.columns) - set(df_previous.columns)
            removed_columns = set(df_previous.columns) - set(df_latest.columns)
            
            if new_columns:
                print(f"\n✅ 新增列 ({len(new_columns)}):")
                fib_new = [col for col in new_columns if col.startswith('Fib_')]
                other_new = [col for col in new_columns if not col.startswith('Fib_')]
                
                if fib_new:
                    print(f"   🔢 斐波那契列: {fib_new}")
                if other_new:
                    print(f"   📊 其他列: {other_new}")
            
            if removed_columns:
                print(f"\n🗑️ 移除列 ({len(removed_columns)}): {list(removed_columns)}")
            
            print(f"\n📈 列数变化: {len(df_previous.columns)} → {len(df_latest.columns)} (净增加: {len(df_latest.columns) - len(df_previous.columns)})")
            
        except Exception as e:
            print(f"❌ 对比失败: {e}")
    else:
        print("ℹ️ 只有一个组合数据文件，无法进行对比")

def main():
    """主函数"""
    print("BTCUSDT 斐波那契水平验证工具")
    print("=" * 80)
    
    # 验证斐波那契数据
    verify_fibonacci_in_combined_data()
    
    # 与之前版本对比
    compare_with_previous_version()
    
    print(f"\n" + "=" * 80)
    print("🎉 验证完成!")
    print("如果看到斐波那契列，说明斐波那契水平已成功添加到组合数据文件中")

if __name__ == "__main__":
    main()
