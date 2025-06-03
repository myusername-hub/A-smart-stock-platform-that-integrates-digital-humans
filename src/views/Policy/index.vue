<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElDialog } from 'element-plus'

const strategy = ref({
  description: '',
  parameters: [{ name: '', defaultValue: '', description: '' }],
  code: ''
})

const historyVisible = ref(false)
const historyStrategies = ref([])

// 保存策略
const saveStrategy = (isPublic = false) => {
  const savedStrategy = {
    ...strategy.value,
    id: Date.now(), // 添加唯一id
    isPublic,
    createTime: new Date().toISOString(),
    lastModified: new Date().toISOString()
  }
  
  // 获取已有策略列表
  const savedStrategies = JSON.parse(localStorage.getItem('strategies') || '[]')
  savedStrategies.push(savedStrategy)
  localStorage.setItem('strategies', JSON.stringify(savedStrategies))
  
  ElMessage({
    message: '策略保存成功！',
    type: 'success',
    duration: 2000
  })
}

// 添加参数
const addParameter = () => {
  strategy.value.parameters.push({ name: '', defaultValue: '', description: '' })
}

// 删除参数
const removeParameter = (index) => {
  strategy.value.parameters.splice(index, 1)
}

// 加载已保存的策略
onMounted(() => {
  const savedStrategies = JSON.parse(localStorage.getItem('strategies') || '[]')
  if (savedStrategies.length > 0) {
    const lastStrategy = savedStrategies[savedStrategies.length - 1]
    strategy.value = {
      description: lastStrategy.description || '',
      parameters: lastStrategy.parameters || [],
      code: lastStrategy.code || ''
    }
  }
})

// 加载历史策略
const loadHistoryStrategies = () => {
  historyStrategies.value = JSON.parse(localStorage.getItem('strategies') || '[]')
  historyVisible.value = true
}

// 使用历史策略
const useHistoryStrategy = (historicalStrategy) => {
  strategy.value = {
    description: historicalStrategy.description,
    parameters: historicalStrategy.parameters,
    code: historicalStrategy.code
  }
  historyVisible.value = false
  ElMessage({
    message: '策略加载成功！',
    type: 'success'
  })
}

// 删除历史策略
const deleteStrategy = (e, strategy) => {
  e.stopPropagation() // 阻止冒泡,避免触发选择策略
  const savedStrategies = JSON.parse(localStorage.getItem('strategies') || '[]')
  const index = savedStrategies.findIndex(item => item.id === strategy.id)
  if (index > -1) {
    savedStrategies.splice(index, 1)
    localStorage.setItem('strategies', JSON.stringify(savedStrategies))
    historyStrategies.value = savedStrategies
    ElMessage({
      message: '策略删除成功！',
      type: 'success'
    })
  }
}
</script>

<template>
  <div class="policy-container">
    <div class="header">
      <h2>我的策略</h2>
      <button class="btn-green" @click="loadHistoryStrategies">历史策略</button>
      <button class="btn-blue">回测历史记录</button>
    </div>

    <div class="content">
      <!-- 策略简介 -->
      <div class="section">
        <h3>策略简介</h3>
        <textarea
          v-model="strategy.description"
          placeholder="给策略起个名字并描述~"
          rows="3"
          class="textarea"
        ></textarea>
      </div>

      <!-- 参数列表 -->
      <div class="section">
        <h3>参数列表</h3>
        <div class="parameter-list">
          <div v-for="(param, index) in strategy.parameters" 
               :key="index" 
               class="parameter-item">
            <input v-model="param.name" type="text" placeholder="变量名" class="input" />
            <input v-model="param.defaultValue" type="text" placeholder="默认值" class="input" />
            <input v-model="param.description" type="text" placeholder="参数描述" class="input" />
            <button class="btn-red" @click="removeParameter(index)">删除</button>
          </div>
          <button class="btn-blue" @click="addParameter">+ 添加参数</button>
        </div>
      </div>

      <!-- 策略代码 -->
      <div class="section">
        <h3>策略代码</h3>
        <div class="code-editor">
          <textarea
            v-model="strategy.code"
            rows="10"
            placeholder="在这里编写你的策略代码"
            class="textarea code-area"
          ></textarea>
          <div class="code-toolbar">
            <button class="btn-blue">插入代码片段</button>
            <button class="btn-blue">回测 API 文档</button>
            <button class="btn-blue">QtShare 数据 API 文档</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="footer">
      <button class="btn-blue" @click="saveStrategy(false)">保存并私有</button>
      <button class="btn-blue" @click="saveStrategy(true)">保存并公开</button>
    </div>

    <!-- 历史策略对话框 -->
    <el-dialog
      v-model="historyVisible"
      title="历史策略"
      width="70%"
    >
      <div class="history-list">
        <div v-for="item in historyStrategies" 
             :key="item.id" 
             class="history-item"
        >
          <div class="history-content" @click="useHistoryStrategy(item)">
            <h4>{{ item.description || '未命名策略' }}</h4>
            <p class="history-time">创建时间: {{ new Date(item.createTime).toLocaleString() }}</p>
          </div>
          <button class="delete-btn" @click="(e) => deleteStrategy(e, item)">
            <i class="el-icon-delete"></i>
            删除
          </button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/theme' as theme;

.policy-container {
  padding: 20px;
  background: theme.$primary-gradient;
  min-height: 100vh;
  border-radius: 12px;
  box-shadow: theme.$shadow-md;

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      font-size: 2rem;
      color: #2d3748;
      font-family: theme.$font-family-base;
      text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
    }

    .btn-green,
    .btn-blue {
      background: linear-gradient(135deg, #38b2ac, #319795); // 柔和的绿色
      color: white;
      padding: 10px 20px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s ease;
      margin-left: 10px;

      &:hover {
        background: linear-gradient(135deg, #319795, #2c7a7b);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
      }
    }

    .btn-blue {
      background: linear-gradient(135deg, #4299e1, #3182ce); // 柔和的蓝色

      &:hover {
        background: linear-gradient(135deg, #3182ce, #2b6cb0);
      }
    }
  }

  .content {
    .section {
      margin-bottom: 20px;
      background: #ffffff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);

      h3 {
        font-size: 1.5rem;
        font-family: theme.$font-family-base;
        color: #2d3748;
        margin-bottom: 15px;
        border-bottom: 2px solid theme.$border-color;
        padding-bottom: 8px;
      }

      .textarea {
        width: 100%;
        outline: none;
        transition: all 0.3s ease;
        resize: none;
        padding: 12px;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        font-size: 1rem;
        color: #2d3748;
        background: #ffffff;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);

        &:focus {
          border-color: #4299e1;
          box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.15);
        }
      }

      .parameter-list {
        margin-bottom: 20px;

        .parameter-item {
          display: flex;
          align-items: center;
          margin-bottom: 10px;

          .input {
            flex: 1;
            padding: 10px;
            margin-right: 10px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            background: #ffffff;
            color: #2d3748;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);

            &:focus {
              border-color: #4299e1;
              box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.15);
            }
          }

          .btn-red {
            background: linear-gradient(135deg, #f56565, #e53e3e);
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;

            &:hover {
              background: linear-gradient(135deg, #e53e3e, #c53030);
              box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            }
          }
        }

        .btn-blue {
          margin-top: 10px;
          padding: 10px 20px;
          background: linear-gradient(135deg, #4299e1, #3182ce);
          color: white;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.3s ease;

          &:hover {
            background: linear-gradient(135deg, #3182ce, #2b6cb0);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
          }
        }
      }

      .code-editor {
        .code-area {
          width: 100%;
          outline: none;
          transition: all 0.3s ease;
          padding: 12px;
          border: 1px solid #e2e8f0;
          border-radius: 8px;
          resize: none;
          font-family: theme.$font-family-code;
          font-size: 1rem;
          color: #2d3748;
          background: #ffffff;
          box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);

          &:focus {
            border-color: #4299e1;
            box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.15);
          }
        }

        .code-toolbar {
          margin-top: 15px;

          .btn-blue {
            margin-right: 10px;
            padding: 10px 20px;
            background: linear-gradient(135deg, #4299e1, #3182ce);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;

            &:hover {
              background: linear-gradient(135deg, #3182ce, #2b6cb0);
              box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            }
          }
        }
      }
    }
  }

  .footer {
    display: flex;
    justify-content: flex-end;
    padding: 20px;
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);

    .btn-blue {
      margin-left: 10px;
      padding: 10px 20px;
      background: linear-gradient(135deg, #4299e1, #3182ce);
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        background: linear-gradient(135deg, #3182ce, #2b6cb0);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
      }
    }
  }

  .history-list {
    .history-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 15px;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      margin-bottom: 10px;
      transition: all 0.3s ease;

      &:hover {
        border-color: #4299e1;
        box-shadow: 0 2px 10px rgba(66, 153, 225, 0.2);
        
        .delete-btn {
          opacity: 1;
        }
      }

      .history-content {
        flex: 1;
        cursor: pointer;
        
        &:hover {
          transform: translateX(5px);
        }
      }

      .delete-btn {
        opacity: 0;
        padding: 8px 15px;
        background: linear-gradient(135deg, #f56565, #e53e3e);
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 5px;

        &:hover {
          background: linear-gradient(135deg, #e53e3e, #c53030);
          transform: scale(1.05);
        }

        i {
          font-size: 14px;
        }
      }
    }
  }
}
</style>