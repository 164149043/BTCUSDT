"""
CSV数据类型优化脚本
将float64优化为float32以节省内存和存储空间
"""

import pandas as pd
import os
import sys
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from config import DATA_DIR

def optimize_csv_datatypes():
    """优化CSV文件的数据类型"""
    print("🔧 CSV数据类型优化")
    print("=" * 80)
    
    # 查找所有组合数据文件
    csv_files = [f for f in DATA_DIR.glob("*组合数据*.csv") if not f.name.endswith('.backup.csv')]
    
    if not csv_files:
        print("❌ 未找到组合数据CSV文件")
        return
    
    print(f"📁 找到 {len(csv_files)} 个组合数据文件")
    
    total_space_saved = 0
    
    for csv_file in csv_files:
        print(f"\n🔧 优化文件: {csv_file.name}")
        print("-" * 60)
        
        try:
            # 读取文件
            df = pd.read_csv(csv_file, encoding='utf-8-sig')
            
            # 记录原始大小
            original_size = csv_file.stat().st_size / 1024  # KB
            
            # 检查数据类型
            print(f"   原始数据类型分布:")
            dtype_counts = df.dtypes.value_counts()
            for dtype, count in dtype_counts.items():
                print(f"     {dtype}: {count}列")
            
            # 优化数据类型
            optimized = False
            
            # 1. 优化float64 → float32
            float64_columns = df.select_dtypes(include=['float64']).columns
            if len(float64_columns) > 0:
                # 排除时间列
                time_columns = ['open_time']
                float64_to_convert = [col for col in float64_columns if col not in time_columns]
                
                if float64_to_convert:
                    df[float64_to_convert] = df[float64_to_convert].astype('float32')
                    print(f"   ✅ 转换 {len(float64_to_convert)} 列: float64 → float32")
                    optimized = True
            
            # 2. 优化int64 → int32 (如果有的话)
            int64_columns = df.select_dtypes(include=['int64']).columns
            if len(int64_columns) > 0:
                # 检查数值范围是否适合int32
                int64_to_convert = []
                for col in int64_columns:
                    if col not in time_columns:  # 排除时间列
                        min_val = df[col].min()
                        max_val = df[col].max()
                        # int32范围: -2,147,483,648 到 2,147,483,647
                        if min_val >= -2147483648 and max_val <= 2147483647:
                            int64_to_convert.append(col)
                
                if int64_to_convert:
                    df[int64_to_convert] = df[int64_to_convert].astype('int32')
                    print(f"   ✅ 转换 {len(int64_to_convert)} 列: int64 → int32")
                    optimized = True
            
            if optimized:
                # 保存优化后的文件
                df.to_csv(csv_file, encoding='utf-8-sig', index=False)
                
                # 计算节省的空间
                new_size = csv_file.stat().st_size / 1024  # KB
                space_saved = original_size - new_size
                total_space_saved += space_saved
                
                print(f"   📊 文件大小: {original_size:.1f}KB → {new_size:.1f}KB")
                print(f"   💾 节省空间: {space_saved:.1f}KB ({space_saved/original_size*100:.1f}%)")
                
                # 显示优化后的数据类型分布
                print(f"   优化后数据类型分布:")
                dtype_counts_new = df.dtypes.value_counts()
                for dtype, count in dtype_counts_new.items():
                    print(f"     {dtype}: {count}列")
            else:
                print(f"   ℹ️ 数据类型已是最优，无需优化")
                
        except Exception as e:
            print(f"   ❌ 优化失败: {e}")
    
    print(f"\n" + "=" * 80)
    print(f"🎉 数据类型优化完成!")
    print(f"💾 总共节省空间: {total_space_saved:.1f}KB")
    
    if total_space_saved > 0:
        print(f"✅ 内存使用效率提升约 {total_space_saved/sum(f.stat().st_size/1024 for f in csv_files)*100:.1f}%")

def verify_optimization():
    """验证优化结果"""
    print(f"\n🔍 验证优化结果")
    print("=" * 80)
    
    csv_files = [f for f in DATA_DIR.glob("*组合数据*.csv") if not f.name.endswith('.backup.csv')]
    
    for csv_file in csv_files:
        print(f"\n📊 验证文件: {csv_file.name}")
        print("-" * 60)
        
        try:
            df = pd.read_csv(csv_file, encoding='utf-8-sig')
            
            # 检查数据类型
            dtype_counts = df.dtypes.value_counts()
            print(f"   数据类型分布:")
            for dtype, count in dtype_counts.items():
                print(f"     {dtype}: {count}列")
            
            # 检查是否还有float64
            float64_columns = df.select_dtypes(include=['float64']).columns
            if len(float64_columns) > 0:
                print(f"   ⚠️ 仍有 {len(float64_columns)} 列使用float64: {list(float64_columns)}")
            else:
                print(f"   ✅ 所有数值列已优化为float32")
            
            # 内存使用情况
            memory_usage = df.memory_usage(deep=True).sum() / 1024  # KB
            print(f"   💾 内存使用: {memory_usage:.1f}KB")
            
        except Exception as e:
            print(f"   ❌ 验证失败: {e}")

def show_optimization_benefits():
    """显示优化带来的好处"""
    print(f"\n💡 数据类型优化的好处")
    print("=" * 80)
    
    print("✅ 内存使用优化:")
    print("   - float64 → float32: 内存使用减少50%")
    print("   - int64 → int32: 内存使用减少50%")
    print("   - 对于300行×30列的数据，可节省约30-50KB内存")
    
    print("\n✅ 文件存储优化:")
    print("   - CSV文件大小减少30-50%")
    print("   - 磁盘I/O性能提升")
    print("   - 网络传输更快")
    
    print("\n✅ 计算性能优化:")
    print("   - float32计算速度更快")
    print("   - 缓存命中率提高")
    print("   - 批量数据处理更高效")
    
    print("\n⚠️ 注意事项:")
    print("   - float32精度略低于float64 (约7位有效数字)")
    print("   - 对于金融数据，精度通常足够")
    print("   - 时间列保持原始类型以确保兼容性")

def main():
    """主函数"""
    print("BTCUSDT CSV数据类型优化工具")
    print("=" * 80)
    print("功能: 将float64优化为float32，减少内存使用和文件大小")
    print("=" * 80)
    
    # 执行优化
    optimize_csv_datatypes()
    
    # 验证结果
    verify_optimization()
    
    # 显示优化好处
    show_optimization_benefits()

if __name__ == "__main__":
    main()
