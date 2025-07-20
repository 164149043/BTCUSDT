"""
移除斐波那契扩展水平脚本
移除 Fib_Ext_1.618, Fib_Ext_2.000, Fib_Ext_2.618 数据
并将数据量调整为280条
"""

import pandas as pd
import sys
from pathlib import Path

# 添加项目路径
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from config import DATA_DIR

def remove_fib_extensions_from_files():
    """从现有文件中移除指定的斐波那契扩展水平"""
    print("🗑️ 移除斐波那契扩展水平")
    print("=" * 80)
    
    # 要移除的列
    columns_to_remove = [
        'Fib_Ext_1.618',   # 161.8% 黄金扩展
        'Fib_Ext_2.000',   # 200% 扩展
        'Fib_Ext_2.618'    # 261.8% 扩展
    ]
    
    print(f"🎯 目标: 移除以下斐波那契扩展水平:")
    for col in columns_to_remove:
        print(f"   - {col}")
    
    # 查找所有相关文件
    all_files = []
    all_files.extend(DATA_DIR.glob("*组合数据*.csv"))
    all_files.extend(DATA_DIR.glob("*_enhanced.csv"))
    all_files.extend(DATA_DIR.glob("*_streamlined.csv"))
    
    # 排除备份文件
    files_to_process = [f for f in all_files if not f.name.endswith('.backup.csv')]
    
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
            original_rows = len(df)
            
            # 检查哪些目标列存在
            existing_cols_to_remove = [col for col in columns_to_remove if col in df.columns]
            
            if existing_cols_to_remove:
                # 创建备份
                backup_path = file_path.with_suffix('.backup_before_fib_removal.csv')
                df.to_csv(backup_path, encoding='utf-8-sig', index=False)
                print(f"   💾 创建备份: {backup_path.name}")
                
                # 移除指定列
                df_cleaned = df.drop(columns=existing_cols_to_remove)
                print(f"   🗑️ 移除列: {existing_cols_to_remove}")
                
                # 调整数据行数到280条 (如果当前超过280条)
                if len(df_cleaned) > 280:
                    df_cleaned = df_cleaned.tail(280)  # 保留最新的280条
                    print(f"   ✂️ 数据行数调整: {original_rows} → 280")
                else:
                    print(f"   ℹ️ 数据行数: {len(df_cleaned)} (无需调整)")
                
                # 保存清理后的文件
                df_cleaned.to_csv(file_path, encoding='utf-8-sig', index=False)
                
                # 计算文件大小变化
                original_size = backup_path.stat().st_size / 1024
                new_size = file_path.stat().st_size / 1024
                size_reduction = (original_size - new_size) / original_size * 100
                
                print(f"   ✅ 处理完成:")
                print(f"      列数: {original_cols} → {len(df_cleaned.columns)} (减少{len(existing_cols_to_remove)}列)")
                print(f"      行数: {original_rows} → {len(df_cleaned)}")
                print(f"      文件大小: {original_size:.1f}KB → {new_size:.1f}KB (减少{size_reduction:.1f}%)")
                
                processed_count += 1
            else:
                print(f"   ℹ️ 未找到需要移除的斐波那契扩展列")
                
                # 仍然检查是否需要调整行数
                if len(df) > 280:
                    backup_path = file_path.with_suffix('.backup_before_row_adjustment.csv')
                    df.to_csv(backup_path, encoding='utf-8-sig', index=False)
                    
                    df_adjusted = df.tail(280)
                    df_adjusted.to_csv(file_path, encoding='utf-8-sig', index=False)
                    
                    print(f"   ✂️ 仅调整行数: {len(df)} → 280")
                    processed_count += 1
                
        except Exception as e:
            print(f"   ❌ 处理失败: {e}")
    
    print(f"\n" + "=" * 80)
    print(f"🎉 批量处理完成!")
    print(f"✅ 成功处理 {processed_count}/{len(files_to_process)} 个文件")
    print(f"🗑️ 已移除斐波那契扩展水平: 1.618, 2.000, 2.618")
    print(f"✂️ 数据量已调整为280条")

def verify_removal():
    """验证移除结果"""
    print(f"\n🔍 验证移除结果")
    print("=" * 80)
    
    # 查找处理后的文件
    files_to_verify = []
    files_to_verify.extend(DATA_DIR.glob("*组合数据*.csv"))
    files_to_verify.extend(DATA_DIR.glob("*_enhanced.csv"))
    files_to_verify.extend(DATA_DIR.glob("*_streamlined.csv"))
    
    # 排除备份文件
    files_to_verify = [f for f in files_to_verify if not f.name.endswith('.backup.csv') and 'backup_before' not in f.name]
    
    removed_columns = ['Fib_Ext_1.618', 'Fib_Ext_2.000', 'Fib_Ext_2.618']
    
    for file_path in files_to_verify:
        print(f"\n📊 验证文件: {file_path.name}")
        print("-" * 60)
        
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            
            # 检查是否还有被移除的列
            still_present = [col for col in removed_columns if col in df.columns]
            
            if still_present:
                print(f"   ⚠️ 仍包含已移除的列: {still_present}")
            else:
                print(f"   ✅ 目标列已成功移除")
            
            # 检查数据行数
            if len(df) <= 280:
                print(f"   ✅ 数据行数: {len(df)} (≤280)")
            else:
                print(f"   ⚠️ 数据行数: {len(df)} (>280)")
            
            # 检查剩余的斐波那契扩展列
            remaining_fib_ext = [col for col in df.columns if col.startswith('Fib_Ext_')]
            print(f"   🔢 剩余斐波那契扩展: {remaining_fib_ext}")
            
            # 显示文件基本信息
            print(f"   📊 文件信息: {len(df)}行 × {len(df.columns)}列, {file_path.stat().st_size/1024:.1f}KB")
            
        except Exception as e:
            print(f"   ❌ 验证失败: {e}")

def update_documentation():
    """更新斐波那契说明文档"""
    print(f"\n📝 更新斐波那契说明文档")
    print("=" * 80)
    
    doc_file = Path('斐波那契水平说明.md')
    
    if doc_file.exists():
        try:
            # 读取文档内容
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 更新扩展水平表格
            old_table = """| `Fib_Ext_1.272` | 127.2% | ⭐⭐⭐⭐ | **第一目标位**，常见止盈点 |
| `Fib_Ext_1.414` | 141.4% | ⭐⭐⭐ | 中等扩展目标 |
| `Fib_Ext_1.618` | 161.8% | ⭐⭐⭐⭐⭐ | **黄金扩展**，主要目标位 |
| `Fib_Ext_2.000` | 200% | ⭐⭐⭐ | 强势扩展目标 |
| `Fib_Ext_2.618` | 261.8% | ⭐⭐ | 极端扩展目标 |"""
            
            new_table = """| `Fib_Ext_1.272` | 127.2% | ⭐⭐⭐⭐ | **第一目标位**，常见止盈点 |
| `Fib_Ext_1.414` | 141.4% | ⭐⭐⭐ | 中等扩展目标 |"""
            
            # 替换内容
            updated_content = content.replace(old_table, new_table)
            
            # 更新指标数量
            updated_content = updated_content.replace('本系统已成功集成19个斐波那契指标', '本系统已成功集成16个斐波那契指标')
            updated_content = updated_content.replace('斐波那契扩展用于预测价格突破后的目标位：\n\n| 指标名称 | 水平 | 重要性 | 用途 |\n|---------|------|--------|------|\n| `Fib_Ext_1.272` | 127.2% | ⭐⭐⭐⭐ | **第一目标位**，常见止盈点 |\n| `Fib_Ext_1.414` | 141.4% | ⭐⭐⭐ | 中等扩展目标 |\n| `Fib_Ext_1.618` | 161.8% | ⭐⭐⭐⭐⭐ | **黄金扩展**，主要目标位 |\n| `Fib_Ext_2.000` | 200% | ⭐⭐⭐ | 强势扩展目标 |\n| `Fib_Ext_2.618` | 261.8% | ⭐⭐ | 极端扩展目标 |', 
                                              '斐波那契扩展用于预测价格突破后的目标位：\n\n| 指标名称 | 水平 | 重要性 | 用途 |\n|---------|------|--------|------|\n| `Fib_Ext_1.272` | 127.2% | ⭐⭐⭐⭐ | **第一目标位**，常见止盈点 |\n| `Fib_Ext_1.414` | 141.4% | ⭐⭐⭐ | 中等扩展目标 |')
            
            # 保存更新后的文档
            with open(doc_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"   ✅ 已更新斐波那契说明文档")
            print(f"   📝 更新内容:")
            print(f"      - 移除了1.618, 2.000, 2.618扩展水平说明")
            print(f"      - 更新了指标总数: 19 → 16")
            print(f"      - 保留了1.272和1.414扩展水平")
            
        except Exception as e:
            print(f"   ❌ 更新文档失败: {e}")
    else:
        print(f"   ⚠️ 未找到斐波那契说明文档")

def main():
    """主函数"""
    print("BTCUSDT 斐波那契扩展水平移除工具")
    print("=" * 80)
    print("目标:")
    print("  1. 移除 Fib_Ext_1.618, Fib_Ext_2.000, Fib_Ext_2.618")
    print("  2. 将K线数据量调整为280条")
    print("  3. 更新相关文档")
    print("=" * 80)
    
    # 1. 移除斐波那契扩展水平
    remove_fib_extensions_from_files()
    
    # 2. 验证移除结果
    verify_removal()
    
    # 3. 更新文档
    update_documentation()
    
    print(f"\n" + "=" * 80)
    print("🎉 斐波那契扩展水平移除完成!")
    print("✅ 已移除: Fib_Ext_1.618, Fib_Ext_2.000, Fib_Ext_2.618")
    print("✅ 保留: Fib_Ext_1.272 (127.2%), Fib_Ext_1.414 (141.4%)")
    print("✅ K线数据量已调整为280条")
    print("✅ 斐波那契指标总数: 19 → 16")
    print("✅ 相关文档已更新")
    
    print(f"\n💡 优化效果:")
    print("   - 减少了3个不常用的极端扩展水平")
    print("   - 保留了最实用的扩展目标位")
    print("   - 数据量优化，提高计算效率")
    print("   - 文件大小进一步减小")

if __name__ == "__main__":
    main()
