<template>
  <div class="backtest-container">
    <!-- 账户信息 -->
    <div class="account-info card">
      <h3 class="section-title">我的账户</h3>
      <div class="account-stats">
        <div class="stat-item">
          <p>总资产</p>
          <h2>0.00</h2>
        </div>
        <div class="stat-item">
          <p>可用资产（现金）</p>
          <h2>0.00</h2>
        </div>
        <div class="stat-item">
          <p>当前收益率</p>
          <h2 class="negative">0%</h2>
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
          <tr>
            <td colspan="7" class="empty-row">暂无持仓数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 交易操作 -->
    <div class="trade-operations card">
      <h3 class="section-title">交易操作</h3>
      <form class="trade-form">
        <div class="form-group">
          <label for="stock">股票</label>
          <input
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
              <input type="radio" name="action" value="buy" checked />
              买入
            </label>
            <label>
              <input type="radio" name="action" value="sell" />
              卖出
            </label>
          </div>
        </div>
        <div class="form-group">
          <label for="quantity">数量</label>
          <input type="number" id="quantity" placeholder="100" class="input" />
        </div>
        <button type="submit" class="btn btn-blue">提交</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Backtest",
};
</script>

<style scoped>
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
</style>