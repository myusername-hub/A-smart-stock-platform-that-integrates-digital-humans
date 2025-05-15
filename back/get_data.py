import os
import akshare as ak
import pandas as pd

# 定义股票代码列表
stock_codes = ["002230", "688111","688777", "688375", "688169", "688120"]
start_date = "20240401"
end_date = "20250514"

# 定义保存数据的文件夹
save_folder = "stock_daily_two_years"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

for code in stock_codes:
    try:
        # 获取股票历史数据
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date, end_date=end_date, adjust="")
        if not stock_zh_a_hist_df.empty:
            print(f"{code} 的实际列名：{stock_zh_a_hist_df.columns}")
            # 修正列名映射，使其与实际列数匹配
            columns = [
                "trade_date",    # 对应 日期
                "ts_code",       # 对应 股票代码
                "open",          # 对应 开盘
                "close",         # 对应 收盘
                "high",          # 对应 最高
                "low",           # 对应 最低
                "vol",           # 对应 成交量
                "amount",        # 对应 成交额
                "amplitude",     # 对应 振幅
                "pct_change",    # 对应 涨跌幅
                "change",        # 对应 涨跌额
                "exchange_rate"  # 对应 换手率
            ]
            if len(stock_zh_a_hist_df.columns) == len(columns):
                stock_zh_a_hist_df.columns = columns
            else:
                print(f"警告：{code} 列数仍不匹配，实际 {len(stock_zh_a_hist_df.columns)} vs 期望 {len(columns)}")
                continue
            # 转换日期格式
            stock_zh_a_hist_df["trade_date"] = pd.to_datetime(stock_zh_a_hist_df["trade_date"]).dt.strftime("%Y%m%d")
            # 调整列顺序
            expected_columns = [
                "ts_code",
                "trade_date",
                "open",
                "high",
                "low",
                "close",
                "change",
                "pct_change",
                "vol",
                "amount",
                "amplitude",
                "exchange_rate"
            ]
            stock_zh_a_hist_df = stock_zh_a_hist_df.reindex(columns=expected_columns)
            # 保存文件
            file_name = os.path.join(save_folder, f"{code}.csv")
            stock_zh_a_hist_df.to_csv(file_name, index=False)
            print(f"{code} 数据已保存至 {file_name}")
            print("当前工作目录：", os.getcwd())
        else:
            print(f"未获取到 {code} 的数据")
    except Exception as e:
        print(f"出错：{code} - {e}")