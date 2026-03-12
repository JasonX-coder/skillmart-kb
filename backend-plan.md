# 企业知识库助手 - 后端技术调研报告

> 调研人：Charlie（后端开发工程师）
> 日期：2026-03-11

---

## 一、框架选型：FastAPI vs Django

### 1.1 核心对比

| 特性 | FastAPI | Django |
|------|---------|--------|
| **定位** | 现代高性能 Web 框架 | 全栈 Web 框架 |
| **异步支持** | 原生异步 (ASGI) | 同步为主 (WSGI)，需额外配置 |
| **性能** | ⭐⭐⭐⭐⭐ 极高 | ⭐⭐⭐ 中等 |
| **学习曲线** | ⭐⭐ 较低 | ⭐⭐⭐ 较陡 |
| **生态系统** | 较新，依赖 Starlette | 成熟完整 |
| **REST API** | 自动生成 OpenAPI/Swagger | 需 DRF 支持 |
| **数据验证** | Pydantic 原生支持 | Django Forms/Serializer |
| **适用场景** | 微服务、API 服务、ML 应用 | 全栈项目、内容管理系统 |

### 1.2 推荐方案：**FastAPI**

**推荐理由：**

1. **高性能**：异步非阻塞架构，吞吐量远高于 Django
2. **现代化**：专为 AI/LLM 应用设计，与 Python 生态完美融合
3. **开发效率**：自动生成 API 文档，类型提示支持 IDE 智能提示
4. **轻量灵活**：无冗余组件，按需引入
5. **LLM 友好**：Starlette 生态丰富，易于集成 LangChain、LlamaIndex 等

**适用场景匹配度：**
- 企业知识库助手需要快速响应、高并发
- 需要对接多种 LLM 和向量数据库
- API 优先的后端服务

---

## 二、向量数据库：Chroma vs Milvus

### 2.1 核心对比

| 特性 | Chroma | Milvus |
|------|--------|--------|
| **定位** | 轻量级嵌入式向量库 | 企业级分布式向量数据库 |
| **架构** | 嵌入式 (SQLite) | 独立服务 (K8s/Docker) |
| **规模** | 适合中小规模 (<100万向量) | 支持十亿级向量 |
| **部署复杂度** | ⭐ 低（Python 库即用） | ⭐⭐⭐⭐ 高 |
| **查询性能** | ⭐⭐⭐ 中等 | ⭐⭐⭐⭐⭐ 卓越 |
| **数据持久化** | 本地文件/对象存储 | 分布式存储 |
| **云原生** | 一般 | 优秀 |
| **Stars** | ~26.5k | ~43.3k |

### 2.2 推荐方案：**Chroma (MVP 阶段)**

**推荐理由：**

1. **快速启动**：pip install chromadb 即可使用，无需额外部署
2. **开箱即用**：内置文本嵌入功能，集成 LlamaIndex/LangChain 方便
3. **轻量灵活**：嵌入式数据库，开发体验好，调试简单
4. **成本可控**：MVP 阶段无需投入运维资源
5. **社区活跃**：AI 应用开发首选向量库，文档丰富

**迁移路径：**
- MVP 阶段：Chroma 快速验证
- 规模化阶段：可平滑迁移至 Milvus 或 Pinecone

---

## 三、LLM 对接：OpenAI API 调用方案

### 3.1 架构设计

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Client    │────▶│   FastAPI    │────▶│  Vector DB  │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   OpenAI     │
                    │    API       │
                    └──────────────┘
```

### 3.2 核心实现方案

#### 3.2.1 基础调用（OpenAI SDK）

```python
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def chat_completion(prompt: str, context: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你是一个企业知识库助手..."},
            {"role": "user", "content": f"参考上下文：{context}\n\n问题：{prompt}"}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    return response.choices[0].message.content
```

#### 3.2.2 RAG（检索增强生成）流程

```python
# 1. 文档向量化存储
def add_document(text: str, metadata: dict):
    embeddings = OpenAIEmbeddings()
    doc_chunks = text_splitter.split_text(text)
    
    for i, chunk in enumerate(doc_chunks):
        chroma_client.add(
            documents=[chunk],
            ids=[f"doc_{metadata['id']}_chunk_{i}"],
            embeddings=[embeddings.embed_query(chunk)],
            metadatas=[{**metadata, "chunk_index": i}]
        )

# 2. 相似性检索
def retrieve_context(query: str, top_k: int = 3):
    results = chroma_client.similarity_search(
        query=query,
        k=top_k
    )
    return "\n".join([doc.page_content for doc in results])

# 3. 生成回答
def answer_question(question: str):
    context = retrieve_context(question)
    return chat_completion(question, context)
```

### 3.3 多模型支持（扩展性设计）

```python
class LLMProvider:
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.clients = {
            "openai": OpenAI(api_key=os.environ["OPENAI_API_KEY"]),
            # 可扩展：anthropic, azure, 本地模型等
        }
    
    def chat(self, messages: list, model: str = "gpt-4o"):
        return self.clients[self.provider].chat.completions.create(
            model=model,
            messages=messages
        )
```

### 3.4 注意事项

1. **API Key 安全**：使用环境变量存储，不硬编码
2. **请求限流**：实现重试机制和速率限制
3. **成本控制**：记录 token 用量，设置预算告警
4. **降级策略**：API 不可用时返回缓存或默认回答

---

## 四、数据库设计（初步）

### 4.1 核心数据表

#### 4.1.1 用户表 (users)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',  -- 'admin', 'user'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

#### 4.1.2 知识库表 (knowledge_bases)

```sql
CREATE TABLE knowledge_bases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    document_count INTEGER DEFAULT 0
);
```

#### 4.1.3 文档表 (documents)

```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    knowledge_base_id UUID REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    file_path VARCHAR(500),
    file_type VARCHAR(50),  -- 'pdf', 'docx', 'txt', 'md'
    file_size BIGINT,
    status VARCHAR(20) DEFAULT 'pending',  -- 'pending', 'processing', 'completed', 'failed'
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);
```

#### 4.1.4 对话会话表 (chat_sessions)

```sql
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    knowledge_base_id UUID REFERENCES knowledge_bases(id),
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    message_count INTEGER DEFAULT 0
);
```

#### 4.1.5 聊天记录表 (chat_messages)

```sql
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL,  -- 'user', 'assistant'
    content TEXT NOT NULL,
    token_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4.1.6 API Key 管理表 (api_keys)

```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    key_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    rate_limit INTEGER DEFAULT 60,  -- 每分钟请求数
    monthly_limit INTEGER DEFAULT 100000,  -- 月限流
    used_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);
```

### 4.2 数据库选型

- **PostgreSQL**：主数据库（支持向量插件 pgvector）
- **Chroma**：向量数据库（独立部署）
- **Redis**：（可选）缓存和会话存储

---

## 五、MVP 阶段后端开发计划

### 5.1 阶段划分

| 阶段 | 周期 | 目标 |
|------|------|------|
| **Week 1** | 项目初始化 | 搭建 FastAPI 项目结构、CI/CD、基础配置 |
| **Week 2** | 核心 API | 用户认证、文档上传、基础 CRUD |
| **Week 3** | 向量化和检索 | 文档解析、向量化存储、相似性检索 |
| **Week 4** | LLM 对接 | RAG 流程集成、多轮对话支持 |
| **Week 5** | 管理和监控 | 日志、监控、API 限流、错误处理 |
| **Week 6** | 测试和部署 | 单元测试、集成测试、容器化部署 |

### 5.2 详细任务

#### Week 1：项目初始化
- [ ] 初始化 FastAPI 项目（Poetry/Pipenv）
- [ ] 配置日志、异常处理、环境变量
- [ ] Docker/Docker Compose 配置
- [ ] CI/CD 基础（GitHub Actions）
- [ ] 数据库迁移（SQLAlchemy/Alembic）

#### Week 2：核心 API
- [ ] 用户注册/登录（JWT 认证）
- [ ] 知识库 CRUD API
- [ ] 文档上传 API（支持 PDF、DOCX、TXT）
- [ ] 文件存储配置（本地/S3）

#### Week 3：向量化和检索
- [ ] 文档解析（PyMuPDF、python-docx）
- [ ] 文本分词（LangChain RecursiveCharacterTextSplitter）
- [ ] 向量化（OpenAI Embeddings）
- [ ] Chroma 集成与检索 API
- [ ] 增量更新机制

#### Week 4：LLM 对接
- [ ] RAG 流程实现
- [ ] 对话历史管理
- [ ] 多轮对话支持
- [ ] 流式响应（Server-Sent Events）
- [ ] 多模型切换（预留扩展）

#### Week 5：管理和监控
- [ ] API 限流（Redis）
- [ ] 请求日志和审计
- [ ] 错误监控和告警
- [ ] 性能指标（Prometheus）
- [ ] API 文档完善

#### Week 6：测试和部署
- [ ] 单元测试（pytest）
- [ ] API 集成测试
- [ ] Docker 镜像构建
- [ ] 部署文档
- [ ] 预发布检查

### 5.3 技术栈汇总

| 类别 | 技术选型 |
|------|----------|
| **Web 框架** | FastAPI |
| **ORM** | SQLAlchemy + Pydantic |
| **数据库** | PostgreSQL 15 |
| **向量库** | Chroma |
| **LLM** | OpenAI API (GPT-4o) |
| **认证** | JWT (Python-Jose) |
| **文档解析** | PyMuPDF, python-docx |
| **文本处理** | LangChain |
| **部署** | Docker + Docker Compose |
| **CI/CD** | GitHub Actions |

### 5.4 风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|----------|
| OpenAI API 限流/不可用 | 服务中断 | 实现缓存+降级策略 |
| 向量检索质量不稳定 | 回答不准确 | 调优 chunk size 和 top_k |
| 大文件处理超时 | 上传失败 | 异步处理 + 进度反馈 |
| 并发性能不足 | 响应慢 | 异步优化 + 缓存 |

---

## 总结

本次技术调研推荐 **FastAPI + Chroma + PostgreSQL** 作为企业知识库助手的后端技术栈，MVP 阶段预计 **6 周** 完成核心功能开发。

该方案兼顾了开发效率、性能和扩展性，能够快速验证产品假设，后续可平滑升级到企业级架构。

---

**调研人**：Charlie  
**日期**：2026-03-11
