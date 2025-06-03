(function() {
  // 获取父窗口URL
  const parentUrl = new URLSearchParams(window.location.search).get('parentUrl');
  
  // 通知父窗口准备完成
  window.parent.postMessage({
    type: 'CHAT_READY'
  }, parentUrl || '*');

  // 监听父窗口消息
  window.addEventListener('message', (event) => {
    if (event.data.type === 'INIT_CONFIG') {
      const { buttonConfig } = event.data.data;
      
      // 注入样式
      const style = document.createElement('style');
      style.textContent = `
        .markdown-body {
          position: relative !important;
        }
        .video-btn {
          ${Object.entries(buttonConfig.style).map(([key, value]) => `${key}: ${value} !important;`).join('\n')}
        }
        .video-btn:hover {
          background: #1976D2 !important;
        }
      `;
      document.head.appendChild(style);

      // 添加按钮到现有消息
      const addButton = (message) => {
        if (message.querySelector('.video-btn')) return;
        
        const stockCode = message.textContent.match(/([0-9]{6})/)?.[1];
        const btn = document.createElement('button');
        btn.className = 'video-btn';
        btn.innerHTML = `
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
            <path d="M8 5v14l11-7z"/>
          </svg>
          <span>${stockCode ? `播放${stockCode}分析` : '播放分析'}</span>
        `;
        
        btn.onclick = (e) => {
          e.stopPropagation();
          window.parent.postMessage({
            type: 'PLAY_VIDEO',
            stockCode
          }, parentUrl || '*');
        };
        
        message.appendChild(btn);
      };

      // 监听新消息
      const observer = new MutationObserver((mutations) => {
        mutations.forEach(mutation => {
          mutation.addedNodes.forEach(node => {
            if (node.classList?.contains('markdown-body')) {
              addButton(node);
            }
          });
        });
      });

      // 添加按钮到现有消息
      document.querySelectorAll('.markdown-body').forEach(addButton);

      // 开始监听新消息
      const container = document.querySelector('.answer-list, .chat-wrapper');
      if (container) {
        observer.observe(container, {
          childList: true,
          subtree: true
        });
      }
    }
  });
})();
