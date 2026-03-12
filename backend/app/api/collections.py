"""收藏管理 API - 将新闻添加到知识库"""

from typing import List
from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.models.database import User, Collection
from app.services.auth import get_current_user

router = APIRouter()


# Schemas
class CollectionCreate(BaseModel):
    """创建收藏"""
    news_id: str
    news_title: str
    news_summary: str = ""
    news_category: str = ""
    news_source: str = ""
    news_url: str = ""
    news_publish_time: str = ""
    category_id: str = ""
    category_name: str = ""
    template_id: int = None
    template_name: str = ""


class CollectionResponse(BaseModel):
    """收藏响应"""
    id: str
    news_id: str
    news_title: str
    news_summary: str
    news_category: str
    news_source: str
    news_url: str
    news_publish_time: str
    category_id: str
    category_name: str
    template_id: int
    template_name: str
    created_at: str

    class Config:
        from_attributes = True


@router.post("", response_model=CollectionResponse)
async def create_collection(
    collection: CollectionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """收藏新闻到知识库"""
    # 检查是否已收藏
    existing = db.query(Collection).filter(
        Collection.user_id == current_user.id,
        Collection.news_id == collection.news_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="已经收藏过这条新闻")
    
    # 创建收藏
    db_collection = Collection(
        user_id=current_user.id,
        **collection.model_dump()
    )
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    
    return CollectionResponse(
        id=db_collection.id,
        news_id=db_collection.news_id,
        news_title=db_collection.news_title,
        news_summary=db_collection.news_summary or "",
        news_category=db_collection.news_category or "",
        news_source=db_collection.news_source or "",
        news_url=db_collection.news_url or "",
        news_publish_time=db_collection.news_publish_time or "",
        category_id=db_collection.category_id or "",
        category_name=db_collection.category_name or "",
        template_id=db_collection.template_id,
        template_name=db_collection.template_name or "",
        created_at=db_collection.created_at.isoformat()
    )


@router.get("", response_model=List[CollectionResponse])
async def get_collections(
    category_id: str = Query(None, description="分类ID"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户收藏列表"""
    query = db.query(Collection).filter(Collection.user_id == current_user.id)
    
    if category_id:
        query = query.filter(Collection.category_id == category_id)
    
    total = query.count()
    offset = (page - 1) * page_size
    
    collections = query.order_by(desc(Collection.created_at)).offset(offset).limit(page_size).all()
    
    return [
        CollectionResponse(
            id=c.id,
            news_id=c.news_id,
            news_title=c.news_title,
            news_summary=c.news_summary or "",
            news_category=c.news_category or "",
            news_source=c.news_source or "",
            news_url=c.news_url or "",
            news_publish_time=c.news_publish_time or "",
            category_id=c.category_id or "",
            category_name=c.category_name or "",
            template_id=c.template_id,
            template_name=c.template_name or "",
            created_at=c.created_at.isoformat()
        )
        for c in collections
    ]


@router.delete("/{collection_id}")
async def delete_collection(
    collection_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除收藏"""
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == current_user.id
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="收藏不存在")
    
    db.delete(collection)
    db.commit()
    
    return {"message": "删除成功"}


@router.get("/categories")
async def get_collection_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取收藏的分类统计"""
    from sqlalchemy import func
    
    results = db.query(
        Collection.category_name,
        Collection.category_id,
        func.count(Collection.id).label('count')
    ).filter(
        Collection.user_id == current_user.id
    ).group_by(
        Collection.category_id,
        Collection.category_name
    ).all()
    
    return [
        {"category_id": r.category_id or "other", "category_name": r.category_name or "未分类", "count": r.count}
        for r in results
    ]
