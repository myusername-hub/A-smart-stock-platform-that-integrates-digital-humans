from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os
import subprocess
from functools import wraps
import time
from threading import Thread

app = Flask(__name__)
# 简化CORS配置
CORS(app)

# 定义需要获取数据的股票代码列表
stock_codes = ["688111", "002230", "688777", "688375", "688169", "688120"]

# 修改数据目录路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, 'back', 'stock_two_years')  # 正确的相对路径

def ensure_data_dir():
    """确保数据目录存在"""
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"确保数据目录存在: {DATA_DIR}")
    print(f"当前目录结构:")
    for root, dirs, files in os.walk(PROJECT_ROOT):
        level = root.replace(PROJECT_ROOT, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

def debug_dirs():
    """打印目录信息用于调试"""
    print("\n=== 目录信息 ===")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"数据目录: {DATA_DIR}")
    print(f"数据目录是否存在: {os.path.exists(DATA_DIR)}")
    if os.path.exists(DATA_DIR):
        print(f"数据文件列表: {os.listdir(DATA_DIR)}")
    print("===============\n")

def debug_route(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print(f"正在访问路由: {f.__name__}")
        try:
            result = f(*args, **kwargs)
            print(f"路由 {f.__name__} 处理成功")
            return result
        except Exception as e:
            print(f"路由 {f.__name__} 发生错误: {str(e)}")
            raise e
    return wrapper

def read_stock_data_from_csv(stock_code):
    """从CSV文件读取股票数据"""
    try:
        # 使用绝对路径
        file_path = os.path.join(DATA_DIR, f'{stock_code}.csv')
        print(f"读取文件路径: {file_path}")
        print(f"当前工作目录: {os.getcwd()}")
        
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return None, f"找不到股票{stock_code}的数据文件"
            
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 确保日期列为datetime类型
        df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
        
        # 按日期排序并获取最新的数据
        df = df.sort_values('trade_date', ascending=False)
        latest_data = df.iloc[0].to_dict()
        
        # 将日期转换回字符串格式
        latest_data['trade_date'] = latest_data['trade_date'].strftime('%Y%m%d')
        
        return latest_data, None
        
    except Exception as e:
        return None, f"读取股票{stock_code}数据时出错: {str(e)}"

def get_daily_stock_data(stock_code):
    """获取股票的每日数据"""
    try:
        # 使用绝对路径
        file_path = os.path.join(DATA_DIR, f'{stock_code}.csv')
        print(f"尝试读取文件: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            print(f"当前目录文件列表: {os.listdir(os.path.dirname(file_path))}")
            return None, f"找不到股票{stock_code}的数据文件"
        
        df = pd.read_csv(file_path)
        df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d').dt.strftime('%Y%m%d')
        df = df.sort_values('trade_date', ascending=True)
        return df.to_dict('records'), None
        
    except Exception as e:
        print(f"处理股票 {stock_code} 时发生错误: {str(e)}")
        return None, str(e)

def update_stock_data():
    """定期更新股票数据"""
    while True:
        try:
            print(f"开始更新股票数据: {datetime.now()}")
            # 这里添加更新CSV文件的逻辑
            # 例如：从数据源下载最新数据并保存到CSV
            
            # 更新完成后休息一段时间（例如1小时）
            time.sleep(3600)
        except Exception as e:
            print(f"更新数据时出错: {e}")
            time.sleep(60)  # 出错时等待1分钟后重试

def init_app():
    """初始化应用"""
    update_thread = Thread(target=update_stock_data, daemon=True)
    update_thread.start()

@app.route('/')
def index():
    """根路由 - 返回API文档"""
    return jsonify({
        "status": "success",
        "message": "欢迎使用股票数据API",
        "api_endpoints": {
            "/api/stock_data": "获取所有股票最新数据",
            "/api/daily_data/<stock_code>": "获取指定股票的历史数据",
            "/api/stock_daily_data": "获取所有股票的历史数据",
            "/api/health": "检查服务器健康状态",
            "/api/stock_kline_data/<stock_code>": "获取指定股票的K线数据"
        }
    })

@app.route('/api/stock_data', methods=['GET'])
@debug_route
def get_stock_data():
    try:
        result = {
            "status": "success",
            "data": [],
            "message": "数据获取成功"
        }

        for code in stock_codes:
            data, error = read_stock_data_from_csv(code)
            if data:
                stock_data = {
                    "code": code,
                    "latest_data": {
                        "ts_code": code,
                        **data  # 展开原始数据
                    }
                }
                print(f"处理股票数据: {stock_data}")
                result["data"].append(stock_data)
            else:
                result["data"].append({
                    "code": code,
                    "error": error
                })
        
        print(f"返回数据: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": []
        }), 500

@app.route('/api/daily_data/<stock_code>', methods=['GET'])
@debug_route
def daily_data(stock_code):
    try:
        data, error = get_daily_stock_data(stock_code)
        if data:
            return jsonify({
                "status": "success",
                "data": {
                    "code": stock_code,
                    "daily_data": data
                },
                "message": "数据获取成功"
            })
        else:
            return jsonify({
                "status": "error",
                "message": error,
                "data": None
            }), 404
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": None
        }), 500

@app.route('/api/stock_daily_data', methods=['GET'])
@debug_route
def get_all_daily_data():
    print("开始处理 /api/stock_daily_data 请求")
    try:
        result = {
            "status": "success",
            "data": [],
            "message": "数据获取成功"
        }
        
        for code in stock_codes:
            print(f"正在获取股票 {code} 的数据")
            data, error = get_daily_stock_data(code)
            if data:
                result["data"].append({
                    "code": code,
                    "daily_data": data
                })
            else:
                print(f"获取股票 {code} 数据失败: {error}")
                result["data"].append({
                    "code": code,
                    "error": error
                })
        
        print("成功获取所有股票数据")
        return jsonify(result)
    except Exception as e:
        print(f"处理请求时发生错误: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": []
        }), 500

def process_kline_data(df, period='day'):
    """处理不同周期的K线数据"""
    # 确保日期格式正确
    df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
    df = df.sort_values('trade_date', ascending=True)
    
    if period == 'day':
        # 日K线：返回最近一天的分时数据
        latest_date = df['trade_date'].max()
        return df[df['trade_date'] == latest_date]
    
    # 根据不同周期筛选数据
    now = pd.Timestamp.now()
    if period == 'week':
        # 周K线：最近7天的数据
        start_date = now - pd.Timedelta(days=7)
        df = df[df['trade_date'] >= start_date]
    elif period == 'month':
        # 月K线：最近30天的数据
        start_date = now - pd.Timedelta(days=30)
        df = df[df['trade_date'] >= start_date]
    elif period == 'year':
        # 年K线：最近365天的数据
        start_date = now - pd.Timedelta(days=365)
        df = df[df['trade_date'] >= start_date]
    
    # 将日期转回字符串格式
    df['trade_date'] = df['trade_date'].dt.strftime('%Y%m%d')
    return df

@app.route('/api/stock_kline_data/<stock_code>')
@debug_route
def get_kline_data(stock_code):
    try:
        period = request.args.get('period', 'year')  # 修改默认值为'year'
        file_path = os.path.join(DATA_DIR, f'{stock_code}.csv')
        
        if not os.path.exists(file_path):
            return jsonify({
                "status": "error",
                "message": f"找不到股票{stock_code}的数据"
            }), 404
            
        df = pd.read_csv(file_path)
        processed_data = process_kline_data(df, period)
        
        return jsonify({
            "status": "success",
            "data": processed_data.to_dict('records'),
            "period": period,
            "timeRange": {
                'day': '今日分时',
                'week': '最近7天',
                'month': '最近30天',
                'year': '最近365天'
            }.get(period, '未知周期'),
            "message": "获取K线数据成功"
        })
    except Exception as e:
        print(f"处理K线数据出错: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# 添加健康检查路由
@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "success",
        "message": "服务器运行正常"
    })

if __name__ == '__main__':
    import socket
    
    def check_port_available(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return True
            except:
                return False
    
    try:
        print(f"项目根目录: {PROJECT_ROOT}")
        print(f"数据目录: {DATA_DIR}")
        ensure_data_dir()  # 添加目录检查
        debug_dirs()  # 添加调试信息
        
        port = 5000
        if not check_port_available(port):
            print(f"错误：端口 {port} 已被占用")
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                for conn in proc.info['connections']:
                    if conn.laddr.port == port:
                        print(f"占用进程: {proc.info['name']} (PID: {proc.info['pid']})")
            exit(1)
        
        # 在启动服务器前初始化应用
        init_app()
        print("正在启动服务器...")
        app.run(
            host='localhost',
            port=port,
            debug=True,
            use_reloader=True
        )
    except Exception as e:
        print(f"服务器启动失败: {e}")
