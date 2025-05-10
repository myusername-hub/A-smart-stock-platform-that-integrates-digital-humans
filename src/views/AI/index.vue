<template>
  <div class="ai-container">
    <div v-show="showChat" 
         class="ai-chat-container"
         ref="chatContainer"
         :style="{ left: chatPosition.x + 'px', top: chatPosition.y + 'px' }">
      <div class="chat-header" @mousedown.stop="startDragChat">
        <div class="header-left">
          <h2>AI 助手</h2>
        </div>
        <div class="header-right">
          <div class="ai-buttons">
            <div class="ai-button" @click.stop="openLocalVideo">
              <el-icon><FolderOpened /></el-icon>
            </div>
            <div class="ai-button" @click.stop="toggleVideo">
              <el-icon><VideoCamera /></el-icon>
            </div>
            <div class="ai-button" @click.stop="toggleChat">
              <el-icon class="chat-icon"><ChatLineRound /></el-icon>
            </div>
            <div class="ai-button" @click.stop="playVideo">
              <el-icon><VideoCamera /></el-icon>
            </div>
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
        <div class="video-wrapper">
          <video 
            ref="videoPlayer"
            class="digital-human-video"
            :src="config.videoUrl"
            controls
            autoplay
          ></video>
          <button class="close-btn" @click="closeVideo">
            <el-icon :size="24" class="close-icon">
              <Close />
            </el-icon>
          </button>
        </div>
      </div>
    </div>

    <!-- 悬浮视频按钮 -->
    <div class="floating-video-btn" @click="openLocalVideo">
      <el-icon><VideoCamera /></el-icon>
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
import Video1 from '@/assets/videos/video1.mp4';
import Video2 from '@/assets/videos/video2.mp4';

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
      clickCount: 0,
      config: {
        useCloud: true,
        iframeId: 'chatbot-iframe',
        shareId: AI_CONFIG.shareId,
        localUrl: AI_CONFIG.local.baseUrl,
        cloudUrl: AI_CONFIG.cloud.baseUrl,
        videoUrl: '',
        defaultVideos: [
          Video1,  // 使用导入的模块路径
          Video2
        ],
        videoList: []
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
    window.addEventListener('message', (event) => {
      if (event.data.type === 'playVideo') {
        this.showVideo = true;
      }
    });
    
    // 添加样式注入
    this.$nextTick(() => {
      this.injectStyles();
    });
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
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
    playVideo() {
      // 根据点击次数设置视频源
      this.config.videoUrl = this.config.defaultVideos[this.clickCount % this.config.defaultVideos.length];
      console.log(`播放视频 ${this.clickCount + 1}:`, this.config.videoUrl);

      // 自动播放视频
      this.showVideo = true;
      if (!this.showChat) {
        this.showChat = true;
      }

      // 切换到下一个视频索引
      this.clickCount++;
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
        // 修改resize时的边界检查
        const maxX = window.innerWidth - chatContainer.offsetWidth - 20; // 20px的安全边距
        const maxY = window.innerHeight - chatContainer.offsetHeight - 20;
        this.chatPosition.x = Math.min(Math.max(20, this.chatPosition.x), maxX);
        this.chatPosition.y = Math.min(Math.max(20, this.chatPosition.y), maxY);
      }
      if (floatButton) {
        this.buttonPosition.x = Math.min(this.buttonPosition.x, window.innerWidth - floatButton.offsetWidth);
        this.buttonPosition.y = Math.min(this.buttonPosition.y, window.innerHeight - floatButton.offsetHeight);
      }
    },
    injectVideoButton() {
      const iframe = document.querySelector('iframe');
      if (!iframe || !iframe.contentWindow || !iframe.contentWindow.document) {
        console.log('无法访问iframe内容');
        return;
      }
      
      const doc = iframe.contentWindow.document;
      const messages = doc.querySelectorAll('.answer-content');
      
      messages.forEach(message => {
        if (!message.querySelector('.video-btn')) {
          const btn = doc.createElement('button');
          btn.className = 'video-btn';
          // 修改这里：使用 SVG 图标替换文本
          btn.innerHTML = `<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path d="M21 6h-7.59l3.29-3.29L16 2l-4 4-4-4-.71.71L10.59 6H3c-1.1 0-2 .89-2 2v12c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.11-.9-2-2-2zm0 14H3V8h18v12zM9 10v8l7-4z"/>
          </svg>`;
          btn.style.cssText = `
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            padding: 8px;
            border: none;
            border-radius: 50%;
            background: #4e83fd;
            color: white;
            cursor: pointer;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            opacity: 1;
          `;
          
          message.style.position = 'relative';
          message.appendChild(btn);
          
          btn.addEventListener('click', () => {
            this.toggleVideo();
          });
        }
      });

      const observer = new MutationObserver(() => {
        console.log('检测到新消息');
        this.injectVideoButton();
      });

      const chatWrapper = doc.querySelector('.answer-list') || doc.querySelector('.chat-wrapper');
      if (chatWrapper) {
        observer.observe(chatWrapper, { 
          childList: true, 
          subtree: true 
        });
        console.log('开始监听聊天容器');
      }
    },

    injectStyles() {
      const iframe = document.querySelector('iframe');
      if (!iframe || !iframe.contentWindow || !iframe.contentWindow.document) {
        setTimeout(() => this.injectStyles(), 1000);
        return;
      }
      
      const doc = iframe.contentWindow.document;
      const style = doc.createElement('style');
      style.textContent = `
        body, .chat-wrapper, .answer-wrapper, .question-wrapper {
          background-color: #2a3a5c !important;
          color: #fff !important;
        }
        .chat-item, .answer-content, .question-content {
          background-color: #2a3a5c !important;
          color: #fff !important;
        }
        .chat-input-wrapper {
          background-color: #2a3a5c !important;
        }
      `;
      doc.head.appendChild(style);
    },

    handleIframeLoad() {
      console.log('iframe加载完成');
      setTimeout(() => {
        this.injectVideoButton();
        this.injectStyles();
        console.log('执行按钮和样式注入');
      }, 2000);
    }
  }
};
</script>

<style scoped lang="scss">
@use '@/assets/theme' as theme;

.ai-container {
  background-color: #2a3a5c;
  .ai-chat-container {
    position: fixed;
    width: 700px;
    height: 500px;
    background-color: #2a3a5c; // 修改背景色为 #2a3a5c
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

      .header-left {
        display: flex;
        align-items: center;

        h2 {
          margin: 0;
          color: rgb(57, 53, 53);
        }
      }

      .header-right {
        display: flex;
        align-items: center;
        gap: 10px;

        .video-btn {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.2);
          color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          z-index: 1000;
          transition: background 0.3s;

          &:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: scale(1.1);
          }

          el-icon {
            font-size: 20px;
          }
        }
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
          z-index: 1000;

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
      
      .video-wrapper {
        position: relative;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      
      .digital-human-video {
        width: 100%;
        height: auto;
        max-height: 100%;
      }
      
      .close-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1002;
        transition: all 0.3s;
        padding: 0;

        .close-icon {
          width: 24px;
          height: 24px;
        }
        
        &:hover {
          background: rgba(255, 255, 255, 0.3);
          transform: scale(1.1);
          .close-icon {
            color: #f56c6c;
          }
        }
      }
    }

    .chat-frame, .local-chat, .cloud-chat {
      height: calc(100% - 60px);
      background-color: #2a3a5c !important;
      
      iframe {
        border: none;
        width: 100%;
        height: 100%;
        background-color: transparent;
      }

      :deep(.chat-input-container),
      :deep(.chat-wrapper),
      :deep(.answer-wrapper),
      :deep(.question-wrapper) {
        background-color: #2a3a5c !important;
        color: #fff !important;
      }

      :deep(.chat-input-box) {
        max-height: 80px !important;
        overflow-y: auto !important;
      }

      :deep(.video-btn) {
        opacity: 1;
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        padding: 8px;
        border: none;
        border-radius: 50%;
        background: #4e83fd;
        color: white;
        cursor: pointer;
        font-size: 16px;
        z-index: 9999;
        transition: opacity 0.3s;

        &:hover {
          background: #3a6cd8 !important;
        }
      }

      :deep(.markdown-body:hover .video-btn) {
        opacity: 1;
      }
    }

    :deep(.markdown-body) {
      background-color: #2a3a5c !important;
      color: #fff !important;
    }

    :deep(.chat-wrapper) {
      background-color: #2a3a5c !important;
    }
  }

  .floating-video-btn {
    position: fixed;
    bottom: 100px;
    right: 20px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: theme.$primary-gradient;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    z-index: 1001;
    transition: transform 0.3s, background 0.3s;

    &:hover {
      transform: scale(1.1);
      background: #3a6cd8; // 替换 theme.$primary-hover 为具体颜色值
    }

    el-icon {
      font-size: 24px;
    }
  }

  .video-btn-container {
    display: flex;
    justify-content: center;
    margin: 5px 0; // 向上移动按钮
    position: relative;
    top: -10px;

    .video-btn {
      padding: 8px 16px;
      border: none;
      border-radius: 4px;
      background: #4e83fd;
      color: white;
      cursor: pointer;
      font-size: 14px;
      transition: background 0.3s;

      &:hover {
        background: #3a6cd8;
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