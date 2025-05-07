export const AI_CONFIG = {
  local: {
    baseUrl: window.__ENV__?.VUE_APP_LOCAL_API_URL || 'http://localhost:3000',
    scriptPath: '/js/iframe.js',
    chatPath: '/chat/share'
  },
  cloud: {
    baseUrl: window.__ENV__?.VUE_APP_CLOUD_API_URL || 'https://cloud.fastgpt.cn',
    scriptPath: '/js/iframe.js',
    chatPath: '/chat/share'
  },
  shareId: window.__ENV__?.VUE_APP_AI_SHARE_ID || 'v1jhpdkhdn3hvsuxreu5mn3b'
};
