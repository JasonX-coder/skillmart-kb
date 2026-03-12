# 企业知识库助手 - 技术架构设计

> 版本：v1.0 | 作者：David（技术总监）| 日期：2026-03-11

---

## 1. 系统架构图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              客户端层 (Client)                               │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        Web 端 (React + TypeScript)                   │    │
│  │   • 用户界面    • 文档上传    • 问答交互    • 历史记录              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼ HTTPS/REST API
┌─────────────────────────────────────────────────────────────────────────────┐
│                              服务端层 (Backend)                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      FastAPI 应用服务器                             │    │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │    │
│  │   │ 认证模块 │  ││ 文档管理API │ 问答 API │  │用户管理  │          │    │
│  │   └──────────┘  └──────────┘  └──────────┘  └──────────┘          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                      │                                       │
│         ┌────────────────────────────┼────────────────────────────┐        │
│         ▼                            ▼                            ▼        │
│  ┌─────────────┐            ┌─────────────────┐           ┌─────────────┐   │
│  │  文件存储   │            │   向量数据库    │           │  关系数据库  │   │
│  │ (MinIO/本地)│            │    (Chroma)     │           │  (PostgreSQL)│   │
│  └─────────────┘            └─────────────────┘           └─────────────┘   │
│                                                                              │
│         ┌─────────────────────────────────────────────────────────────┐     │
│         │                    LLM 服务层                                │     │
│  │  OpenAI API (GPT-4) / Ollama (本地模型)  │     嵌入模型 (text-embedding) │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 技术选型

### 2.1 前端技术栈

| 技术 | 选择 | 理由 |
|------|------|------|
| 框架 | React 18 | 生态成熟，组件化开发效率高 |
| 语言 | TypeScript | 类型安全，减少运行时错误 |
| UI 组件库 | Ant Design 5.x | 企业级组件库，文档完善 |
| 状态管理 | Zustand | 轻量级，API 简洁 |
| HTTP 客户端 | Axios | 拦截器支持好，配置灵活 |
| 构建工具 | Vite | 开发启动快，热更新优秀 |

### 2.2 后端技术栈

| 技术 | 选择 | 理由 |
|------|------|------|
| Web 框架 | FastAPI | 异步高性能，自动生成 API 文档 |
| 语言 | Python 3.11 | AI/ML 生态丰富 |
| ORM | SQLAlchemy 2.0 | 类型安全，迁移方便 |
| 认证 | JWT + Passlib | 轻量级 stateless 认证 |
| 文件处理 | python-docx, pypdf2 | 支持多种文档格式 |
| 向量数据库 | Chroma | 轻量易用，MVP 阶段首选 |
| LLM 集成 | LangChain | 统一封装多种 LLM |
| 任务队列 | Celery + Redis | 异步处理文档解析和向量化 |

### 2.3 基础设施

| 组件 | 选择 | 说明 |
|------|------|------|
| 数据库 | PostgreSQL 15 | 关系型数据存储 |
| 向量库 | Chroma (本地) | MVP 阶段使用 |
| 对象存储 | MinIO | 自托管对象存储（可替代 AWS S3） |
| 缓存 | Redis | Session + 缓存 |
| 容器 | Docker | 一键部署 |
| 反向代理 | Nginx | 负载均衡 + SSL |

---

## 3. API 设计

### 3.1 认证模块

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/auth/register` | 用户注册 |
| POST | `/api/auth/login` | 用户登录 |
| POST | `/api/auth/refresh` | 刷新 Token |
| GET | `/api/auth/me` | 获取当前用户信息 |

### 3.2 文档管理模块

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/documents` | 获取文档列表 |
| POST | `/api/documents` | 上传文档 |
| GET | `/api/documents/{id}` | 获取文档详情 |
| DELETE | `/api/documents/{id}` | 删除文档 |
| PUT | `/api/documents/{id}/tags` | 更新文档标签 |

### 3.3 问答模块

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/qa/ask` | 提问（返回流式响应） |
| GET | `/api/qa/history` | 获取问答历史 |
| DELETE | `/api/qa/history/{id}` | 删除单条记录 |

### 3.4 核心接口示例

#### 3.4.1 提问接口

```json
// POST /api/qa/ask
Request:
{
  "question": "如何申请年假？",
  "document_ids": ["doc_123", "doc_456"],  // 可选，指定范围
  "top_k": 3  // 返回Top-K个相关片段
}

Response (SSE 流式):
{
  "answer": "根据公司制度，员工年假申请流程如下：...",
  "sources": [
    {
      "document_id": "doc_123",
      "chunk_content": "年假申请需提前...",
      "score": 0.92
    }
  ]
}
```

#### 3.4.2 文档上传接口

```json
// POST /api/documents
Request (multipart/form-data):
{
  "file": "<binary>",
  "tags": ["HR", "政策"],
  "category": "管理制度"
}

Response:
{
  "id": "doc_789",
  "filename": "员工手册.pdf",
  "status": "processing",
  "message": "文档上传成功，正在处理中..."
}
```

---

## 4. 数据库设计

### 4.1 数据模型

```sql
-- 用户表
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- 文档表
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(20) NOT NULL,  -- pdf, docx, txt, md
    file_size BIGINT NOT NULL,
    category VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',  -- pending, processing, completed, failed
    chunk_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 文档标签表
CREATE TABLE document_tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    tag VARCHAR(50) NOT NULL,
    UNIQUE(document_id, tag)
);

-- 问答历史表
CREATE TABLE qa_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT,
    sources JSONB,  -- 存储引用来源
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 向量数据存储在 Chroma
-- Collection: documents
-- Fields: document_id, chunk_text, chunk_index, embedding
```

### 4.2 ER 关系图

```
┌──────────┐       ┌─────────────┐       ┌────────────┐
│  users   │       │ documents   │       │ qa_history │
├──────────┤       ├─────────────┤       ├────────────┤
│ id (PK)  │◄──────│ user_id(FK) │       │ user_id(FK)│
│ username │       │ id (PK)     │       │ id (PK)    │
│ email    │       │ filename    │       │ question   │
│ password │       │ file_path   │       │ answer     │
└──────────┘       │ category    │       │ sources    │
                   └─────────────┘       └────────────┘
                         │
                         │ 1:N
                         ▼
                   ┌───────────────┐
                   │document_tags  │
                   ├───────────────┤
                   │ document_id(FK)│
                   │ tag           │
                   └───────────────┘
```

---

## 5. 部署方案

### 5.1 环境规划

| 环境 | 用途 | 部署方式 |
|------|------|----------|
| 开发 | 本地开发调试 | Docker Compose |
| 测试 | 集成测试 | Docker Compose |
| 生产 | 正式环境 | K8s / 云服务器 |

### 5.2 Docker Compose 开发环境

```yaml
version: '3.8'

services:
  # 前端
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000

  # 后端
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/knowledge_base
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
      - redis

  # 关系数据库
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=knowledge_base
    volumes:
      - pgdata:/var/lib/postgresql/data

  # 缓存
  redis:
    image: redis:7-alpine

  # 向量数据库
  chroma:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"

  # 对象存储
  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    ports:
      - "9000:9000"
      - "9001:9001"

volumes:
  pgdata:
```

### 5.3 生产部署建议

#### 5.3.1 架构

```
                    ┌─────────────┐
                    │   CDN       │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Nginx     │
                    │  (SSL终结)  │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌─────────┐  ┌─────────┐  ┌─────────┐
        │Backend-1│  │Backend-2│  │Backend-3│  (多实例)
        └────┬────┘  └────┬────┘  └────┬────┘
             │            │            │
        ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
        │PostgreSQL│  │  Redis  │  │  MinIO  │
        │ (主从)   │  │ (集群)  │  │ (分布式)│
        └─────────┘  └─────────┘  └─────────┘
                           │
                      ┌────▼────┐
                      │ Chroma  │
                      │(集群)   │
                      └─────────┘
```

#### 5.3.2 推荐配置

| 组件 | 配置 | 说明 |
|------|------|------|
| Backend | 2-4 CPU, 4-8 GB | 根据并发量调整 |
| PostgreSQL | 2 CPU, 4 GB | 主从部署 |
| Redis | 1 CPU, 2 GB | 缓存 + Session |
| MinIO | 2-4 CPU, 按需存储 | 分布式模式 |
| Chroma | 2-4 CPU, 8-16 GB | 视文档量而定 |

---

## 6. 安全考虑

- [ ] JWT Token 过期时间设置（建议 24h）
- [ ] 密码加密存储（bcrypt）
- [ ] API 限流防护
- [ ] 文件上传类型白名单
- [ ] 文件大小限制（建议 50MB）
- [ ] HTTPS 全站加密
- [ ] 敏感数据脱敏日志

---

## 7. 下一步工作

1. **详细设计**：细化各模块的数据库表结构
2. **接口定义**：编写 OpenAPI/Swagger 文档
3. **技术验证**：POC 验证文档向量化和问答效果
4. **开发计划**：拆解 Sprint 任务

---

*如有疑问，请随时沟通。*
