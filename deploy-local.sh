#!/bin/bash

# SkillMart 企业知识库助手 - 一键部署脚本（无 Chroma 版）
# 用于本地测试

set -e

echo "🚀 SkillMart 本地部署"
echo "====================="

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }

cd /Users/jasonchen/.openclaw/workspace-jason

# 创建数据目录
mkdir -p data/postgres data/redis data/chroma data/uploads

# 创建简化的 docker-compose
cat > docker-compose.local.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=knowledge_base
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - ./data/redis:/data
    restart: unless-stopped

networks:
  default:
    name: skillmart-network
EOF

log_info "启动 PostgreSQL 和 Redis..."
docker-compose -f docker-compose.local.yml up -d db redis

log_info "等待数据库就绪..."
sleep 8

log_info "检查服务状态..."
docker-compose -f docker-compose.local.yml ps

echo ""
echo "====================="
echo -e "${GREEN}数据库服务启动成功！${NC}"
echo "====================="
echo ""
echo "PostgreSQL: localhost:5432"
echo "Redis:      localhost:6379"
echo ""
echo "下一步：手动启动后端服务"
echo "  cd backend"
echo "  pip install -r requirements.txt"  
echo "  uvicorn app.main:app --reload"
