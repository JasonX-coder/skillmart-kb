"""问答服务"""

from sqlalchemy.orm import Session
from typing import Optional, List, Tuple, AsyncGenerator
import uuid
import json

from app.models.database import QAHistory
from app.schemas.qa import QARequest, Source


async def ask_question(
    db: Session,
    request: QARequest,
    user_id: uuid.UUID
) -> AsyncGenerator[dict, None]:
    """问答（流式响应）"""
    # TODO: 实现完整的 RAG 流程
    # 1. 检索相关文档
    # 2. 构建 prompt
    # 3. 调用 LLM
    # 4. 流式返回结果
    
    # 模拟流式响应
    answer_parts = [
        "您好！",
        "根据知识库检索，",
        "我找到了相关信息...",
        "\n\n希望这个回答对您有帮助。"
    ]
    
    sources = [
        {
            "document_id": "doc_sample_1",
            "chunk_content": "这是示例文档内容...",
            "score": 0.95
        }
    ]
    
    # 流式返回
    for i, part in enumerate(answer_parts):
        chunk = {"answer": part, "done": False}
        if i == len(answer_parts) - 1:
            chunk["sources"] = sources
            chunk["done"] = True
        yield chunk
    
    # 保存到历史记录
    history = QAHistory(
        user_id=user_id,
        question=request.question,
        answer="".join(answer_parts),
        sources=json.dumps(sources)
    )
    db.add(history)
    db.commit()


def get_qa_history(
    db: Session,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 20
) -> Tuple[List[QAHistory], int]:
    """获取问答历史"""
    query = db.query(QAHistory).filter(QAHistory.user_id == user_id)
    total = query.count()
    history = query.order_by(QAHistory.created_at.desc()).offset(skip).limit(limit).all()
    
    # 转换 sources 从 JSON 字符串到列表
    for h in history:
        if h.sources and isinstance(h.sources, str):
            h.sources = json.loads(h.sources)
    
    return history, total


def delete_qa_history(
    db: Session,
    history_id: str,
    user_id: uuid.UUID
) -> bool:
    """删除问答记录"""
    history = db.query(QAHistory).filter(
        QAHistory.id == history_id,
        QAHistory.user_id == user_id
    ).first()
    
    if not history:
        return False
    
    db.delete(history)
    db.commit()
    return True
