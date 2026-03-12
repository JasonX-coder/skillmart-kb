// 知识库文章
export interface Article {
  id: number
  title: string
  content: string
  summary?: string
  authorId: number
  authorName: string
  categoryId?: number
  categoryName?: string
  tags: string[]
  viewCount: number
  likeCount: number
  isPublished: boolean
  createdAt: string
  updatedAt: string
}

// 文章列表查询参数
export interface ArticleQueryParams {
  page: number
  pageSize: number
  keyword?: string
  categoryId?: number
  tag?: string
  isPublished?: boolean
}

// 文章列表响应
export interface ArticleListResponse {
  list: Article[]
  total: number
  page: number
  pageSize: number
}

// 创建/更新文章请求
export interface ArticleRequest {
  title: string
  content: string
  summary?: string
  categoryId?: number
  tags?: string[]
  isPublished: boolean
}

// 分类
export interface Category {
  id: number
  name: string
  parentId?: number
  sort: number
  createdAt: string
}

// 标签
export interface Tag {
  id: number
  name: string
  count: number
}
