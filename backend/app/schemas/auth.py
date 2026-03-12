"""认证相关 Pydantic 模型"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    """Token 响应"""
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    """用户创建请求"""
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """用户响应"""
    id: str
    username: str
    email: str
    is_active: bool
    
    class Config:
        from_attributes = True
