"""
激进交易模式配置文件
专为高频、高风险、高收益的加密货币交易设计
"""

# 激进模式开关
AGGRESSIVE_MODE_ENABLED = True

# 多时间框架配置 - 增加短期时间框架
AGGRESSIVE_TIMEFRAMES = {
    '5m': {
        'interval': '5m', 
        'name': '5分钟线', 
        'limit': 100, 
        'desc': '超短线剥头皮',
        'weight': 0.4  # 高权重用于快速信号
    },
    '15m': {
        'interval': '15m', 
        'name': '15分钟线', 
        'limit': 200, 
        'desc': '短线交易',
        'weight': 0.3
    },
    '1h': {
        'interval': '1h', 
        'name': '1小时线', 
        'limit': 200, 
        'desc': '中短期确认',
        'weight': 0.2
    },
    '4h': {
        'interval': '4h', 
        'name': '4小时线', 
        'limit': 100, 
        'desc': '趋势确认',
        'weight': 0.1  # 低权重，仅用于趋势确认
    }
}

# 激进技术指标参数
AGGRESSIVE_INDICATORS = {
    '5分钟线': {
        'description': '超激进剥头皮参数',
        'MA_SHORT_TERM': 5,      # 极短MA
        'MA_LONG_TERM': 13,      # 短期MA
        'MACD_FAST': 3,          # 极快MACD
        'MACD_SLOW': 8,          
        'MACD_SIGNAL': 3,        
        'RSI_PERIOD': 5,         # 极敏感RSI
        'BB_PERIOD': 10,         # 极短布林带
        'BB_STD_DEV': 1.5,       # 更紧的布林带
        'STOCH_FASTK': 5,        
        'STOCH_SLOWK': 3,
        'STOCH_SLOWD': 3,
        'ATR_PERIOD': 5,         # 极短ATR
        'ADX_PERIOD': 5
    }
}

# 激进信号阈值
AGGRESSIVE_THRESHOLDS = {
    'RSI_EXTREME_OVERBOUGHT': 80,    # 极度超买
    'RSI_EXTREME_OVERSOLD': 20,      # 极度超卖
    'RSI_STRONG_SELL': 70,           # 强卖出
    'RSI_STRONG_BUY': 30,            # 强买入
    'BB_SQUEEZE_THRESHOLD': 0.02,    # 布林带挤压阈值
    'VOLUME_SPIKE_MULTIPLIER': 2.0,  # 成交量激增倍数
    'MACD_DIVERGENCE_THRESHOLD': 0.1 # MACD背离阈值
}

# 激进交易参数
AGGRESSIVE_TRADING = {
    'MAX_LEVERAGE': 5,               # 最大杠杆倍数
    'POSITION_SIZE_MULTIPLIER': 1.5, # 仓位倍数
    'STOP_LOSS_ATR_MULTIPLIER': 1.0, # 极紧止损
    'TAKE_PROFIT_ATR_MULTIPLIER': 4.0, # 大目标位
    'TRAILING_STOP_ENABLED': True,    # 启用移动止损
    'SCALPING_MODE': True,           # 剥头皮模式
    'MAX_HOLDING_MINUTES': 60,       # 最大持仓时间(分钟)
    'MIN_PROFIT_TARGET': 0.5,        # 最小盈利目标(%)
    'MAX_LOSS_TOLERANCE': 1.0        # 最大亏损容忍(%)
}

# 激进信号权重配置
AGGRESSIVE_SIGNAL_WEIGHTS = {
    'SHORT_TERM_MA': 0.35,    # 短期MA权重最高
    'MACD': 0.25,             # MACD次之
    'RSI': 0.20,              # RSI重要
    'BB_BREAKOUT': 0.15,      # 布林带突破
    'VOLUME': 0.05            # 成交量最低
}

# 多重确认策略
MULTI_TIMEFRAME_CONFIRMATION = {
    'REQUIRED_CONFIRMATIONS': 2,      # 至少需要2个时间框架确认
    'PRIMARY_TIMEFRAME': '15m',       # 主要时间框架
    'CONFIRMATION_TIMEFRAMES': ['5m', '1h'], # 确认时间框架
    'DIVERGENCE_DETECTION': True,     # 启用背离检测
    'MOMENTUM_CONFIRMATION': True     # 启用动量确认
}

# 风险管理参数
AGGRESSIVE_RISK_MANAGEMENT = {
    'MAX_DAILY_TRADES': 20,          # 每日最大交易次数
    'MAX_CONCURRENT_POSITIONS': 3,    # 最大同时持仓数
    'DAILY_LOSS_LIMIT': 5.0,         # 每日最大亏损(%)
    'PROFIT_TAKING_LEVELS': [1.0, 2.0, 3.0], # 分批止盈点(%)
    'POSITION_SCALING': True,         # 启用仓位缩放
    'EMERGENCY_STOP': True           # 紧急停止开关
}

# 市场状态检测
MARKET_CONDITION_FILTERS = {
    'VOLATILITY_THRESHOLD': 0.02,    # 波动率阈值
    'TREND_STRENGTH_MIN': 25,        # 最小趋势强度(ADX)
    'VOLUME_CONFIRMATION': True,     # 成交量确认
    'NEWS_IMPACT_FILTER': True,      # 新闻影响过滤
    'MARKET_HOURS_ONLY': False       # 仅在特定时间交易
}

# 激进模式警告
AGGRESSIVE_MODE_WARNINGS = [
    "⚠️ 激进模式启用：高风险高收益策略",
    "⚠️ 建议仅有经验的交易者使用",
    "⚠️ 严格执行止损，避免情绪化交易",
    "⚠️ 建议使用模拟账户先行测试",
    "⚠️ 市场剧烈波动时请谨慎使用"
]

def get_aggressive_params(timeframe):
    """获取激进模式参数"""
    return AGGRESSIVE_INDICATORS.get(timeframe, AGGRESSIVE_INDICATORS['5分钟线'])

def is_aggressive_signal(signal_strength):
    """判断是否为激进信号"""
    return signal_strength >= 0.7  # 降低信号强度要求

def calculate_aggressive_position_size(account_balance, risk_per_trade=0.03):
    """计算激进模式仓位大小"""
    base_position = account_balance * risk_per_trade
    return base_position * AGGRESSIVE_TRADING['POSITION_SIZE_MULTIPLIER']

def get_aggressive_stop_loss(entry_price, atr, direction='long'):
    """计算激进止损位"""
    multiplier = AGGRESSIVE_TRADING['STOP_LOSS_ATR_MULTIPLIER']
    if direction == 'long':
        return entry_price - (atr * multiplier)
    else:
        return entry_price + (atr * multiplier)

def get_aggressive_take_profit(entry_price, atr, direction='long'):
    """计算激进目标位"""
    multiplier = AGGRESSIVE_TRADING['TAKE_PROFIT_ATR_MULTIPLIER']
    if direction == 'long':
        return entry_price + (atr * multiplier)
    else:
        return entry_price - (atr * multiplier)

# 激进模式状态检查
def check_aggressive_mode_conditions():
    """检查激进模式启用条件"""
    conditions = {
        'mode_enabled': AGGRESSIVE_MODE_ENABLED,
        'risk_management_active': AGGRESSIVE_RISK_MANAGEMENT['EMERGENCY_STOP'],
        'market_conditions_suitable': True,  # 需要实时检测
        'account_balance_sufficient': True   # 需要实时检测
    }
    return all(conditions.values())

if __name__ == '__main__':
    print("=== 激进交易模式配置 ===")
    print(f"激进模式状态: {'启用' if AGGRESSIVE_MODE_ENABLED else '禁用'}")
    print(f"最大杠杆: {AGGRESSIVE_TRADING['MAX_LEVERAGE']}倍")
    print(f"剥头皮模式: {'启用' if AGGRESSIVE_TRADING['SCALPING_MODE'] else '禁用'}")
    print("\n激进模式警告:")
    for warning in AGGRESSIVE_MODE_WARNINGS:
        print(warning)
