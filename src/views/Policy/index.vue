<template>
  <div class="policy-container">
    <div class="header">
      <h2>我的策略</h2>
      <button class="btn-green">新建一个策略</button>
      <button class="btn-blue">回测历史记录</button>
    </div>

    <div class="content">
      <!-- 策略简介 -->
      <div class="section">
        <h3>策略简介</h3>
        <textarea
          placeholder="给策略起个名字并描述~"
          rows="3"
          class="textarea"
        ></textarea>
      </div>

      <!-- 参数列表 -->
      <div class="section">
        <h3>参数列表</h3>
        <div class="parameter-list">
          <div class="parameter-item">
            <input type="text" placeholder="变量名" class="input" />
            <input type="text" placeholder="默认值" class="input" />
            <input type="text" placeholder="参数描述" class="input" />
            <button class="btn-red">删除</button>
          </div>
          <button class="btn-blue">+ 添加参数</button>
        </div>
      </div>

      <!-- 策略代码 -->
      <div class="section">
        <h3>策略代码</h3>
        <div class="code-editor">
          <textarea
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
      <button class="btn-blue">保存并私有</button>
      <button class="btn-blue">保存并公开</button>
    </div>
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
}
</style>