<template>
  <div class="knowledge-edit">
    <div class="edit-header">
      <el-button @click="router.back()">取消</el-button>
      <el-button type="primary" :loading="saving" @click="handleSave">
        {{ isEdit ? '保存修改' : '发布文章' }}
      </el-button>
    </div>
    
    <el-card class="edit-card">
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="form.title" placeholder="请输入文章标题" />
        </el-form-item>
        
        <el-form-item label="摘要">
          <el-input
            v-model="form.summary"
            type="textarea"
            :rows="2"
            placeholder="请输入文章摘要（可选）"
          />
        </el-form-item>
        
        <el-form-item label="标签">
          <el-select
            v-model="form.tags"
            multiple
            filterable
            allow-create
            placeholder="请选择或输入标签"
            style="width: 100%"
          >
            <el-option v-for="tag in tagOptions" :key="tag" :label="tag" :value="tag" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="发布">
          <el-switch v-model="form.isPublished" />
        </el-form-item>
        
        <el-form-item label="内容">
          <div class="editor-container">
            <el-input
              v-model="form.content"
              type="textarea"
              :rows="20"
              placeholder="请输入 Markdown 格式的文章内容"
            />
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const saving = ref(false)
const isEdit = computed(() => !!route.params.id)

const form = reactive({
  title: '',
  summary: '',
  content: '',
  tags: [] as string[],
  isPublished: true
})

const tagOptions = ['Vue', 'React', 'TypeScript', 'Node.js', '前端', '后端', '数据库']

const fetchArticle = async () => {
  if (!isEdit.value) return
  
  const id = route.params.id as string
  
  // TODO: 调用 API 获取文章详情
  // const data = await request.get(`/articles/${id}`)
  
  // 模拟
  form.title = 'Vue 3 组合式 API 最佳实践'
  form.summary = '本文介绍 Vue 3 组合式 API 的使用方式和最佳实践'
  form.content = '# Vue 3 组合式 API 最佳实践\n\n## 什么是组合式 API？\n\n组合式 API 是 Vue 3 引入的一种新的代码组织方式。'
  form.tags = ['Vue', '前端']
  form.isPublished = true
}

const handleSave = async () => {
  if (!form.title.trim()) {
    ElMessage.warning('请输入文章标题')
    return
  }
  
  if (!form.content.trim()) {
    ElMessage.warning('请输入文章内容')
    return
  }
  
  saving.value = true
  try {
    // TODO: 调用 API 保存文章
    // if (isEdit.value) {
    //   await request.put(`/articles/${route.params.id}`, form)
    // } else {
    //   await request.post('/articles', form)
    // }
    
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success(isEdit.value ? '保存成功' : '发布成功')
    router.push('/knowledge')
  } catch (error) {
    console.error(error)
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchArticle()
})
</script>

<style lang="scss" scoped>
.knowledge-edit {
  .edit-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16px;
  }
  
  .edit-card {
    .editor-container {
      width: 100%;
      
      :deep(.el-textarea__inner) {
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 14px;
        line-height: 1.6;
      }
    }
  }
}
</style>
