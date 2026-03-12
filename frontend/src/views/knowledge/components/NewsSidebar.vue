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
        >
          <div class="news-header" @click="openNews(item)">
            <div class="news-meta">
              <el-tag :type="getTypeColor(item.category)" size="small">
                {{ item.category }}
              </el-tag>
              <span class="time">{{ formatTime(item.publish_time) }}</span>
            </div>
            <h4 class="news-title">{{ item.title }}</h4>
            <p class="news-summary">{{ item.summary }}</p>
          </div>
          
          <!-- 收藏按钮 -->
          <div class="news-actions">
            <el-button 
              type="primary" 
              size="small" 
              text
              @click.stop="openCollectionDialog(item)"
            >
              <el-icon><Star /></el-icon>
              收藏到知识库
            </el-button>
          </div>
        </div>
      </template>
    </div>
    
    <el-empty v-if="!loading && newsList.length === 0" description="暂无资讯" :image-size="60" />
    
    <!-- 收藏弹窗 -->
    <el-dialog
      v-model="collectionDialogVisible"
      title="收藏到知识库"
      width="500px"
      destroy-on-close
    >
      <el-form v-if="selectedNews" label-width="100px">
        <el-form-item label="新闻标题">
          <div class="news-preview-title">{{ selectedNews.title }}</div>
        </el-form-item>
        
        <el-form-item label="选择分类">
          <el-select v-model="collectionForm.category_id" placeholder="请选择分类" style="width: 100%">
            <el-option
              v-for="cat in categoryOptions"
              :key="cat.id"
              :label="cat.name"
              :value="String(cat.id)"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="选择模板">
          <el-select v-model="collectionForm.template_id" placeholder="可选模板" clearable style="width: 100%">
            <el-option
              v-for="tpl in templateOptions"
              :key="tpl.id"
              :label="tpl.name"
              :value="tpl.id"
            >
              <span>{{ tpl.name }}</span>
              <span style="color: #999; font-size: 12px; margin-left: 8px">{{ tpl.description }}</span>
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="collectionDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="saveToCollection">
          确认收藏
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Notification, Refresh, Star } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getNews } from '@/api/news'
import { createCollection } from '@/api/collection'

interface NewsItem {
  id: string
  title: string
  summary: string
  category: string
  publish_time: string
  source: string
  url?: string
}

interface CategoryOption {
  id: number
  name: string
}

interface TemplateOption {
  id: number
  name: string
  description: string
}

const loading = ref(false)
const activeCategory = ref<string | number>('all')
const newsList = ref<NewsItem[]>([])

// 收藏相关
const collectionDialogVisible = ref(false)
const selectedNews = ref<NewsItem | null>(null)
const saving = ref(false)
const collectionForm = ref({
  category_id: '',
  template_id: null as number | null
})

// 分类选项 - 与 CategoryNav 保持一致
const categoryOptions = ref<CategoryOption[]>([
  { id: 11, name: '前端开发' },
  { id: 12, name: '后端开发' },
  { id: 13, name: '人工智能' },
  { id: 14, name: '云计算' },
  { id: 21, name: '市场营销' },
  { id: 22, name: '产品运营' },
  { id: 23, name: '战略规划' },
  { id: 31, name: '法规解读' },
  { id: 32, name: '行业标准' },
  { id: 41, name: '动态趋势' },
  { id: 42, name: '案例分析' },
  { id: 51, name: '员工手册' },
  { id: 52, name: '技能提升' }
])

// 模板选项
const templateOptions = ref<TemplateOption[]>([
  { id: 1, name: '培训手册', description: '员工入职培训、操作指南' },
  { id: 2, name: 'FAQ', description: '常见问题解答' },
  { id: 3, name: '产品文档', description: '产品功能说明、使用手册' },
  { id: 4, name: '技术文档', description: 'API文档、技术方案' },
  { id: 5, name: '政策制度', description: '公司规章制度、政策文件' },
  { id: 6, name: '案例分析', description: '业务案例、经验总结' }
])

const categories = ref([
  { id: 'all', name: '全部' },
  { id: 'tech', name: '技术' },
  { id: 'business', name: '商业' },
  { id: 'policy', name: '政策' },
  { id: 'industry', name: '行业' }
])

const fetchNews = async (forceRefresh = false) => {
  loading.value = true
  try {
    const params: any = {}
    if (activeCategory.value !== 'all') {
      params.category = activeCategory.value
    }
    if (forceRefresh) {
      params.refresh = true
    }
    
    const data = await getNews(params)
    newsList.value = data || []
  } catch (error) {
    console.error('获取资讯失败:', error)
    ElMessage.error('获取资讯失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const refreshNews = () => {
  fetchNews(true)
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

// 打开收藏弹窗
const openCollectionDialog = (item: NewsItem) => {
  selectedNews.value = item
  collectionForm.value = {
    category_id: '',
    template_id: null
  }
  collectionDialogVisible.value = true
}

// 保存到收藏
const saveToCollection = async () => {
  if (!selectedNews.value) return
  
  if (!collectionForm.value.category_id) {
    ElMessage.warning('请选择分类')
    return
  }
  
  saving.value = true
  try {
    const category = categoryOptions.value.find(c => String(c.id) === collectionForm.value.category_id)
    const template = templateOptions.value.find(t => t.id === collectionForm.value.template_id)
    
    await createCollection({
      news_id: selectedNews.value.id,
      news_title: selectedNews.value.title,
      news_summary: selectedNews.value.summary,
      news_category: selectedNews.value.category,
      news_source: selectedNews.value.source,
      news_url: selectedNews.value.url || '',
      news_publish_time: selectedNews.value.publish_time,
      category_id: collectionForm.value.category_id,
      category_name: category?.name || '',
      template_id: collectionForm.value.template_id || undefined,
      template_name: template?.name
    })
    
    ElMessage.success('收藏成功！')
    collectionDialogVisible.value = false
  } catch (error: any) {
    console.error('收藏失败:', error)
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('收藏失败，请稍后重试')
    }
  } finally {
    saving.value = false
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
      
      &:last-child {
        border-bottom: none;
      }
      
      .news-header {
        cursor: pointer;
        transition: all 0.2s;
        
        &:hover {
          .news-title {
            color: #005ea2;
          }
        }
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
      
      .news-actions {
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px dashed #f0f0f0;
        
        .el-button {
          font-size: 12px;
        }
      }
    }
  }
}

.news-preview-title {
  font-size: 14px;
  color: #303133;
  line-height: 1.5;
  word-break: break-all;
}

:deep(.el-dialog__body) {
  padding-top: 16px;
}
</style>
