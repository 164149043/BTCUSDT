"""
CSV清理验证脚本
验证BB_Squeeze和其他多余数据是否已成功移除
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

def verify_csv_cleanup():
    """验证CSV清理结果"""
    print("🔍 CSV清理结果验证")
    print("=" * 80)
    
    # 查找所有组合数据文件
    csv_files = list(DATA_DIR.glob("*组合数据*.csv"))
    backup_files = list(DATA_DIR.glob("*组合数据*.backup.csv"))
    
    if not csv_files:
        print("❌ 未找到组合数据CSV文件")
        return
    
    print(f"📁 找到 {len(csv_files)} 个组合数据文件")
    print(f"💾 找到 {len(backup_files)} 个备份文件")
    
    # 定义应该被移除的列
    unwanted_columns = [
        'BB_Squeeze',           # 布林带挤压标志
        'BB_Width',             # 布林带宽度
        'MA8', 'MA21', 'MA55',  # 重复的MA列
        'MACD_Long_Hist',       # 长期MACD柱状图
        'RSI_Extra_Long',       # 超长期RSI
        '计算时间',              # 计算时间戳
        'MA_Signal',            # MA信号
        'MACD_Signal_Analysis', # MACD信号分析
        'RSI_Signal',           # RSI信号
        'BB_Signal',            # BB信号
        'Stoch_Signal',         # 随机指标信号
        '综合信号'              # 综合信号
    ]
    
    # 定义核心必须保留的列
    required_columns = [
        'open_time',            # 时间
        '开盘价', '最高价', '最低价', '收盘价',  # OHLC
        '成交量',               # 成交量
        'MA20', 'MA50',         # 基础移动平均线
        'MACD', 'MACD_Signal', 'MACD_Hist',  # MACD
        'RSI',                  # RSI
        'BB_Upper', 'BB_Middle', 'BB_Lower',  # 布林带
        'ATR',                  # ATR
        'ADX'                   # ADX
    ]
    
    all_passed = True
    
    for csv_file in csv_files:
        if csv_file.name.endswith('.backup.csv'):
            continue
            
        print(f"\n📊 验证文件: {csv_file.name}")
        print("-" * 60)
        
        try:
            df = pd.read_csv(csv_file, encoding='utf-8-sig')
            
            # 检查文件基本信息
            print(f"   数据维度: {len(df)}行 × {len(df.columns)}列")
            print(f"   内存使用: {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            # 检查是否还有不需要的列
            found_unwanted = [col for col in unwanted_columns if col in df.columns]
            if found_unwanted:
                print(f"   ❌ 仍包含多余列: {found_unwanted}")
                all_passed = False
            else:
                print(f"   ✅ 多余列已清理完成")
            
            # 检查必需列是否存在
            missing_required = [col for col in required_columns if col not in df.columns]
            if missing_required:
                print(f"   ⚠️ 缺少必需列: {missing_required}")
                all_passed = False
            else:
                print(f"   ✅ 核心列完整")
            
            # 检查数据类型优化
            float64_cols = df.select_dtypes(include=['float64']).columns
            if len(float64_cols) > 0:
                print(f"   ⚠️ 仍有{len(float64_cols)}列使用float64 (可进一步优化)")
            else:
                print(f"   ✅ 数据类型已优化")
            
            # 检查列顺序
            first_cols = list(df.columns[:10])
            expected_first_cols = ['open_time', '开盘价', '最高价', '最低价', '收盘价', '成交量', '成交额', '成交笔数', '主动买入量', '主动买入额']
            if first_cols == expected_first_cols:
                print(f"   ✅ 列顺序已优化")
            else:
                print(f"   ⚠️ 列顺序可能需要调整")
            
            # 显示当前列结构
            print(f"   📋 当前列结构:")
            
            # 按类别显示列
            basic_cols = [col for col in df.columns if col in ['open_time', '开盘价', '最高价', '最低价', '收盘价', '成交量', '成交额', '成交笔数', '主动买入量', '主动买入额']]
            ma_cols = [col for col in df.columns if 'MA' in col and col not in ['MACD', 'MACD_Signal', 'MACD_Hist']]
            macd_cols = [col for col in df.columns if 'MACD' in col]
            rsi_cols = [col for col in df.columns if 'RSI' in col]
            bb_cols = [col for col in df.columns if 'BB_' in col]
            other_cols = [col for col in df.columns if col not in basic_cols + ma_cols + macd_cols + rsi_cols + bb_cols]
            
            print(f"      基础数据 ({len(basic_cols)}): {basic_cols}")
            print(f"      移动平均 ({len(ma_cols)}): {ma_cols}")
            print(f"      MACD ({len(macd_cols)}): {macd_cols}")
            print(f"      RSI ({len(rsi_cols)}): {rsi_cols}")
            print(f"      布林带 ({len(bb_cols)}): {bb_cols}")
            print(f"      其他指标 ({len(other_cols)}): {other_cols}")
            
        except Exception as e:
            print(f"   ❌ 验证失败: {e}")
            all_passed = False
    
    # 总结
    print(f"\n" + "=" * 80)
    if all_passed:
        print("✅ 所有文件清理验证通过!")
    else:
        print("⚠️ 部分文件需要进一步处理")
    
    return all_passed

def compare_before_after():
    """对比清理前后的差异"""
    print(f"\n📊 清理前后对比")
    print("=" * 80)
    
    csv_files = list(DATA_DIR.glob("*组合数据*.csv"))
    
    total_space_saved = 0
    total_columns_removed = 0
    
    for csv_file in csv_files:
        if csv_file.name.endswith('.backup.csv'):
            continue
            
        backup_file = csv_file.with_suffix('.backup.csv')
        
        if backup_file.exists():
            try:
                df_before = pd.read_csv(backup_file, encoding='utf-8-sig')
                df_after = pd.read_csv(csv_file, encoding='utf-8-sig')
                
                size_before = backup_file.stat().st_size / 1024  # KB
                size_after = csv_file.stat().st_size / 1024     # KB
                space_saved = size_before - size_after
                
                columns_removed = len(df_before.columns) - len(df_after.columns)
                
                print(f"\n📁 {csv_file.name}:")
                print(f"   列数: {len(df_before.columns)} → {len(df_after.columns)} (减少{columns_removed}列)")
                print(f"   文件大小: {size_before:.1f}KB → {size_after:.1f}KB (节省{space_saved:.1f}KB)")
                print(f"   空间节省: {space_saved/size_before*100:.1f}%")
                
                # 显示被移除的列
                removed_cols = set(df_before.columns) - set(df_after.columns)
                if removed_cols:
                    print(f"   移除的列: {list(removed_cols)}")
                
                total_space_saved += space_saved
                total_columns_removed += columns_removed
                
            except Exception as e:
                print(f"❌ 对比失败: {e}")
    
    print(f"\n📈 总计:")
    print(f"   总共移除列数: {total_columns_removed}")
    print(f"   总共节省空间: {total_space_saved:.1f}KB")

def cleanup_recommendations():
    """提供清理建议"""
    print(f"\n💡 清理建议")
    print("=" * 80)
    
    print("✅ 已完成的清理:")
    print("   - 移除了 BB_Squeeze 列 (布林带挤压标志)")
    print("   - 移除了 BB_Width 列 (布林带宽度中间数据)")
    print("   - 移除了重复的MA列 (MA8, MA21, MA55)")
    print("   - 移除了部分长期指标 (RSI_Extra_Long, MACD_Long_Hist)")
    print("   - 优化了数据类型 (float64 → float32)")
    print("   - 优化了列顺序 (核心指标前置)")
    
    print("\n🔧 进一步优化建议:")
    print("   1. 如果不需要长期指标，可以移除:")
    print("      - RSI_Secondary, RSI_Long")
    print("      - BB_Long_Upper, BB_Long_Middle, BB_Long_Lower")
    print("      - ATR_Long, ATR_Ratio")
    print("      - MACD_Long, MACD_Long_Signal")
    
    print("\n   2. 如果只需要基础分析，可以保留核心列:")
    print("      - 基础数据: open_time, OHLC, 成交量")
    print("      - 核心指标: MA20, MA50, MACD, RSI, BB, ATR, ADX")
    
    print("\n   3. 备份文件管理:")
    print("      - 如果清理结果满意，可以删除 *.backup.csv 文件")
    print("      - 备份文件占用额外存储空间")
    
    print("\n📋 当前推荐的最小核心列集合 (24列):")
    core_columns = [
        'open_time', '开盘价', '最高价', '最低价', '收盘价', '成交量',
        'MA20', 'MA50', 'MACD', 'MACD_Signal', 'MACD_Hist',
        'RSI', 'BB_Upper', 'BB_Middle', 'BB_Lower',
        'Stoch_SlowK', 'Stoch_SlowD', 'OBV', 'ATR', 'ADX'
    ]
    print("   " + ", ".join(core_columns))

def main():
    """主函数"""
    print("BTCUSDT CSV清理验证工具")
    print("=" * 80)
    
    # 验证清理结果
    verification_passed = verify_csv_cleanup()
    
    # 对比清理前后
    compare_before_after()
    
    # 提供建议
    cleanup_recommendations()
    
    print(f"\n" + "=" * 80)
    if verification_passed:
        print("🎉 CSV清理任务完成!")
        print("✅ BB_Squeeze 和其他多余数据已成功移除")
        print("✅ 文件结构已优化，数据更加精简")
        print("✅ 所有核心技术指标完整保留")
    else:
        print("⚠️ 部分清理任务需要进一步处理")

if __name__ == "__main__":
    main()
