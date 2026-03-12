"""文档管理模块路由"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path

from app.core.database import get_db
from app.schemas.document import DocumentResponse, DocumentListResponse
from app.services.document import (
    upload_document,
    get_documents,
    get_document,
    delete_document
)
from app.services.auth import get_current_user

router = APIRouter()


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取文档列表"""
    documents, total = get_documents(db, current_user.id, skip, limit)
    return {"items": documents, "total": total}


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    file: UploadFile = File(...),
    category: str = None,
    tags: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """上传文档"""
    document = await upload_document(
        db, file, current_user.id, category, tags
    )
    return document


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document_detail(
    document_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取文档详情"""
    document = get_document(db, document_id, current_user.id)
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除文档"""
    success = delete_document(db, document_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="文档不存在")
    return None
