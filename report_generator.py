"""
分析报告生成模块
功能：加载技术指标数据，生成易于DeepSeek理解的交易分析报告
输出：包含技术分析和交易建议的文本报告
"""
import pandas as pd
import os
import sys
from pathlib import Path
from datetime import datetime

# ===== 路径修复 =====
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from config import DATA_DIR, INDICATORS_FILENAME, REPORT_FILENAME, SYMBOL, get_filenames

    print("✅ 成功导入 config 模块")
except ImportError as e:
    print(f"❌ 导入 config 模块失败: {e}")
    # 使用默认配置
    DATA_DIR = Path('data')
    INDICATORS_FILENAME = 'BTCUSDT_技术指标分析_.csv'
    REPORT_FILENAME = 'BTCUSDT_交易分析报告_.txt'
    SYMBOL = 'BTCUSDT'
    print("⚠️ 使用默认配置继续运行")


# ===== 报告生成函数 =====
def generate_trading_report(indicators_filename=None, report_filename=None, timeframe_name=None):
    """
    主函数：生成交易分析报告
    参数:
        indicators_filename: 指标数据文件名
        report_filename: 报告文件名
        timeframe_name: 时间周期名称
    """
    print("\n" + "=" * 50)
    print(f"开始生成交易分析报告 - {timeframe_name or '日线'}")
    print("=" * 50)

    # 1. 加载技术指标数据
    indicators_path = DATA_DIR / (indicators_filename or INDICATORS_FILENAME)
    if not indicators_path.exists():
        print(f"❌ 错误: 技术指标文件不存在 - {indicators_path}")
        return None

    try:
        # 读取CSV文件
        df = pd.read_csv(indicators_path, encoding='utf-8-sig')

        # 检查必要的列是否存在
        required_columns = ['开盘价', '收盘价', 'MA20', 'MA50', 'RSI', 'MACD', '综合信号']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"❌ 错误: 数据文件缺少必要的列 - {missing_cols}")
            return None

        print(f"✅ 成功加载技术指标数据, 共 {len(df)} 条记录")
    except Exception as e:
        print(f"❌ 加载数据失败: {e}")
        return None

    # 2. 提取最新数据点
    latest_data = df.iloc[-1]

    # 3. 生成报告
    report = create_analysis_report(df, latest_data)

    # 4. 保存报告
    report_path = DATA_DIR / (report_filename or REPORT_FILENAME)
    save_report(report, report_path)

    print(f"✅ 交易分析报告生成完成! 文件保存至: {report_path}")

    return report_path


def create_analysis_report(df, latest_data):
    """
    创建完整的分析报告
    """
    # 报告头部信息
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"===== {SYMBOL} 技术分析报告 {report_date} =====\n\n"

    # 1. 价格概览
    report += price_overview_section(df, latest_data)

    # 2. 指标分析
    report += indicators_analysis_section(latest_data)

    # 3. 近期信号变化
    report += recent_signals_section(df)

    # 4. 综合分析
    report += comprehensive_analysis_section(latest_data)

    # 5. 交易建议
    report += trading_recommendation_section(latest_data)

    # 6. 数据说明
    report += data_description_section()

    return report


def price_overview_section(df, latest_data):
    """价格概览部分"""
    section = "📈 1. 价格概览\n"
    section += "-" * 50 + "\n"

    # 最新价格
    current_price = latest_data['收盘价']
    prev_price = df.iloc[-2]['收盘价'] if len(df) > 1 else current_price
    price_change = current_price - prev_price
    price_change_pct = (price_change / prev_price) * 100 if prev_price != 0 else 0

    section += f"● 当前价格: ${current_price:,.2f} "
    section += f"({price_change:+.2f}, {price_change_pct:+.2f}%)\n"

    # 近期价格范围
    last_5_days = df.iloc[-5:]
    high_5d = last_5_days['最高价'].max()
    low_5d = last_5_days['最低价'].min()
    section += f"● 近5日价格范围: ${low_5d:,.2f} - ${high_5d:,.2f}\n"

    # 成交量分析
    current_volume = latest_data['成交量']
    avg_volume_5d = last_5_days['成交量'].mean()
    volume_change_pct = ((current_volume - avg_volume_5d) / avg_volume_5d) * 100

    section += f"● 当前成交量: {current_volume:,.2f} "
    section += f"({volume_change_pct:+.2f}% 对比5日均值)\n\n"

    return section


def indicators_analysis_section(latest_data):
    """指标分析部分"""
    section = "📊 2. 关键指标分析\n"
    section += "-" * 50 + "\n"

    # 移动平均线
    ma20 = latest_data['MA20']
    ma50 = latest_data['MA50']
    ma_relation = "高于" if ma20 > ma50 else "低于"
    section += f"● 移动平均线: \n"
    section += f"  - MA20: ${ma20:,.2f}\n"
    section += f"  - MA50: ${ma50:,.2f}\n"
    section += f"  - MA20 {ma_relation} MA50 ({'金叉' if ma20 > ma50 else '死叉'}信号)\n"

    # MACD
    macd = latest_data['MACD']
    macd_signal = latest_data['MACD_Signal']
    macd_relation = "高于" if macd > macd_signal else "低于"
    section += f"● MACD指标: \n"
    section += f"  - MACD线: {macd:.4f}\n"
    section += f"  - 信号线: {macd_signal:.4f}\n"
    section += f"  - MACD线 {macd_relation} 信号线 ({'看涨' if macd > macd_signal else '看跌'}信号)\n"

    # RSI
    rsi = latest_data['RSI']
    rsi_status = "超买" if rsi > 70 else "超卖" if rsi < 30 else "中性"
    section += f"● RSI指标: {rsi:.2f} ({rsi_status}区域)\n"

    # 布林带
    price = latest_data['收盘价']
    bb_upper = latest_data['BB_Upper']
    bb_lower = latest_data['BB_Lower']
    bb_status = "突破上轨" if price > bb_upper else "突破下轨" if price < bb_lower else "正常范围"
    section += f"● 布林带: \n"
    section += f"  - 价格位置: ${price:,.2f}\n"
    section += f"  - 上轨: ${bb_upper:,.2f}\n"
    section += f"  - 下轨: ${bb_lower:,.2f}\n"
    section += f"  - 状态: {bb_status}\n"

    section += "\n"
    return section


def recent_signals_section(df):
    """近期信号变化部分"""
    section = "🔔 3. 近期信号变化\n"
    section += "-" * 50 + "\n"

    # 获取最近5天的数据
    last_5_days = df.iloc[-5:]

    # 反转顺序，从最新到最旧
    last_5_days = last_5_days.iloc[::-1]

    # 提取日期索引
    if 'open_time' in last_5_days.columns:
        dates = last_5_days['open_time']
    elif '日期' in last_5_days.columns:
        dates = last_5_days['日期']
    else:
        dates = [f"Day -{i}" for i in range(4, -1, -1)]

    # 为每一天生成信号摘要
    for i, (index, row) in enumerate(last_5_days.iterrows()):
        date_str = dates.iloc[i] if isinstance(dates, pd.Series) else dates[i]

        section += f"● {date_str}:\n"

        # MA信号
        ma_signal = row.get('MA_Signal', '中性')
        section += f"  - MA信号: {ma_signal}"

        # MACD信号
        macd_signal = row.get('MACD_Signal_Analysis', '中性')
        section += f", MACD: {macd_signal}"

        # RSI信号
        rsi_signal = row.get('RSI_Signal', '中性')
        section += f", RSI: {rsi_signal}"

        # 综合信号
        combined_signal = row.get('综合信号', '中性')
        section += f", 综合信号: {combined_signal}\n"

    section += "\n"
    return section


def comprehensive_analysis_section(latest_data):
    """综合分析部分"""
    section = "🧠 4. 综合分析\n"
    section += "-" * 50 + "\n"

    # 提取关键信号
    combined_signal = latest_data.get('综合信号', '中性')
    rsi = latest_data['RSI']
    macd_diff = latest_data['MACD'] - latest_data['MACD_Signal']

    # 根据信号生成分析
    if combined_signal == '强烈看涨':
        section += "● 市场呈现强劲看涨趋势，多个指标一致发出买入信号。\n"
        section += "● 技术指标显示买方力量主导市场，价格动能强劲。\n"
    elif combined_signal == '看涨':
        section += "● 市场呈现看涨趋势，主要技术指标偏向积极。\n"
        section += "● 价格走势显示买方力量增强，但需关注关键阻力位。\n"
    elif combined_signal == '强烈看跌':
        section += "● 市场呈现强烈看跌趋势，多个指标一致发出卖出信号。\n"
        section += "● 技术指标显示卖方力量主导市场，价格下行压力大。\n"
    elif combined_signal == '看跌':
        section += "● 市场呈现看跌趋势，主要技术指标偏向消极。\n"
        section += "● 价格走势显示卖方力量增强，需关注关键支撑位。\n"
    else:
        section += "● 市场呈现中性趋势，技术指标未形成一致方向。\n"
        section += "● 价格可能进入盘整阶段，等待更明确信号。\n"

    # RSI特定分析
    if rsi > 70:
        section += "● RSI进入超买区域，警惕短期回调风险。\n"
    elif rsi < 30:
        section += "● RSI进入超卖区域，可能出现反弹机会。\n"

    # MACD特定分析
    if macd_diff > 0:
        section += "● MACD柱状图为正值且可能扩大，显示上涨动能增强。\n"
    elif macd_diff < 0:
        section += "● MACD柱状图为负值且可能扩大，显示下跌动能增强。\n"

    section += "\n"
    return section


def trading_recommendation_section(latest_data):
    """交易建议部分"""
    section = "💡 5. 交易建议\n"
    section += "-" * 50 + "\n"

    # 提取关键信号
    combined_signal = latest_data.get('综合信号', '中性')
    rsi = latest_data['RSI']

    # 根据信号生成建议
    if combined_signal == '强烈看涨':
        section += "● 建议策略: 积极买入或加仓\n"
        section += "● 入场点: 当前价格或小幅回调时\n"
        section += "● 止损位: 设置在MA50下方或近期低点下方\n"
        section += "● 目标位: 布林带上轨或前期高点\n"
    elif combined_signal == '看涨':
        section += "● 建议策略: 谨慎买入\n"
        section += "● 入场点: 等待小幅回调至MA20附近\n"
        section += "● 止损位: 设置在MA50下方\n"
        section += "● 目标位: 布林带上轨或阻力位\n"
    elif combined_signal == '强烈看跌':
        section += "● 建议策略: 积极卖出或减仓\n"
        section += "● 入场点: 当前价格或小幅反弹时\n"
        section += "● 止损位: 设置在MA50上方或近期高点上方\n"
        section += "● 目标位: 布林带下轨或前期低点\n"
    elif combined_signal == '看跌':
        section += "● 建议策略: 谨慎卖出或观望\n"
        section += "● 入场点: 等待小幅反弹至MA20附近\n"
        section += "● 止损位: 设置在MA50上方\n"
        section += "● 目标位: 布林带下轨或支撑位\n"
    else:  # 中性
        section += "● 建议策略: 观望或区间交易\n"
        section += "● 入场点: 布林带下轨买入，上轨卖出\n"
        section += "● 止损位: 区间外设置止损\n"
        section += "● 目标位: 区间另一端\n"

    # 风险管理建议
    section += "\n● 风险管理建议:\n"
    section += "  - 单笔交易风险控制在总资金的1-2%\n"
    section += "  - 使用止损单管理下行风险\n"
    section += "  - 关注重要经济事件和新闻\n"

    section += "\n"
    return section


def data_description_section():
    """数据说明部分"""
    section = "📝 6. 数据说明\n"
    section += "-" * 50 + "\n"

    section += "● 数据来源: 币安交易所(Binance) BTCUSDT日线数据\n"
    section += "● 指标说明:\n"
    section += "  - MA20/MA50: 20日/50日移动平均线\n"
    section += "  - MACD: 异同移动平均线\n"
    section += "  - RSI: 相对强弱指标(超买>70, 超卖<30)\n"
    section += "  - BB: 布林带(20日, 2倍标准差)\n"
    section += "● 综合信号: 基于多个技术指标的加权评估\n\n"

    section += "💬 请将此报告全文发送给DeepSeek AI获取详细解读和策略建议\n"

    return section


def save_report(report_content, file_path):
    """
    保存报告到文本文件
    """
    # 确保目录存在
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # 保存报告
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"💾 报告已保存: {file_path}")


def get_latest_report_path():
    """获取最新的报告文件路径"""
    report_path = DATA_DIR / REPORT_FILENAME
    return report_path if report_path.exists() else None


if __name__ == "__main__":
    print("=" * 50)
    print("交易报告生成模块测试")
    print("=" * 50)

    try:
        # 生成报告
        report_path = generate_trading_report()

        if report_path:
            # 打印报告内容
            print("\n生成报告内容预览:")
            with open(report_path, 'r', encoding='utf-8') as f:
                print(f.read())
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback

        traceback.print_exc()