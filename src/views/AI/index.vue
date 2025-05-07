<template>
  <div class="ai-container">
    <div v-show="showChat" 
         class="ai-chat-container"
         ref="chatContainer"
         :style="{ left: chatPosition.x + 'px', top: chatPosition.y + 'px' }">
      <div class="chat-header" @mousedown.stop="startDragChat">
        <h2>AI 助手</h2>
        <div class="ai-buttons">
          <!-- 添加本地视频按钮 -->
          <div class="ai-button" @click.stop="openLocalVideo">
            <el-icon><FolderOpened /></el-icon>
          </div>
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

      <!-- 视频播放容器 -->
      <div v-if="showVideo" class="video-container">
        <video 
          ref="videoPlayer"
          class="digital-human-video"
          :src="config.videoUrl"
          controls
          autoplay
        ></video>
        <div class="close-video" @click="closeVideo">
          <el-icon><Close /></el-icon>
        </div>
      </div>
    </div>

    <!-- 悬浮按钮 -->
    <div class="ai-float-button" 
         ref="floatButton"
         @mousedown.stop="startDragButton"
         :style="{ left: buttonPosition.x + 'px', top: buttonPosition.y + 'px' }">
      <el-icon class="chat-icon" @click.stop="toggleChat">
        <Comment />
      </el-icon>
    </div>

    <!-- 隐藏的文件输入框 -->
    <input 
      type="file" 
      ref="fileInput"
      accept="video/mp4"
      style="display: none"
      @change="handleFileSelect"
    >
  </div>
</template>

<script>
import { Comment, VideoCamera, Close, ChatLineRound, FolderOpened } from '@element-plus/icons-vue';
import { AI_CONFIG } from '@/config/ai.config';

export default {
  name: "AI",
  components: {
    Comment,
    ChatLineRound,
    VideoCamera,
    Close,
    FolderOpened
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
        videoUrl: '/src/assets/videos/digital-human.mp4',
        videoList: [] // 存储视频列表
      },
      chatPosition: {
        x: Math.min(window.innerWidth - 720, window.innerWidth - 720), // 考虑到容器宽度700px + padding
        y: Math.min(20, window.innerHeight - 520) // 考虑到容器高度500px + padding
      },
      buttonPosition: {
        x: window.innerWidth - 100,
        y: window.innerHeight - 100
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
  methods: {handleResize() {
      const chatContainer = this.$refs.chatContainer;
      const floatButton = this.$refs.floatButton;
      if (chatContainer) {
        // 修改resize时的边界检查
        const maxX = window.innerWidth - chatContainer.offsetWidth - 20; // 20px的安全边距
        const maxY = window.innerHeight - chatContainer.offsetHeight - 20;
        this.chatPosition.x = Math.min(Math.max(20, this.chatPosition.x), maxX);
        this.chatPosition.y = Math.min(Math.max(20, this.chatPosition.y), maxY);
      }
      // ... 其他代码保持不变 ...
    },
    handleIframeLoad() {
      console.log('AI 助手就绪');
    },
    openLocalVideo() {
      this.$refs.fileInput.click();
    },
    handleFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        const videoUrl = URL.createObjectURL(file);
        this.config.videoList.push({
          url: videoUrl,
          name: file.name
        });
        this.config.videoUrl = videoUrl;
        this.showVideo = true;
        if (!this.showChat) {
          this.showChat = true;
        }
      }
      // 清除input的值，允许重复选择同一个文件
      event.target.value = '';
    },
    closeVideo() {
      this.showVideo = false;
      if (this.$refs.videoPlayer) {
        this.$refs.videoPlayer.pause();
      }
    },
    toggleChat() {
      this.showChat = !this.showChat;
      if (!this.showChat) {
        this.closeVideo();
      }
    },
    toggleVideo() {
      this.showVideo = !this.showVideo;
      if (!this.showChat) {
        this.showChat = true;
      }
    },
    // ... 其他现有方法保持不变 ...
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
      const padding = 20;
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
  // ... 现有样式保持不变 ...
  .ai-chat-container {
    position: fixed;
    width: 700px;
    height: 500px;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    z-index: 800;

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
        max-height: 100%;
      }
      
      .close-video {
        position: absolute;
        top: 10px;
        right: 10px;
        padding: 5px;
        font-size: 20px;
        color: white;
        cursor: pointer;
        z-index: 1002;
        
        &:hover {
          color: #f56c6c;
        }
      }
    }
    .chat-frame, .local-chat, .cloud-chat {
      height: calc(100% - 60px);
      
      iframe {
        border: none;
        width: 100%;
        height: 100%;
      }

      // 添加以下样式来调整iframe内部的输入框高度
      :deep(.chat-input-container) {
        max-height: 100px !important; // 限制输入框最大高度
      }

      :deep(.chat-input-box) {
        max-height: 80px !important; // 限制实际输入区域最大高度
        overflow-y: auto !important; // 添加垂直滚动条
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
      color: #3a3ae6;
      cursor: pointer;
      width: 70%;
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