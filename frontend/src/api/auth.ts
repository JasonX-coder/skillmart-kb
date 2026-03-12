// 认证 API
import request from '@/api'

// 登录
export interface LoginParams {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export const login = (data: LoginParams) => {
  // FastAPI OAuth2PasswordRequestForm 需要 form-data 格式
  const formData = new FormData()
  formData.append('username', data.username)
  formData.append('password', data.password)
  return request.post<LoginResponse>('/auth/login', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

// 注册
export interface RegisterParams {
  username: string
  email: string
  password: string
  full_name?: string
}

export interface UserInfo {
  id: string
  username: string
  email: string
  full_name?: string
  is_active: boolean
  created_at: string
}

export const register = (data: RegisterParams) => {
  return request.post<UserInfo>('/auth/register', data)
}

// 获取当前用户信息
export const getCurrentUser = () => {
  return request.get<UserInfo>('/auth/me')
}
