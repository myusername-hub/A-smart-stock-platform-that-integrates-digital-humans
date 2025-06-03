<template>
  <div class="backtest-container">
    <!-- 账户信息 -->
    <div class="account-info card">
      <h3 class="section-title">我的账户</h3>
      <div class="account-stats">
        <div class="stat-item">
          <p>总资产</p>
          <h2>{{ account.totalAssets.toFixed(2) }}</h2>
        </div>
        <div class="stat-item">
          <p>可用资产（现金）</p>
          <h2>{{ account.availableCash.toFixed(2) }}</h2>
        </div>
        <div class="stat-item">
          <p>当前收益率</p>
          <h2 :class="{ negative: account.profitRate < 0 }">{{ account.profitRate }}%</h2>
        </div>
      </div>
    </div>

    <!-- 当前持仓 -->
    <div class="current-holdings card">
      <h3 class="section-title">当前持仓</h3>
      <table class="holdings-table">
        <thead>
          <tr>
            <th>股票代码</th>
            <th>股票名称</th>
            <th>平均买入价格</th>
            <th>当前价格</th>
            <th>当前收益率</th>
            <th>持仓数量</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="holdings.length === 0">
            <td colspan="7" class="empty-row">暂无持仓数据</td>
          </tr>
          <tr v-for="holding in holdings" :key="holding.code">
            <td>{{ holding.code }}</td>
            <td>{{ holding.name }}</td>
            <td>{{ holding.avgPrice.toFixed(2) }}</td>
            <td>{{ holding.currentPrice.toFixed(2) }}</td>
            <td>{{ ((holding.currentPrice - holding.avgPrice) / holding.avgPrice * 100).toFixed(2) }}%</td>
            <td>{{ holding.quantity }}</td>
            <td>
              <button class="btn btn-red" @click="sellAll(holding.code)">清仓</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 交易操作 -->
    <div class="trade-operations card">
      <h3 class="section-title">交易操作</h3>
      <form class="trade-form" @submit="handleTrade">
        <div class="form-group">
          <label for="stock">股票</label>
          <input
            v-model="tradeForm.stockCode"
            type="text"
            id="stock"
            placeholder="股票代码/名称/首字母..."
            class="input"
          />
        </div>
        <div class="form-group">
          <label>操作</label>
          <div class="radio-group">
            <label>
              <input type="radio" v-model="tradeForm.action" value="buy" />
              买入
            </label>
            <label>
              <input type="radio" v-model="tradeForm.action" value="sell" />
              卖出
            </label>
          </div>
        </div>
        <div class="form-group">
          <label for="quantity">数量</label>
          <input
            v-model.number="tradeForm.quantity"
            type="number"
            id="quantity"
            placeholder="100"
            class="input"
          />
        </div>
        <button type="submit" class="btn" :class="tradeForm.action === 'buy' ? 'btn-blue' : 'btn-red'">
          {{ tradeForm.action === 'buy' ? '买入' : '卖出' }}
        </button>
      </form>
    </div>

    <!-- 添加图表分析区域 -->
    <div class="analysis-section">
      <div class="chart-row">
        <!-- 资产分布饼图 -->
        <div class="chart-card card">
          <h3 class="section-title">资产分布</h3>
          <div ref="pieChartRef" class="chart"></div>
        </div>
        
        <!-- 收益曲线图 -->
        <div class="chart-card card">
          <h3 class="section-title">收益走势</h3>
          <div ref="lineChartRef" class="chart"></div>
        </div>
      </div>
      
      <!-- 风险指标 -->
      <div class="risk-metrics card">
        <h3 class="section-title">风险指标</h3>
        <div class="metrics-grid">
          <div class="metric-item">
            <p>夏普比率</p>
            <h3>{{ riskMetrics.sharpeRatio.toFixed(2) }}</h3>
          </div>
          <div class="metric-item">
            <p>最大回撤</p>
            <h3>{{ riskMetrics.maxDrawdown.toFixed(2) }}%</h3>
          </div>
          <div class="metric-item">
            <p>波动率</p>
            <h3>{{ riskMetrics.volatility.toFixed(2) }}%</h3>
          </div>
          <div class="metric-item">
            <p>年化收益</p>
            <h3>{{ riskMetrics.annualReturn.toFixed(2) }}%</h3>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import { stockNameMap } from '@/utils/stockMap'; // 导入股票映射表
import * as echarts from "echarts";

export default {
  name: "Backtest",
  setup() {
    const account = ref({
      totalAssets: 1000000, // 初始资金100万
      availableCash: 1000000,
      profitRate: 0
    });
    
    const holdings = ref([]); // 当前持仓
    const tradeForm = ref({
      stockCode: '',
      action: 'buy',
      quantity: 100
    });

    const pieChartRef = ref(null);
    const lineChartRef = ref(null);
    const profitHistory = ref([]);
    const riskMetrics = ref({
      sharpeRatio: 0,
      maxDrawdown: 0,
      volatility: 0,
      annualReturn: 0
    });

    // 验证股票代码/名称
    const validateStock = (input) => {
      // 检查是否为股票代码
      if (stockNameMap[input]) {
        return {
          code: input,
          name: stockNameMap[input]
        };
      }
      
      // 检查是否为股票名称
      const stockCodes = Object.entries(stockNameMap).find(([code, name]) => name === input);
      if (stockCodes) {
        tradeForm.value.stockCode = stockCodes[0];
        return {
          code: stockCodes[0],
          name: stockCodes[1]
        };
      }
      
      return false;
    };

    // 初始化数据
    onMounted(() => {
      const savedAccount = localStorage.getItem('backtest_account');
      const savedHoldings = localStorage.getItem('backtest_holdings');
      
      if (savedAccount) {
        account.value = JSON.parse(savedAccount);
      }
      if (savedHoldings) {
        holdings.value = JSON.parse(savedHoldings);
      }

      // 初始化图表
      initPieChart();
      initLineChart();
      calculateRiskMetrics();
      
      // 监听窗口大小变化
      window.addEventListener('resize', () => {
        initPieChart();
        initLineChart();
      });
    });

    // 保存数据到本地存储
    const saveToStorage = () => {
      localStorage.setItem('backtest_account', JSON.stringify(account.value));
      localStorage.setItem('backtest_holdings', JSON.stringify(holdings.value));
    };

    // 初始化饼图
    const initPieChart = () => {
      if (!pieChartRef.value) return;
      const chart = echarts.init(pieChartRef.value);
      
      // 计算每个持仓的市值
      const holdingsValue = holdings.value.map(h => ({
        name: `${h.name}(${h.code})`,
        value: Math.round(h.quantity * h.currentPrice * 100) / 100  // 保留两位小数
      }));

      const data = [
        { 
          name: '现金', 
          value: Math.round(account.value.availableCash * 100) / 100 
        },
        ...holdingsValue
      ];

      const option = {
        grid: {
          left: '10%',
          right: '10%',
          top: '15%',
          bottom: '10%',
          containLabel: true
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} ({d}%)'
        },
        series: [{
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['50%', '55%'],  // 调整饼图中心位置
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            formatter: '{b}\n{d}%'
          },
          data: data
        }]
      };
      
      chart.setOption(option);
    };

    // 初始化折线图
    const initLineChart = () => {
      if (!lineChartRef.value) return;
      const chart = echarts.init(lineChartRef.value);
      
      // 如果没有历史数据，创建一条持平的线
      let dates, profits;
      if (profitHistory.value.length === 0) {
        const today = new Date();
        dates = Array.from({length: 7}, (_, i) => {
          const date = new Date(today);
          date.setDate(date.getDate() - (6 - i));
          return date.toISOString().split('T')[0];
        });
        profits = new Array(7).fill(0);  // 创建全为0的数组
      } else {
        dates = profitHistory.value.map(item => item.date);
        profits = profitHistory.value.map(item => item.profit);
      }

      const option = {
        grid: {
          left: '10%',      // 左边距
          right: '10%',     // 右边距
          top: '15%',       // 上边距
          bottom: '10%',    // 下边距
          containLabel: true // 确保刻度标签在区域内
        },
        tooltip: {
          trigger: 'axis',
          formatter: '{b}<br/>收益率: {c}%'
        },
        xAxis: {
          type: 'category',
          data: dates,
          boundaryGap: false  // 让折线图从起点开始
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: '{value}%'
          },
          splitLine: {
            show: true,
            lineStyle: {
              type: 'dashed'
            }
          }
        },
        series: [{
          name: '收益率',
          data: profits,
          type: 'line',
          smooth: true,
          symbol: 'circle',  // 数据点样式
          symbolSize: 6,     // 数据点大小
          itemStyle: {
            color: '#409EFF'  // 线条颜色
          },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [{
                offset: 0,
                color: 'rgba(64,158,255,0.2)'
              }, {
                offset: 1,
                color: 'rgba(64,158,255,0)'
              }]
            }
          }
        }]
      };
      
      chart.setOption(option);
    };

    // 计算风险指标
    const calculateRiskMetrics = () => {
      if (profitHistory.value.length < 2) return;
      
      const profits = profitHistory.value.map(item => item.profit);
      const returns = profits.map((p, i) => i > 0 ? p - profits[i-1] : 0);
      
      // 计算夏普比率
      const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length;
      const stdDev = Math.sqrt(returns.reduce((a, b) => a + Math.pow(b - avgReturn, 2), 0) / returns.length);
      riskMetrics.value.sharpeRatio = (avgReturn - 0.02) / stdDev; // 假设无风险利率为2%
      
      // 计算最大回撤
      let maxDrawdown = 0;
      let peak = profits[0];
      for (const profit of profits) {
        if (profit > peak) peak = profit;
        const drawdown = (peak - profit) / peak * 100;
        if (drawdown > maxDrawdown) maxDrawdown = drawdown;
      }
      riskMetrics.value.maxDrawdown = maxDrawdown;
      
      // 计算波动率
      riskMetrics.value.volatility = stdDev * Math.sqrt(252) * 100; // 年化波动率
      
      // 计算年化收益
      const totalReturn = profits[profits.length - 1];
      const days = profitHistory.value.length;
      riskMetrics.value.annualReturn = (Math.pow(1 + totalReturn/100, 365/days) - 1) * 100;
    };

    // 更新交易后的数据处理
    const updateAfterTrade = () => {
      // 更新收益历史
      const today = new Date().toISOString().split('T')[0];
      profitHistory.value.push({
        date: today,
        profit: account.value.profitRate
      });
      
      // 更新图表和指标
      initPieChart();
      initLineChart();
      calculateRiskMetrics();
      saveToStorage();
    };

    // 处理交易提交
    const handleTrade = (e) => {
      e.preventDefault();
      
      // 验证表单
      if (!tradeForm.value.stockCode || !tradeForm.value.quantity) {
        ElMessage.warning('请填写完整信息');
        return;
      }

      // 验证股票并获取股票信息
      const stockInfo = validateStock(tradeForm.value.stockCode);
      if (!stockInfo) {
        ElMessage.error('没有此股票名称/代码');
        return;
      }

      const mockPrice = 10; // 模拟当前价格，实际应该从行情数据获取
      const amount = mockPrice * tradeForm.value.quantity;

      if (tradeForm.value.action === 'buy') {
        // 检查资金是否足够
        if (amount > account.value.availableCash) {
          ElMessage.error('可用资金不足');
          return;
        }

        // 更新账户和持仓
        account.value.availableCash -= amount;
        
        const existingHolding = holdings.value.find(h => h.code === stockInfo.code);
        if (existingHolding) {
          existingHolding.quantity += tradeForm.value.quantity;
          existingHolding.avgPrice = (existingHolding.avgPrice + mockPrice) / 2;
        } else {
          holdings.value.push({
            code: stockInfo.code,
            name: stockInfo.name || '未知',
            quantity: tradeForm.value.quantity,
            avgPrice: mockPrice,
            currentPrice: mockPrice
          });
        }
      } else {
        // 卖出逻辑...
        const holding = holdings.value.find(h => h.code === stockInfo.code);
        if (!holding || holding.quantity < tradeForm.value.quantity) {
          ElMessage.error('持仓不足');
          return;
        }

        account.value.availableCash += amount;
        holding.quantity -= tradeForm.value.quantity;
        if (holding.quantity === 0) {
          holdings.value = holdings.value.filter(h => h.code !== stockInfo.code);
        }
      }

      // 更新总资产和收益率
      const totalHoldingsValue = holdings.value.reduce((sum, h) => sum + h.quantity * h.currentPrice, 0);
      account.value.totalAssets = account.value.availableCash + totalHoldingsValue;
      account.value.profitRate = ((account.value.totalAssets - 1000000) / 1000000 * 100).toFixed(2);

      // 保存到本地存储
      saveToStorage();
      
      ElMessage.success('交易成功');
      tradeForm.value.quantity = 100; // 重置表单

      updateAfterTrade();
    };

    const sellAll = (stockCode) => {
      const holding = holdings.value.find(h => h.code === stockCode);
      if (!holding) return;

      const amount = holding.currentPrice * holding.quantity;
      account.value.availableCash += amount;
      holdings.value = holdings.value.filter(h => h.code !== stockCode);

      // 更新总资产和收益率
      const totalHoldingsValue = holdings.value.reduce((sum, h) => sum + h.quantity * h.currentPrice, 0);
      account.value.totalAssets = account.value.availableCash + totalHoldingsValue;
      account.value.profitRate = ((account.value.totalAssets - 1000000) / 1000000 * 100).toFixed(2);

      saveToStorage();
      ElMessage.success('清仓成功');

      updateAfterTrade();
    };

    return {
      account,
      holdings,
      tradeForm,
      handleTrade,
      sellAll,
      validateStock,
      pieChartRef,
      lineChartRef,
      riskMetrics
    };
  }
};
</script>

<style scoped>
@use '@/assets/theme' as theme;
.backtest-container {
  padding: 20px;
  background: linear-gradient(135deg, #e8f5ff, #d4e9f9); /* 清新浅蓝渐变背景 */
  font-family: 'Segoe UI', Arial, sans-serif;
  color: #2c3e50; /* 深蓝文字 */
  min-height: 100vh;
}

.card {
  background: #ffffff; /* 白色卡片背景 */
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); /* 柔和的阴影 */
  padding: 20px;
  margin-bottom: 20px;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #2c3e50; /* 深蓝文字 */
  border-bottom: 2px solid #b3d4fc; /* 浅蓝分割线 */
  padding-bottom: 5px;
}

.account-stats {
  display: flex;
  justify-content: space-between;
  text-align: center;
}

.stat-item {
  flex: 1;
}

.stat-item p {
  font-size: 1rem;
  color: #7f8c8d; /* 灰色文字 */
}

.stat-item h2 {
  font-size: 1.8rem;
  margin: 5px 0;
  color: #2c3e50; /* 深蓝文字 */
}

.stat-item .negative {
  color: #e74c3c; /* 红色用于负收益 */
}

.holdings-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

.holdings-table th,
.holdings-table td {
  border: 1px solid #dceefb; /* 浅蓝边框 */
  padding: 10px;
  text-align: center;
  color: #2c3e50; /* 深蓝文字 */
}

.holdings-table th {
  background: #f4f9fd; /* 浅蓝表头背景 */
  font-weight: bold;
}

.holdings-table .empty-row {
  color: #7f8c8d; /* 灰色文字 */
}

.trade-form {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

.input {
  width: 100%;
  padding: 12px;
  border: 1px solid #dceefb; /* 浅蓝边框 */
  border-radius: 8px;
  background: #ffffff; /* 白色背景 */
  color: #2c3e50; /* 深蓝文字 */
  box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.05); /* 内阴影 */
}

.radio-group {
  display: flex;
  gap: 15px;
}

.radio-group label {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #2c3e50; /* 深蓝文字 */
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 50px; /* 圆角按钮 */
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-blue {
  background: linear-gradient(135deg, #66b3ff, #4da6ff); /* 清新蓝色渐变按钮 */
  color: white;
}

.btn-blue:hover {
  background: linear-gradient(135deg, #4da6ff, #3498db); /* 悬停时更深的渐变 */
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1); /* 悬停时阴影 */
}

.btn-red {
  background: linear-gradient(135deg, #ff6b6b, #ff4c4c); /* 清新红色渐变按钮 */
  color: white;
}

.btn-red:hover {
  background: linear-gradient(135deg, #ff4c4c, #e74c3c); /* 悬停时更深的渐变 */
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1); /* 悬停时阴影 */
}

.analysis-section {
  margin-top: 20px;
}

.chart-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  min-height: 400px;
}

.chart {
  width: 100%;
  height: 350px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  text-align: center;
}

.metric-item {
  background: #f8fafc;
  padding: 15px;
  border-radius: 8px;
}

.metric-item p {
  color: #64748b;
  margin-bottom: 8px;
}

.metric-item h3 {
  font-size: 1.5rem;
  color: #334155;
}
</style>