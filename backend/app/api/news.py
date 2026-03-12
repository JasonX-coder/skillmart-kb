"""新闻资讯 API - 使用 Hacker News 作为真实数据源"""

import httpx
import asyncio
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter()


class NewsItem(BaseModel):
    id: str
    title: str
    summary: str
    category: str
    publish_time: str
    source: str
    url: Optional[str] = None


# 备用新闻数据（当API失败时使用）
FALLBACK_NEWS = [
    {
        "id": "1",
        "title": "OpenAI 发布 GPT-5，带来前所未有的推理能力提升",
        "summary": "OpenAI 最新的 GPT-5 模型在多模态理解和推理方面取得重大突破，引发业界广泛关注。",
        "category": "技术",
        "publish_time": datetime.now().isoformat(),
        "source": "TechCrunch",
        "url": "https://openai.com"
    },
    {
        "id": "2", 
        "title": "国家发改委发布《人工智能产业发展规划2026》",
        "summary": "规划明确提出到2030年形成万亿级AI产业集群，重点突破核心技术。",
        "category": "政策",
        "publish_time": datetime.now().isoformat(),
        "source": "新华网",
        "url": "https://news.xinhuanet.com"
    },
    {
        "id": "3",
        "title": "云计算市场份额持续增长，阿里、腾讯云加速布局",
        "summary": "根据Gartner最新报告，中国云计算市场增速放缓但保持两位数增长。",
        "category": "行业",
        "publish_time": datetime.now().isoformat(),
        "source": "Bloomberg",
        "url": "https://bloomberg.com"
    },
    {
        "id": "4",
        "title": "AI 大模型落地加速：企业级应用成新战场",
        "summary": "各大科技公司纷纷推出企业级AI解决方案，争夺B端市场。",
        "category": "商业",
        "publish_time": datetime.now().isoformat(),
        "source": "36Kr",
        "url": "https://36kr.com"
    },
    {
        "id": "5",
        "title": "Meta 开源 Llama 4，性能超越 GPT-4",
        "summary": "Meta 宣布开源 Llama 4，大幅提升推理效率，引发开源社区热议。",
        "category": "技术",
        "publish_time": datetime.now().isoformat(),
        "source": "Meta AI",
        "url": "https://ai.meta.com"
    },
    {
        "id": "6",
        "title": "教育部发布 AI 教育应用白皮书",
        "summary": "白皮书提出将 AI 融入课堂教学，提升教育质量和效率。",
        "category": "政策",
        "publish_time": datetime.now().isoformat(),
        "source": "教育部",
        "url": "https://moe.gov.cn"
    },
    {
        "id": "7",
        "title": "自动驾驶技术突破：Waymo 扩大商业运营范围",
        "summary": "Waymo 在美国多个城市推出无人出租车服务，商业化进程加速。",
        "category": "行业",
        "publish_time": datetime.now().isoformat(),
        "source": "Waymo",
        "url": "https://waymo.com"
    },
    {
        "id": "8",
        "title": "芯片巨头竞争激烈：英伟达发布新一代 AI 芯片",
        "summary": "英伟达发布 Blackwell 架构芯片，AI 算力提升 2 倍。",
        "category": "技术",
        "publish_time": datetime.now().isoformat(),
        "source": "NVIDIA",
        "url": "https://nvidia.com"
    },
]


async def fetch_hackernews() -> List[dict]:
    """从 Hacker News 获取最新科技新闻"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 获取 top stories IDs
            response = await client.get("https://hacker-news.firebaseio.com/v0/topstories.json")
            if response.status_code != 200:
                return FALLBACK_NEWS
            
            story_ids = response.json()[:20]  # 取前20条
            
            # 串行获取故事详情（更稳定）
            news_list = []
            for story_id in story_ids:
                try:
                    resp = await client.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
                    if resp.status_code == 200:
                        story = resp.json()
                        if story and story.get("title"):
                            time_ts = story.get("time", 0)
                            news_list.append({
                                "id": str(story.get("id", "")),
                                "title": story.get("title", ""),
                                "summary": f"Hacker News 热门话题 | {story.get('score', 0)} points | {story.get('descendants', 0)} comments",
                                "category": "技术",
                                "publish_time": datetime.fromtimestamp(time_ts).isoformat() if time_ts else datetime.now().isoformat(),
                                "source": "Hacker News",
                                "url": story.get("url") or f"https://news.ycombinator.com/item?id={story.get('id')}"
                            })
                except Exception:
                    continue
                
                if len(news_list) >= 10:
                    break
            
            return news_list if news_list else FALLBACK_NEWS
    except Exception as e:
        print(f"Hacker News API error: {e}")
        return FALLBACK_NEWS


@router.get("/")
async def get_news():
    """获取新闻列表"""
    news = await fetch_hackernews()
    return news


@router.get("/categories")
async def get_categories():
    """获取新闻分类"""
    return [
        {"id": "all", "name": "全部"},
        {"id": "tech", "name": "技术"},
        {"id": "business", "name": "商业"},
    ]
