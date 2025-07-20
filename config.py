"""
币安API配置模块
功能：管理敏感信息、全局配置和路径设置
注意：请先在项目根目录创建 .env 文件存储API密钥
"""

import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv  # 用于加载.env文件中的环境变量

# --------------------------
# 环境变量加载
# --------------------------
# 加载项目根目录下的.env文件
load_dotenv()

# --------------------------
# 目录路径配置
# --------------------------
# 项目根目录
BASE_DIR = Path(__file__).resolve().parent

# 数据存储目录 (自动创建如果不存在)
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True, parents=True)

# 日志目录
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# --------------------------
# 币安API配置
# --------------------------
# 从环境变量获取API密钥（确保已在.env文件中设置）
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

# API基础地址
BINANCE_API_URL = "https://fapi.binance.com"  # 期货API地址
BINANCE_TESTNET_URL = "https://testnet.binancefuture.com"  # 测试网地址

# 交易对和K线类型配置
SYMBOL = 'BTCUSDT'       # 交易对符号
INTERVAL = '1d'          # K线间隔 (默认日线)
KLINE_LIMIT = 120        # 每次请求获取的K线数量 (默认120条数据)
USE_TESTNET = False      # 是否使用测试网络

# 时间周期配置 - 优化数据量到220条
TIMEFRAME_OPTIONS = {
    '1': {'interval': '15m', 'name': '15分钟线', 'limit': 220, 'desc': '最近2.3天'},   # 220个15分钟 ≈ 2.3天
    '2': {'interval': '1h', 'name': '1小时线', 'limit': 220, 'desc': '最近9.2天'},    # 220小时 ≈ 9.2天
    '3': {'interval': '4h', 'name': '4小时线', 'limit': 220, 'desc': '最近36.7天'},   # 220*4小时 ≈ 36.7天
    '4': {'interval': '1d', 'name': '日线', 'limit': 220, 'desc': '最近220天'}        # 220天
}

# --------------------------
# 文件命名配置
# --------------------------
# 获取当前日期（可从环境变量覆盖）
current_date = os.getenv('RUN_DATE', datetime.now().strftime("%Y%m%d"))

# 动态生成文件名的函数
def get_filenames(timeframe_name):
    """根据时间周期生成文件名"""
    return {
        'raw': f"{SYMBOL}_{timeframe_name}原始数据_{current_date}.csv",
        'indicators': f"{SYMBOL}_{timeframe_name}技术指标分析_{current_date}.csv",
        'combined': f"{SYMBOL}_{timeframe_name}组合数据_{current_date}.csv",
        'report': f"{SYMBOL}_{timeframe_name}交易分析报告_{current_date}.txt"
    }

# 默认文件名（向后兼容）
RAW_DATA_FILENAME = f"{SYMBOL}_日线原始数据_{current_date}.csv"
INDICATORS_FILENAME = f"{SYMBOL}_日线技术指标分析_{current_date}.csv"
COMBINED_FILENAME = f"{SYMBOL}_日线组合数据_{current_date}.csv"
REPORT_FILENAME = f"{SYMBOL}_日线交易分析报告_{current_date}.txt"

# 日志文件名格式：app_20240717.log
LOG_FILENAME = f"app_{current_date}.log"

# --------------------------
# TA-Lib 指标参数配置
# --------------------------
# 移动平均线参数
MA_SHORT_TERM = 20    # 短期均线周期
MA_LONG_TERM = 50     # 长期均线周期

# MACD参数
MACD_FAST = 12        # 快速EMA周期
MACD_SLOW = 26        # 慢速EMA周期
MACD_SIGNAL = 9       # 信号线周期

# RSI参数
RSI_PERIOD = 14       # RSI计算周期

# 布林带参数
BB_PERIOD = 20        # 布林带周期
BB_STD_DEV = 2        # 标准差倍数

# 随机指标参数
STOCH_FASTK = 14      # 快速K线周期
STOCH_SLOWK = 3       # 慢速K线周期
STOCH_SLOWD = 3       # 慢速D线周期

# ATR参数
ATR_PERIOD = 14       # 平均真实波幅周期

# ADX参数
ADX_PERIOD = 14       # ADX计算周期

# 针对不同时间周期优化的技术指标参数 (300条数据优化版)
TIMEFRAME_INDICATOR_PARAMS = {
    '15分钟线': {
        'description': '激进短线交易，极敏感参数 (300条数据优化)',
        'MA_SHORT_TERM': 8,      # 快速MA
        'MA_MEDIUM_TERM': 21,    # 中期MA
        'MA_LONG_TERM': 55,      # 长期MA (新增，利用300条数据)
        'MACD_FAST': 5,          # 极快的MACD快线
        'MACD_SLOW': 13,         # 更快的MACD慢线
        'MACD_SIGNAL': 5,        # 更快的信号线
        'RSI_PERIOD': 7,         # 主RSI
        'RSI_SECONDARY': 14,     # 辅助RSI确认 (新增)
        'RSI_LONG': 21,          # 长期RSI过滤 (新增)
        'BB_PERIOD': 12,         # 短期布林带
        'BB_LONG_PERIOD': 30,    # 长期布林带 (新增)
        'BB_STD_DEV': 1.8,       # 更紧的布林带
        'STOCH_FASTK': 7,        # 更快的随机指标
        'STOCH_SLOWK': 3,
        'STOCH_SLOWD': 3,
        'ATR_PERIOD': 8,         # 短期ATR
        'ATR_LONG_PERIOD': 21,   # 长期ATR (新增)
        'ADX_PERIOD': 8,
        'FIB_LOOKBACK_PERIOD': 30  # 斐波那契回看周期 (短期)
    },
    '1小时线': {
        'description': '激进短中期分析，多层次确认 (300条数据优化)',
        'MA_SHORT_TERM': 9,      # 快速MA
        'MA_MEDIUM_TERM': 21,    # 中期MA
        'MA_LONG_TERM': 89,      # 长期MA (新增，斐波那契数列)
        'MACD_FAST': 6,          # 快速MACD
        'MACD_SLOW': 15,         # 标准MACD
        'MACD_SIGNAL': 5,        # 快信号线
        'MACD_LONG_FAST': 12,    # 长期MACD快线 (新增)
        'MACD_LONG_SLOW': 26,    # 长期MACD慢线 (新增)
        'RSI_PERIOD': 9,         # 主RSI
        'RSI_SECONDARY': 14,     # 标准RSI
        'RSI_LONG': 30,          # 长期RSI (新增)
        'BB_PERIOD': 14,         # 短期布林带
        'BB_LONG_PERIOD': 50,    # 长期布林带 (新增)
        'BB_STD_DEV': 1.9,       # 标准差
        'STOCH_FASTK': 9,        # 快速随机指标
        'STOCH_SLOWK': 3,
        'STOCH_SLOWD': 3,
        'ATR_PERIOD': 10,        # 短期ATR
        'ATR_LONG_PERIOD': 30,   # 长期ATR (新增)
        'ADX_PERIOD': 10,
        'FIB_LOOKBACK_PERIOD': 40  # 斐波那契回看周期 (中期)
    },
    '4小时线': {
        'description': '中期分析，标准+长期指标组合 (300条数据优化)',
        'MA_SHORT_TERM': 20,     # 标准短期MA
        'MA_MEDIUM_TERM': 50,    # 标准中期MA
        'MA_LONG_TERM': 144,     # 长期MA (斐波那契数列)
        'MACD_FAST': 12,         # 标准MACD
        'MACD_SLOW': 26,
        'MACD_SIGNAL': 9,
        'MACD_LONG_FAST': 19,    # 保守MACD (新增)
        'MACD_LONG_SLOW': 39,    # 保守MACD (新增)
        'RSI_PERIOD': 14,        # 标准RSI
        'RSI_LONG': 21,          # 长期RSI
        'RSI_EXTRA_LONG': 50,    # 超长期RSI (新增)
        'BB_PERIOD': 20,         # 标准布林带
        'BB_LONG_PERIOD': 89,    # 长期布林带 (新增)
        'BB_STD_DEV': 2,
        'STOCH_FASTK': 14,
        'STOCH_SLOWK': 3,
        'STOCH_SLOWD': 3,
        'ATR_PERIOD': 14,        # 标准ATR
        'ATR_LONG_PERIOD': 50,   # 长期ATR (新增)
        'ADX_PERIOD': 14,
        'FIB_LOOKBACK_PERIOD': 60  # 斐波那契回看周期 (长期)
    },
    '日线': {
        'description': '长期分析，多层次MA系统 (220条数据优化)',
        'MA_SHORT_TERM': 21,     # 短期MA
        'MA_MEDIUM_TERM': 55,    # 中期MA
        'MA_LONG_TERM': 150,     # 长期MA (从200调整为150)
        'MA_EXTRA_LONG': 200,    # 超长期MA (从300调整为200)
        'MACD_FAST': 12,         # 标准MACD
        'MACD_SLOW': 26,
        'MACD_SIGNAL': 9,
        'MACD_LONG_FAST': 19,    # 长期MACD
        'MACD_LONG_SLOW': 39,
        'MACD_LONG_SIGNAL': 9,
        'RSI_PERIOD': 14,        # 标准RSI
        'RSI_LONG': 21,          # 长期RSI
        'RSI_EXTRA_LONG': 50,    # 超长期RSI
        'BB_PERIOD': 21,         # 标准布林带
        'BB_LONG_PERIOD': 89,    # 长期布林带 (从100调整为89)
        'BB_STD_DEV': 2,
        'STOCH_FASTK': 14,
        'STOCH_SLOWK': 3,
        'STOCH_SLOWD': 3,
        'STOCH_LONG_FASTK': 21,  # 长期随机指标
        'ATR_PERIOD': 14,        # 标准ATR
        'ATR_LONG_PERIOD': 50,   # 长期ATR
        'ADX_PERIOD': 14,
        'FIB_LOOKBACK_PERIOD': 80  # 斐波那契回看周期 (从100调整为80)
    }
}

def get_indicator_params(timeframe_name):
    """根据时间周期获取优化的技术指标参数"""
    return TIMEFRAME_INDICATOR_PARAMS.get(timeframe_name, {
        'MA_SHORT_TERM': MA_SHORT_TERM,
        'MA_LONG_TERM': MA_LONG_TERM,
        'MACD_FAST': MACD_FAST,
        'MACD_SLOW': MACD_SLOW,
        'MACD_SIGNAL': MACD_SIGNAL,
        'RSI_PERIOD': RSI_PERIOD,
        'BB_PERIOD': BB_PERIOD,
        'BB_STD_DEV': BB_STD_DEV,
        'STOCH_FASTK': STOCH_FASTK,
        'STOCH_SLOWK': STOCH_SLOWK,
        'STOCH_SLOWD': STOCH_SLOWD,
        'ATR_PERIOD': ATR_PERIOD,
        'ADX_PERIOD': ADX_PERIOD
    })

# --------------------------
# 交易策略参数 (激进化配置)
# --------------------------
# 信号阈值 - 激进化设置
RSI_OVERBOUGHT = 75   # RSI超买阈值 (从70调整为75，更激进)
RSI_OVERSOLD = 25     # RSI超卖阈值 (从30调整为25，更激进)
RSI_STRONG_BUY = 35   # RSI强买入信号阈值 (新增)
RSI_STRONG_SELL = 65  # RSI强卖出信号阈值 (新增)

# 综合信号权重 - 激进化配置 (增加短期指标权重)
SIGNAL_WEIGHTS = {
    'MA': 0.25,      # 减少长期MA权重
    'MACD': 0.3,     # 增加MACD权重 (更敏感)
    'RSI': 0.25,     # 增加RSI权重
    'BB': 0.15,      # 保持布林带权重
    'VOLUME': 0.05   # 减少成交量权重
}

# 激进交易参数
AGGRESSIVE_MODE = True        # 激进模式开关
SCALPING_MODE = True         # 剥头皮模式
MIN_SIGNAL_STRENGTH = 0.6    # 最小信号强度 (从0.7降低到0.6)
ATR_STOP_MULTIPLIER = 1.5    # ATR止损倍数 (从2.0降低到1.5，更紧的止损)
ATR_TARGET_MULTIPLIER = 3.0  # ATR目标倍数 (更大的盈亏比)

# --------------------------
# 日志配置
# --------------------------
LOG_LEVEL = "INFO"    # 日志级别 (DEBUG/INFO/WARNING/ERROR/CRITICAL)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# --------------------------
# 验证关键配置
# --------------------------
if not BINANCE_API_KEY or not BINANCE_API_SECRET:
    raise ValueError("未检测到币安API密钥! 请检查.env文件配置")

# 测试输出配置信息（实际使用时可注释掉）
if __name__ == '__main__':
    print("\n=== 配置信息 ===")
    print(f"API密钥: {'已设置' if BINANCE_API_KEY else '未设置'}")
    print(f"使用测试网络: {'是' if USE_TESTNET else '否'}")
    print(f"交易对: {SYMBOL}")
    print(f"K线间隔: {INTERVAL}")

    print("\n路径配置:")
    print(f"数据目录: {DATA_DIR}")
    print(f"日志目录: {LOG_DIR}")

    print("\n文件配置:")
    print(f"原始数据文件: {RAW_DATA_FILENAME}")
    print(f"技术指标文件: {INDICATORS_FILENAME}")
    print(f"组合数据文件: {COMBINED_FILENAME}")
    print(f"分析报告文件: {REPORT_FILENAME}")

    print("\n技术指标参数:")
    print(f"移动平均线: MA{MA_SHORT_TERM}/MA{MA_LONG_TERM}")
    print(f"MACD: {MACD_FAST}-{MACD_SLOW}-{MACD_SIGNAL}")
    print(f"RSI周期: {RSI_PERIOD}")
    print(f"布林带: {BB_PERIOD}期 {BB_STD_DEV}倍标准差")

    print("\n策略参数:")
    print(f"RSI阈值: 超买>{RSI_OVERBOUGHT} 超卖<{RSI_OVERSOLD}")
    print("信号权重:", SIGNAL_WEIGHTS)