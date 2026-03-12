"""SkillMart 企业知识库助手 - FastAPI 应用入口"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api import auth, documents, qa, news


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print("🚀 应用启动中...")
    yield
    # 关闭时
    print("👋 应用关闭中...")


app = FastAPI(
    title="SkillMart 企业知识库助手 API",
    description="基于 RAG 的企业知识库问答系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(documents.router, prefix="/api/documents", tags=["文档管理"])
app.include_router(qa.router, prefix="/api/qa", tags=["问答"])
app.include_router(news.router, prefix="/api/news", tags=["新闻资讯"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to SkillMart Knowledge Base API",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}
