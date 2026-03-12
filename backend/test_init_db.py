#!/usr/bin/env python3
"""测试脚本 - 初始化数据库"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base
from app.models.database import User, Document, DocumentTag, QAHistory
from app.core.security import get_password_hash

def init_db():
    """初始化数据库表"""
    print("创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表创建成功!")
    
    # 创建测试用户
    from sqlalchemy.orm import Session
    session = Session(bind=engine)
    
    # 检查是否已有用户
    existing_user = session.query(User).filter(User.username == "admin").first()
    if not existing_user:
        print("创建测试用户...")
        admin = User(
            username="admin",
            email="admin@skillmart.com",
            password_hash=get_password_hash("admin123"),
            role="admin",
            is_active=True
        )
        session.add(admin)
        
        # 普通用户
        user = User(
            username="testuser",
            email="test@skillmart.com",
            password_hash=get_password_hash("test123"),
            role="user",
            is_active=True
        )
        session.add(user)
        session.commit()
        print("测试用户创建成功!")
    else:
        print("测试用户已存在")
    
    session.close()

if __name__ == "__main__":
    init_db()
