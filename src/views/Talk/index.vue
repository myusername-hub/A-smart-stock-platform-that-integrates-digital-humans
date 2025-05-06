<template>
  <div class="discussion-container">
    <!-- 讨论区标题 -->
    <div class="discussion-header">
      <h2 class="discussion-title">
        <i class="iconfont icon-discuss"></i> 讨论区
      </h2>
    </div>

    <!-- 讨论内容 -->
    <div class="discussion-content card">
      <div class="discussion-item">
        <p class="discussion-text">这支股票不错</p>
        <p class="discussion-meta">
          由 <span class="author">am</span> 发表于 2024/03/16 20:36:13 | 最后回复 2024/03/16 20:36:13
        </p>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination">
      <button class="btn btn-blue">1</button>
      <button class="btn btn-blue">»</button>
    </div>

    <!-- 发表新主题 -->
    <div class="new-topic card">
      <h3 class="section-title">+ 发表新主题</h3>
      <form class="new-topic-form">
        <div class="form-group">
          <input
            type="text"
            placeholder="请输入标题"
            class="input"
          />
        </div>
        <div class="form-group">
          <textarea
            placeholder="请输入内容"
            rows="5"
            class="textarea"
          ></textarea>
        </div>
        <div class="form-group">
          <input
            type="text"
            placeholder="相关股票（可选）"
            class="input"
          />
        </div>
        <button type="submit" class="btn btn-green">发表主题</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Discussion",
};
</script>

<style scoped>
@use '@/assets/theme' as theme;
.discussion-container {
  padding: 20px;
  background: #f9f9f9;
  font-family: 'Segoe UI', Arial, sans-serif;
  color: #2c3e50;
  min-height: 100vh;
}

.card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.discussion-header {
  margin-bottom: 20px;
}

.discussion-title {
  font-size: 1.8rem;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 10px;
}

.discussion-content {
  padding: 15px;
}

.discussion-item {
  margin-bottom: 15px;
}

.discussion-text {
  font-size: 1.2rem;
  color: #2c3e50;
  margin-bottom: 5px;
}

.discussion-meta {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.author {
  font-weight: bold;
  color: #3498db;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.new-topic {
  padding: 20px;
}

.section-title {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #2c3e50;
  border-bottom: 2px solid #b3d4fc;
  padding-bottom: 5px;
}

.new-topic-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.input,
.textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #dceefb;
  border-radius: 8px;
  background: #ffffff;
  color: #2c3e50;
  box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.05);
}

.textarea {
  resize: none;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-blue {
  background: linear-gradient(135deg, #66b3ff, #4da6ff);
  color: white;
}

.btn-blue:hover {
  background: linear-gradient(135deg, #4da6ff, #3498db);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.btn-green {
  background: linear-gradient(135deg, #28a745, #218838);
  color: white;
}

.btn-green:hover {
  background: linear-gradient(135deg, #218838, #1e7e34);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}
</style>