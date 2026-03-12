<template>
  <div class="knowledge-detail">
    <el-button class="back-btn" @click="router.back()">
      <el-icon><ArrowLeft /></el-icon>
      返回
    </el-button>
    
    <el-card v-if="article" class="detail-card">
      <template #header>
        <div class="header">
          <h1>{{ article.title }}</h1>
        </div>
      </template>
      
      <div class="meta">
        <span class="time">发布于 {{ article.createdAt }}</span>
      </div>
      
      <el-divider />
      
      <div class="content">
        {{ article.content }}
      </div>
    </el-card>
    
    <el-empty v-else description="文章不存在" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const article = ref<any>(null)

const fetchArticle = async () => {
  const id = route.params.id as string
  
  // TODO: 调用 API 获取文章详情
  // const data = await request.get(`/articles/${id}`)
  
  // 模拟数据
  article.value = {
    id: Number(id),
    title: '示例文章',
    content: '这是文章内容...',
    createdAt: new Date().toLocaleDateString()
  }
}

onMounted(() => {
  fetchArticle()
})
</script>

<style lang="scss" scoped>
.knowledge-detail {
  padding: 20px;
}

.back-btn {
  margin-bottom: 20px;
}

.detail-card {
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    h1 {
      margin: 0;
      font-size: 20px;
    }
  }
  
  .meta {
    color: #909399;
    font-size: 14px;
  }
  
  .content {
    line-height: 1.8;
    white-space: pre-wrap;
  }
}
</style>
