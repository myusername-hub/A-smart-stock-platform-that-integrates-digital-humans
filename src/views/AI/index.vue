<template>
  <div class="ai-container">
    <div v-show="showChat" 
         class="ai-chat-container"
         ref="chatContainer"
         :style="{ left: chatPosition.x + 'px', top: chatPosition.y + 'px' }">
      <div class="chat-header" @mousedown.stop="startDragChat">
        <h2>AI 助手</h2>
        <div class="ai-buttons">
          <div class="ai-button" @click.stop="toggleVideo">
            <el-icon><VideoCamera /></el-icon>
          </div>
          <div class="ai-button" @click.stop="toggleChat">
            <el-icon class="chat-icon"><ChatLineRound /></el-icon>
          </div>
        </div>
      </div>
      <!-- 本地开发环境聊天框 -->
      <div v-if="!config.useCloud" class="local-chat">
        <iframe
          :src="`${config.localUrl}/chat/share?shareId=${config.shareId}`"
          :id="config.iframeId"
          frameborder="0"
          width="100%"
          height="100%"
          @load="handleIframeLoad"
        ></iframe>
      </div>
      <!-- 云环境聊天框 -->
      <div v-else class="cloud-chat">
        <iframe
          :src="`${config.cloudUrl}/chat/share?shareId=${config.shareId}`"
          :id="config.iframeId"
          frameborder="0"
          width="100%"
          height="100%"
          @load="handleIframeLoad"
        ></iframe>
      </div>
    </div>
    <!-- 修改后的浮动按钮部分 -->
    <div class="ai-float-button" 
         ref="floatButton"
         @mousedown.stop="startDragButton"
         :style="{ left: buttonPosition.x + 'px', top: buttonPosition.y + 'px' }">
      <el-icon class="chat-icon" @click.stop="toggleChat">
        <Comment />
      </el-icon>
    </div>
  </div>
</template>

<script>
import { Comment, VideoCamera, Close, ChatLineRound } from '@element-plus/icons-vue';
import { AI_CONFIG } from '@/config/ai.config';

export default {
  name: "AI",
  components: {
    Comment,
    ChatLineRound,
    VideoCamera,
    Close
  },
  data() {
    return {
      showChat: false,
      showVideo: false,
      config: {
        useCloud: true,
        iframeId: 'chatbot-iframe',
        shareId: AI_CONFIG.shareId,
        localUrl: AI_CONFIG.local.baseUrl,
        cloudUrl: AI_CONFIG.cloud.baseUrl,
        videoUrl: '/src/assets/videos/digital-human.mp4'
      },
      chatPosition: {
        x: window.innerWidth - 420,
        y: 20
      },
      buttonPosition: {
        x: window.innerWidth - 100, // 距离右边界增加到100px
        y: window.innerHeight - 100 // 距离下边界增加到100px
      },
      isDragging: false,
      dragTarget: null,
      dragOffset: { x: 0, y: 0 }
    }
  },
  mounted() {
    window.addEventListener('resize', this.handleResize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleIframeLoad() {
      console.log('AI 助手就绪');
    },
    toggleChat() {
      this.showChat = !this.showChat;
    },
    toggleVideo() {
      this.showVideo = !this.showVideo;
      if (!this.showChat) {
        this.showChat = true;
      }
    },
    startDragChat(event) {
      if (event.target.closest('.ai-button')) return;
      event.preventDefault();
      this.startDrag(event, 'chat');
    },
    startDragButton(event) {
      if (event.target.closest('.chat-icon')) return;
      event.preventDefault();
      this.startDrag(event, 'button');
    },
    startDrag(event, type) {
      this.isDragging = true;
      this.dragTarget = type;
      
      const target = type === 'chat' ? this.chatPosition : this.buttonPosition;
      this.dragOffset = {
        x: event.clientX - target.x,
        y: event.clientY - target.y
      };
      
      document.addEventListener('mousemove', this.onDrag);
      document.addEventListener('mouseup', this.stopDrag);
    },
    onDrag(event) {
      if (!this.isDragging) return;
      
      const target = this.dragTarget === 'chat' ? this.chatPosition : this.buttonPosition;
      const element = this.dragTarget === 'chat' ? this.$refs.chatContainer : this.$refs.floatButton;
      
      if (!element) return;
      
      let newX = event.clientX - this.dragOffset.x;
      let newY = event.clientY - this.dragOffset.y;
      
      // 增加边界间距
      const padding = 20; // 设置20px的边界间距
      const maxX = window.innerWidth - element.offsetWidth - padding;
      const maxY = window.innerHeight - element.offsetHeight - padding;
      
      newX = Math.min(Math.max(padding, newX), maxX);
      newY = Math.min(Math.max(padding, newY), maxY);
      
      target.x = newX;
      target.y = newY;
    },
    stopDrag() {
      setTimeout(() => {
        this.isDragging = false;
      }, 0);
      document.removeEventListener('mousemove', this.onDrag);
      document.removeEventListener('mouseup', this.stopDrag);
    },
    handleResize() {
      const chatContainer = this.$refs.chatContainer;
      const floatButton = this.$refs.floatButton;
      
      if (chatContainer) {
        this.chatPosition.x = Math.min(this.chatPosition.x, window.innerWidth - chatContainer.offsetWidth);
        this.chatPosition.y = Math.min(this.chatPosition.y, window.innerHeight - chatContainer.offsetHeight);
      }
      
      if (floatButton) {
        this.buttonPosition.x = Math.min(this.buttonPosition.x, window.innerWidth - floatButton.offsetWidth);
        this.buttonPosition.y = Math.min(this.buttonPosition.y, window.innerHeight - floatButton.offsetHeight);
      }
    }
  }
};
</script>

<style scoped lang="scss">
@use '@/assets/theme' as theme;

.ai-container {
  .ai-chat-container {
    position: fixed;
    width: 400px;
    height: 500px;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    z-index: 1000;

    .chat-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 15px;
      background: theme.$primary-gradient;
      cursor: move;
      user-select: none;

      h2 {
        margin: 0;
        color: rgb(57, 53, 53);
      }

      .ai-buttons {
        display: flex;
        gap: 8px;

        .ai-button {
          width: 32px;
          height: 32px;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.2);
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;

          &:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.05);
            transition: all 0.2s;
          }
        }
      }
    }

    .local-chat,
    .cloud-chat {
      height: calc(100% - 50px);
    }

    .video-container {
      position: absolute;
      left: 0;
      top: 0;
      width: 50%;
      height: 100%;
      background: rgba(0, 0, 0, 0.8);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1001;
      
      .digital-human-video {
        width: 100%;
        height: auto;
      }
      
      .close-video {
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 20px;
        color: white;
        cursor: pointer;
        
        &:hover {
          color: #f56c6c;
        }
      }
    }
  }

  .ai-float-button {
    position: fixed;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: theme.$primary-gradient;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: move;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    z-index: 1000;
    user-select: none;
    
    .chat-icon {
      font-size: 10px;
      color:#3a3ae6;
      cursor: pointer;;
      width: 70%;;
      height: 70%;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    &:hover {
      transform: scale(1.1);
      transition: all 0.3s ease;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }
  }
}
</style>