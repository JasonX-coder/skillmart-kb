"""问答模块路由"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json

from app.core.database import get_db
from app.schemas.qa import QARequest, QAResponse, QAHistoryResponse
from app.services.qa import ask_question, get_qa_history, delete_qa_history
from app.services.auth import get_current_user

router = APIRouter()


@router.post("/ask")
async def ask(
    request: QARequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """提问（流式响应）"""
    async def generate():
        async for chunk in ask_question(
            db, request, current_user.id
        ):
            yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.get("/history", response_model=QAHistoryResponse)
async def list_history(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取问答历史"""
    history, total = get_qa_history(db, current_user.id, skip, limit)
    return {"items": history, "total": total}


@router.delete("/history/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_history(
    history_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """删除问答记录"""
    success = delete_qa_history(db, history_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="记录不存在")
    return None
