<script>
import "../../assets/iconfont.css";
import { useRouter } from 'vue-router'

export default {
  setup() {
    const router = useRouter()
    
    const goToPage = (path) => {
      router.push(path)
    }
    
    return {
      goToPage
    }
  }
}
</script>
<template>
  <div class="all">
    <div class="header">
      <h2>欢迎来到股票量化交易系统</h2>
      <a href="#">开始</a>
    </div>
    <hr />
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
            <span class="body"
              >基于股评、新闻和股票基本面数据的股票推荐方法。</span
            >
            <a @click="goToPage('/recommend')">开始浏览 ></a>
          </div>
        </li>
        <li>
          <div class="forecast">
            <p class="title">
              <i class="iconfont icon-gupiao"></i>股票走势预测
            </p>
            <span class="body"
              >采用深度学习模型:引入注意力机制的双向LSTM模型对股票价格变化进行精准预测。</span
            >
            <a @click="goToPage('/forecast')">点击进入 ></a>
          </div>
        </li>
        <li>
          <div class="policy">
            <p class="title">
              <i class="iconfont icon-package_filled"></i>策略市场
            </p>
            <span class="body"
              >编写策略，策略的编写是为了确定具体的买卖规则和条件，以及在何时生成交易信号，从而实现自动化交易。</span
            >
            <a @click="goToPage('/policy')">寻找其它策略 ></a>
          </div>
        </li>
        <li>
          <div class="backtest">
            <p class="title"><i class="iconfont icon-huice"></i>回测</p>
            <span class="body"
              >回测是将编写好的交易策略应用于历史市场数据，模拟真实的交易环境，通过评估策略在过去的表现来判断其盈利能力和风险控制能力。</span
            >
            <a @click="goToPage('/backtest')">去回测 ></a>
          </div>
        </li>
        <li>
          <div class="talk">
            <p class="title">
              <i class="iconfont icon-leftfont-123"></i>讨论区
            </p>
            <span class="body"
              >和其他用户交流的开放平台，用户可以在论坛区域发帖留言和回帖交流，帮助用户交换信息、交流心得体会。</span
            >
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
  background-color: #f9f9f9;
  .header {
    text-align: center;
    background: url(../../image/background.jpg) no-repeat center center;
    background-size: cover;
    padding: 20px 0;
    h2 {
      font-size: 2.5rem;
      color: rgb(251, 251, 252);
      margin-bottom: 30px;
    }
    a {
      display: inline-block;
      padding: 10px 20px;
      background-color: #e74c3c; /* 设置为红色背景 */
      color: #fff;
      border-radius: 5px;
      text-decoration: none;
      font-size: 1.2rem;
      transition: background-color 0.3s ease;
      outline: none;
      &:hover {
        background-color: #c0392b; /* 悬停时的深红色 */
      }
    }
    hr {
      height: 2px;
      background-color: #333; /* 设置为浅灰色 */
    }
  }
  .body {
    position: relative;
    ul {
      flex-wrap: wrap;
      display: flex;
      li {
        width: 30%;
        height: 190px;
        display: flex;
        justify-content: space-between;
        flex-direction: row;
        margin: 20px;
        .now,
        .recommend,
        .forecast,
        .policy,
        .backtest,
        .talk {
          cursor: pointer;
          padding: 20px;
          border-radius: 5px;
          transition: transform 0.3s ease;
        }
        p.title {
          font-size: 1.2rem;
          font-weight: 500;
          color: #333;
          margin-bottom: 10px;
          i {
            margin-right: 10px; /* 图标和文字之间的间距 */
            font-size: 25px;
          }
        }
        span.body {
          display: block;
          height: 60px;
          font-size: 1rem;
          color: #666; /* 设置为深灰色 */
          margin-bottom: 10px; /* 添加底部间距 */
        }
        a {
          display: block;
          margin: 20px auto;
          width: 130px;
          height: 40px;
          text-align: center;
          padding: 10px 15px;
          background-color: #1b8eda; /* 设置为蓝色背景 */
          color: #fff;
          border-radius: 5px;
          text-decoration: none;
          font-size: 14px;
          transition: background-color 0.3s ease;
          &:hover {
            background-color: #0f6299; /* 悬停时的深蓝色 */
            transform: translateY(-5px);
          }
        }
      }
    }
    .ai {
      position: fixed;
      bottom: 20px;
      right: 20px;
      border-radius: 50%;
      background-color: #e4e4e9;
      transition: transform 0.3s ease;
      &:hover {
        transform: scale(1.2);
        color: #0f6299; /* 悬停时的深蓝色 */
      }
       a {
        font-size: 40px;
        padding: 10px 20px;
        display: inline-block;
      }
    }
  }
}
</style>