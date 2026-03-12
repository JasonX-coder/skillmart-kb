"""应用配置"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用
    APP_NAME: str = "SkillMart Knowledge Base"
    DEBUG: bool = True
    
    # 数据库 - 使用 SQLite 用于测试
    DATABASE_URL: str = "sqlite:///./data/knowledge.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Chroma
    CHROMA_PERSIST_DIR: str = "./data/chroma"
    
    # 文件上传
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt", ".md"]
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # News API (免费新闻数据源)
    NEWS_API_KEY: str = ""  # newsdata.io API key (可选)
    NEWS_CACHE_MINUTES: int = 30  # 新闻缓存时间
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
