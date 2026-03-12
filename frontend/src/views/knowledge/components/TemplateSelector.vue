<template>
  <div class="template-selector">
    <div class="selector-header">
      <h3><el-icon><Document /></el-icon> 知识库模板</h3>
      <el-button link type="primary" size="small" @click="showAllTemplates">
        查看全部
      </el-button>
    </div>
    
    <div class="template-grid">
      <div
        v-for="template in templates"
        :key="template.id"
        class="template-card"
        :class="{ active: selectedId === template.id }"
        @click="selectTemplate(template)"
      >
        <div class="template-icon" :style="{ background: template.color }">
          <el-icon :size="24"><component :is="template.icon" /></el-icon>
        </div>
        <div class="template-info">
          <h4>{{ template.name }}</h4>
          <p>{{ template.description }}</p>
        </div>
        <el-tag v-if="selectedId === template.id" type="success" size="small" class="selected-tag">
          已选择
        </el-tag>
      </div>
    </div>
    
    <!-- 模板预览弹窗 -->
    <el-dialog
      v-model="previewVisible"
      title="模板预览"
      width="700px"
      destroy-on-close
    >
      <div v-if="previewTemplate" class="template-preview">
        <div class="preview-header">
          <div class="preview-icon" :style="{ background: previewTemplate.color }">
            <el-icon :size="32"><component :is="previewTemplate.icon" /></el-icon>
          </div>
          <div>
            <h2>{{ previewTemplate.name }}</h2>
            <p>{{ previewTemplate.description }}</p>
          </div>
        </div>
        
        <el-divider />
        
        <div class="preview-content">
          <h4>预设结构：</h4>
          <ul>
            <li v-for="(item, index) in previewTemplate.structure" :key="index">
              {{ item }}
            </li>
          </ul>
        </div>
        
        <div class="preview-fields">
          <h4>元数据字段：</h4>
          <div class="field-tags">
            <el-tag v-for="field in previewTemplate.fields" :key="field" size="small">
              {{ field }}
            </el-tag>
          </div>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="previewVisible = false">关闭</el-button>
        <el-button type="primary" @click="applyTemplate">使用此模板</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Document, School, QuestionFilled, Box, Files, Collection, Scale } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

interface Template {
  id: number
  name: string
  description: string
  icon: string
  color: string
  structure: string[]
  fields: string[]
}

const emit = defineEmits<{
  (e: 'select', template: Template): void
}>()

const selectedId = ref<number | null>(null)
const previewVisible = ref(false)
const previewTemplate = ref<Template | null>(null)

const templates = ref<Template[]>([
  {
    id: 1,
    name: '培训手册',
    description: '员工入职培训、操作指南',
    icon: 'School',
    color: '#409eff',
    structure: ['培训目标', '培训内容', '操作步骤', '考核标准', '常见问题'],
    fields: ['培训类型', '适用对象', '培训时长', '考核方式']
  },
  {
    id: 2,
    name: 'FAQ',
    description: '常见问题解答',
    icon: 'QuestionFilled',
    color: '#67c23a',
    structure: ['问题描述', '问题原因', '解决方案', '相关链接'],
    fields: ['问题分类', '关键词', 'FAQ编号', '浏览次数']
  },
  {
    id: 3,
    name: '产品文档',
    description: '产品功能说明、使用手册',
    icon: 'Box',
    color: '#e6a23c',
    structure: ['产品概述', '功能介绍', '使用教程', '版本记录'],
    fields: ['产品名称', '版本号', '适用平台', '文档状态']
  },
  {
    id: 4,
    name: '技术文档',
    description: 'API文档、技术方案',
    icon: 'Files',
    color: '#909399',
    structure: ['概述', '技术架构', '接口说明', '代码示例', '部署指南'],
    fields: ['技术栈', 'API版本', '维护人', '文档类型']
  },
  {
    id: 5,
    name: '政策制度',
    description: '公司规章制度、政策文件',
    icon: 'Scale',
    color: '#f56c6c',
    structure: ['制度目的', '适用范围', '具体条款', '违规处理', '修订记录'],
    fields: ['制度类型', '发布部门', '生效日期', '保密等级']
  },
  {
    id: 6,
    name: '案例分析',
    description: '业务案例、经验总结',
    icon: 'Collection',
    color: '#8e44ad',
    structure: ['案例背景', '问题分析', '解决方案', '实施效果', '经验教训'],
    fields: ['案例类型', '行业领域', '项目周期', '成果指标']
  }
])

const selectTemplate = (template: Template) => {
  selectedId.value = template.id
  emit('select', template)
  ElMessage.success(`已选择模板: ${template.name}`)
}

const showAllTemplates = () => {
  previewVisible.value = true
  previewTemplate.value = null
}

const applyTemplate = () => {
  if (previewTemplate.value) {
    selectedId.value = previewTemplate.value.id
    emit('select', previewTemplate.value)
    ElMessage.success('模板应用成功')
  }
  previewVisible.value = false
}

// 预览指定模板
const previewTemplateById = (id: number) => {
  previewTemplate.value = templates.value.find(t => t.id === id) || null
  previewVisible.value = true
}

defineExpose({
  previewTemplateById
})
</script>

<style lang="scss" scoped>
.template-selector {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  
  .selector-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 12px;
    margin-bottom: 16px;
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
  
  .template-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .template-card {
    position: relative;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px;
    border: 1px solid #ebeef5;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
    
    &:hover {
      border-color: #0c2d6b;
      box-shadow: 0 2px 8px rgba(12, 45, 107, 0.1);
    }
    
    &.active {
      border-color: #0c2d6b;
      background: #f5f8ff;
    }
    
    .template-icon {
      flex-shrink: 0;
      width: 40px;
      height: 40px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
    }
    
    .template-info {
      flex: 1;
      min-width: 0;
      
      h4 {
        margin: 0 0 4px;
        font-size: 14px;
        font-weight: 600;
        color: #303133;
      }
      
      p {
        margin: 0;
        font-size: 12px;
        color: #909399;
        line-height: 1.4;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
    }
    
    .selected-tag {
      position: absolute;
      top: 8px;
      right: 8px;
    }
  }
}

.template-preview {
  .preview-header {
    display: flex;
    align-items: center;
    gap: 16px;
    
    .preview-icon {
      width: 64px;
      height: 64px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
    }
    
    h2 {
      margin: 0 0 4px;
      font-size: 20px;
      color: #0c2d6b;
    }
    
    p {
      margin: 0;
      color: #606266;
    }
  }
  
  .preview-content {
    margin-bottom: 20px;
    
    h4 {
      margin: 0 0 12px;
      color: #303133;
    }
    
    ul {
      margin: 0;
      padding-left: 20px;
      
      li {
        line-height: 2;
        color: #606266;
      }
    }
  }
  
  .preview-fields {
    h4 {
      margin: 0 0 12px;
      color: #303133;
    }
    
    .field-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
  }
}
</style>
