<template>
  <div class="view-panel">
    <h2>🤖 Agentic RAG 知识检索终端</h2>
    <el-card class="chat-card" shadow="never">
      <div class="chat-window" ref="chatWindow">
        <div v-for="(msg, index) in chatHistory" :key="index" :class="['message-wrapper', msg.role === 'user' ? 'is-user' : 'is-ai']">
          <div class="avatar">{{ msg.role === 'user' ? '🧔' : '🧠' }}</div>
          <div class="bubble-container">
            <div class="message-bubble">
              <p style="white-space: pre-wrap; margin: 0; line-height: 1.6;">{{ msg.content }}</p>
            </div>
            <div class="action-row" v-if="msg.role === 'assistant' && msg.content.includes('[底层原始PDF]')">
              <el-button type="warning" size="small" :icon="Collection" plain @click="promptSaveToWiki(msg.content)">
                💾 发现新知识！提炼为 Wiki 词条
              </el-button>
            </div>
          </div>
        </div>
        <div v-if="isChatting" class="message-wrapper is-ai">
          <div class="avatar">🧠</div>
          <div class="message-bubble loading-bubble">
            <el-icon class="is-loading" style="margin-right: 5px;"><Loading /></el-icon> 正在翻阅目录与向量库...
          </div>
        </div>
      </div>
      <div class="chat-input-area">
        <el-input v-model="currentMessage" type="textarea" :rows="3" placeholder="向知识库提问..." @keydown.enter.prevent="sendMessage" />
        <el-button type="primary" class="send-btn" @click="sendMessage">发送</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { Collection, Loading } from '@element-plus/icons-vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const currentMessage = ref('')
const isChatting = ref(false)
const chatWindow = ref(null)
const chatHistory = ref([{ role: 'assistant', content: '随时准备为您检索知识库！' }])

const scrollToBottom = async () => {
  await nextTick()
  if (chatWindow.value) chatWindow.value.scrollTop = chatWindow.value.scrollHeight
}

const sendMessage = async () => {
  const text = currentMessage.value.trim()
  if (!text) return
  chatHistory.value.push({ role: 'user', content: text })
  currentMessage.value = ''
  scrollToBottom()
  isChatting.value = true

  try {
    const res = await axios.post('http://localhost:8080/api/wiki/chat', { question: text })
    chatHistory.value.push({ role: 'assistant', content: res.data })
  } catch (err) {
    chatHistory.value.push({ role: 'assistant', content: '❌ 报错了: ' + err.message })
  } finally {
    isChatting.value = false
    scrollToBottom()
  }
}

const promptSaveToWiki = (content) => {
  ElMessageBox.prompt('请输入这个新知识点的精简标题：', '沉淀至 Wiki 图谱', {
    confirmButtonText: '保存',
    cancelButtonText: '取消',
    inputPattern: /.+/,
    inputErrorMessage: '标题不能为空哦！',
  }).then(async ({ value }) => {
    try {
      const res = await axios.post('http://localhost:8080/api/wiki/save', { topic: value, content: content })
      ElMessage.success(res.data)
    } catch (err) {
      ElMessage.error('保存失败：' + err.message)
    }
  }).catch(() => {})
}
</script>

<style scoped>
.view-panel { height: 100%; display: flex; flex-direction: column; }
h2 { margin-top: 0; margin-bottom: 25px; color: var(--text-main); font-weight: 500; }
.chat-card { display: flex; flex-direction: column; height: calc(100vh - 120px); background-color: var(--bg-panel); border: 1px solid var(--border-line);}
.chat-window { flex: 1; overflow-y: auto; padding: 20px; }
.message-wrapper { display: flex; margin-bottom: 25px; align-items: flex-start; }
.message-wrapper.is-user { flex-direction: row-reverse; }
.avatar { font-size: 28px; margin: 0 15px; }
.bubble-container { display: flex; flex-direction: column; align-items: flex-start; max-width: 75%; }
.is-user .bubble-container { align-items: flex-end; }
.message-bubble { padding: 14px 18px; border-radius: 10px; font-size: 15px; color: var(--text-main); }
.is-user .message-bubble { background-color: #2c6e49; color: #fff; border-top-right-radius: 0; }
.is-ai .message-bubble { background-color: var(--chat-ai-bg); border-top-left-radius: 0; border: 1px solid var(--chat-ai-border); }
.loading-bubble { color: var(--text-muted) !important; font-style: italic; display: flex; align-items: center; }
.action-row { margin-top: 8px; }
.chat-input-area { display: flex; gap: 10px; margin-top: 20px; padding-top: 20px; border-top: 1px solid var(--border-line);}
:deep(.el-textarea__inner) { background-color: var(--bg-card); color: var(--text-main); border-color: var(--border-line); }
.send-btn { height: 75px; width: 120px; }
</style>