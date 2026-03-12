"""文档服务"""

from sqlalchemy.orm import Session
from typing import Optional, List, Tuple
import uuid
import os
from pathlib import Path

from app.models.database import Document, DocumentTag
from app.core.config import settings
from app.core.security import decode_token


async def upload_document(
    db: Session,
    file,
    user_id: uuid.UUID,
    category: Optional[str] = None,
    tags: Optional[str] = None
) -> Document:
    """上传文档"""
    # 获取文件扩展名
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    # 检查文件类型
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise ValueError(f"不支持的文件类型: {file_ext}")
    
    # 生成存储路径
    upload_dir = Path("./data/uploads") / str(user_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_id = uuid.uuid4()
    file_path = upload_dir / f"{file_id}{file_ext}"
    
    # 保存文件
    content = await file.read()
    file_path.write_bytes(content)
    
    # 检查文件大小
    file_size = len(content)
    if file_size > settings.MAX_FILE_SIZE:
        file_path.unlink()
        raise ValueError(f"文件大小超过限制: {settings.MAX_FILE_SIZE / 1024 / 1024}MB")
    
    # 创建文档记录
    document = Document(
        id=file_id,
        user_id=user_id,
        filename=file.filename,
        file_path=str(file_path),
        file_type=file_ext[1:],  # 去掉点号
        file_size=file_size,
        category=category,
        status="pending"
    )
    db.add(document)
    
    # 处理标签
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        for tag in tag_list:
            doc_tag = DocumentTag(document_id=document.id, tag=tag)
            db.add(doc_tag)
    
    db.commit()
    db.refresh(document)
    
    return document


def get_documents(
    db: Session,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 20
) -> Tuple[List[Document], int]:
    """获取文档列表"""
    query = db.query(Document).filter(Document.user_id == user_id)
    total = query.count()
    documents = query.order_by(Document.created_at.desc()).offset(skip).limit(limit).all()
    return documents, total


def get_document(
    db: Session,
    document_id: str,
    user_id: uuid.UUID
) -> Optional[Document]:
    """获取文档详情"""
    return db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user_id
    ).first()


def delete_document(
    db: Session,
    document_id: str,
    user_id: uuid.UUID
) -> bool:
    """删除文档"""
    document = get_document(db, document_id, user_id)
    if not document:
        return False
    
    # 删除文件
    if os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    db.delete(document)
    db.commit()
    return True
