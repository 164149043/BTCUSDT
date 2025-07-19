"""
币安数据抓取模块 - 官方推荐实现
功能：从币安API获取BTCUSDT日线K线数据，并进行数据清洗和保存
依赖：binance-futures-connector, pandas
参考：https://github.com/binance/binance-futures-connector-python
"""

import time
import pandas as pd
from binance.um_futures import UMFutures  # 官方推荐导入方式
from config import DATA_DIR, RAW_DATA_FILENAME, SYMBOL, INTERVAL, KLINE_LIMIT, BINANCE_API_KEY, BINANCE_API_SECRET, get_filenames

def get_binance_client():
    """
    创建并返回币安API客户端实例
    官方文档：https://binance-connector.github.io/python-binance/index.html
    """
    return UMFutures(
        key=BINANCE_API_KEY,
        secret=BINANCE_API_SECRET,
        base_url="https://fapi.binance.com"  # 期货API基础地址
    )

def fetch_historical_klines(client, symbol, interval):
    """
    获取最新的K线数据
    官方文档：https://binance-connector.github.io/python-binance/endpoints/market_data/get_klines.html
    """
    print(f"⏳ 开始获取 {symbol} 最新数据, 时间间隔: {interval}...")

    try:
        # 设置请求参数 - 获取最新数据
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': KLINE_LIMIT  # 直接从配置中获取限制数量
        }

        # 发送API请求 - 使用官方推荐调用方式
        response = client.klines(**params)

        # 如果没有数据，则返回空列表
        if not response:
            print("ℹ️ 没有获取到数据")
            return []

        print(f"✅ 数据获取完成, 共 {len(response)} 条记录")
        return response

    except Exception as e:
        print(f"⚠️ 请求失败: {e}")
        # 如果是API限制错误，等待更长时间
        if "API rate limit" in str(e):
            print("🚦 遇到API限制，等待60秒...")
            time.sleep(60)
            # 重试一次
            return client.klines(**params)
        else:
            time.sleep(1)  # 失败后等待1秒重试
            return []

def process_klines_data(klines):
    """
    处理原始K线数据并转换为DataFrame
    """
    # 定义列名 (根据币安API文档)
    columns = [
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_volume', 'trades',
        'taker_buy_base', 'taker_buy_quote', 'ignore'
    ]

    # 创建DataFrame
    df = pd.DataFrame(klines, columns=columns, dtype=float)

    # 转换时间戳为可读格式 (UTC时间)
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

    # 设置时间列为索引
    df.set_index('open_time', inplace=True)

    # 删除不必要的列
    df.drop(columns=['ignore', 'close_time'], inplace=True)

    # 重命名列（中文描述）
    df.rename(columns={
        'open': '开盘价',
        'high': '最高价',
        'low': '最低价',
        'close': '收盘价',
        'volume': '成交量',
        'quote_volume': '成交额',
        'trades': '成交笔数',
        'taker_buy_base': '主动买入量',
        'taker_buy_quote': '主动买入额'
    }, inplace=True)

    # 按时间升序排列
    df.sort_index(ascending=True, inplace=True)

    return df

def save_raw_data(df, file_path):
    """保存原始数据到CSV文件"""
    # 创建副本以避免修改原始数据
    df_copy = df.copy()

    # 重置索引，将时间索引转换为列
    df_copy.reset_index(inplace=True)

    # 将时间格式化为字符串（UTC时间）
    df_copy['open_time'] = df_copy['open_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    df_copy.to_csv(file_path, encoding='utf-8-sig', index=False)  # utf-8-sig 支持Excel中文
    print(f"💾 数据已保存至: {file_path}")

def fetch_and_save_btcusdt_data(interval=None, limit=None, timeframe_name=None):
    """
    主函数：获取并保存BTCUSDT K线数据
    参数:
        interval: K线间隔 (如 '15m', '1h', '4h', '1d')
        limit: 获取数据条数
        timeframe_name: 时间周期名称 (如 '15分钟线', '日线')
    """
    # 使用传入参数或默认值
    use_interval = interval or INTERVAL
    use_limit = limit or KLINE_LIMIT
    use_timeframe_name = timeframe_name or "日线"

    print(f"📊 获取 {use_timeframe_name} 数据 (间隔: {use_interval}, 数量: {use_limit})")

    # 创建API客户端
    client = get_binance_client()

    # 直接使用参数，不修改全局变量
    try:
        # 设置请求参数
        params = {
            'symbol': SYMBOL,
            'interval': use_interval,
            'limit': use_limit
        }

        # 发送API请求
        response = client.klines(**params)

        # 如果没有数据，则返回空列表
        if not response:
            print("ℹ️ 没有获取到数据")
            return None

        print(f"✅ 数据获取完成, 共 {len(response)} 条记录")

        # 处理数据
        df = process_klines_data(response)

        # 生成文件名
        if timeframe_name:
            filenames = get_filenames(use_timeframe_name)
            raw_data_path = DATA_DIR / filenames['raw']
        else:
            raw_data_path = DATA_DIR / RAW_DATA_FILENAME

        # 保存数据
        save_raw_data(df, raw_data_path)

        return raw_data_path
    except Exception as e:
        print(f"⚠️ 请求失败: {e}")
        return None

def fetch_and_save_btcusdt_daily():
    """
    向后兼容函数：获取并保存BTCUSDT日线数据
    """
    return fetch_and_save_btcusdt_data()

if __name__ == "__main__":
    # 测试运行
    print("="*50)
    print("BTCUSDT日线数据抓取测试")
    print("="*50)

    try:
        file_path = fetch_and_save_btcusdt_daily()
        print(f"\n测试成功! 文件保存位置: {file_path}")

        # 显示数据预览
        df = pd.read_csv(file_path)
        print("\n数据预览:")
        print(df[['开盘价', '最高价', '最低价', '收盘价', '成交量']].tail(5))

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        # 提供详细的错误诊断
        print("\n可能的原因及解决方案:")
        print("1. API密钥无效 - 检查 .env 文件中的 BINANCE_API_KEY 和 BINANCE_API_SECRET")
        print("2. 网络连接问题 - 确保可以访问 https://fapi.binance.com")
        print("3. 时间同步问题 - 确保系统时间准确（币安API要求时间误差在30秒内）")
        print("4. 包安装问题 - 尝试重新安装: pip install binance-futures-connector pandas python-dotenv")
        print("5. 防火墙阻止 - 暂时禁用防火墙或杀毒软件测试")