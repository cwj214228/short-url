# 短链接服务

一个类似 Bitly/TinyURL 的公开短链接服务，基于 FastAPI 和 Vue 3 构建。

## 功能特性

- **公开短链接** - 无需账号即可创建短链接
- **用户认证** - 支持注册/登录，使用 JWT Token
- **链接管理** - 创建、编辑、删除、批量创建链接
- **自定义别名** - 使用自定义别名创建品牌化短链接
- **点击统计** - 按国家、设备、浏览器和时间线追踪点击
- **自定义域名** - 用户可绑定自己的域名
- **二维码生成** - 为链接生成二维码

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | FastAPI (Python 3.11) |
| 前端 | Vue 3 + Vite + TypeScript |
| 数据库 | MySQL 8.0 |
| 缓存 | Redis |
| UI | TailwindCSS |
| 状态管理 | Pinia |
| 路由 | Vue Router |
| 反向代理 | Nginx |
| 容器化 | Docker |

## 系统架构

```
┌─────────────────────────────────────────────────┐
│                    用户浏览器                      │
└─────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────┐
│                      Nginx                       │
│              (反向代理，端口 8080)                 │
└─────────────────────────────────────────────────┘
          │                        │
          ▼                        ▼
┌──────────────────┐    ┌──────────────────┐
│      前端        │    │      后端        │
│  (Vue 3, :3000)  │    │  (FastAPI, :8000)│
└──────────────────┘    └──────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
            ┌──────────────┐        ┌──────────────┐
            │    MySQL     │        │    Redis     │
            │  (端口 3306)  │        │  (端口 6379)  │
            └──────────────┘        └──────────────┘
```

## 环境要求

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (现代 Python 包管理器)
- Node.js 20+
- MySQL 8.0
- Redis 7+
- Docker & Docker Compose (可选)

## 环境变量

在 `backend/` 目录下创建 `.env` 文件：

```env
# 数据库
DATABASE_URL=mysql+pymysql://shorturl:shorturlpassword@localhost:3306/shorturl

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT (生产环境请修改！)
SECRET_KEY=your-super-secret-key-change-in-production

# 应用配置
DEBUG=True
DEFAULT_DOMAIN=localhost:8000
SHORT_CODE_LENGTH=8
```

## 安装

### 方式一：Docker（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

服务地址：
- 前端：http://localhost:8080
- 后端 API：http://localhost:8080/api
- API 文档：http://localhost:8080/api/docs

### 方式二：手动安装

#### 后端

```bash
cd backend

# 安装 uv（如果还没有）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建虚拟环境并安装依赖
uv sync

# 或手动方式：
# uv venv
# uv pip install -r requirements.txt

# 创建 MySQL 数据库
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS shorturl CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u root -p -e "CREATE USER IF NOT EXISTS 'shorturl'@'localhost' IDENTIFIED BY 'shorturlpassword';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON shorturl.* TO 'shorturl'@'localhost';"
mysql -u root -p -e "FLUSH PRIVILEGES;"

# 启动 Redis（确保运行中）
redis-server

# 启动应用
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端地址：http://localhost:3000，会自动代理 API 请求到 http://localhost:8000。

## API 文档

后端启动后访问：
- Swagger UI：http://localhost:8000/api/docs
- ReDoc：http://localhost:8000/api/redoc

### 主要接口

#### 认证
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/register` | 注册新用户 |
| POST | `/api/auth/login` | 登录获取 Token |
| POST | `/api/auth/refresh` | 刷新访问 Token |
| GET | `/api/auth/me` | 获取当前用户信息 |

#### 链接
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/links` | 创建短链接 |
| GET | `/api/links` | 获取用户链接列表 |
| GET | `/api/links/{code}` | 获取链接详情 |
| PUT | `/api/links/{code}` | 更新链接 |
| DELETE | `/api/links/{code}` | 删除链接 |
| POST | `/api/links/batch` | 批量创建链接 |

#### 统计
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/links/{code}/stats` | 获取链接统计 |
| GET | `/api/links/{code}/stats/timeline` | 获取点击时间线 |

#### 域名
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/domains` | 获取用户域名列表 |
| POST | `/api/domains` | 添加新域名 |
| POST | `/api/domains/verify` | 验证域名所有权 |
| DELETE | `/api/domains/{domain}` | 删除域名 |

#### 公开接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/{short_code}` | 跳转到原始 URL |
| GET | `/api/info/{code}` | 获取链接信息（公开） |

## 项目结构

```
.
├── backend/
│   ├── app/
│   │   ├── api/            # API 路由处理
│   │   │   ├── auth.py     # 认证接口
│   │   │   ├── links.py    # 链接 CRUD 接口
│   │   │   ├── stats.py    # 统计接口
│   │   │   ├── domains.py  # 域名管理
│   │   │   └── public.py   # 公开跳转处理
│   │   ├── core/           # 核心配置
│   │   │   ├── config.py   # 设置和环境变量
│   │   │   ├── database.py # SQLAlchemy 配置
│   │   │   └── security.py # JWT 和密码工具
│   │   ├── models/         # 数据库模型
│   │   │   ├── user.py     # 用户模型
│   │   │   ├── link.py     # 链接模型
│   │   │   ├── stat.py     # 点击统计模型
│   │   │   └── domain.py   # 自定义域名模型
│   │   ├── schemas/        # Pydantic 数据模式
│   │   ├── services/       # 业务逻辑
│   │   │   └── short_code.py # 短码生成
│   │   └── main.py         # FastAPI 应用入口
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/            # Axios API 客户端
│   │   ├── components/     # Vue 组件
│   │   │   └── NavBar.vue
│   │   ├── router/         # Vue Router 配置
│   │   ├── stores/         # Pinia 状态管理
│   │   │   ├── auth.ts     # 认证状态
│   │   │   └── links.ts    # 链接状态
│   │   ├── views/          # 页面组件
│   │   │   ├── HomePage.vue
│   │   │   ├── LoginPage.vue
│   │   │   ├── RegisterPage.vue
│   │   │   ├── DashboardPage.vue
│   │   │   ├── LinksPage.vue
│   │   │   ├── CreateLinkPage.vue
│   │   │   ├── EditLinkPage.vue
│   │   │   ├── LinkStatsPage.vue
│   │   │   ├── DomainsPage.vue
│   │   │   └── SettingsPage.vue
│   │   ├── App.vue
│   │   ├── main.ts
│   │   └── assets/
│   │       └── main.css
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── nginx/
│   └── nginx.conf           # Nginx 配置
│
├── docker-compose.yml       # Docker 编排
└── README.md
```

## 开发

### 运行测试

后端测试：
```bash
cd backend
uv run pytest
```

前端测试（如果已添加）：
```bash
cd frontend
npm test
```

### 代码规范

后端代码检查：
```bash
cd backend
ruff check .
black .
```

前端代码检查：
```bash
cd frontend
npm run lint
```

## 部署

### Docker 生产部署

1. 克隆仓库
2. 修改后端 `.env` 中的 `SECRET_KEY`
3. 修改 `nginx/nginx.conf` 中的域名
4. 修改 `backend/app/main.py` 中的 CORS 配置
5. 运行 `docker-compose -f docker-compose.yml up -d`

### 手动生产部署

1. 构建前端：`cd frontend && npm run build`
2. 使用 Nginx 提供 `frontend/dist/` 静态文件
3. 使用 Gunicorn/Uvicorn 运行后端
4. 配置 Nginx 代理 API 和静态文件

## 许可证

MIT
