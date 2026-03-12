# 🎯 SkillMart 企业知识库助手

<p align="center">
  <img src="https://img.shields.io/badge/Vue3-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white" alt="Vue3">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
</p>

> 帮助企业构建智能知识库，员工可以通过 AI 快速检索和问答内部文档

## 📌 产品简介

**SkillMart 企业知识库助手** 是一款面向企业的智能知识管理平台。

### 核心价值

- 📚 **集中管理** - 统一管理企业各类文档、培训资料
- 🔍 **智能检索** - 快速搜索定位所需知识
- 💬 **AI 问答** - 基于 RAG 技术，智能回答员工问题
- 👥 **权限控制** - 完善的用户和角色管理

### 目标用户

| 角色 | 典型用户 | 核心需求 |
|------|---------|---------|
| 管理员 | IT 负责人、行政 | 文档上传管理、知识库维护 |
| 普通员工 | 业务人员、客服、技术支持 | 快速查询答案、获取准确信息 |

## 🛠 技术栈

### 前端
- Vue 3 + TypeScript
- Vite 构建工具
- Pinia 状态管理
- Vue Router

### 后端
- FastAPI (Python)
- SQLAlchemy ORM
- PostgreSQL 数据库
- Redis 缓存
- Chroma 向量数据库

## 🚀 快速开始

### 本地开发

```bash
# 1. 克隆项目
git clone https://github.com/JasonX-coder/skillmart-kb.git
cd skillmart-kb

# 2. 启动后端
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001

# 3. 启动前端
cd frontend
npm install
npm run dev
```

访问 http://localhost:3001

### Docker 部署

```bash
# 一键部署
docker-compose up -d
```

详见 [部署文档](./DEPLOY.md)

## 📱 功能特性

### V1.0 (当前版本)
- ✅ 用户注册/登录
- ✅ 文档上传与管理
- ✅ 文档搜索
- ✅ 全文索引

### V1.1 (规划中)
- ⏳ 用户权限管理
- ⏳ 角色控制

### V2.0 (规划中)
- 🤖 RAG 智能问答
- 📊 使用分析

## 📁 项目结构

```
skillmart-kb/
├── frontend/           # Vue3 前端
│   ├── src/
│   │   ├── api/      # API 调用
│   │   ├── components/ # 组件
│   │   ├── views/    # 页面视图
│   │   ├── stores/   # 状态管理
│   │   └── router/   # 路由配置
│   └── package.json
│
├── backend/           # FastAPI 后端
│   ├── app/
│   │   ├── api/      # API 路由
│   │   ├── core/     # 核心配置
│   │   ├── models/   # 数据模型
│   │   ├── schemas/  # Pydantic 模型
│   │   └── services/ # 业务逻辑
│   └── requirements.txt
│
├── DEPLOY.md         # 部署文档
└── README.md
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

<p align="center">Built with ❤️ by SkillMart Team</p>
