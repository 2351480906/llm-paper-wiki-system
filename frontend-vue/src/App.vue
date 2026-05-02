<template>
  <el-container class="app-container" :class="{ 'is-dark': isDarkMode }">

    <!-- 🌟 左侧导航侧边栏 -->
    <el-aside width="240px" class="sidebar">
      <div class="logo-header">
        <span class="logo-icon">🧠</span>
        <span class="logo-text">Cyber Scholar</span>
      </div>

      <el-menu
          :default-active="activeMenu"
          class="main-menu"
          :background-color="isDarkMode ? '#1e1e2d' : '#f5f7fa'"
          :text-color="isDarkMode ? '#a1a5b7' : '#333'"
          active-text-color="#409EFF"
          @select="handleSelect"
      >
        <el-menu-item index="upload">
          <el-icon><Upload /></el-icon>
          <span>文献解析工作台</span>
        </el-menu-item>

        <el-menu-item index="wiki">
          <el-icon><Document /></el-icon>
          <span>知识库图谱查阅</span>
        </el-menu-item>

        <el-menu-item index="chat">
          <el-icon><ChatDotRound /></el-icon>
          <span>Agent 智能问答</span>
        </el-menu-item>

        <el-menu-item index="settings">
          <el-icon><Setting /></el-icon>
          <span>系统引擎设置</span>
        </el-menu-item>
      </el-menu>

      <!-- 主题切换按钮放在底部 -->
      <div class="theme-switch-wrapper">
        <el-switch
            v-model="isDarkMode"
            inline-prompt
            :active-icon="Moon"
            :inactive-icon="Sunny"
            style="--el-switch-on-color: #4a4a4a; --el-switch-off-color: #dcdfe6"
            @change="toggleTheme"
        />
        <span class="theme-label">{{ isDarkMode ? '暗黑模式' : '明亮模式' }}</span>
      </div>
    </el-aside>

    <!-- 🌟 右侧主内容区 -->
    <el-container>
      <el-main class="main-content">
        <!-- 🌟 核心修改：使用 KeepAlive 实现页面缓存保活 -->
        <KeepAlive>
          <component :is="currentComponent" />
        </KeepAlive>
      </el-main>
    </el-container>

  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Upload, Document, ChatDotRound, Setting, Moon, Sunny } from '@element-plus/icons-vue'

// 引入你的四个核心视图组件
import UploadView from './components/UploadView.vue'
import WikiView from './components/WikiView.vue'
import ChatView from './components/ChatView.vue'
import SettingsView from './components/SettingsView.vue'

// 状态管理
const activeMenu = ref('upload')
const isDarkMode = ref(false)

// 🌟 核心修改：建立一个“菜单标识”到“具体组件”的映射表
const viewMap = {
  upload: UploadView,
  wiki: WikiView,
  chat: ChatView,
  settings: SettingsView
}

// 🌟 核心修改：计算出当前应该显示的组件
const currentComponent = computed(() => viewMap[activeMenu.value])

// 菜单切换逻辑
const handleSelect = (index) => {
  activeMenu.value = index
}

// 主题切换逻辑
const toggleTheme = (val) => {
  if (val) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// 页面加载时初始化主题
onMounted(() => {
  toggleTheme(isDarkMode.value)
})
</script>

<style>
/* 保持你原来的全局 CSS 变量和样式不变 */
:root {
  --bg-main: #ffffff;
  --bg-panel: #fcfcfc;
  --bg-card: #ffffff;
  --bg-hover: #f0f2f5;
  --text-main: #303133;
  --text-muted: #909399;
  --border-line: #e4e7ed;
}

:root.dark {
  --bg-main: #151521;
  --bg-panel: #1e1e2d;
  --bg-card: #1b1b29;
  --bg-hover: #2b2b40;
  --text-main: #e1e3e8;
  --text-muted: #a1a5b7;
  --border-line: #2b2b40;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  background-color: var(--bg-main);
  color: var(--text-main);
  transition: background-color 0.3s, color 0.3s;
}

.app-container {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.sidebar {
  display: flex;
  flex-direction: column;
  background-color: var(--bg-panel) !important;
  border-right: 1px solid var(--border-line);
  transition: background-color 0.3s;
}

.logo-header {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  font-size: 18px;
  font-weight: bold;
  color: var(--text-main);
  border-bottom: 1px solid var(--border-line);
}
.logo-icon { margin-right: 8px; font-size: 22px; }

.main-menu { flex: 1; border-right: none; }

.theme-switch-wrapper {
  padding: 20px;
  display: flex;
  align-items: center;
  border-top: 1px solid var(--border-line);
}
.theme-label { margin-left: 10px; font-size: 13px; color: var(--text-muted); }

.main-content {
  background-color: var(--bg-main);
  padding: 20px;
  height: 100%;
  box-sizing: border-box;
  overflow-y: hidden;
}
</style>