<template>
  <div class="category-nav">
    <div class="nav-header">
      <h3><el-icon><Folder /></el-icon> 文章分类</h3>
    </div>
    
    <el-tree
      :data="categoryTree"
      :props="treeProps"
      node-key="id"
      :expand-on-click-node="false"
      :default-expand-all="true"
      @node-click="handleNodeClick"
    >
      <template #default="{ node, data }">
        <div class="custom-tree-node">
          <span class="node-label">
            <el-icon v-if="data.icon"><component :is="data.icon" /></el-icon>
            {{ node.label }}
          </span>
          <el-badge
            v-if="data.count > 0"
            :value="data.count"
            :max="99"
            type="primary"
            class="node-badge"
          />
        </div>
      </template>
    </el-tree>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Folder, FolderOpened, Document, Setting, TrendCharts, School, Briefcase } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

interface CategoryNode {
  id: number
  name: string
  icon?: string
  count?: number
  children?: CategoryNode[]
}

const emit = defineEmits<{
  (e: 'select', category: CategoryNode): void
}>()

const treeProps = {
  children: 'children',
  label: 'name'
}

// 模拟分类数据
const categoryTree = ref<CategoryNode[]>([
  {
    id: 1,
    name: '技术',
    icon: 'Setting',
    count: 45,
    children: [
      { id: 11, name: '前端开发', count: 18 },
      { id: 12, name: '后端开发', count: 15 },
      { id: 13, name: '人工智能', count: 8 },
      { id: 14, name: '云计算', count: 4 }
    ]
  },
  {
    id: 2,
    name: '商业',
    icon: 'TrendCharts',
    count: 32,
    children: [
      { id: 21, name: '市场营销', count: 12 },
      { id: 22, name: '产品运营', count: 14 },
      { id: 23, name: '战略规划', count: 6 }
    ]
  },
  {
    id: 3,
    name: '政策',
    icon: 'Document',
    count: 20,
    children: [
      { id: 31, name: '法规解读', count: 12 },
      { id: 32, name: '行业标准', count: 8 }
    ]
  },
  {
    id: 4,
    name: '行业',
    icon: 'Briefcase',
    count: 28,
    children: [
      { id: 41, name: '动态趋势', count: 16 },
      { id: 42, name: '案例分析', count: 12 }
    ]
  },
  {
    id: 5,
    name: '培训',
    icon: 'School',
    count: 15,
    children: [
      { id: 51, name: '员工手册', count: 8 },
      { id: 52, name: '技能提升', count: 7 }
    ]
  }
])

const handleNodeClick = (data: CategoryNode) => {
  if (!data.children || data.children.length === 0) {
    emit('select', data)
    ElMessage.success(`已切换到: ${data.name}`)
  }
}
</script>

<style lang="scss" scoped>
.category-nav {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  
  .nav-header {
    padding-bottom: 12px;
    margin-bottom: 12px;
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
  
  :deep(.el-tree) {
    background: transparent;
    
    .el-tree-node__content {
      height: 36px;
      border-radius: 4px;
      margin-bottom: 2px;
      
      &:hover {
        background: #f5f7fa;
      }
    }
    
    .el-tree-node.is-current > .el-tree-node__content {
      background: #e6f0ff;
    }
    
    .el-tree-node__expand-icon {
      color: #0c2d6b;
      
      &.is-leaf {
        color: transparent;
      }
    }
  }
  
  .custom-tree-node {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding-right: 8px;
    
    .node-label {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 14px;
      color: #303133;
    }
    
    .node-badge {
      margin-right: 8px;
    }
  }
}
</style>
