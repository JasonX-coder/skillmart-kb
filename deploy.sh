#!/bin/bash

# SkillMart 企业知识库助手 - 一键部署脚本
# 用法: ./deploy.sh [local|server]

set -e

MODE=${1:-local}

echo "🚀 SkillMart 部署脚本"
echo "====================="
echo "部署模式: $MODE"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查 Docker
if ! command -v docker &> /dev/null; then
    log_error "Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

log_info "检查 Docker 服务..."
if ! docker ps &> /dev/null; then
    log_error "Docker 服务未启动，请先启动 Docker"
    exit 1
fi

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 创建必要目录
log_info "创建数据目录..."
mkdir -p data/postgres data/chroma data/uploads

# 本地模式配置
if [ "$MODE" = "local" ]; then
    log_info "配置本地模式..."
    
    # 修改环境变量为本地
    export DATABASE_URL="postgresql://postgres:postgres@db:5432/knowledge_base"
    export REDIS_URL="redis://redis:6379"
    export SECRET_KEY="dev-local-secret-key-$(date +%s)"
    export OPENAI_API_KEY="${OPENAI_API_KEY:-}"
    export CORS_ORIGINS="[\"http://localhost:5173\",\"http://localhost:3000\"]"
    
    # 创建本地 docker-compose 文件
    cat > docker-compose.local.yml << 'EOF'
version: '3.8'

services:
  # 后端
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/knowledge_base
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=dev-local-secret-key
      - OPENAI_API_KEY=${OPENAI_API_KEY:-}
      - CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
    volumes:
      - ./data:/app/data
      - ./data/uploads:/app/uploads
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # 数据库
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

  # 缓存
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - ./data/redis:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

  # 向量数据库
  chroma:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - ./data/chroma:/chroma/chroma
    restart: unless-stopped

volumes:
  pgdata:
  chromadata:
  redisdata:
EOF

    COMPOSE_FILE="docker-compose.local.yml"
else
    COMPOSE_FILE="docker-compose.yml"
fi

# 停止已有容器
log_info "停止已有容器..."
docker-compose -f $COMPOSE_FILE down 2>/dev/null || true

# 构建并启动
log_info "构建并启动服务..."
docker-compose -f $COMPOSE_FILE up -d --build

# 等待服务健康
log_info "等待服务启动..."
sleep 10

# 检查服务状态
log_info "检查服务状态..."
docker-compose -f $COMPOSE_FILE ps

echo ""
echo "====================="
echo -e "${GREEN}部署完成！${NC}"
echo "====================="
echo ""
echo "服务地址："
echo "  - 后端 API:    http://localhost:8000"
echo "  - API 文档:    http://localhost:8000/docs"
echo "  - Chroma:     http://localhost:8001"
echo ""
echo "查看日志: docker-compose -f $COMPOSE_FILE logs -f"
echo "停止服务: docker-compose -f $COMPOSE_FILE down"
echo ""
