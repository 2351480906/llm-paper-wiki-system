<template>
  <div class="view-panel">
    <h2>⚙️ 引擎核心设置</h2>
    <el-card shadow="never" class="settings-card">
      <el-form label-position="top" size="large">

        <el-form-item label="📚 知识库物理存储路径 (绝对路径)">
          <el-input
              v-model="settings.base_path"
              placeholder="例如: D:/MyResearch/KnowledgeBase"
          />
          <div class="field-desc">
            所有的 PDF 实体文件、Markdown 解析结果、分类账本都将保存在此目录下。
          </div>
        </el-form-item>

        <!-- 🌟 核心修改：支持既可选择又可手动输入 -->
        <el-form-item label="🧠 驱动大模型版本">
          <el-select
              v-model="settings.llm_model"
              filterable
              allow-create
              default-first-option
              placeholder="请选择常用模型，或直接点击此处手动键入任意模型名称"
              style="width: 100%;"
          >
            <!-- 保留几个最常用的作为快捷提示，用户也可以无视它们直接打字 -->
            <el-option label="qwen-plus (通义千问 Plus - 均衡)" value="qwen-plus" />
            <el-option label="qwen-max (通义千问 Max - 强推理)" value="qwen-max" />
            <el-option label="qwen-turbo (通义千问 Turbo - 极速)" value="qwen-turbo" />
            <el-option label="qwen-long (通义千问 Long - 长文本)" value="qwen-long" />
          </el-select>
          <div class="field-desc">
            💡 支持任意兼容模型。您可以直接在上方输入框内手动输入模型代码（例如：<code>qwen-max-latest</code>），输入后按回车键确认即可。
          </div>
        </el-form-item>

        <el-button type="primary" :loading="isSaving" @click="saveSettings">
          💾 保存并应用全局配置
        </el-button>

      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const settings = ref({ base_path: '', llm_model: '' })
const isSaving = ref(false)

const loadSettings = async () => {
  try {
    const res = await axios.get('http://localhost:8080/api/wiki/settings')
    if (res.data.status === 'success') {
      settings.value.base_path = res.data.base_path
      settings.value.llm_model = res.data.llm_model
    }
  } catch (e) {
    ElMessage.error('无法读取当前设置')
  }
}

const saveSettings = async () => {
  if (!settings.value.base_path) return ElMessage.warning('路径不能为空！')
  if (!settings.value.llm_model) return ElMessage.warning('模型名称不能为空！')

  isSaving.value = true
  try {
    const res = await axios.post('http://localhost:8080/api/wiki/settings', settings.value)
    if (res.data.status === 'success') {
      ElMessageBox.alert(res.data.message, '操作成功', { type: 'success' })
    } else {
      ElMessage.error(res.data.message)
    }
  } catch (e) {
    ElMessage.error('网络错误导致保存失败')
  } finally {
    isSaving.value = false
  }
}

onMounted(() => { loadSettings() })
</script>

<style scoped>
.view-panel { height: 100%; display: flex; flex-direction: column; }
h2 { margin-top: 0; margin-bottom: 25px; color: var(--text-main); font-weight: 500; }
.settings-card { background-color: var(--bg-panel); border: 1px solid var(--border-line); border-radius: 8px; padding: 20px; max-width: 800px; }
.field-desc { font-size: 13px; color: var(--text-muted); margin-top: 6px; line-height: 1.5; }
:deep(.el-form-item__label) { color: var(--text-main); font-weight: bold; }
code { background-color: var(--bg-hover); padding: 2px 4px; border-radius: 4px; color: #f56c6c; border: 1px solid var(--border-line); }
</style>