<template>
  <div class="chat-view-container">
    <!-- 🌟 顶部标题 -->
    <div class="chat-header">
      <h2>🧠 Cyber Scholar 智能问答</h2>
      <p class="subtitle">支持多轮推理与工具调用，随时将优质回答沉淀至知识库</p>
    </div>

    <!-- 🌟 聊天记录展示区 -->
    <div class="chat-messages" ref="messagesContainer">
      <div
          v-for="(msg, index) in chatList"
          :key="index"
          :class="['message-wrapper', msg.role]"
      >
        <div class="message-container">
          <!-- 角色头像 -->
          <div class="avatar">
            {{ msg.role === 'user' ? '🧑‍💻' : '🤖' }}
          </div>

          <!-- 消息气泡 -->
          <div class="message-bubble">
            <!-- Markdown 渲染区 -->
            <div class="markdown-body" v-html="renderMarkdown(msg.content)"></div>

            <!-- 🌟 知识沉淀操作栏 (仅对 AI 回复显示) -->
            <div v-if="msg.role === 'ai' && index > 0" class="message-actions">
              <el-button
                  type="primary"
                  size="small"
                  text
                  bg
                  @click="openMergeDialog(index)"
              >
                <el-icon><DocumentAdd /></el-icon> 沉淀至 Wiki
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 加载状态动画 -->
      <div v-if="isSending" class="message-wrapper ai">
        <div class="message-container">
          <div class="avatar">🤖</div>
          <div class="message-bubble typing-indicator">
            <span class="dot"></span><span class="dot"></span><span class="dot"></span>
            <span style="margin-left: 8px; font-size: 13px;">Agent 正在深度思考...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 🌟 底部输入区 -->
    <div class="chat-input-area">
      <el-input
          v-model="userInput"
          type="textarea"
          :rows="3"
          resize="none"
          placeholder="问点什么吧...（例如：我的库里有关于大模型的论文吗？）"
          @keydown.enter.exact.prevent="sendMessage"
          class="custom-textarea"
      />
      <div class="action-bar">
        <!-- 清空记忆按钮 -->
        <el-button type="danger" plain @click="clearChat" :icon="Delete">
          清空记忆
        </el-button>

        <!-- 发送按钮 -->
        <el-button type="primary" :loading="isSending" @click="sendMessage" :icon="Position">
          发 送 (Enter)
        </el-button>
      </div>
    </div>

    <!-- 🌟 知识沉淀确认弹窗 -->
    <el-dialog
        v-model="mergeDialogVisible"
        title="🧠 将知识沉淀至 Wiki"
        width="420px"
        destroy-on-close
    >
      <div class="dialog-tip">
        系统将召唤大模型，把这段问答智能融合（排重、补充细节）到指定的文献笔记中。
      </div>
      <el-form label-position="top">
        <el-form-item label="目标文献名称 (需与左侧目录中的名称一致)">
          <el-input v-model="targetFilename" placeholder="例如：EF-Net" clearable>
            <template #append>.md</template>
          </el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="mergeDialogVisible = false">取 消</el-button>
          <el-button type="primary" :loading="isMerging" @click="confirmMerge">
            开始智能融合
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { DocumentAdd, Position, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { marked } from 'marked'

// ==========================================
// 1. 聊天核心状态与逻辑
// ==========================================
const defaultGreeting = '你好！我是 Cyber Scholar。很高兴继续为您服务。👋\n\n刚才我们探讨了文献相关内容，请问接下来有什么我可以帮您的？'
const chatList = ref([{ role: 'ai', content: defaultGreeting }])
const userInput = ref('')
const isSending = ref(false)
const messagesContainer = ref(null)

const renderMarkdown = (text) => {
  if (!text) return ''
  return marked(text)
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 清空记忆
const clearChat = () => {
  ElMessageBox.confirm('确定要清空当前的对话记忆吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    chatList.value = [{ role: 'ai', content: defaultGreeting }]
    ElMessage.success('记忆已清空')
  }).catch(() => {})
}

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim() || isSending.value) return

  const question = userInput.value.trim()
  chatList.value.push({ role: 'user', content: question })
  userInput.value = ''
  isSending.value = true
  scrollToBottom()

  try {
    const res = await axios.post('http://localhost:8000/api/ai/chat', {
      messages: chatList.value.map(m => ({
        role: m.role === 'ai' ? 'assistant' : m.role,  // 翻译身份！
        content: m.content
      }))
    })

    const aiAnswer = res.data.content || res.data.answer || res.data.message
    chatList.value.push({ role: 'ai', content: aiAnswer })
  } catch (error) {
    console.error(error)
    chatList.value.push({ role: 'ai', content: '❌ 请求失败: ' + (error.response?.data || error.message) })
  } finally {
    isSending.value = false
    scrollToBottom()
  }
}

// ==========================================
// 2. 知识沉淀 (Wiki Merge) 逻辑
// ==========================================
const mergeDialogVisible = ref(false)
const isMerging = ref(false)
const targetFilename = ref('')
const pendingMergeData = ref({ question: '', answer: '' })

const openMergeDialog = (aiMsgIndex) => {
  const userMsg = chatList.value[aiMsgIndex - 1]
  const aiMsg = chatList.value[aiMsgIndex]

  if (!userMsg || userMsg.role !== 'user') {
    ElMessage.warning('未能精准抓取到您的提问，无法融合。')
    return
  }

  pendingMergeData.value.question = userMsg.content
  pendingMergeData.value.answer = aiMsg.content
  targetFilename.value = ''
  mergeDialogVisible.value = true
}

const confirmMerge = async () => {
  if (!targetFilename.value.trim()) {
    ElMessage.warning('请输入目标文献的名称！')
    return
  }

  isMerging.value = true
  try {
    const response = await axios.post('http://localhost:8000/api/ai/wiki/merge', {
      filename: targetFilename.value.trim(),
      question: pendingMergeData.value.question,
      answer: pendingMergeData.value.answer
    })

    const resultMsg = response.data
    if (resultMsg.includes('✅') || resultMsg.includes('🎉')) {
      ElMessage.success({ message: resultMsg, duration: 4000 })
      mergeDialogVisible.value = false
    } else {
      ElMessage.error(resultMsg)
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('请求失败，请检查后端服务是否正常。')
  } finally {
    isMerging.value = false
  }
}
</script>

<style scoped>
/* 容器整体布局 */
.chat-view-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  max-height: 100vh;
  background-color: var(--bg-main, #f5f7fa);
  border-radius: 12px;
  overflow: hidden;
}

.chat-header {
  padding: 20px;
  background-color: #fff;
  border-bottom: 1px solid #ebeef5;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  z-index: 2;
}

.chat-header h2 {
  margin: 0 0 5px 0;
  font-size: 18px;
  color: #303133;
}

.subtitle { margin: 0; font-size: 13px; color: #909399; }

/* 🌟 核心修改：聊天记录区域 Flexbox 布局 */
.chat-messages {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
  scroll-behavior: smooth;
}

.message-wrapper {
  display: flex;
  width: 100%;
}

/* AI 靠左 */
.message-wrapper.ai {
  justify-content: flex-start;
}

/* User 靠右 */
.message-wrapper.user {
  justify-content: flex-end;
}

/* 气泡与头像的容器 */
.message-container {
  display: flex;
  max-width: 85%;
  gap: 16px;
}

/* User 容器翻转，头像在右侧 */
.message-wrapper.user .message-container {
  flex-direction: row-reverse;
}

/* 头像样式 */
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.message-wrapper.ai .avatar { background-color: #fff; }
.message-wrapper.user .avatar { background-color: #ecf5ff; }

/* 🌟 核心修改：气泡样式 */
.message-bubble {
  padding: 14px 18px;
  border-radius: 12px;
  font-size: 15px;
  line-height: 1.6;
  word-break: break-word;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

/* AI 气泡样式（白底灰字） */
.message-wrapper.ai .message-bubble {
  background-color: #ffffff;
  border: 1px solid #ebeef5;
  color: #303133;
  border-top-left-radius: 4px; /* 聊天小尾巴效果 */
}

/* User 气泡样式（蓝底白字） */
.message-wrapper.user .message-bubble {
  background-color: #409eff;
  color: #ffffff;
  border-top-right-radius: 4px; /* 聊天小尾巴效果 */
}

/* 强制把 User 气泡里的 Markdown 文字变成白色 */
.message-wrapper.user .message-bubble :deep(p),
.message-wrapper.user .message-bubble :deep(li),
.message-wrapper.user .message-bubble :deep(span) {
  color: #ffffff !important;
}
.message-wrapper.user .message-bubble :deep(strong) {
  color: #ffeba6 !important; /* 强调文字变成浅黄色避免刺眼 */
}

/* 消除 Markdown 首尾自带的段落间距 */
.markdown-body :deep(> *:first-child) { margin-top: 0; }
.markdown-body :deep(> *:last-child) { margin-bottom: 0; }

/* 沉淀按钮样式 */
.message-actions {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #ebeef5;
  display: flex;
  justify-content: flex-end;
}

/* 🌟 让 Markdown 里的图片自适应宽度，带有圆角和阴影，学术范十足 */
.markdown-body :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin: 15px 0;
  display: block;
}

/* AI 视觉解析的提示语可以加个显眼的左侧边框 */
.markdown-body :deep(strong) {
  color: #1890ff; /* 将“AI 视觉解析：”等强调文字变为主题蓝 */
}

/* 打字机加载动画 */
.typing-indicator {
  display: flex;
  align-items: center;
  color: #909399;
}
.dot {
  width: 6px; height: 6px; margin: 0 2px;
  background-color: #c0c4cc; border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out both;
}
.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* 底部输入区 */
.chat-input-area {
  padding: 16px 24px;
  background-color: #fff;
  border-top: 1px solid #ebeef5;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.02);
  z-index: 2;
}

.custom-textarea :deep(.el-textarea__inner) {
  border-radius: 8px;
  padding: 12px;
  font-size: 14px;
  background-color: #f5f7fa;
  border: 1px solid transparent;
  transition: all 0.3s;
}
.custom-textarea :deep(.el-textarea__inner:focus) {
  background-color: #fff;
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64,158,255,0.1);
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

/* 弹窗提示文本 */
.dialog-tip {
  font-size: 13px;
  color: #909399;
  margin-bottom: 20px;
  line-height: 1.5;
  background: #f4f4f5;
  padding: 10px 14px;
  border-radius: 6px;
}
</style>