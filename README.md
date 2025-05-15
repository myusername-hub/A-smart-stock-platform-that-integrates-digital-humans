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
└── public/               # 公共资源目录
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

### 4. 其他功能模块
- 实时行情
- 股票推荐
- 股票走势预测
- 策略市场
- 回测功能
- 讨论区

## 技术栈
- Vue 3
- Vite
- Vue Router
- Pinia 状态管理
- SCSS
- JWT 认证

## 开发说明

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).
