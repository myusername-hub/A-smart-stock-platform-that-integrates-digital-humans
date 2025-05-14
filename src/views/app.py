from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)

# 定义需要获取数据的股票代码列表
stock_codes = ["688111", "002230", "688777", "688375", "688169", "688120"]

# 修改为绝对路径
BASE_DIR = r"D:\my first contribute\stock\stock_daily_two_years"

# 添加API前缀
API_PREFIX = '/api'


def read_stock_data_from_csv(stock_code):
    """从CSV文件读取股票数据"""
    try:
        # 使用绝对路径构建文件路径
        file_path = os.path.join(BASE_DIR, f'{stock_code}.csv')

        # 检查文件是否存在
        if not os.path.exists(file_path):
            return None, f"找不到股票{stock_code}的数据文件"

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 确保日期列为datetime类型
        df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')

        # 按日期排序并获取最新的数据
        df = df.sort_values('trade_date', ascending=False)

        # 确保返回的数据中 ts_code 是字符串类型
        latest_data = df.iloc[0].to_dict()
        latest_data['ts_code'] = str(latest_data['ts_code'])
        latest_data['trade_date'] = latest_data['trade_date'].strftime('%Y%m%d')

        return latest_data, None

    except Exception as e:
        return None, f"读取股票{stock_code}数据时出错: {str(e)}"


def convert_to_period_data(df, period):
    """将日K数据转换为周K、月K、年K数据"""
    # 确保日期列为datetime类型
    df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
    
    # 设置日期索引
    df.set_index('trade_date', inplace=True)
    
    # 根据不同周期进行重采样
    if period == 'week':
        grouped = df.resample('W')
    elif period == 'month':
        grouped = df.resample('M')
    elif period == 'year':
        grouped = df.resample('Y')
    else:  # 默认日K
        return df.reset_index()
    
    # 聚合数据
    period_data = grouped.agg({
        'open': 'first',     # 开盘价取第一个
        'high': 'max',       # 最高价取最大值
        'low': 'min',        # 最低价取最小值
        'close': 'last',     # 收盘价取最后一个
        'vol': 'sum',        # 成交量求和
        'amount': 'sum'      # 成交额求和
    })
    
    return period_data.reset_index()


@app.route(f'{API_PREFIX}/stock_daily_data', methods=['GET'])
def get_stock_data():
    all_stock_data = []

    for code in stock_codes:
        data, error = read_stock_data_from_csv(code)
        if data:
            all_stock_data.append(data)
        else:
            all_stock_data.append({
                "ts_code": code,
                "message": error
            })

    return jsonify(all_stock_data)


@app.route(f'{API_PREFIX}/stock_kline_data/<stock_code>', methods=['GET'])
def get_stock_kline_data(stock_code):
    try:
        period = request.args.get('period', 'day')
        
        if not stock_code or len(stock_code) != 6:
            return jsonify({"error": "无效的股票代码格式"}), 400
            
        file_path = os.path.join(BASE_DIR, f'{stock_code}.csv')
        if not os.path.exists(file_path):
            return jsonify({"error": "股票数据文件不存在"}), 404
            
        df = pd.read_csv(file_path)
        df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
        
        # 按日期排序
        df = df.sort_values('trade_date', ascending=True)
        
        # 根据不同周期筛选数据
        if period == 'day':
            # 获取最近一天的所有数据
            latest_date = df['trade_date'].max()
            df = df[df['trade_date'] == latest_date]
        elif period == 'week':
            # 获取最近7天的数据
            latest_date = df['trade_date'].max()
            week_ago = latest_date - timedelta(days=7)
            df = df[df['trade_date'] >= week_ago]
        elif period == 'month':
            # 获取最近30天的数据
            latest_date = df['trade_date'].max()
            month_ago = latest_date - timedelta(days=30)
            df = df[df['trade_date'] >= month_ago]
        else:  # year
            # 获取最近365天的数据
            latest_date = df['trade_date'].max()
            year_ago = latest_date - timedelta(days=365)
            df = df[df['trade_date'] >= year_ago]
        
        # 转换日期格式
        df['trade_date'] = df['trade_date'].dt.strftime('%Y%m%d')
        data = df.to_dict('records')
        print(f"成功读取{period}K线数据，记录数: {len(data)}")
        return jsonify(data)
        
    except Exception as e:
        print(f"处理请求时发生错误: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    return "股票数据服务器正在运行"


if __name__ == '__main__':
    # 启动时打印一些调试信息
    print(f"数据目录: {BASE_DIR}")
    print(f"可用的股票文件:")
    if os.path.exists(BASE_DIR):
        files = os.listdir(BASE_DIR)
        for file in files:
            print(f"  - {file}")
    else:
        print("警告: 数据目录不存在!")

    app.run(debug=True, port=5000)