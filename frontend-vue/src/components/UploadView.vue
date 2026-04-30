<template>
  <div class="view-panel">
    <h2>📤 原始文献摄入与特征提取</h2>
    <el-card shadow="never" class="panel-card">
      <div class="upload-area">
        <el-upload
            drag
            action="#"
            :auto-upload="false"
            :on-change="handleFileChange"
            :limit="1"
            accept=".pdf"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">将 PDF 拖拽至此，或 <em>点击上传</em></div>
        </el-upload>
      </div>

      <div class="options-area">
        <div class="options-header">
          <h3>定向特征提取策略</h3>
          <el-checkbox v-model="checkAll" :indeterminate="isIndeterminate" @change="handleCheckAllChange">
            全选
          </el-checkbox>
        </div>
        <el-checkbox-group v-model="selectedOptions" @change="handleCheckedOptionsChange">
          <el-checkbox v-for="opt in extractionOptions" :key="opt" :label="opt" />
        </el-checkbox-group>
      </div>

      <el-button type="primary" size="large" class="submit-btn" :loading="isUploading" @click="submitTask">
        {{ isUploading ? '文献入库与向量化中...' : '🚀 开始解析并沉淀至图谱' }}
      </el-button>

      <el-alert v-if="uploadMessage" :title="uploadMessage" :type="uploadType" show-icon style="margin-top:20px" />
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const selectedFile = ref(null)
const isUploading = ref(false)
const uploadMessage = ref('')
const uploadType = ref('success')

const extractionOptions = ['算法结构', '训练数据集', '训练结果表现', '创新点', '局限性', '参考文献']
const selectedOptions = ref([...extractionOptions])
const checkAll = ref(true)
const isIndeterminate = ref(false)

const handleCheckAllChange = (val) => {
  selectedOptions.value = val ? [...extractionOptions] : []
  isIndeterminate.value = false
}
const handleCheckedOptionsChange = (value) => {
  const checkedCount = value.length
  checkAll.value = checkedCount === extractionOptions.length
  isIndeterminate.value = checkedCount > 0 && checkedCount < extractionOptions.length
}

const handleFileChange = (uploadFile) => { selectedFile.value = uploadFile.raw }

const submitTask = async () => {
  if (!selectedFile.value) return ElMessage.warning('请先选择文献！')
  if (selectedOptions.value.length === 0) return ElMessage.warning('请至少选择一项提取内容！')

  // 🌟 新增：拦截查重机制
  try {
    const checkRes = await axios.get(`http://localhost:8080/api/wiki/check?filename=${selectedFile.value.name}`)
    if (checkRes.data.exists) {
      // 触发危险操作警告弹窗
      await ElMessageBox.confirm(
          `知识库中已存在【${selectedFile.value.name}】的解析图谱。如果继续，将彻底覆盖之前的向量数据与 Wiki 内容，是否确认覆盖？`,
          '⚠️ 文献冲突警告',
          {
            confirmButtonText: '继续并覆盖',
            cancelButtonText: '取消',
            type: 'warning',
          }
      )
    }
  } catch (error) {
    if (error === 'cancel') {
      // 用户点击了取消，直接中断上传流程
      ElMessage.info('已取消上传')
      return
    }
    // 其他网络错误我们暂不拦截，让它继续抛给下面的逻辑处理
  }

  // 走到这里，说明要么是新文件，要么是用户确认要覆盖旧文件
  isUploading.value = true
  uploadMessage.value = ''

  const formData = new FormData()
  formData.append('file', selectedFile.value)
  selectedOptions.value.forEach(opt => formData.append('options', opt))

  try {
    const res = await axios.post('http://localhost:8080/api/wiki/upload', formData)
    uploadType.value = 'success'
    uploadMessage.value = res.data
  } catch (err) {
    uploadType.value = 'error'
    uploadMessage.value = err.message
  } finally {
    isUploading.value = false
  }
}
</script>

<style scoped>
.view-panel { height: 100%; display: flex; flex-direction: column; }
h2 { margin-top: 0; margin-bottom: 25px; color: var(--text-main); font-weight: 500; }
.panel-card { background-color: var(--bg-panel); border: 1px solid var(--border-line); color: var(--text-main); border-radius: 8px; padding: 20px; }
.options-area { margin: 30px 0; background: var(--bg-card); padding: 20px; border-radius: 8px; border: 1px solid var(--border-line); }
.options-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid var(--border-line); padding-bottom: 10px; }
.options-header h3 { margin: 0; font-size: 16px; color: var(--text-main); }
:deep(.el-checkbox) { color: var(--text-main); }
:deep(.el-checkbox__input.is-checked .el-checkbox__inner) { background-color: #409eff; border-color: #409eff; }
.submit-btn { width: 100%; }
:deep(.el-upload-dragger) { background-color: var(--bg-card); border-color: var(--border-line); }
:deep(.el-upload-dragger:hover) { border-color: #409eff; }
</style>