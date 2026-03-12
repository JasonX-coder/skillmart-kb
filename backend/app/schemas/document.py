"""文档相关 Pydantic 模型"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DocumentResponse(BaseModel):
    """文档响应"""
    id: str
    filename: str
    file_type: str
    file_size: int
    category: Optional[str] = None
    status: str
    chunk_count: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """文档列表响应"""
    items: List[DocumentResponse]
    total: int
