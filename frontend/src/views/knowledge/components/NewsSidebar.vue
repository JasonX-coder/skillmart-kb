<template>
  <div class="news-sidebar">
    <div class="sidebar-header">
      <h3><el-icon><Notification /></el-icon> 行业资讯</h3>
      <el-button link type="primary" size="small" @click="refreshNews">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>
    
    <!-- 分类标签 -->
    <div class="category-tags">
      <el-tag
        v-for="cat in categories"
        :key="cat.id"
        :type="activeCategory === cat.id ? 'primary' : 'info'"
        size="small"
        effect="plain"
        @click="switchCategory(cat.id)"
      >
        {{ cat.name }}
      </el-tag>
    </div>
    
    <!-- 新闻列表 -->
    <div class="news-list">
      <div v-if="loading" class="loading-state">
        <el-skeleton :rows="3" animated />
      </div>
      
      <template v-else>
        <div
          v-for="item in newsList"
          :key="item.id"
          class="news-item"
          @click="openNews(item)"
        >
          <div class="news-meta">
            <el-tag :type="getTypeColor(item.category)" size="small">
              {{ item.category }}
            </el-tag>
            <span class="time">{{ formatTime(item.publishTime) }}</span>
          </div>
          <h4 class="news-title">{{ item.title }}</h4>
          <p class="news-summary">{{ item.summary }}</p>
        </div>
      </template>
    </div>
    
    <el-empty v-if="!loading && newsList.length === 0" description="暂无资讯" :image-size="60" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Notification, Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

interface NewsItem {
  id: number
  title: string
  summary: string
  category: string
  publishTime: string
  source: string
  url?: string
}

const loading = ref(false)
const activeCategory = ref<string | number>('all')

const categories = ref([
  { id: 'all', name: '全部' },
  { id: 'tech', name: '技术' },
  { id: 'business', name: '商业' },
  { id: 'policy', name: '政策' },
  { id: 'industry', name: '行业' }
])

// 模拟新闻数据
const mockNews: NewsItem[] = [
  {
    id: 1,
    title: 'AI 大模型在各行业加速落地，企业级应用成新蓝海',
    summary: '随着技术成熟度提升，AI 大模型正在从实验室走向企业实际应用场景...',
    category: '技术',
    publishTime: '2026-03-12T15:30:00Z',
    source: 'TechCrunch'
  },
  {
    id: 2,
    title: '国家发布新一代人工智能发展规划',
    summary: '国务院近日印发《新一代人工智能发展规划》，明确未来十年发展目标...',
    category: '政策',
    publishTime: '2026-03-12T10:00:00Z',
    source: '新华社'
  },
  {
    id: 3,
    title: '2026 年全球云计算市场规模将突破万亿美元',
    summary: '据 Gartner 最新报告，云计算服务需求持续强劲增长...',
    category: '行业',
    publishTime: '2026-03-11T20:00:00Z',
    source: 'Bloomberg'
  },
  {
    id: 4,
    title: '企业数字化转型进入深水区，AI Agent 成关键抓手',
    summary: '数字化转型正在从概念验证进入规模化落地阶段，AI Agent 成为企业新宠...',
    category: '商业',
    publishTime: '2026-03-11T14:00:00Z',
    source: '36Kr'
  },
  {
    id: 5,
    title: 'TypeScript 5.4 发布，带来多项语法糖与性能优化',
    summary: 'TypeScript 团队正式发布 5.4 版本，新增多项开发友好特性...',
    category: '技术',
    publishTime: '2026-03-10T09:00:00Z',
    source: 'InfoQ'
  }
]

const newsList = ref<NewsItem[]>([])

const fetchNews = async () => {
  loading.value = true
  try {
    // TODO: 调用真实 API
    // const { data } = await axios.get('/api/news', { params: { category: activeCategory.value } })
    
    // 模拟
    await new Promise(resolve => setTimeout(resolve, 500))
    if (activeCategory.value === 'all') {
      newsList.value = mockNews
    } else {
      const catMap: Record<string, string> = {
        tech: '技术',
        business: '商业',
        policy: '政策',
        industry: '行业'
      }
      newsList.value = mockNews.filter(n => n.category === catMap[activeCategory.value as string])
    }
  } catch (error) {
    ElMessage.error('获取资讯失败')
  } finally {
    loading.value = false
  }
}

const refreshNews = () => {
  fetchNews()
  ElMessage.success('资讯已刷新')
}

const switchCategory = (id: string | number) => {
  activeCategory.value = id
  fetchNews()
}

const getTypeColor = (category: string) => {
  const map: Record<string, string> = {
    '技术': 'danger',
    '商业': 'success',
    '政策': 'warning',
    '行业': 'primary'
  }
  return map[category] || 'info'
}

const formatTime = (time: string) => {
  const date = new Date(time)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const hours = Math.floor(diff / (1000 * 60 * 60))
  
  if (hours < 1) return '刚刚'
  if (hours < 24) return `${hours}h前`
  const days = Math.floor(hours / 24)
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString('zh-CN')
}

const openNews = (item: NewsItem) => {
  if (item.url) {
    window.open(item.url, '_blank')
  } else {
    ElMessage.info('详情页开发中...')
  }
}

onMounted(() => {
  fetchNews()
})
</script>

<style lang="scss" scoped>
.news-sidebar {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  
  .sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    padding-bottom: 12px;
    border-bottom: 2px solid #0c2d6b;
    
    h3 {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
      color: #0c2d6b;
      display: flex;
      align-items: center;
      gap: 6px;
    }
  }
  
  .category-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 16px;
    
    .el-tag {
      cursor: pointer;
      transition: all 0.2s;
      
      &:hover {
        transform: scale(1.05);
      }
    }
  }
  
  .news-list {
    .loading-state {
      padding: 12px 0;
    }
    
    .news-item {
      padding: 12px 0;
      border-bottom: 1px solid #f0f0f0;
      cursor: pointer;
      transition: all 0.2s;
      
      &:hover {
        .news-title {
          color: #005ea2;
        }
      }
      
      &:last-child {
        border-bottom: none;
      }
      
      .news-meta {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 6px;
        
        .time {
          font-size: 12px;
          color: #909399;
        }
      }
      
      .news-title {
        margin: 0 0 6px;
        font-size: 14px;
        font-weight: 500;
        color: #303133;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        transition: color 0.2s;
      }
      
      .news-summary {
        margin: 0;
        font-size: 12px;
        color: #909399;
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
    }
  }
}
</style>
