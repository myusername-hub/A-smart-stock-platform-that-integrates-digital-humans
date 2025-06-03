<template>
  <div class="investigation-container">
    <div class="survey-box" v-if="!isCompleted">
      <h2 class="title">投资风险评估问卷</h2>
      <div class="questions">
        <div v-for="(q, index) in questions" :key="index" class="question">
          <h3>{{ q.question }}</h3>
          <div class="options">
            <label v-for="(option, idx) in q.options" :key="idx">
              <input 
                type="radio" 
                :name="'q'+index" 
                :value="option.score"
                v-model="answers[index]"
                required
              >
              {{ option.text }}
            </label>
          </div>
        </div>
      </div>
      <button @click="submitSurvey" :disabled="!isValid">
        {{ isSubmitting ? '提交中...' : '提交问卷' }}
      </button>
    </div>

    <div v-else class="result-box">
      <h2>评估结果</h2>
      <div class="risk-level">
        您的风险承受能力为：<span>{{ riskLevel }}</span>
      </div>
      <div class="risk-desc">{{ riskDescription }}</div>
      <button class="know-btn" @click="handleIKnow">我知道了</button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Investigation',
  setup() {
    const router = useRouter()
    const questions = [
      {
        question: '您的投资经验有多少年？',
        options: [
          { text: '无经验', score: 1 },
          { text: '1-3年', score: 2 },
          { text: '3-5年', score: 3 },
          { text: '5年以上', score: 4 }
        ]
      },
      {
        question: '您能承受的最大投资损失是多少？',
        options: [
          { text: '本金损失0-10%', score: 1 },
          { text: '本金损失10-30%', score: 2 },
          { text: '本金损失30-50%', score: 3 },
          { text: '本金损失50%以上', score: 4 }
        ]
      },
      {
        question: '您的投资目标是？',
        options: [
          { text: '保本为主', score: 1 },
          { text: '稳健增值', score: 2 },
          { text: '追求收益', score: 3 },
          { text: '高风险高收益', score: 4 }
        ]
      },
      {
        question: '您的年龄属于？',
        options: [
          { text: '60岁及以上', score: 1 },
          { text: '45-59岁', score: 2 },
          { text: '30-44岁', score: 3 },
          { text: '18-29岁', score: 4 }
        ]
      },
      {
        question: '您的年收入水平？',
        options: [
          { text: '10万元以下', score: 1 },
          { text: '10-30万元', score: 2 },
          { text: '30-100万元', score: 3 },
          { text: '100万元以上', score: 4 }
        ]
      },
      {
        question: '您的家庭状况？',
        options: [
          { text: '有较重经济负担', score: 1 },
          { text: '有一定经济负担', score: 2 },
          { text: '经济负担较轻', score: 3 },
          { text: '无经济负担', score: 4 }
        ]
      },
      {
        question: '您对投资知识的了解程度？',
        options: [
          { text: '不了解', score: 1 },
          { text: '略有了解', score: 2 },
          { text: '较为熟悉', score: 3 },
          { text: '非常熟悉', score: 4 }
        ]
      },
      {
        question: '面对投资风险，您的态度是？',
        options: [
          { text: '极度厌恶风险', score: 1 },
          { text: '较为谨慎', score: 2 },
          { text: '可以接受一定风险', score: 3 },
          { text: '乐于承担高风险', score: 4 }
        ]
      }
    ]

    const answers = ref([])
    const isCompleted = ref(false)
    const isSubmitting = ref(false)
    const riskLevel = ref('')
    const riskDescription = ref('')

    const isValid = computed(() => {
      return answers.value.length === questions.length
    })

    const calculateRiskLevel = (score) => {
      if (score <= 12) return '保守型'
      if (score <= 20) return '稳健型'
      return '激进型'
    }

    const submitSurvey = async () => {
      if (!isValid.value) return
      
      isSubmitting.value = true
      try {
        const totalScore = answers.value.reduce((sum, score) => sum + score, 0)
        const level = calculateRiskLevel(totalScore)
        
        // 保存结果到localStorage
        localStorage.setItem('riskAssessment', JSON.stringify({
          score: totalScore,
          level,
          date: new Date().toISOString()
        }))

        riskLevel.value = level
        riskDescription.value = getRiskDescription(level)
        isCompleted.value = true
      } catch (error) {
        console.error('提交失败:', error)
        alert('提交失败，请重试')
      } finally {
        isSubmitting.value = false
      }
    }

    const getRiskDescription = (level) => {
      const descriptions = {
        '保守型': '您倾向于选择风险较低、收益稳定的投资产品',
        '稳健型': '您能够接受适度的投资风险，追求适中的投资收益',
        '激进型': '您能够承受较高的投资风险，追求高额回报'
      }
      return descriptions[level] || ''
    }

    const handleIKnow = () => {
      // 读取之前的操作类型和股票代码
      const action = localStorage.getItem('investigationAction')
      const code = localStorage.getItem('investigationStockCode')
      if (action === 'buy') {
        router.push({ path: '/buy', query: { code } })
      } else if (action === 'sell') {
        router.push({ path: '/sell', query: { code } })
      } else {
        router.push('/')
      }
    }

    return {
      questions,
      answers,
      isCompleted,
      isSubmitting,
      isValid,
      riskLevel,
      riskDescription,
      submitSurvey,
      handleIKnow
    }
  }
}
</script>

<style scoped lang="scss">
.investigation-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;

  .survey-box, .result-box {
    background: #fff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }

  .title {
    text-align: center;
    margin-bottom: 30px;
    color: #333;
  }

  .question {
    margin-bottom: 24px;
    
    h3 {
      margin-bottom: 12px;
      color: #333;
    }

    .options {
      display: flex;
      flex-direction: column;
      gap: 12px;

      label {
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
      }
    }
  }

  button {
    width: 100%;
    padding: 12px;
    background: #1890ff;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }

  .result-box {
    text-align: center;

    .risk-level {
      margin: 20px 0;
      font-size: 18px;
      
      span {
        color: #1890ff;
        font-weight: bold;
      }
    }

    .risk-desc {
      color: #666;
      line-height: 1.5;
    }

    .know-btn {
      margin-top: 30px;
      padding: 10px 30px;
      background: #409eff;
      color: #fff;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.2s;
    }

    .know-btn:hover {
      background: #66b1ff;
    }
  }
}
</style>
