<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const stockCode = route.params.code
const comments = ref([])
const newComment = ref('')

// 获取评论数据
const fetchComments = async () => {
  // TODO: 从后端获取评论数据
  comments.value = []
}

// 发布评论
const submitComment = async () => {
  if (!newComment.value.trim()) return
  // TODO: 提交评论到后端
  newComment.value = ''
}

onMounted(() => {
  fetchComments()
})
</script>

<template>
  <div class="talk-container">
    <div class="header">
      <h2>{{ stockCode }} 讨论区</h2>
    </div>

    <div class="comment-list">
      <div v-if="comments.length" class="comments">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <span class="username">{{ comment.username }}</span>
            <span class="time">{{ comment.time }}</span>
          </div>
          <div class="comment-content">{{ comment.content }}</div>
        </div>
      </div>
      <div v-else class="empty-message">暂无评论</div>
    </div>

    <div class="comment-input">
      <textarea 
        v-model="newComment"
        placeholder="说说你的想法..."
        rows="3"
      ></textarea>
      <button @click="submitComment">发布</button>
    </div>
  </div>
</template>

<style scoped>
.talk-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.header {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.comment-list {
  margin-bottom: 100px;
}

.comment-item {
  padding: 15px;
  border-bottom: 1px solid #ebeef5;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.username {
  color: #409eff;
}

.time {
  color: #909399;
}

.comment-content {
  line-height: 1.5;
}

.empty-message {
  text-align: center;
  padding: 40px;
  color: #909399;
}

.comment-input {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 15px 20px;
  background-color: #fff;
  box-shadow: 0 -2px 12px 0 rgba(0,0,0,0.1);
  display: flex;
  gap: 10px;
}

.comment-input textarea {
  flex: 1;
  padding: 10px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  resize: none;
}

.comment-input button {
  padding: 0 20px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.comment-input button:hover {
  opacity: 0.8;
}
</style>