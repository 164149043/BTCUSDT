"""
主执行模块
功能：协调整个BTCUSDT日线分析流程
1. 数据抓取 → 2. 指标计算 → 3. 数据组合 → 4. 报告生成
"""
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# ===== 设置环境变量 =====
# 设置当前日期作为文件后缀
os.environ['RUN_DATE'] = datetime.now().strftime("%Y%m%d")

# ===== 添加项目路径 =====
# 获取当前脚本所在目录
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# ===== 导入各模块 =====
try:
    from binance_client import fetch_and_save_btcusdt_data, fetch_and_save_btcusdt_daily
    from ta_calculator import calculate_indicators
    from combined_data_processor import combine_data  # 新增导入
    from report_generator import generate_trading_report
    from config import DATA_DIR, RAW_DATA_FILENAME, INDICATORS_FILENAME, REPORT_FILENAME, COMBINED_FILENAME, TIMEFRAME_OPTIONS, get_filenames

    print("✅ 所有模块导入成功")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    print("请确保以下文件存在于当前目录:")
    print(" - binance_client.py")
    print(" - ta_calculator.py")
    print(" - combined_data_processor.py")  # 新增提示
    print(" - report_generator.py")
    print(" - config.py")
    sys.exit(1)


# ===== 日志设置 =====
def log_step(step, message):
    """记录步骤日志"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{step}] {message}")


# ===== 时间周期选择 =====
def select_timeframe():
    """选择时间周期"""
    print("\n" + "=" * 50)
    print("请选择K线时间周期:")
    print("=" * 50)

    for key, config in TIMEFRAME_OPTIONS.items():
        print(f"{key}. {config['name']} ({config['desc']})")

    while True:
        choice = input("\n请选择时间周期 (1-4): ").strip()
        if choice in TIMEFRAME_OPTIONS:
            return TIMEFRAME_OPTIONS[choice]
        else:
            print("❌ 无效选择，请输入1-4之间的数字")


# ===== 主流程函数 =====
def main_analysis_flow():
    """
    主分析流程
    """
    print("\n" + "=" * 50)
    print(f"BTCUSDT K线分析流程启动 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    # 0. 选择时间周期
    timeframe_config = select_timeframe()
    interval = timeframe_config['interval']
    limit = timeframe_config['limit']
    timeframe_name = timeframe_config['name']

    print(f"\n📊 已选择: {timeframe_name} (间隔: {interval}, 获取: {limit}条数据)")

    # 生成文件名
    filenames = get_filenames(timeframe_name)

    # 1. 准备数据目录
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # 2. 数据抓取
    log_step("STEP 1", f"开始抓取币安{timeframe_name}数据...")
    try:
        raw_data_path = fetch_and_save_btcusdt_data(
            interval=interval,
            limit=limit,
            timeframe_name=timeframe_name
        )
        log_step("STEP 1", f"数据抓取完成! 文件位置: {raw_data_path}")
    except Exception as e:
        log_step("ERROR", f"数据抓取失败: {e}")
        return

    # 3. 技术指标计算
    log_step("STEP 2", f"开始计算{timeframe_name}技术指标...")
    time.sleep(1)  # 短暂延迟确保文件写入完成
    try:
        indicators_path = calculate_indicators(
            raw_filename=filenames['raw'],
            indicators_filename=filenames['indicators'],
            timeframe_name=timeframe_name
        )
        if indicators_path:
            log_step("STEP 2", f"指标计算完成! 文件位置: {indicators_path}")
        else:
            log_step("ERROR", "指标计算失败!")
            return
    except Exception as e:
        log_step("ERROR", f"指标计算失败: {e}")
        return

    # 4. 组合数据处理
    log_step("STEP 3", f"开始组合{timeframe_name}原始数据和技术指标数据...")
    time.sleep(1)
    try:
        combined_path = combine_data(
            raw_filename=filenames['raw'],
            indicators_filename=filenames['indicators'],
            combined_filename=filenames['combined'],
            timeframe_name=timeframe_name
        )
        if combined_path:
            log_step("STEP 3", f"数据组合完成! 文件位置: {combined_path}")
        else:
            log_step("ERROR", "数据组合失败!")
            return
    except Exception as e:
        log_step("ERROR", f"数据组合失败: {e}")
        return

    # 5. 生成分析报告
    log_step("STEP 4", f"开始生成{timeframe_name}交易分析报告...")
    time.sleep(1)  # 短暂延迟确保文件写入完成
    try:
        report_path = generate_trading_report(
            indicators_filename=filenames['indicators'],
            report_filename=filenames['report'],
            timeframe_name=timeframe_name
        )
        if report_path:
            log_step("STEP 4", f"报告生成完成! 文件位置: {report_path}")
        else:
            log_step("ERROR", "报告生成失败!")
            return
    except Exception as e:
        log_step("ERROR", f"报告生成失败: {e}")
        return

    # 6. 完成提示
    log_step("COMPLETE", f"{timeframe_name}分析流程成功完成!")
    print("\n" + "=" * 50)
    print(f"生成的{timeframe_name}文件:")
    print(f"1. 原始数据: {raw_data_path}")
    print(f"2. 技术指标: {indicators_path}")
    print(f"3. 组合数据: {combined_path}")
    print(f"4. 分析报告: {report_path}")
    print("\n下一步操作:")
    print("1. 打开报告文件查看分析结果")
    print("2. 将组合数据文件发送给DeepSeek AI进行深度分析")
    print("3. 将报告内容发送给DeepSeek AI获取详细建议")
    print("=" * 50)


def display_file_paths():
    """显示文件路径信息"""
    print("\n当前配置的文件路径:")
    print(f"● 原始数据文件: {DATA_DIR / RAW_DATA_FILENAME}")
    print(f"● 技术指标文件: {DATA_DIR / INDICATORS_FILENAME}")
    print(f"● 组合数据文件: {DATA_DIR / COMBINED_FILENAME}")  # 新增显示
    print(f"● 分析报告文件: {DATA_DIR / REPORT_FILENAME}")

    # 检查文件是否存在
    print("\n文件存在状态:")
    raw_exists = "存在" if (DATA_DIR / RAW_DATA_FILENAME).exists() else "不存在"
    indicators_exists = "存在" if (DATA_DIR / INDICATORS_FILENAME).exists() else "不存在"
    combined_exists = "存在" if (DATA_DIR / COMBINED_FILENAME).exists() else "不存在"  # 新增检查
    report_exists = "存在" if (DATA_DIR / REPORT_FILENAME).exists() else "不存在"

    print(f"● 原始数据: {raw_exists}")
    print(f"● 技术指标: {indicators_exists}")
    print(f"● 组合数据: {combined_exists}")  # 新增显示
    print(f"● 分析报告: {report_exists}")


def run_test_mode():
    """测试模式：运行各模块测试"""
    print("\n" + "=" * 50)
    print("进入测试模式")
    print("=" * 50)

    print("\n[测试1] 数据抓取模块测试...")
    try:
        from binance_client import fetch_and_save_btcusdt_daily
        raw_path = fetch_and_save_btcusdt_daily()
        print(f"✓ 数据抓取测试成功! 文件: {raw_path}")
    except Exception as e:
        print(f"✗ 数据抓取测试失败: {e}")

    print("\n[测试2] 技术指标计算测试...")
    try:
        from ta_calculator import calculate_indicators
        indicators_path = calculate_indicators()
        print(f"✓ 指标计算测试成功! 文件: {indicators_path}")
    except Exception as e:
        print(f"✗ 指标计算测试失败: {e}")

    print("\n[测试3] 组合数据处理测试...")  # 新增测试
    try:
        from combined_data_processor import combine_data
        combined_path = combine_data()
        print(f"✓ 数据组合测试成功! 文件: {combined_path}")
    except Exception as e:
        print(f"✗ 数据组合测试失败: {e}")

    print("\n[测试4] 报告生成模块测试...")
    try:
        from report_generator import generate_trading_report
        report_path = generate_trading_report()
        print(f"✓ 报告生成测试成功! 文件: {report_path}")

        # 显示报告前几行
        if report_path and report_path.exists():
            print("\n报告预览:")
            with open(report_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i < 15:  # 显示前15行
                        print(line.strip())
                    else:
                        break
    except Exception as e:
        print(f"✗ 报告生成测试失败: {e}")

    print("\n测试完成!")


if __name__ == "__main__":
    print("=" * 50)
    print("BTCUSDT多时间周期分析系统")
    print("=" * 50)
    print("选项:")
    print("1. 执行完整分析流程 (支持多时间周期)")
    print("2. 显示文件路径信息")
    print("3. 运行测试模式")
    print("4. 退出")

    choice = input("\n请选择操作 (1-4): ")

    if choice == "1":
        main_analysis_flow()
    elif choice == "2":
        display_file_paths()
    elif choice == "3":
        run_test_mode()
    elif choice == "4":
        print("退出程序")
    else:
        print("无效选择，请重新运行")