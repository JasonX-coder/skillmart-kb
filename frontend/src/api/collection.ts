import { request } from './index'

// 收藏类型定义
export interface CollectionCreate {
  news_id: string
  news_title: string
  news_summary: string
  news_category: string
  news_source: string
  news_url?: string
  news_publish_time: string
  category_id: string
  category_name: string
  template_id?: number
  template_name?: string
}

export interface Collection {
  id: string
  news_id: string
  news_title: string
  news_summary: string
  news_category: string
  news_source: string
  news_url: string
  news_publish_time: string
  category_id: string
  category_name: string
  template_id: number | null
  template_name: string
  created_at: string
}

// 创建收藏
export const createCollection = (data: CollectionCreate) => {
  return request.post<Collection>('/collections', data)
}

// 获取收藏列表
export const getCollections = (params?: { category_id?: string; page?: number; page_size?: number }) => {
  return request.get<Collection[]>('/collections', { params })
}

// 删除收藏
export const deleteCollection = (id: string) => {
  return request.delete(`/collections/${id}`)
}

// 获取收藏分类统计
export const getCollectionCategories = () => {
  return request.get<{ category_id: string; category_name: string; count: number }[]>('/collections/categories')
}
