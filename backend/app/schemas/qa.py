"""问答相关 Pydantic 模型"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class QARequest(BaseModel):
    """问答请求"""
    question: str
    document_ids: Optional[List[str]] = None
    top_k: int = 3


class Source(BaseModel):
    """来源"""
    document_id: str
    chunk_content: str
    score: float


class QAStreamChunk(BaseModel):
    """流式响应块"""
    answer: str
    sources: Optional[List[Source]] = None
    done: bool = False


class QAResponse(BaseModel):
    """问答响应（非流式）"""
    answer: str
    sources: Optional[List[Source]] = None


class QAHistoryItem(BaseModel):
    """历史记录项"""
    id: str
    question: str
    answer: Optional[str] = None
    sources: Optional[List[Dict[str, Any]]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class QAHistoryResponse(BaseModel):
    """历史记录响应"""
    items: List[QAHistoryItem]
    total: int
