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
.policy-container {
  padding: 20px;
  background: linear-gradient(135deg, #1e2a38, #2a3d4f); // 高级感的深蓝渐变背景
  min-height: 100vh;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      font-size: 2rem;
      color: #f0f4f8; // 柔和的浅色文字
      text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
    }

    .btn-green,
    .btn-blue {
      background: linear-gradient(135deg, #28a745, #218838); // 渐变绿色按钮
      color: white;
      padding: 10px 20px; // 调整按钮大小
      border: none;
      border-radius: 8px; // 圆角更柔和
      cursor: pointer;
      transition: all 0.3s ease;
      margin-left: 10px; // 增加按钮之间的间隔

      &:hover {
        background: linear-gradient(135deg, #218838, #1e7e34);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); // 更柔和的阴影
      }
    }

    .btn-blue {
      background: linear-gradient(135deg, #236a8e, #1b5470); // 渐变蓝色按钮

      &:hover {
        background: linear-gradient(135deg, #1b5470, #123954);
      }
    }
  }

  .content {
    .section {
      margin-bottom: 20px;

      h3 {
        font-size: 1.5rem;
        color: #f0f4f8; // 柔和的浅色文字
        margin-bottom: 10px;
        border-bottom: 2px solid #3a4a5a; // 增加分割线
        padding-bottom: 5px;
      }

      .textarea {
        width: 100%;
        padding: 10px; // 调整文本框内边距
        border: 1px solid #3a4a5a; // 更暗的边框颜色
        border-radius: 8px;
        resize: none;
        font-size: 1rem; // 调整字体大小
        color: #f0f4f8; // 柔和的浅色文字
        background: #2e3f50; // 深蓝背景
        box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.2);
      }

      .parameter-list {
        margin-bottom: 20px;

        .parameter-item {
          display: flex;
          align-items: center;
          margin-bottom: 10px; // 增加参数项之间的间隔

          .input {
            flex: 1;
            padding: 10px;
            margin-right: 10px; // 增加输入框之间的间隔
            border: 1px solid #3a4a5a; // 更暗的边框颜色
            border-radius: 8px;
            background: #2e3f50; // 深蓝背景
            color: #f0f4f8; // 柔和的浅色文字
            box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.2);
          }

          .btn-red {
            background: linear-gradient(135deg, #dc3545, #c82333); // 渐变红色按钮
            color: white;
            padding: 10px 20px; // 调整按钮大小
            border: none;
            border-radius: 8px; // 圆角更柔和
            cursor: pointer;
            transition: all 0.3s ease;

            &:hover {
              background: linear-gradient(135deg, #c82333, #a71d2a);
              box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); // 更柔和的阴影
            }
          }
        }

        .btn-blue {
          margin-top: 10px; // 增加按钮与参数列表的间隔
          padding: 10px 20px; // 调整按钮大小
          background: linear-gradient(135deg, #236a8e, #1b5470); // 渐变蓝色按钮
          border-radius: 8px; // 圆角更柔和
          display: inline-block;
          cursor: pointer;
          transition: all 0.3s ease;

          &:hover {
            background: linear-gradient(135deg, #1b5470, #123954);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); // 更柔和的阴影
          }
        }
      }

      .code-editor {
        .code-area {
          width: 100%;
          padding: 10px; // 调整文本框内边距
          border: 1px solid #3a4a5a; // 更暗的边框颜色
          border-radius: 8px;
          resize: none;
          font-family: monospace;
          font-size: 1rem; // 调整字体大小
          color: #f0f4f8; // 柔和的浅色文字
          background: #2e3f50; // 深蓝背景
          box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.2);
        }

        .code-toolbar {
          margin-top: 15px; // 增加工具栏与代码区域的间隔

          .btn-blue {
            margin-right: 10px; // 增加按钮之间的间隔
            padding: 10px 20px; // 调整按钮大小
            background: linear-gradient(135deg, #236a8e, #1b5470); // 渐变蓝色按钮
            border-radius: 8px; // 圆角更柔和
            cursor: pointer;
            transition: all 0.3s ease;

            &:hover {
              background: linear-gradient(135deg, #1b5470, #123954);
              box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); // 更柔和的阴影
            }
          }
        }
      }
    }
  }

  .footer {
    display: flex;
    justify-content: flex-end;

    .btn-blue {
      margin-left: 10px; // 增加按钮之间的间隔
      padding: 10px 20px; // 调整按钮大小
      background: linear-gradient(135deg, #236a8e, #1b5470); // 渐变蓝色按钮
      border-radius: 8px; // 圆角更柔和

      &:hover {
        background: linear-gradient(135deg, #1b5470, #123954);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); // 更柔和的阴影
      }
    }
  }
}
</style>