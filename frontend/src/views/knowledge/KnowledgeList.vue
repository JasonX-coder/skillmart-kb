<template>
  <div class="knowledge-list">
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索知识库..."
        clearable
        @clear="handleSearch"
        @keyup.enter="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
        <template #append>
          <el-button :icon="Search" @click="handleSearch" />
        </template>
      </el-input>
      
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新建文章
      </el-button>
    </div>
    
    <!-- 文章列表 -->
    <div class="article-list">
      <el-empty v-if="!loading && articleList.length === 0" description="暂无知识文章" />
      
      <div v-else class="article-cards">
        <el-card
          v-for="article in articleList"
          :key="article.id"
          class="article-card"
          shadow="hover"
          @click="handleView(article.id)"
        >
          <template #header>
            <div class="card-header">
              <h3 class="title">{{ article.title }}</h3>
              <el-tag v-if="article.isPublished" type="success" size="small">已发布</el-tag>
              <el-tag v-else type="info" size="small">草稿</el-tag>
            </div>
          </template>
          
          <p class="summary">{{ article.summary || '暂无摘要' }}</p>
          
          <div class="card-footer">
            <div class="author">
              <el-avatar :size="20" :src="''">{{ article.authorName[0] }}</el-avatar>
              <span>{{ article.authorName }}</span>
            </div>
            <div class="meta">
              <span><el-icon><View /></el-icon> {{ article.viewCount }}</span>
              <span><el-icon><Star /></el-icon> {{ article.likeCount }}</span>
              <span>{{ formatDate(article.createdAt) }}</span>
            </div>
          </div>
          
          <div v-if="article.tags?.length" class="tags">
            <el-tag v-for="tag in article.tags" :key="tag" size="small" type="info">
              {{ tag }}
            </el-tag>
          </div>
        </el-card>
      </div>
    </div>
    
    <!-- 分页 -->
    <div v-if="total > 0" class="pagination">
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Plus, View, Star } from '@element-plus/icons-vue'
import { formatDate } from '@/utils/format'
import type { Article, ArticleQueryParams } from '@/types/knowledge'

const router = useRouter()

const loading = ref(false)
const searchKeyword = ref('')
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const articleList = ref<Article[]>([])

// 模拟数据
const mockArticles: Article[] = [
  {
    id: 1,
    title: 'Vue 3 组合式 API 最佳实践',
    content: '',
    summary: '本文介绍 Vue 3 组合式 API 的使用方式和最佳实践，帮助开发者更好地组织代码。',
    authorId: 1,
    authorName: 'Bob',
    tags: ['Vue', '前端'],
    viewCount: 128,
    likeCount: 12,
    isPublished: true,
    createdAt: '2026-03-10T10:00:00Z',
    updatedAt: '2026-03-10T10:00:00Z'
  },
  {
    id: 2,
    title: 'TypeScript 入门指南',
    content: '',
    summary: 'TypeScript 是 JavaScript 的超集，本文带你快速入门 TypeScript 开发。',
    authorId: 1,
    authorName: 'Bob',
    tags: ['TypeScript', '前端'],
    viewCount: 256,
    likeCount: 45,
    isPublished: true,
    createdAt: '2026-03-09T15:30:00Z',
    updatedAt: '2026-03-09T15:30:00Z'
  },
  {
    id: 3,
    title: 'Element Plus 组件使用笔记',
    content: '',
    summary: 'Element Plus 是 Vue 3 的企业级 UI 组件库，本文记录了常用组件的使用方法。',
    authorId: 1,
    authorName: 'Bob',
    tags: ['Element Plus', 'UI'],
    viewCount: 89,
    likeCount: 8,
    isPublished: true,
    createdAt: '2026-03-08T09:00:00Z',
    updatedAt: '2026-03-08T09:00:00Z'
  }
]

const fetchArticles = async () => {
  loading.value = true
  try {
    // TODO: 调用 API 获取文章列表
    // const params: ArticleQueryParams = {
    //   page: page.value,
    //   pageSize: pageSize.value,
    //   keyword: searchKeyword.value
    // }
    // const data = await request.get('/articles', { params })
    
    // 模拟
    articleList.value = mockArticles
    total.value = mockArticles.length
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  page.value = 1
  fetchArticles()
}

const handleCreate = () => {
  router.push('/knowledge/edit')
}

const handleView = (id: number) => {
  router.push(`/knowledge/${id}`)
}

const handlePageChange = (val: number) => {
  page.value = val
  fetchArticles()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  page.value = 1
  fetchArticles()
}

onMounted(() => {
  fetchArticles()
})
</script>

<style lang="scss" scoped>
.knowledge-list {
  .search-bar {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    
    .el-input {
      max-width: 400px;
    }
  }
  
  .article-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
  }
  
  .article-card {
    cursor: pointer;
    transition: transform 0.2s;
    
    &:hover {
      transform: translateY(-4px);
    }
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .title {
        font-size: 16px;
        font-weight: 600;
        margin: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
    }
    
    .summary {
      color: #606266;
      font-size: 14px;
      line-height: 1.6;
      margin-bottom: 12px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    
    .card-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
      color: #909399;
      
      .author {
        display: flex;
        align-items: center;
        gap: 6px;
      }
      
      .meta {
        display: flex;
        gap: 12px;
        
        span {
          display: flex;
          align-items: center;
          gap: 4px;
        }
      }
    }
    
    .tags {
      margin-top: 12px;
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
    }
  }
  
  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>
