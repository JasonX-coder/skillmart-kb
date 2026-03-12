// 用户类型
export interface User {
  id: number
  username: string
  email: string
  nickname?: string
  avatar?: string
  role: 'admin' | 'user'
  createdAt: string
  updatedAt: string
}

// 登录请求
export interface LoginRequest {
  username: string
  password: string
}

// 注册请求
export interface RegisterRequest {
  username: string
  email: string
  password: string
  confirmPassword: string
}

// 登录响应
export interface LoginResponse {
  token: string
  user: User
}
