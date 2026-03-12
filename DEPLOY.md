# SkillMart 企业知识库助手 - 部署方案

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                         云服务器                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Nginx     │  │  Frontend   │  │   Backend   │        │
│  │  (端口 80)  │  │  (端口 5173)│  │  (端口 8000)│        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                           │               │                  │
│                     ┌─────┴───────────────┴─────┐            │
│                     │      Docker Network       │            │
│                     └───────────────────────────┘            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  PostgreSQL │  │    Redis    │  │   Chroma    │          │
│  │  (端口 5432)│  │  (端口 6379)│  │  (端口 8001)│          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## 部署步骤

### 1. 云服务器准备

**推荐配置：**
- 系统：Ubuntu 22.04 LTS
- 规格：2核 4GB RAM 起
- 存储：50GB SSD

### 2. 安装 Docker

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
sudo systemctl enable docker
sudo systemctl start docker

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. 配置防火墙

```bash
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 22/tcp   # SSH
sudo ufw enable
```

### 4. 部署应用

```bash
# 1. 创建项目目录
mkdir -p ~/skillmart && cd ~/skillmart

# 2. 创建目录结构
mkdir -p frontend backend data

# 3. 复制代码（通过 Git 或 SCP）

# 4. 启动服务
docker-compose up -d
```

### 5. Docker Compose 配置

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  # 前端
  frontend:
    build: ./frontend
    ports:
      - "5173:80"
    depends_on:
      - backend
    restart: unless-stopped

  # 后端
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/knowledge_base
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=${SECRET_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
    depends_on:
      - db
      - redis
    restart: unless-stopped

  # 数据库
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=knowledge_base
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped

  # 缓存
  redis:
    image: redis:7-alpine
    restart: unless-stopped

  # 向量数据库
  chroma:
    image: chromadb/chroma:latest
    restart: unless-stopped

  # Nginx 反向代理
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  pgdata:
```

### 6. Nginx 配置

创建 `nginx.conf`：

```nginx
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:80;
    }
    
    upstream backend {
        server backend:8000;
    }
    
    server {
        listen 80;
        server_name your-domain.com;
        
        # 前端
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        # 后端 API
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
        
        # WebSocket 支持（如需要）
        location /ws {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

## 环境变量

创建 `.env` 文件：

```bash
# 安全密钥（务必修改）
SECRET_KEY=your-super-secret-key-change-this

# OpenAI API Key（如使用）
OPENAI_API_KEY=sk-xxxxx
```

## 验证部署

```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 测试 API
curl http://localhost:8000/health

# 测试前端
curl http://localhost
```

## 域名配置（可选）

1. 购买域名
2. 配置 DNS A 记录指向服务器 IP
3. 使用 Let's Encrypt 配置 HTTPS（推荐）

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取 SSL 证书
sudo certbot --nginx -d your-domain.com
```

## 维护命令

```bash
# 重启服务
docker-compose restart

# 更新代码后重新构建
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# 查看资源使用
docker stats
```

---

## OpenClaw 集成

部署完成后，OpenClaw 可通过以下方式访问：
- Web UI: `http://<服务器IP>/`
- API: `http://<服务器IP>/api/`
- API Docs: `http://<服务器IP>/docs`

---

如需我进一步细化某个部分，请指示。
