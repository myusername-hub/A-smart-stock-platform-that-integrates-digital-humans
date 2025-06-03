# 广财股票量化交易平台

## 项目结构说明

```
stock/
├── src/                    # 源代码目录
│   ├── assets/            # 静态资源
│   │   ├── theme.scss     # 全局主题样式
│   │   └── iconfont.css   # 图标字体文件
│   ├── components/        # 公共组件
│   ├── store/             # 状态管理
│   │   └── auth.js        # 用户认证状态管理
│   ├── views/             # 页面组件
│   │   ├── Home/          # 主页模块
│   │   │   ├── Home.vue   # 主页面组件
│   │   │   └── TheHeader.vue # 导航栏组件
│   │   ├── Login/         # 登录模块
│   │   │   └── index.vue  # 登录页面
│   │   ├── Register/      # 注册模块
│   │   │   └── index.vue  # 注册页面
│   │   └── Investigation/ # 风险评估问卷模块
│   │       └── index.vue  # 问卷页面
│   ├── App.vue            # 根组件
│   ├── main.js           # 入口文件
│   └── router.js         # 路由配置
├── back/                   # 后端服务目录
│   ├── app.py             # Flask 主应用
│   ├── stock_two_years/   # 股票历史数据
│   │   └── *.csv         # 股票数据文件
│   └── requirements.txt   # Python依赖
├── vite.config.js         # Vite 配置文件
├── package.json           # 项目依赖配置
├── .env                   # 环境变量配置
└── README.md             # 项目说明文档
```

## 主要功能模块

### 1. 用户认证模块
- `Login/index.vue`: 用户登录页面，支持动画效果
- `Register/index.vue`: 用户注册页面
- `store/auth.js`: 处理用户认证状态管理

### 2. 主页模块
- `Home/Home.vue`: 展示主要功能入口，包括实时行情、股票推荐等
- `Home/TheHeader.vue`: 全局导航栏，包含搜索功能和用户状态显示

### 3. 风险评估模块
- `Investigation/index.vue`: 用户风险承受能力评估问卷

### 4. 实时行情模块
- `Now/index.vue`: 展示所有股票的实时数据，包括涨跌幅、成交量等
- 支持分页和搜索功能
- 自动更新数据

### 5. 预测分析模块
- `Forecast/index.vue`: 股票走势预测与分析
- `Forecast/Infore.vue`: 股票预测排名
- 支持历史数据可视化
- 多维度技术分析

### 6. 讨论交流模块
- `Talk/index.vue`: 股票讨论区
- 支持实时评论和互动
- 分享投资见解

### 7. 数据服务
- `back/app.py`: 后端服务接口
- 提供实时行情数据
- 历史数据查询
- K线图数据支持

### 4. 其他功能模块
- 实时行情
- 股票推荐
- 股票走势预测
- 策略市场
- 回测功能
- 讨论区

## 主要配置文件

### 前端配置
- `vite.config.js`: Vite构建配置，包含代理设置和路径别名
- `package.json`: 项目依赖和脚本命令
- `.env`: 环境变量配置文件

### 后端配置
- `back/requirements.txt`: Python项目依赖
- `back/app.py`: Flask应用主程序，提供API服务
- `back/stock_two_years/`: 股票历史数据目录

## 项目启动步骤

1. 前端启动
```bash
# 安装依赖
npm install

# 开发环境启动
npm run dev

# 生产环境构建
npm run build
```

2. 后端启动
```bash
# 进入后端目录
cd back

# 安装Python依赖
pip install -r requirements.txt

# 启动Flask服务
python app.py
```

## 技术栈
- Vue 3
- Vite
- Vue Router
- Pinia 状态管理
- SCSS
- JWT 认证

## 项目功能特点

1. 实时数据
   - 支持多只股票同时监控
   - 自动更新行情数据
   - 精准的涨跌幅计算

2. 智能预测
   - 基于历史数据的趋势分析
   - 多周期K线图展示
   - 预测结果可视化

3. 交互体验
   - 响应式布局设计
   - 流畅的动画效果
   - 友好的错误提示

4. 数据可靠性
   - 实时数据验证
   - 异常处理机制
   - 自动重试机制

## 开发说明

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).
