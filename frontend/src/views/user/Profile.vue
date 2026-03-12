<template>
  <div class="profile-page">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>个人中心</h2>
        </div>
      </template>
      
      <el-form :model="userForm" label-width="100px">
        <el-form-item label="头像">
          <el-avatar :size="80" :src="userForm.avatar">
            {{ userForm.username[0]?.toUpperCase() }}
          </el-avatar>
        </el-form-item>
        
        <el-form-item label="用户名">
          <el-input v-model="userForm.username" disabled />
        </el-form-item>
        
        <el-form-item label="邮箱">
          <el-input v-model="userForm.email" />
        </el-form-item>
        
        <el-form-item label="昵称">
          <el-input v-model="userForm.nickname" placeholder="请输入昵称" />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" :loading="saving" @click="handleSave">
            保存修改
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="stats-card">
      <template #header>
        <div class="card-header">
          <h2>数据统计</h2>
        </div>
      </template>
      
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-value">{{ stats.articleCount }}</div>
          <div class="stat-label">文章数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ stats.viewCount }}</div>
          <div class="stat-label">总浏览</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ stats.likeCount }}</div>
          <div class="stat-label">获赞数</div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const saving = ref(false)

const userForm = reactive({
  username: '',
  email: '',
  nickname: '',
  avatar: ''
})

const stats = reactive({
  articleCount: 0,
  viewCount: 0,
  likeCount: 0
})

const fetchUserInfo = async () => {
  // TODO: 调用 API 获取用户信息
  // const data = await request.get('/user/profile')
  
  // 模拟
  userForm.username = authStore.userInfo?.username || 'bob'
  userForm.email = authStore.userInfo?.email || 'bob@skillmart.com'
  userForm.nickname = '前端开发者'
  userForm.avatar = ''
  
  stats.articleCount = 3
  stats.viewCount = 473
  stats.likeCount = 65
}

const handleSave = async () => {
  saving.value = true
  try {
    // TODO: 调用 API 更新用户信息
    // await request.put('/user/profile', userForm)
    
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('保存成功')
  } catch (error) {
    console.error(error)
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchUserInfo()
})
</script>

<style lang="scss" scoped>
.profile-page {
  display: flex;
  gap: 20px;
  
  .profile-card {
    flex: 1;
  }
  
  .stats-card {
    width: 300px;
    
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      text-align: center;
      
      .stat-item {
        .stat-value {
          font-size: 24px;
          font-weight: 600;
          color: #409eff;
        }
        
        .stat-label {
          font-size: 13px;
          color: #909399;
          margin-top: 4px;
        }
      }
    }
  }
}
</style>
