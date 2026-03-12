<template>
  <el-container class="app-layout">
    <!-- 侧边栏 -->
    <el-aside :width="uiStore.sidebarVisible ? '200px' : '64px'" class="sidebar">
      <div class="logo">
        <el-icon v-if="uiStore.sidebarVisible" :size="24"><Collection /></el-icon>
        <span v-if="uiStore.sidebarVisible" class="logo-text">知识库</span>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        :collapse="!uiStore.sidebarVisible"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/knowledge">
          <el-icon><Document /></el-icon>
          <template #title>知识列表</template>
        </el-menu-item>
        
        <el-menu-item index="/profile">
          <el-icon><User /></el-icon>
          <template #title>个人中心</template>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <!-- 主体区域 -->
    <el-container>
      <!-- 头部 -->
      <el-header class="header">
        <div class="header-left">
          <el-icon class="collapse-btn" @click="uiStore.toggleSidebar">
            <Fold v-if="uiStore.sidebarVisible" />
            <Expand v-else />
          </el-icon>
        </div>
        
        <div class="header-right">
          <el-button type="primary" @click="handleCreate">
            <el-icon><Plus /></el-icon>
            <span>新建文章</span>
          </el-button>
          
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-avatar :size="32" :src="userAvatar">
                {{ authStore.userInfo?.username?.[0]?.toUpperCase() || 'U' }}
              </el-avatar>
              <span class="username">{{ authStore.userInfo?.username || '用户' }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <!-- 内容区域 -->
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Collection, Document, User, Fold, Expand, Plus } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUiStore()

const activeMenu = computed(() => route.path)

const userAvatar = '' // 可配置头像

const handleCreate = () => {
  router.push('/knowledge/edit')
}

const handleCommand = (command: string) => {
  if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'logout') {
    authStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }
}
</script>

<style lang="scss" scoped>
.app-layout {
  height: 100vh;
}

.sidebar {
  background: #304156;
  transition: width 0.3s;
  overflow: hidden;
  
  .logo {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    background: #263445;
    
    .logo-text {
      margin-left: 8px;
      font-size: 16px;
      font-weight: bold;
    }
  }
  
  .sidebar-menu {
    border-right: none;
    background: #304156;
    
    &:not(.el-menu--collapse) {
      width: 200px;
    }
  }
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  padding: 0 20px;
  
  .header-left {
    display: flex;
    align-items: center;
    
    .collapse-btn {
      font-size: 20px;
      cursor: pointer;
      color: #606266;
      
      &:hover {
        color: #409eff;
      }
    }
  }
  
  .header-right {
    display: flex;
    align-items: center;
    gap: 16px;
    
    .user-info {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      
      .username {
        color: #606266;
      }
    }
  }
}

.main-content {
  background: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}
</style>
