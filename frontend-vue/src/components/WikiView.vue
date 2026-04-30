<template>
  <div class="view-panel wiki-view">
    <h2>📖 已处理文献图谱 (Wiki)</h2>
    <el-container class="wiki-container">
      <el-aside width="300px" class="wiki-sidebar">
        <el-menu background-color="transparent" :text-color="isDark ? '#ccc' : '#333'" active-text-color="#67c23a" @select="fetchWikiContent">
          <el-menu-item v-for="file in wikiFiles" :key="file" :index="file">
            <el-icon><Document /></el-icon>
            <span class="truncate-text">{{ file.replace('.md', '') }}</span>
          </el-menu-item>
          <div v-if="wikiFiles.length === 0" class="empty-tip">暂无文献</div>
        </el-menu>
      </el-aside>

      <el-main class="wiki-main">
        <div v-if="parsedSections.length > 0">
          <el-card v-for="sec in parsedSections" :key="sec.id" class="wiki-section-card" shadow="hover">
            <template #header>
              <div class="section-title">
                <el-icon style="margin-right: 8px;"><CollectionTag /></el-icon>
                {{ sec.title }}
              </div>
            </template>
            <div class="markdown-body" v-html="sec.html"></div>
          </el-card>
        </div>
        <div v-else class="placeholder-tip">👈 请选择文献以查看</div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Document, CollectionTag } from '@element-plus/icons-vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// --- 🌟 引入基础库 ---
import { marked } from 'marked'
import katex from 'katex'
import 'katex/dist/katex.min.css'

// ==========================================
// 🌟 核心修复：手写高鲁棒性 Markdown 解析器
// 彻底隔离 LaTeX 下标(_) 与 Markdown 斜体(_) 的冲突
// ==========================================

// 1. 块级公式拦截器 ($$ ... $$)
const blockMath = {
  name: 'blockMath',
  level: 'block',
  start(src) { return src.indexOf('$$'); },
  tokenizer(src) {
    const match = /^\$\$([\s\S]+?)\$\$/.exec(src);
    if (match) {
      return { type: 'blockMath', raw: match[0], text: match[1] };
    }
  },
  renderer(token) {
    try {
      return `<div style="text-align: center; margin: 1em 0; overflow-x: auto;">
                ${katex.renderToString(token.text, { displayMode: true, throwOnError: false })}
              </div>`;
    } catch(e) { return token.raw; }
  }
};

// 2. 行内公式拦截器 ($ ... $)
const inlineMath = {
  name: 'inlineMath',
  level: 'inline',
  start(src) { return src.indexOf('$'); },
  tokenizer(src) {
    // 匹配 $...$ 且紧密贴合中文边界，内部不包含换行
    const match = /^\$([^$\n]+?)\$/.exec(src);
    if (match) {
      return { type: 'inlineMath', raw: match[0], text: match[1] };
    }
  },
  renderer(token) {
    try {
      return katex.renderToString(token.text, { displayMode: false, throwOnError: false });
    } catch(e) { return token.raw; }
  }
};

// 强制注入最高优先级
marked.use({ extensions: [blockMath, inlineMath] });


const wikiFiles = ref([])
const currentWikiContent = ref('')
const isDark = ref(document.documentElement.classList.contains('dark'))

// --- 🌟 分块渲染与数字乱码清洗 ---
const parsedSections = computed(() => {
  const content = currentWikiContent.value.trim()
  if (!content) return []

  const parts = content.split(/(?=^##\s+)/m)

  const results = []
  parts.forEach((part, index) => {
    const text = part.trim()
    if (!text) return

    const lines = text.split('\n')
    let title = ''
    let body = ''

    const titleMatch = lines[0].match(/^##\s+(.+)/)
    if (titleMatch) {
      title = titleMatch[1].replace(/\*\*/g, '').trim()
      body = lines.slice(1).join('\n')

      // 清洗大模型瞎加的 $ 百分比符号 (如 $99.36\%$ -> 99.36%)
      body = body.replace(/\$([0-9.]+\s*\\?%)\$/g, (match, p1) => p1.replace('\\', ''))
    } else {
      return
    }

    results.push({
      id: index,
      title: title,
      html: marked.parse(body)
    })
  })
  return results
})

const loadWikiList = async () => {
  try {
    const res = await axios.get('http://localhost:8080/api/wiki/list')
    if (res.data.status === 'success') wikiFiles.value = res.data.files
  } catch (error) { ElMessage.error('列表加载失败') }
}

const fetchWikiContent = async (filename) => {
  try {
    const res = await axios.get(`http://localhost:8080/api/wiki/content?filename=${filename}`)
    if (res.data.status === 'success') currentWikiContent.value = res.data.content
  } catch (error) { ElMessage.error('读取失败') }
}

defineExpose({ loadWikiList })
onMounted(() => { loadWikiList() })
</script>

<style scoped>
.view-panel { height: 100%; display: flex; flex-direction: column; }
.wiki-container { height: calc(100vh - 120px); border: 1px solid var(--border-line); border-radius: 8px; overflow: hidden; }
.wiki-sidebar { border-right: 1px solid var(--border-line); background: var(--bg-card); }
.wiki-main { background: var(--bg-panel); padding: 30px; overflow-y: auto; }
.wiki-section-card { background-color: var(--bg-card); border: 1px solid var(--border-line); margin-bottom: 25px; }
.section-title { font-size: 18px; font-weight: bold; color: #67c23a; display: flex; align-items: center; }

/* 🌟 美化特征提取的小标题 (h3) */
:deep(.markdown-body h3) {
  color: #409eff;
  font-size: 1.15em;
  font-weight: bold;
  border-left: 5px solid #409eff;
  padding-left: 12px;
  background-color: var(--bg-hover);
  padding-top: 8px;
  padding-bottom: 8px;
  border-radius: 0 6px 6px 0;
  margin-top: 25px;
  margin-bottom: 15px;
}

/* 🌟 公式排版优化 */
:deep(.katex) {
  font-size: 1.1em;
  color: inherit;
}
.markdown-body { color: var(--text-main); line-height: 1.8; font-size: 15px; }
:deep(.markdown-body h1), :deep(.markdown-body h2) { color: var(--text-main); margin-top: 15px; margin-bottom: 10px; }
:deep(.markdown-body p) { margin-bottom: 1em; }
:deep(.markdown-body ul), :deep(.markdown-body ol) { padding-left: 20px; margin-bottom: 15px; }
:deep(.markdown-body strong) { color: #e6a23c; } /* 重点加粗词使用醒目色 */
:deep(.markdown-body code) { background-color: var(--bg-hover); padding: 3px 6px; border-radius: 4px; color: #f56c6c; border: 1px solid var(--border-line); font-family: monospace; }
</style>