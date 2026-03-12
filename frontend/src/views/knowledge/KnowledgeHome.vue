<template>
  <div class="knowledge-layout">
    <!-- 左侧分类导航 -->
    <aside class="left-sidebar">
      <CategoryNav @select="handleCategorySelect" />
      
      <!-- 模板选择器 -->
      <div class="template-section">
        <TemplateSelector @select="handleTemplateSelect" ref="templateRef" />
      </div>
    </aside>
    
    <!-- 中间主内容区 -->
    <main class="main-content">
      <div class="content-header">
        <div class="breadcrumb">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>知识库</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentCategory">
              {{ currentCategory.name }}
            </el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <h1 class="page-title">
          {{ currentCategory?.name || '全部文章' }}
          <span class="article-count">共 {{ total }} 篇</span>
        </h1>
      </div>
      
      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索知识库文章..."
          clearable
          size="large"
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        
        <el-button type="primary" size="large" @click="handleCreate">
          <el-icon><Plus /></el-icon>
          新建文章
        </el-button>
      </div>
      
      <!-- 筛选标签 -->
      <div class="filter-tags" v-if="selectedTemplate">
        <span class="filter-label">已选模板:</span>
        <el-tag type="primary" closable @close="clearTemplate">
          {{ selectedTemplate.name }}
        </el-tag>
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
                <div class="header-tags">
                  <el-tag v-if="article.category" size="small" type="info">
                    {{ article.category }}
                  </el-tag>
                  <el-tag v-if="article.isPublished" type="success" size="small">
                    已发布
                  </el-tag>
                  <el-tag v-else type="info" size="small">草稿</el-tag>
                </div>
              </div>
            </template>
            
            <p class="summary">{{ article.summary || '暂无摘要' }}</p>
            
            <div class="card-footer">
              <div class="author">
                <el-avatar :size="24" :src="''">{{ article.authorName?.[0] }}</el-avatar>
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
          layout="total, sizes, prev, pager, next, jumper"
          background
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </main>
    
    <!-- 右侧新闻侧边栏 -->
    <aside class="right-sidebar">
      <NewsSidebar />
    </aside>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Plus, View, Star } from '@element-plus/icons-vue'
import { formatDate } from '@/utils/format'
import type { Article } from '@/types/knowledge'

import CategoryNav from './components/CategoryNav.vue'
import NewsSidebar from './components/NewsSidebar.vue'
import TemplateSelector from './components/TemplateSelector.vue'

const router = useRouter()

// 状态
const loading = ref(false)
const searchKeyword = ref('')
const page = ref(1)
const pageSize = ref(12)
const total = ref(0)
const articleList = ref<Article[]>([])
const currentCategory = ref<{ id: number; name: string } | null>(null)
const selectedTemplate = ref<any>(null)
const templateRef = ref<InstanceType<typeof TemplateSelector> | null>(null)

// 模拟数据
const mockArticles: Article[] = [
  {
    id: 1,
    title: 'Vue 3 组合式 API 最佳实践',
    content: '',
    summary: '本文介绍 Vue 3 组合式 API 的使用方式和最佳实践，帮助开发者更好地组织代码。',
    authorId: 1,
    authorName: 'Bob',
    category: '前端开发',
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
    category: '前端开发',
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
    authorName: 'Alice',
    category: '前端开发',
    tags: ['Element Plus', 'UI'],
    viewCount: 89,
    likeCount: 8,
    isPublished: true,
    createdAt: '2026-03-08T09:00:00Z',
    updatedAt: '2026-03-08T09:00:00Z'
  },
  {
    id: 4,
    title: 'Kubernetes 集群部署实战',
    content: '',
    summary: '从零开始搭建 Kubernetes 生产环境集群，包含节点配置、网络策略和存储方案。',
    authorId: 2,
    authorName: 'Charlie',
    category: '云计算',
    tags: ['K8s', 'DevOps'],
    viewCount: 312,
    likeCount: 56,
    isPublished: true,
    createdAt: '2026-03-07T14:00:00Z',
    updatedAt: '2026-03-07T14:00:00Z'
  },
  {
    id: 5,
    title: 'AI Agent 在企业数字化中的应用',
    content: '',
    summary: '探讨 AI Agent 技术在企业场景中的落地实践，包括智能客服、知识管理等。',
    authorId: 2,
    authorName: 'Charlie',
    category: '人工智能',
    tags: ['AI', 'Agent', '数字化'],
    viewCount: 456,
    likeCount: 78,
    isPublished: true,
    createdAt: '2026-03-06T11:00:00Z',
    updatedAt: '2026-03-06T11:00:00Z'
  },
  {
    id: 6,
    title: '公司信息安全制度 V2.0',
    content: '',
    summary: '2026 年最新版公司信息安全管理制度，包含数据分类、访问控制等规范。',
    authorId: 3,
    authorName: 'David',
    category: '政策制度',
    tags: ['安全', '制度'],
    viewCount: 234,
    likeCount: 23,
    isPublished: true,
    createdAt: '2026-03-05T08:00:00Z',
    updatedAt: '2026-03-05T08:00:00Z'
  }
]

const fetchArticles = async () => {
  loading.value = true
  try {
    // TODO: 调用 API
    // const params = { page: page.value, pageSize: pageSize.value, keyword: searchKeyword.value, categoryId: currentCategory.value?.id }
    // const data = await request.get('/articles', { params })
    
    // 模拟
    await new Promise(resolve => setTimeout(resolve, 300))
    
    let filtered = [...mockArticles]
    if (currentCategory.value) {
      filtered = filtered.filter(a => a.category === currentCategory.value?.name)
    }
    if (searchKeyword.value) {
      const kw = searchKeyword.value.toLowerCase()
      filtered = filtered.filter(a => 
        a.title.toLowerCase().includes(kw) || 
        a.summary?.toLowerCase().includes(kw)
      )
    }
    
    articleList.value = filtered
    total.value = filtered.length
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
  if (selectedTemplate.value) {
    router.push({ 
      path: '/knowledge/edit', 
      query: { template: selectedTemplate.value.id } 
    })
  } else {
    router.push('/knowledge/edit')
  }
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

const handleCategorySelect = (category: { id: number; name: string }) => {
  currentCategory.value = category
  page.value = 1
  fetchArticles()
}

const handleTemplateSelect = (template: any) => {
  selectedTemplate.value = template
  ElMessage.success(`已应用模板: ${template.name}`)
}

const clearTemplate = () => {
  selectedTemplate.value = null
}

onMounted(() => {
  fetchArticles()
})
</script>

<style lang="scss" scoped>
.knowledge-layout {
  display: grid;
  grid-template-columns: 260px 1fr 300px;
  gap: 20px;
  max-width: 1600px;
  margin: 0 auto;
  padding: 20px;
  min-height: calc(100vh - 60px);
  
  .left-sidebar {
    display: flex;
    flex-direction: column;
    gap: 20px;
    
    .template-section {
      margin-top: 0;
    }
  }
  
  .main-content {
    .content-header {
      margin-bottom: 20px;
      
      .breadcrumb {
        margin-bottom: 8px;
      }
      
      .page-title {
        margin: 0;
        font-size: 24px;
        font-weight: 600;
        color: #0c2d6b;
        
        .article-count {
          font-size: 14px;
          font-weight: 400;
          color: #909399;
          margin-left: 12px;
        }
      }
    }
    
    .search-bar {
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
      
      .el-input {
        flex: 1;
        max-width: 500px;
      }
    }
    
    .filter-tags {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 16px;
      
      .filter-label {
        font-size: 14px;
        color: #606266;
      }
    }
    
    .article-cards {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 16px;
    }
    
    .article-card {
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
      
      &:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(12, 45, 107, 0.15);
      }
      
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 8px;
        
        .title {
          font-size: 16px;
          font-weight: 600;
          margin: 0;
          flex: 1;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          color: #0c2d6b;
        }
        
        .header-tags {
          display: flex;
          gap: 4px;
          flex-shrink: 0;
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
        margin-bottom: 12px;
        
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
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
      }
    }
    
    .pagination {
      margin-top: 24px;
      display: flex;
      justify-content: center;
    }
  }
  
  .right-sidebar {
    position: sticky;
    top: 20px;
    align-self: start;
  }
}

// 响应式
@media (max-width: 1400px) {
  .knowledge-layout {
    grid-template-columns: 240px 1fr 280px;
  }
}

@media (max-width: 1200px) {
  .knowledge-layout {
    grid-template-columns: 1fr;
    
    .left-sidebar {
      display: none;
    }
    
    .right-sidebar {
      display: none;
    }
  }
}
</style>
