"""SQLAlchemy 数据模型"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, Integer, BigInteger, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")  # admin, user
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    qa_history = relationship("QAHistory", back_populates="user", cascade="all, delete-orphan")


class Document(Base):
    """文档模型"""
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(20), nullable=False)  # pdf, docx, txt, md
    file_size = Column(BigInteger, nullable=False)
    category = Column(String(50))
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    error_message = Column(Text)
    chunk_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="documents")
    tags = relationship("DocumentTag", back_populates="document", cascade="all, delete-orphan")


class DocumentTag(Base):
    """文档标签模型"""
    __tablename__ = "document_tags"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    tag = Column(String(50), nullable=False)
    
    # 关系
    document = relationship("Document", back_populates="tags")


class QAHistory(Base):
    """问答历史模型"""
    __tablename__ = "qa_history"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text)
    sources = Column(JSON)  # 存储引用来源
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="qa_history")


class Collection(Base):
    """收藏表 - 用于保存新闻到知识库"""
    __tablename__ = "collections"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # 新闻信息
    news_id = Column(String(100), nullable=False)
    news_title = Column(Text, nullable=False)
    news_summary = Column(Text)
    news_category = Column(String(50))
    news_source = Column(String(100))
    news_url = Column(String(500))
    news_publish_time = Column(String(50))
    
    # 知识库分类
    category_id = Column(String(50))  # 对应分类导航的 id
    category_name = Column(String(100))
    
    # 模板
    template_id = Column(Integer)
    template_name = Column(String(100))
    
    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User")
