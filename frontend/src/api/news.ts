import { request } from './index'

// 新闻类型定义
export interface NewsItem {
  id: string
  title: string
  summary: string
  category: string
  publish_time: string
  source: string
  url?: string
}

export interface NewsCategory {
  id: string
  name: string
}

// 获取新闻列表
export const getNews = (params?: { category?: string; refresh?: boolean }) => {
  return request.get<NewsItem[]>('/news', { params })
}

// 获取新闻分类
export const getNewsCategories = () => {
  return request.get<NewsCategory[]>('/news/categories')
}
