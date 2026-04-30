<template>
  <div class="app-container">
    <el-container class="layout-container">

      <el-aside width="220px" class="sidebar">
        <div class="logo">🧠 赛博大脑中枢</div>
        <el-menu
            :default-active="activeMenu"
            class="el-menu-vertical"
            background-color="transparent"
            :text-color="isDarkMode ? '#fff' : '#333'"
            active-text-color="#409eff"
            @select="handleMenuSelect"
        >
          <el-menu-item index="upload">
            <el-icon><Upload /></el-icon>
            <span>文献摄入工作台</span>
          </el-menu-item>
          <el-menu-item index="wiki">
            <el-icon><Reading /></el-icon>
            <span>知识库图谱查阅</span>
          </el-menu-item>
          <el-menu-item index="chat">
            <el-icon><ChatDotRound /></el-icon>
            <span>Agent 智能问答</span>
          </el-menu-item>
        </el-menu>

        <div class="theme-switch">
          <el-switch
              v-model="isDarkMode"
              inline-prompt
              active-text="🌙 暗黑"
              inactive-text="☀️ 白天"
              @change="toggleTheme"
          />
        </div>
      </el-aside>

      <el-main class="main-content">
        <UploadView v-if="activeMenu === 'upload'" />
        <WikiView v-if="activeMenu === 'wiki'" ref="wikiViewRef" />
        <ChatView v-if="activeMenu === 'chat'" />
      </el-main>

    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { Upload, Reading, ChatDotRound } from '@element-plus/icons-vue'
import UploadView from './components/UploadView.vue'
import WikiView from './components/WikiView.vue'
import ChatView from './components/ChatView.vue'

const activeMenu = ref('upload')
const wikiViewRef = ref(null)

// 🌟 主题切换逻辑
const isDarkMode = ref(false)

const toggleTheme = (val) => {
  const root = document.documentElement
  if (val) {
    root.setAttribute('data-theme', 'dark')
    root.classList.add('dark') // 兼容 Element Plus 自带的暗黑模式
  } else {
    root.setAttribute('data-theme', 'light')
    root.classList.remove('dark')
  }
}

onMounted(() => {
  // 页面加载时初始化主题
  toggleTheme(isDarkMode.value)
})

const handleMenuSelect = async (index) => {
  activeMenu.value = index
  if (index === 'wiki') {
    await nextTick()
    if (wikiViewRef.value) wikiViewRef.value.loadWikiList()
  }
}
</script>

<style>
/* 🌟 全局 CSS 变量定义：白天模式 vs 黑夜模式 */
:root[data-theme="light"] {
  --bg-app: #f0f2f5;
  --bg-panel: #ffffff;
  --bg-card: #fafafa;
  --bg-hover: #f5f7fa;
  --text-main: #303133;
  --text-muted: #909399;
  border-color: #dcdfe6;
  --border-line: #e4e7ed;
  --chat-ai-bg: #ffffff;
  --chat-ai-border: #dcdfe6;
}

:root[data-theme="dark"] {
  --bg-app: #121212;
  --bg-panel: #1e1e1e;
  --bg-card: #252525;
  --bg-hover: #2a2a2a;
  --text-main: #e0e0e0;
  --text-muted: #888888;
  --border-line: #333333;
  --chat-ai-bg: #333333;
  --chat-ai-border: #555555;
}

body { margin: 0; }

.app-container {
  height: 100vh;
  background-color: var(--bg-app);
  color: var(--text-main);
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  transition: background-color 0.3s;
}

.layout-container { height: 100%; }

.sidebar {
  background-color: var(--bg-panel);
  border-right: 1px solid var(--border-line);
  display: flex;
  flex-direction: column;
  transition: background-color 0.3s;
}

.logo {
  padding: 20px;
  font-size: 20px;
  font-weight: bold;
  color: var(--text-main);
  text-align: center;
  border-bottom: 1px solid var(--border-line);
}

.el-menu { border-right: none; flex: 1; }

.theme-switch {
  padding: 20px;
  text-align: center;
  border-top: 1px solid var(--border-line);
}

.main-content { padding: 30px; overflow-y: hidden; }
</style>