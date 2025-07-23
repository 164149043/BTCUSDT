import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')

# 查找最新的完整组合数据文件
all_files = list(DATA_DIR.glob("*组合数据*.csv"))
latest_files = [f for f in all_files if not f.name.endswith('_23col.csv')]

if latest_files:
    latest_file = max(latest_files, key=lambda x: x.stat().st_mtime)
    print(f"📁 验证文件: {latest_file.name}")
    
    df = pd.read_csv(latest_file, encoding='utf-8-sig')
    print(f"📊 总列数: {len(df.columns)}")
    print(f"📊 数据行数: {len(df)}")
    
    print("\n🔍 DeepSeek新增指标验证:")
    indicators = ['MA3', 'Volume_MA20', 'Volume_Ratio', 'MA_Fast_Signal', 'MACD_Zero_Cross', 'BB_Breakout_Strength', 'Fib_Key_Zone']
    
    for ind in indicators:
        if ind in df.columns:
            valid_count = df[ind].notna().sum()
            print(f"  ✅ {ind}: {valid_count}/{len(df)} 有效数据")
        else:
            print(f"  ❌ {ind}: 未找到")
    
    print(f"\n📋 所有列名:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
else:
    print("❌ 未找到完整组合数据文件")
