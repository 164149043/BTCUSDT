"""
技术指标计算模块
功能：加载原始K线数据，使用TA-Lib计算技术指标，并保存结果
依赖：pandas, numpy, TA-Lib
"""
import pandas as pd
import numpy as np
import talib
import os
import sys
from pathlib import Path
from datetime import datetime

# ===== 路径修复 =====
# 确保可以导入config模块
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from config import DATA_DIR, RAW_DATA_FILENAME, INDICATORS_FILENAME, \
        MA_SHORT_TERM, MA_LONG_TERM, MACD_FAST, MACD_SLOW, MACD_SIGNAL, \
        RSI_PERIOD, BB_PERIOD, BB_STD_DEV, ATR_PERIOD, \
        get_filenames, get_indicator_params

    print("✅ 成功导入 config 模块")

    # ===== 在参数部分添加激进模式配置 =====
    try:
        from config import AGGRESSIVE_MODE_ENABLED, AGGRESSIVE_SIGNAL_WEIGHTS
    except ImportError:
        AGGRESSIVE_MODE_ENABLED = False
        AGGRESSIVE_SIGNAL_WEIGHTS = {
            'MA': 1.2,
            'MACD': 1.3,
            'RSI': 1.4,
            'BB': 1.2,
            'FIB': 1.5
        }
        print("⚠️ 使用内置激进模式配置")

    # 尝试导入激进模式配置
    try:
        from aggressive_config import (
            AGGRESSIVE_MODE_ENABLED, AGGRESSIVE_SIGNAL_WEIGHTS,
            AGGRESSIVE_THRESHOLDS, get_aggressive_params
        )
        AGGRESSIVE_AVAILABLE = True
        if AGGRESSIVE_MODE_ENABLED:
            print("🚀 激进模式配置已加载")
    except ImportError:
        AGGRESSIVE_AVAILABLE = False
        if not 'AGGRESSIVE_MODE_ENABLED' in locals():
            AGGRESSIVE_MODE_ENABLED = False
        print("ℹ️ 激进模式配置未找到，使用标准模式")
except ImportError as e:
    print(f"❌ 导入 config 模块失败: {e}")
    # 尝试直接定义变量（备选方案）
    DATA_DIR = Path('data')
    RAW_DATA_FILENAME = 'BTCUSDT_日线原始数据_.csv'
    INDICATORS_FILENAME = 'BTCUSDT_技术指标分析_.csv'
    MA_SHORT_TERM = 20
    MA_LONG_TERM = 50
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    RSI_PERIOD = 14
    BB_PERIOD = 20
    BB_STD_DEV = 2
    print("⚠️ 使用默认配置继续运行")


# ===== 主函数 =====
def calculate_indicators(raw_filename=None, indicators_filename=None, timeframe_name=None):
    """
    主函数：加载原始数据，计算技术指标，保存结果
    参数:
        raw_filename: 原始数据文件名
        indicators_filename: 指标数据文件名
        timeframe_name: 时间周期名称
    """
    print("\n" + "=" * 50)
    print(f"开始计算技术指标 - {timeframe_name or '日线'}")
    print("=" * 50)

    # 获取针对当前时间周期优化的参数
    if timeframe_name:
        params = get_indicator_params(timeframe_name)
        print(f"📊 使用{timeframe_name}优化参数: {params['description']}")
    else:
        # 使用默认参数
        params = {
            'MA_SHORT_TERM': MA_SHORT_TERM,
            'MA_LONG_TERM': MA_LONG_TERM,
            'MACD_FAST': MACD_FAST,
            'MACD_SLOW': MACD_SLOW,
            'MACD_SIGNAL': MACD_SIGNAL,
            'RSI_PERIOD': RSI_PERIOD,
            'BB_PERIOD': BB_PERIOD,
            'BB_STD_DEV': BB_STD_DEV
        }

    # ===== 在calculate_indicators函数中启用激进模式 =====
    # 应用激进模式参数覆盖
    if AGGRESSIVE_MODE_ENABLED:
        print("🚀 应用激进模式参数优化")
        # 缩短所有主要指标周期
        params['MA_SHORT_TERM'] = max(5, int(params.get('MA_SHORT_TERM', MA_SHORT_TERM) * 0.7))
        params['MA_LONG_TERM'] = max(10, int(params.get('MA_LONG_TERM', MA_LONG_TERM) * 0.8))
        params['MACD_FAST'] = max(8, int(params.get('MACD_FAST', MACD_FAST) * 0.7))
        params['MACD_SLOW'] = max(18, int(params.get('MACD_SLOW', MACD_SLOW) * 0.7))
        params['RSI_PERIOD'] = max(7, int(params.get('RSI_PERIOD', RSI_PERIOD) * 0.7))

    # 1. 确定文件路径
    if raw_filename:
        raw_data_path = DATA_DIR / raw_filename
    else:
        raw_data_path = DATA_DIR / RAW_DATA_FILENAME

    if not raw_data_path.exists():
        print(f"❌ 错误: 原始数据文件不存在 - {raw_data_path}")
        return None

    try:
        # 读取CSV文件，正确处理中文列名
        df = pd.read_csv(raw_data_path, encoding='utf-8-sig')

        # 检查必要的列是否存在
        required_columns = ['开盘价', '最高价', '最低价', '收盘价', '成交量']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"❌ 错误: 数据文件缺少必要的列 - {missing_cols}")
            return None

        print(f"✅ 成功加载原始数据, 共 {len(df)} 条记录")
    except Exception as e:
        print(f"❌ 加载数据失败: {e}")
        return None

    # 2. 转换数据类型
    df = convert_data_types(df)

    # 3. 计算技术指标
    df = compute_ta_indicators(df, params)

    # 4. 添加信号分析
    df = add_signal_analysis(df, params)

    # 5. 保存结果
    if indicators_filename:
        indicators_path = DATA_DIR / indicators_filename
    else:
        indicators_path = DATA_DIR / INDICATORS_FILENAME

    save_indicators(df, indicators_path)

    print(f"✅ 技术指标计算完成! 文件保存至: {indicators_path}")

    return indicators_path


def convert_data_types(df):
    """
    转换数据类型为适合TA-Lib计算
    """
    # 转换时间列为datetime类型
    if 'open_time' in df.columns:
        df['open_time'] = pd.to_datetime(df['open_time'])
        df.set_index('open_time', inplace=True)
    elif 'open_time' not in df.index.name:
        # 如果open_time不在索引中，尝试设置第一列为索引
        df.set_index(df.columns[0], inplace=True)

    # 确保数值列是浮点数类型
    numeric_cols = ['开盘价', '最高价', '最低价', '收盘价', '成交量']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 移除可能的NaN值
    df.dropna(subset=['收盘价'], inplace=True)

    return df


# ===== 修改compute_ta_indicators函数 =====
def compute_ta_indicators(df, params=None):
    """
    使用TA-Lib计算技术指标
    参数:
        df: 数据框
        params: 技术指标参数字典
    """
    print("🔧 计算技术指标中...")

    # 使用传入的参数或默认参数
    if params is None:
        params = {
            'MA_SHORT_TERM': MA_SHORT_TERM,
            'MA_LONG_TERM': MA_LONG_TERM,
            'MACD_FAST': MACD_FAST,
            'MACD_SLOW': MACD_SLOW,
            'MACD_SIGNAL': MACD_SIGNAL,
            'RSI_PERIOD': RSI_PERIOD,
            'BB_PERIOD': BB_PERIOD,
            'BB_STD_DEV': BB_STD_DEV
        }

    # 提取价格序列
    close = df['收盘价'].values
    high = df['最高价'].values
    low = df['最低价'].values
    volume = df['成交量'].values

    # 1. 移动平均线系统 - 使用更短周期
    ma_short = max(5, int(params.get('MA_SHORT_TERM', MA_SHORT_TERM) * 0.7))  # 缩短30%
    ma_medium = params.get('MA_MEDIUM_TERM', params.get('MA_LONG_TERM', MA_LONG_TERM))
    ma_long = max(10, int(params.get('MA_LONG_TERM', MA_LONG_TERM) * 0.8))  # 缩短20%

    # 增加超短期均线 (3日)
    df['MA3'] = talib.MA(close, timeperiod=3)

    # 基础MA计算
    df[f'MA{ma_short}'] = talib.MA(close, timeperiod=ma_short)
    df[f'MA{ma_medium}'] = talib.MA(close, timeperiod=ma_medium)

    # 长期MA (利用300条数据)
    if ma_long != ma_medium:
        df[f'MA{ma_long}'] = talib.MA(close, timeperiod=ma_long)

    # 超长期MA (如果有定义)
    ma_extra_long = params.get('MA_EXTRA_LONG')
    if ma_extra_long and ma_extra_long <= len(df):
        df[f'MA{ma_extra_long}'] = talib.MA(close, timeperiod=ma_extra_long)

    # 为了保持向后兼容，也保留MA20和MA50列名
    df['MA20'] = df[f'MA{ma_short}']
    df['MA50'] = df[f'MA{ma_medium}']

    # 新增长期MA列
    if ma_long > 50:
        df['MA_LONG'] = df[f'MA{ma_long}']

    # 2. MACD - 使用更灵敏的参数
    macd_fast = max(8, int(params.get('MACD_FAST', MACD_FAST) * 0.7))  # 缩短30%
    macd_slow = max(18, int(params.get('MACD_SLOW', MACD_SLOW) * 0.7))  # 缩短30%
    macd_signal = params.get('MACD_SIGNAL', MACD_SIGNAL)
    macd, macd_signal_line, macd_hist = talib.MACD(
        close,
        fastperiod=macd_fast,
        slowperiod=macd_slow,
        signalperiod=macd_signal
    )
    df['MACD'] = macd
    df['MACD_Signal'] = macd_signal_line
    df['MACD_Hist'] = macd_hist

    # 长期MACD (如果定义)
    macd_long_fast = params.get('MACD_LONG_FAST')
    macd_long_slow = params.get('MACD_LONG_SLOW')
    if macd_long_fast and macd_long_slow:
        macd_long_signal = params.get('MACD_LONG_SIGNAL', macd_signal)
        macd_long, macd_long_signal_line, macd_long_hist = talib.MACD(
            close,
            fastperiod=macd_long_fast,
            slowperiod=macd_long_slow,
            signalperiod=macd_long_signal
        )
        df['MACD_Long'] = macd_long
        df['MACD_Long_Signal'] = macd_long_signal_line
        df['MACD_Long_Hist'] = macd_long_hist

    # 3. RSI - 使用更短周期
    rsi_period = max(7, int(params.get('RSI_PERIOD', RSI_PERIOD) * 0.7))  # 缩短30%
    df['RSI'] = talib.RSI(close, timeperiod=rsi_period)

    # 辅助RSI (如果定义)
    rsi_secondary = params.get('RSI_SECONDARY')
    if rsi_secondary and rsi_secondary != rsi_period:
        df['RSI_Secondary'] = talib.RSI(close, timeperiod=rsi_secondary)

    # 长期RSI (如果定义)
    rsi_long = params.get('RSI_LONG')
    if rsi_long and rsi_long != rsi_period:
        df['RSI_Long'] = talib.RSI(close, timeperiod=rsi_long)

    # 超长期RSI (如果定义)
    rsi_extra_long = params.get('RSI_EXTRA_LONG')
    if rsi_extra_long and rsi_extra_long <= len(df):
        df['RSI_Extra_Long'] = talib.RSI(close, timeperiod=rsi_extra_long)

    # 4. 布林带 - 放宽波动范围
    bb_period = params.get('BB_PERIOD', BB_PERIOD)
    bb_std_dev = min(3.0, params.get('BB_STD_DEV', BB_STD_DEV) * 1.5)  # 放宽50%
    upper, middle, lower = talib.BBANDS(
        close,
        timeperiod=bb_period,
        nbdevup=bb_std_dev,
        nbdevdn=bb_std_dev
    )
    df['BB_Upper'] = upper
    df['BB_Middle'] = middle
    df['BB_Lower'] = lower

    # 5. 添加成交量指标 - 量价确认
    df['Volume_MA20'] = talib.MA(volume, timeperiod=20)
    df['Volume_Ratio'] = volume / df['Volume_MA20']

    # 长期布林带 (如果定义)
    bb_long_period = params.get('BB_LONG_PERIOD')
    if bb_long_period and bb_long_period <= len(df):
        upper_long, middle_long, lower_long = talib.BBANDS(
            close,
            timeperiod=bb_long_period,
            nbdevup=bb_std_dev,
            nbdevdn=bb_std_dev
        )
        df['BB_Long_Upper'] = upper_long
        df['BB_Long_Middle'] = middle_long
        df['BB_Long_Lower'] = lower_long

    # 5. 随机指标
    stoch_fastk = params.get('STOCH_FASTK', 14)
    stoch_slowk = params.get('STOCH_SLOWK', 3)
    stoch_slowd = params.get('STOCH_SLOWD', 3)
    slowk, slowd = talib.STOCH(
        high, low, close,
        fastk_period=stoch_fastk,
        slowk_period=stoch_slowk,
        slowk_matype=0,
        slowd_period=stoch_slowd,
        slowd_matype=0
    )
    df['Stoch_SlowK'] = slowk
    df['Stoch_SlowD'] = slowd

    # 6. 成交量指标
    df['OBV'] = talib.OBV(close, volume)

    # 7. 多重ATR系统（平均真实波幅）(300条数据优化版)
    # 主ATR
    atr_period = params.get('ATR_PERIOD', ATR_PERIOD)
    df['ATR'] = talib.ATR(high, low, close, timeperiod=atr_period)

    # 长期ATR (如果定义)
    atr_long_period = params.get('ATR_LONG_PERIOD')
    if atr_long_period and atr_long_period != atr_period:
        df['ATR_Long'] = talib.ATR(high, low, close, timeperiod=atr_long_period)

        # ATR比率 (短期ATR / 长期ATR) - 波动率变化指标
        df['ATR_Ratio'] = df['ATR'] / df['ATR_Long']

    # 8. ADX（平均趋向指数）
    adx_period = params.get('ADX_PERIOD', 14)
    df['ADX'] = talib.ADX(high, low, close, timeperiod=adx_period)

    # 9. 斐波那契水平计算
    fib_lookback = params.get('FIB_LOOKBACK_PERIOD', 50)
    df = calculate_fibonacci_levels(df, lookback_period=fib_lookback)

    # 10. 斐波那契交易信号
    df = add_fibonacci_signals(df)

    # 添加计算时间戳
    df['计算时间'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return df


def calculate_fibonacci_levels(df, lookback_period=50):
    """
    计算斐波那契回调和扩展水平
    参数:
        df: 数据框，包含高低价数据
        lookback_period: 回看周期，用于确定高低点
    返回:
        df: 添加了斐波那契水平的数据框
    """
    print("🔢 计算斐波那契水平...")

    # 斐波那契回调水平
    fib_retracement_levels = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]
    # 斐波那契扩展水平 (移除1.618, 2.0, 2.618)
    fib_extension_levels = [1.272, 1.414]

    # 初始化斐波那契列
    for level in fib_retracement_levels:
        df[f'Fib_Ret_{level:.3f}'] = np.nan

    for level in fib_extension_levels:
        df[f'Fib_Ext_{level:.3f}'] = np.nan

    # 添加趋势方向和关键点
    df['Fib_Trend'] = 'neutral'
    df['Fib_High'] = np.nan
    df['Fib_Low'] = np.nan

    # 计算滚动高低点
    df['Rolling_High'] = df['最高价'].rolling(window=lookback_period, center=True).max()
    df['Rolling_Low'] = df['最低价'].rolling(window=lookback_period, center=True).min()

    for i in range(lookback_period, len(df) - lookback_period):
        # 获取当前窗口的高低点
        window_high = df['Rolling_High'].iloc[i]
        window_low = df['Rolling_Low'].iloc[i]
        current_price = df['收盘价'].iloc[i]

        if pd.notna(window_high) and pd.notna(window_low) and window_high != window_low:
            # 记录关键点
            df.loc[df.index[i], 'Fib_High'] = window_high
            df.loc[df.index[i], 'Fib_Low'] = window_low

            # 判断趋势方向
            price_range = window_high - window_low
            price_position = (current_price - window_low) / price_range

            if price_position > 0.6:
                trend = 'uptrend'
            elif price_position < 0.4:
                trend = 'downtrend'
            else:
                trend = 'neutral'

            df.loc[df.index[i], 'Fib_Trend'] = trend

            # 计算斐波那契回调水平
            for level in fib_retracement_levels:
                if trend == 'uptrend':
                    # 上升趋势：从低点向高点的回调
                    fib_price = window_high - (window_high - window_low) * level
                elif trend == 'downtrend':
                    # 下降趋势：从高点向低点的回调
                    fib_price = window_low + (window_high - window_low) * level
                else:
                    # 中性趋势：使用中点
                    fib_price = window_low + (window_high - window_low) * level

                df.loc[df.index[i], f'Fib_Ret_{level:.3f}'] = fib_price

            # 计算斐波那契扩展水平
            for level in fib_extension_levels:
                if trend == 'uptrend':
                    # 上升趋势扩展
                    fib_price = window_high + (window_high - window_low) * (level - 1)
                elif trend == 'downtrend':
                    # 下降趋势扩展
                    fib_price = window_low - (window_high - window_low) * (level - 1)
                else:
                    # 中性趋势扩展
                    fib_price = window_high + (window_high - window_low) * (level - 1)

                df.loc[df.index[i], f'Fib_Ext_{level:.3f}'] = fib_price

    # 清理临时列
    df.drop(['Rolling_High', 'Rolling_Low'], axis=1, inplace=True)

    # 前向填充斐波那契水平（保持最近的有效值）
    fib_columns = [col for col in df.columns if col.startswith('Fib_')]
    for col in fib_columns:
        if col not in ['Fib_Trend', 'Fib_High', 'Fib_Low']:
            df[col] = df[col].ffill()  # 使用新的方法替代fillna(method='ffill')

    # 填充趋势和关键点
    df['Fib_Trend'] = df['Fib_Trend'].ffill()
    df['Fib_High'] = df['Fib_High'].ffill()
    df['Fib_Low'] = df['Fib_Low'].ffill()

    print(f"✅ 斐波那契水平计算完成，添加了{len(fib_retracement_levels + fib_extension_levels) + 3}个斐波那契指标")

    return df

def add_fibonacci_signals(df):
    """
    添加基于斐波那契水平的交易信号
    """
    print("🎯 生成斐波那契交易信号...")

    # 初始化信号列
    df['Fib_Signal'] = 'neutral'
    df['Fib_Support_Level'] = np.nan
    df['Fib_Resistance_Level'] = np.nan
    df['Fib_Price_Position'] = np.nan

    # 关键斐波那契水平
    key_retracement_levels = ['Fib_Ret_0.382', 'Fib_Ret_0.500', 'Fib_Ret_0.618']
    key_extension_levels = ['Fib_Ext_1.272', 'Fib_Ext_1.414']

    for i in range(len(df)):
        current_price = df['收盘价'].iloc[i]
        trend = df['Fib_Trend'].iloc[i]

        if pd.notna(current_price) and trend != 'neutral':
            # 找到最近的支撑和阻力水平
            support_levels = []
            resistance_levels = []

            # 检查回调水平
            for level_col in key_retracement_levels:
                if level_col in df.columns:
                    level_price = df[level_col].iloc[i]
                    if pd.notna(level_price):
                        if level_price < current_price:
                            support_levels.append(level_price)
                        elif level_price > current_price:
                            resistance_levels.append(level_price)

            # 检查扩展水平
            for level_col in key_extension_levels:
                if level_col in df.columns:
                    level_price = df[level_col].iloc[i]
                    if pd.notna(level_price):
                        if trend == 'uptrend' and level_price > current_price:
                            resistance_levels.append(level_price)
                        elif trend == 'downtrend' and level_price < current_price:
                            support_levels.append(level_price)

            # 确定最近的支撑和阻力
            if support_levels:
                nearest_support = max(support_levels)  # 最近的支撑（最高的支撑位）
                df.loc[df.index[i], 'Fib_Support_Level'] = nearest_support

            if resistance_levels:
                nearest_resistance = min(resistance_levels)  # 最近的阻力（最低的阻力位）
                df.loc[df.index[i], 'Fib_Resistance_Level'] = nearest_resistance

            # 计算价格在斐波那契区间的位置
            fib_high = df['Fib_High'].iloc[i]
            fib_low = df['Fib_Low'].iloc[i]
            if pd.notna(fib_high) and pd.notna(fib_low) and fib_high != fib_low:
                price_position = (current_price - fib_low) / (fib_high - fib_low)
                df.loc[df.index[i], 'Fib_Price_Position'] = price_position

                # 生成交易信号
                tolerance = 0.02  # 2%的容差

                # 检查是否接近关键斐波那契水平
                if abs(price_position - 0.382) < tolerance:
                    signal = 'fib_382_bounce' if trend == 'uptrend' else 'fib_382_reject'
                elif abs(price_position - 0.5) < tolerance:
                    signal = 'fib_50_bounce' if trend == 'uptrend' else 'fib_50_reject'
                elif abs(price_position - 0.618) < tolerance:
                    signal = 'fib_618_bounce' if trend == 'uptrend' else 'fib_618_reject'
                elif price_position > 1.0:
                    signal = 'fib_breakout_up'
                elif price_position < 0.0:
                    signal = 'fib_breakout_down'
                elif 0.618 < price_position < 0.786:
                    signal = 'fib_golden_zone'
                else:
                    signal = 'neutral'

                # 增强信号检测 - 添加成交量确认
                if signal != 'neutral' and 'Volume_Ratio' in df.columns:
                    vol_ratio = df['Volume_Ratio'].iloc[i]
                    if vol_ratio > 1.2:
                        signal = signal + "_带量"
                    elif vol_ratio < 0.8:
                        signal = signal + "_缩量"

                df.loc[df.index[i], 'Fib_Signal'] = signal

    print("✅ 斐波那契交易信号生成完成")
    return df

def add_signal_analysis(df, params=None):
    """
    添加基于指标的交易信号分析
    参数:
        df: 数据框
        params: 技术指标参数字典
    """
    print("🔍 添加信号分析...")

    # 使用传入的参数或默认参数
    if params is None:
        params = {
            'MA_SHORT_TERM': MA_SHORT_TERM,
            'MA_LONG_TERM': MA_LONG_TERM
        }

    # 激进模式参数
    rsi_overbought = 80 if AGGRESSIVE_MODE_ENABLED else 75
    rsi_oversold = 20 if AGGRESSIVE_MODE_ENABLED else 25

    # 1. 移动平均线交叉信号 - 增加超短期均线交叉
    if 'MA3' in df.columns:
        df['MA_Fast_Signal'] = np.where(
            df['MA3'] > df['MA20'],
            '快速金叉',
            np.where(df['MA3'] < df['MA20'], '快速死叉', '中性')
        )

    # 保持原有MA信号
    df['MA_Signal'] = np.where(
        df['MA20'] > df['MA50'],
        '金叉',
        np.where(df['MA20'] < df['MA50'], '死叉', '中性')
    )

    # 2. MACD信号 - 增加零轴交叉检测
    df['MACD_Signal_Analysis'] = np.where(
        df['MACD'] > df['MACD_Signal'],
        '看涨',
        np.where(df['MACD'] < df['MACD_Signal'], '看跌', '中性')
    )

    df['MACD_Zero_Cross'] = np.select(
        [
            (df['MACD'] > 0) & (df['MACD'].shift(1) <= 0),
            (df['MACD'] < 0) & (df['MACD'].shift(1) >= 0)
        ],
        ['零轴上穿', '零轴下穿'],
        default=''
    )

    # 3. RSI信号 - 使用更激进的阈值
    df['RSI_Signal'] = np.select(
        [
            df['RSI'] >= rsi_overbought,
            df['RSI'] <= rsi_oversold,
            (df['RSI'] >= 70) & (df['RSI'] < rsi_overbought),
            (df['RSI'] <= 30) & (df['RSI'] > rsi_oversold),
            (df['RSI'] > 50) & (df['RSI'] < 70),
            (df['RSI'] > 30) & (df['RSI'] <= 50)
        ],
        ['极度超买', '极度超卖', '强卖出', '强买入', '看涨区域', '看跌区域'],
        default='中性'
    )

    # 4. 布林带信号 - 增加突破强度检测
    # 计算布林带宽度用于挤压检测
    df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Middle']
    df['BB_Squeeze'] = df['BB_Width'] < df['BB_Width'].rolling(20).mean() * 0.8  # 挤压检测

    # 增加成交量确认的突破信号
    if 'Volume_Ratio' in df.columns:
        df['BB_Breakout_Strength'] = np.where(
            (df['收盘价'] > df['BB_Upper']) & (df['Volume_Ratio'] > 1.5),
            '带量突破上轨',
            np.where((df['收盘价'] < df['BB_Lower']) & (df['Volume_Ratio'] > 1.5),
                    '带量突破下轨', '')
        )

    df['BB_Signal'] = np.select(
        [
            (df['收盘价'] > df['BB_Upper']) & df['BB_Squeeze'],           # 挤压后突破上轨
            (df['收盘价'] < df['BB_Lower']) & df['BB_Squeeze'],           # 挤压后突破下轨
            df['收盘价'] > df['BB_Upper'],                                # 普通突破上轨
            df['收盘价'] < df['BB_Lower'],                                # 普通突破下轨
            (df['收盘价'] > df['BB_Middle'] * 1.005) & (df['收盘价'] <= df['BB_Upper']),  # 强势上轨区域
            (df['收盘价'] < df['BB_Middle'] * 0.995) & (df['收盘价'] >= df['BB_Lower'])   # 弱势下轨区域
        ],
        ['强力突破上轨', '强力突破下轨', '突破上轨', '突破下轨', '强势上轨区域', '弱势下轨区域'],
        default='中轨附近'
    )

    # 5. 随机指标信号
    df['Stoch_Signal'] = np.select(
        [
            (df['Stoch_SlowK'] > 80) & (df['Stoch_SlowD'] > 80),
            (df['Stoch_SlowK'] < 20) & (df['Stoch_SlowD'] < 20),
            (df['Stoch_SlowK'] > df['Stoch_SlowD']),
            (df['Stoch_SlowK'] < df['Stoch_SlowD'])
        ],
        ['超买交叉', '超卖交叉', '看涨交叉', '看跌交叉'],
        default='中性'
    )

    # 5.5. 斐波那契信号增强
    if 'Fib_Price_Position' in df.columns:
        df['Fib_Key_Zone'] = np.select(
            [
                (df['Fib_Price_Position'] >= 0.35) & (df['Fib_Price_Position'] <= 0.40),
                (df['Fib_Price_Position'] >= 0.58) & (df['Fib_Price_Position'] <= 0.62),
                (df['Fib_Price_Position'] >= 0.75) & (df['Fib_Price_Position'] <= 0.80)
            ],
            ['关键支撑区', '反转区', '强势区'],
            default=''
        )

    # 6. 增强综合信号强度 - 300条数据多层次确认
    # 检查是否有长期指标
    has_long_indicators = 'RSI_Long' in df.columns or 'MACD_Long' in df.columns

    if has_long_indicators:
        # 使用多重时间框架确认的增强信号
        conditions = [
            # 超强看涨信号 (新增)
            (df.get('MA_Fast_Signal', '') == '快速金叉') &
            (df.get('MACD_Zero_Cross', '') == '零轴上穿') &
            (df.get('Volume_Ratio', 1) > 1.5) &
            (df.get('Fib_Key_Zone', '') == '关键支撑区'),

            # 超强看跌信号 (新增)
            (df.get('MA_Fast_Signal', '') == '快速死叉') &
            (df.get('MACD_Zero_Cross', '') == '零轴下穿') &
            (df.get('Volume_Ratio', 1) > 1.5) &
            (df.get('Fib_Key_Zone', '') == '强势区'),

            # 超强信号 - 所有时间框架一致 + 激进指标
            (df['MA_Signal'] == '金叉') & (df['MACD_Signal_Analysis'] == '看涨') &
            (df['RSI_Signal'].isin(['强买入', '看涨区域'])) &
            (df['BB_Signal'].isin(['强力突破上轨', '突破上轨', '强势上轨区域'])) &
            (df.get('RSI_Long', 50) < 70),  # 长期RSI未超买

            (df['MA_Signal'] == '死叉') & (df['MACD_Signal_Analysis'] == '看跌') &
            (df['RSI_Signal'].isin(['强卖出', '看跌区域'])) &
            (df['BB_Signal'].isin(['强力突破下轨', '突破下轨', '弱势下轨区域'])) &
            (df.get('RSI_Long', 50) > 30),  # 长期RSI未超卖

            # 极强信号 - 多个激进指标同时触发
            (df['MA_Signal'] == '金叉') & (df['MACD_Signal_Analysis'] == '看涨') &
            (df['RSI_Signal'].isin(['强买入', '看涨区域'])) &
            (df['BB_Signal'].isin(['强力突破上轨', '突破上轨', '强势上轨区域'])),

            (df['MA_Signal'] == '死叉') & (df['MACD_Signal_Analysis'] == '看跌') &
            (df['RSI_Signal'].isin(['强卖出', '看跌区域'])) &
            (df['BB_Signal'].isin(['强力突破下轨', '突破下轨', '弱势下轨区域'])),

            # 强信号 - 部分激进指标触发
            (df['MA_Signal'] == '金叉') & (df['MACD_Signal_Analysis'] == '看涨') &
            (df['RSI_Signal'].isin(['强买入', '看涨区域'])),

            (df['MA_Signal'] == '死叉') & (df['MACD_Signal_Analysis'] == '看跌') &
            (df['RSI_Signal'].isin(['强卖出', '看跌区域'])),

            # 中等信号 - 传统信号
            (df['MA_Signal'] == '金叉') & (df['MACD_Signal_Analysis'] == '看涨'),
            (df['MA_Signal'] == '死叉') & (df['MACD_Signal_Analysis'] == '看跌'),
        ]
        choices = ['🔥超强看涨', '🔥超强看跌', '超强看涨', '超强看跌', '极强看涨', '极强看跌', '强烈看涨', '强烈看跌', '看涨', '看跌']
    else:
        # 原有的信号逻辑
        conditions = [
            # 极强信号 - 多个激进指标同时触发
            (df['MA_Signal'] == '金叉') & (df['MACD_Signal_Analysis'] == '看涨') &
            (df['RSI_Signal'].isin(['强买入', '看涨区域'])) &
            (df['BB_Signal'].isin(['强力突破上轨', '突破上轨', '强势上轨区域'])),

            (df['MA_Signal'] == '死叉') & (df['MACD_Signal_Analysis'] == '看跌') &
            (df['RSI_Signal'].isin(['强卖出', '看跌区域'])) &
            (df['BB_Signal'].isin(['强力突破下轨', '突破下轨', '弱势下轨区域'])),

            # 强信号 - 部分激进指标触发
            (df['MA_Signal'] == '金叉') & (df['MACD_Signal_Analysis'] == '看涨') &
            (df['RSI_Signal'].isin(['强买入', '看涨区域'])),

            (df['MA_Signal'] == '死叉') & (df['MACD_Signal_Analysis'] == '看跌') &
            (df['RSI_Signal'].isin(['强卖出', '看跌区域'])),

            # 中等信号 - 传统信号
            (df['MA_Signal'] == '金叉') & (df['MACD_Signal_Analysis'] == '看涨'),
            (df['MA_Signal'] == '死叉') & (df['MACD_Signal_Analysis'] == '看跌'),
        ]
        choices = ['极强看涨', '极强看跌', '强烈看涨', '强烈看跌', '看涨', '看跌']

    df['综合信号'] = np.select(conditions, choices, default='中性')

    return df


def save_indicators(df, file_path):
    """
    保存技术指标数据到CSV文件
    """
    # 确保目录存在
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # 保存数据，使用utf-8-sig编码支持Excel中文
    df.to_csv(file_path, encoding='utf-8-sig')

    # 打印文件信息
    print(f"💾 指标数据已保存: {file_path}")
    print(f"📊 包含 {len(df.columns)} 列技术指标和分析信号")


def get_latest_indicators_path():
    """获取最新的技术指标文件路径"""
    indicators_path = DATA_DIR / INDICATORS_FILENAME
    return indicators_path if indicators_path.exists() else None


if __name__ == "__main__":
    print("=" * 50)
    print("技术指标计算模块测试")
    print("=" * 50)

    try:
        # 执行指标计算
        result_path = calculate_indicators()

        if result_path:
            # 加载并预览结果
            df = pd.read_csv(result_path, encoding='utf-8-sig')
            print("\n技术指标数据预览:")
            # 显示最后5行的重要列
            preview_cols = ['开盘价', '收盘价', 'MA20', 'MA50', 'RSI', 'MACD', '综合信号']
            available_cols = [col for col in preview_cols if col in df.columns]
            print(df[available_cols].tail(5))

            # 显示信号分布
            if '综合信号' in df.columns:
                print("\n信号分布统计:")
                print(df['综合信号'].value_counts())
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback

        traceback.print_exc()