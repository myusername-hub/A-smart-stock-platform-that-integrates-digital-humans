<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import "../../assets/iconfont.css"

export default {
  setup() {
    const router = useRouter()
    const searchQuery = ref('')
    
    // 页面跳转
    const goToPage = (path) => {
      router.push(path)
    }
    
    // 搜索功能
    const handleSearch = () => {
      if (!searchQuery.value.trim()) {
        alert('请输入股票代码或名称')
        return
      }
      
      router.push({
        path: '/search',
        query: { q: searchQuery.value }
      })
    }

    // 搜索框回车事件处理
    const handleKeyPress = (event) => {
      if (event.key === 'Enter') {
        handleSearch()
      }
    }

    return {
      searchQuery,
      goToPage,
      handleSearch,
      handleKeyPress
    }
  }
}
</script>

<template>
  <div class="all">
    <div class="header">
      <div class="nav">
        <div class="search-box">
          <input type="text" placeholder="搜索股票..." class="search-input" />
          <button class="search-btn"><i class="iconfont icon-search"></i></button>
        </div>
        <div class="auth-links">
          <a @click="goToPage('/login')" class="auth-link">登录</a>
          <span class="divider">|</span>
          <a @click="goToPage('/register')" class="auth-link">注册</a>
        </div>
      </div>
      <div class="scroll-container">
        <div class="scroll-text">欢迎来到股票量化交易系统</div>
      </div>
    </div>
    <div class="body">
      <ul>
        <li>
          <div class="now">
            <p class="title"><i class="iconfont icon-shijian"></i>实时行情</p>
            <span class="body">行情数据实时更新，带来流畅的实时行情体验。</span>
            <a @click="goToPage('/now')">进入股票市场 ></a>
          </div>
        </li>
        <li>
          <div class="recommend">
            <p class="title">
              <i class="iconfont icon-weibiaoti1"></i>股票推荐
            </p>
            <span class="body">基于股评、新闻和股票基本面数据的股票推荐方法。</span>
            <a @click="goToPage('/recommend')">开始浏览 ></a>
          </div>
        </li>
        <li>
          <div class="forecast">
            <p class="title">
              <i class="iconfont icon-gupiao"></i>股票走势预测
            </p>
            <span class="body">采用深度学习模型:引入注意力机制的双向LSTM模型对股票价格变化进行精准预测。</span>
            <a @click="goToPage('/forecast')">点击进入 ></a>
          </div>
        </li>
        <li>
          <div class="policy">
            <p class="title">
              <i class="iconfont icon-package_filled"></i>策略市场
            </p>
            <span class="body">编写策略，策略的编写是为了确定具体的买卖规则和条件，以及在何时生成交易信号，从而实现自动化交易。</span>
            <a @click="goToPage('/policy')">寻找其它策略 ></a>
          </div>
        </li>
        <li>
          <div class="backtest">
            <p class="title"><i class="iconfont icon-huice"></i>回测</p>
            <span class="body">回测是将编写好的交易策略应用于历史市场数据，模拟真实的交易环境，通过评估策略在过去的表现来判断其盈利能力和风险控制能力。</span>
            <a @click="goToPage('/backtest')">去回测 ></a>
          </div>
        </li>
        <li>
          <div class="talk">
            <p class="title">
              <i class="iconfont icon-leftfont-123"></i>讨论区
            </p>
            <span class="body">和其他用户交流的开放平台，用户可以在论坛区域发帖留言和回帖交流，帮助用户交换信息、交流心得体会。</span>
            <a @click="goToPage('/talk')">点击进入 ></a>
          </div>
        </li>
      </ul>
      <div class="ai">
        <a @click="goToPage('/ai')" class="iconfont icon-robot-3-line"></a>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.all {
  background: linear-gradient(135deg, #1a1f35 0%, #2a3a5c 100%);
  min-height: 100vh;

  .header {
    background: linear-gradient(rgba(26, 31, 53, 0.8), rgba(42, 58, 92, 0.9)),
                url(../../image/background.jpg) no-repeat center center;
    background-size: cover;
    padding: 40px 0;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    margin-bottom: 30px;
    position: relative;
    overflow: hidden;

    .nav {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      padding: 20px 40px;
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      z-index: 10;
      
      .search-box {
        display: flex;
        align-items: center;
        margin-right: 30px;

        .search-input {
          width: 250px;
          height: 36px;
          padding: 0 15px;
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 8px;
          background: rgba(255, 255, 255, 0.1);
          color: #e6f1ff;
          font-size: 14px;
          transition: all 0.3s ease;
          margin-right: 20px;

          &::placeholder {
            color: rgba(230, 241, 255, 0.5);
          }

          &:focus {
            outline: none;
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
          }
        }

        .search-btn {
          margin-left: -40px;
          background: transparent;
          border: none;
          color: #e6f1ff;
          cursor: pointer;
          padding: 8px;
          transition: all 0.3s ease;

          &:hover {
            color: #64b3f4;
          }

          i {
            font-size: 18px;
          }
        }
      }

      .auth-links {
        display: flex;
        align-items: center;
        gap: 15px;

        .auth-link {
          color: #e6f1ff;
          text-decoration: none;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.3s ease;
          padding: 6px 0;
          border-radius: 6px;

          &:hover {
            color: #64b3f4;
          }
        }

        .divider {
          color: rgba(230, 241, 255, 0.3);
        }
      }
    }

    .scroll-container {
      width: 100%;
      height: 120px;
      overflow: hidden;
      white-space: nowrap;
      line-height: 120px;
      .scroll-text {
        text-align: center;
        display: inline-block;
        font-size: 2.8rem;
        color: #e6f1ff;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        animation: scrollText 15s linear infinite;
        padding-left: 100%;
      }

      @keyframes scrollText {
        0% {
          transform: translateX(100%);
        }
        100% {
          transform: translateX(-100%);
        }
      }
    }
  }

  .body {
    position: relative;
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 40px;

    ul {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      gap: 30px;
      padding: 20px 0;

      li {
        width: calc(33.33% - 20px);
        height: 260px;
        display: flex;

        .now,
        .recommend,
        .forecast,
        .policy,
        .backtest,
        .talk {
          cursor: pointer;
          padding: 25px;
          border-radius: 12px;
          background: linear-gradient(145deg, #202942, #2d3c5f);
          box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
          transition: all 0.3s ease;
          border: 1px solid rgba(255, 255, 255, 0.05);
          width: 100%;
          display: flex;
          flex-direction: column;

          &:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            background: linear-gradient(145deg, #2d3c5f, #202942);
          }

          p.title {
            height: 40px;
            font-size: 1.3rem;
            font-weight: 500;
            color: #e6f1ff;
            display: flex;
            align-items: center;
            margin-bottom: 15px;

            i {
              margin-right: 12px;
              font-size: 28px;
              background: linear-gradient(135deg, #64b3f4 0%, #c2e59c 100%);
              -webkit-background-clip: text;
              -webkit-text-fill-color: transparent;
            }
          }

          span.body {
            height: 100px;
            font-size: 1rem;
            color: #a8b2d1;
            line-height: 1.6;
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 4;
            -webkit-box-orient: vertical;
          }

          a {
            margin-top: auto;
            margin-left: auto;
            margin-right: auto;
            display: block;
            width: 140px;
            height: 40px;
            text-align: center;
            padding: 10px 15px;
            background: linear-gradient(135deg, #0a4d8c 0%, #1b6fa8 100%);
            color: #fff;
            border-radius: 8px;
            text-decoration: none;
            font-size: 14px;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);

            &:hover {
              background: linear-gradient(135deg, #1b6fa8 0%, #0a4d8c 100%);
              transform: translateY(-2px);
              box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            }
          }
        }
      }
    }

    .ai {
      position: fixed;
      bottom: 30px;
      right: 30px;
      border-radius: 50%;
      background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
      transition: all 0.3s ease;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.1);

      &:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        background: linear-gradient(135deg, #4e4376 0%, #2b5876 100%);
      }

      a {
        font-size: 40px;
        padding: 15px 25px;
        display: inline-block;
        color: #e6f1ff;
        cursor: pointer;
      }
    }
  }
}
</style>