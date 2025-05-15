<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { stockNameMap } from '@/utils/stockMap'

const route = useRoute()
const router = useRouter()
const stockCode = route.params.code
const stockName = stockNameMap[stockCode] || '未知股票'
const comments = ref([])
const newComment = ref('')
const username = ref('')

// 模拟评论数据
const mockComments = [
  {
    id: 1,
    username: '投资达人',
    avatar: 'https://picsum.photos/40',
    content: '这支股票近期表现不错',
    time: '2024-01-20 14:30',
    likes: 12,
    replies: 3,
    isLiked: false
  },
  {
    id: 2,
    username: '股市分析师',
    avatar: 'https://picsum.photos/41',
    content: '建议关注主力资金动向',
    time: '2024-01-20 15:20',
    likes: 8,
    replies: 2,
    isLiked: false
  }
]

// 获取评论数据
const fetchComments = async () => {
  // 从localStorage获取评论数据
  const savedComments = localStorage.getItem(`comments_${stockCode}`)
  if (savedComments) {
    comments.value = JSON.parse(savedComments)
  } else {
    comments.value = mockComments
    localStorage.setItem(`comments_${stockCode}`, JSON.stringify(mockComments))
  }
}

// 更新讨论量
const updateDiscussionCount = () => {
  const savedDiscussions = localStorage.getItem('stockDiscussions')
  if (savedDiscussions) {
    const discussions = JSON.parse(savedDiscussions)
    const stockIndex = discussions.findIndex(item => item.code === stockCode)
    if (stockIndex !== -1) {
      discussions[stockIndex].discussionCount = comments.value.length
      localStorage.setItem('stockDiscussions', JSON.stringify(discussions))
    }
  }
}

// 检查登录状态
const checkLoginStatus = () => {
  const user = JSON.parse(localStorage.getItem('user'))
  if (!user || !user.username) {
    alert('请先登录')
    router.push('/login')
    return false
  }
  username.value = user.username
  return true
}

// 发布评论
const submitComment = async () => {
  if (!checkLoginStatus()) return
  if (!newComment.value.trim()) return
  
  const newCommentData = {
    id: Date.now(),
    username: username.value,
    avatar: 'https://picsum.photos/42',
    content: newComment.value,
    time: new Date().toLocaleString(),
    likes: 0,
    replies: 0,
    isLiked: false
  }
  
  comments.value.unshift(newCommentData)
  newComment.value = ''
  
  // 保存评论到localStorage
  localStorage.setItem(`comments_${stockCode}`, JSON.stringify(comments.value))
  // 更新讨论量
  updateDiscussionCount()
}

// 点赞功能
const handleLike = (comment) => {
  comment.isLiked = !comment.isLiked
  comment.likes += comment.isLiked ? 1 : -1
  
  // 保存更新后的评论数据到localStorage
  localStorage.setItem(`comments_${stockCode}`, JSON.stringify(comments.value))
}

onMounted(() => {
  checkLoginStatus()
  fetchComments()
})
</script>

<template>
  <div class="talk-container">
    <div class="header">
      <h2>{{ stockName }} ({{ stockCode }}) 讨论区</h2>
    </div>

    <div class="comment-list">
      <div v-if="comments.length" class="comments">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="user-info">
            <img :src="comment.avatar" class="avatar" alt="用户头像">
            <div class="comment-content">
              <div class="comment-header">
                <span class="username">{{ comment.username }}</span>
                <span class="time">{{ comment.time }}</span>
              </div>
              <div class="comment-text">{{ comment.content }}</div>
              <div class="comment-actions">
                <span class="action" @click="handleLike(comment)">
                  <i class="iconfont icon-dianzan" :class="{ 'is-liked': comment.isLiked }"></i>
                  {{ comment.likes }}
                </span>
                <span class="action">
                  <i class="iconfont icon-pinglun"></i>
                  {{ comment.replies }}
                </span>
              </div>
            </div>
          </div>
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

<style scoped lang="scss">
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

.user-info {
  display: flex;
  gap: 12px;
  
  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
}

.comment-content {
  flex: 1;
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

.comment-text {
  margin: 8px 0;
}

.comment-actions {
  display: flex;
  gap: 16px;
  color: #909399;
  font-size: 14px;

  .action {
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 4px;

    &:hover {
      color: #409eff;
    }

    .iconfont {
      font-size: 16px;
      line-height: 1;

      &.is-liked {
        color: #409eff;
        font-weight: bold;
      }
    }
  }
}

.empty-message {
  text-align: center;
  padding: 40px;
  color: #909399;
}

.comment-input {
  height: 80px;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 15px 20px;
  background-color: #fff;
  box-shadow: 0 -2px 12px 0 rgba(0,0,0,0.1);
  display: flex;
  gap: 10px;

  textarea {
    flex: 1;
    padding: 10px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    resize: none;
  }

  button {
    padding: 0 20px;
    background-color: #409eff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
      opacity: 0.8;
    }
  }
}
</style>