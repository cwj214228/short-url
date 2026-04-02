# 短链接服务 (Short URL Service) 设计文档

**日期**: 2026-04-02
**状态**: 已批准

---

## 一、项目概述

### 1.1 项目定位
面向公众的短链接服务，类似 Bitly/TinyURL，支持用户注册、链接管理、点击统计、自定义域名等功能。

### 1.2 核心功能
- 公开创建短链接（无需登录）
- 用户系统（注册/登录/JWT认证）
- 个人链接管理（创建/编辑/删除/标签）
- 点击统计分析（时间线/地域/设备）
- 批量创建链接
- 自定义短码支持
- 自定义域名绑定
- QR码生成
- API 接口

### 1.3 技术栈
- **后端**: FastAPI (Python)
- **前端**: Vue 3 + Vite + TailwindCSS
- **数据库**: MySQL 8.0
- **缓存**: Redis
- **部署**: 传统服务器 (VPS)

---

## 二、系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                         用户端 (Vue 3)                       │
│         首页 / 登录注册 / 链接管理 / 统计看板 / 设置          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      反向代理 (Nginx)                        │
│                   静态资源 / SSL / 负载均衡                   │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│    FastAPI 后端服务      │     │      Redis 缓存         │
│  - 用户认证 (JWT)        │     │  - 短码去重检测          │
│  - 链接 CRUD            │     │  - 热点数据缓存          │
│  - 统计服务              │     │  - Session 存储          │
│  - 自定义域名管理        │     └─────────────────────────┘
│  - API 接口              │
└─────────────────────────┘
              │
              ▼
┌─────────────────────────┐
│       MySQL 数据库       │
│  - 用户表               │
│  - 链接表               │
│  - 域名表               │
│  - 点击统计表            │
└─────────────────────────┘
```

---

## 三、数据库设计

### 3.1 用户表 (users)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK, AUTO_INCREMENT) | 用户ID |
| email | VARCHAR(255) UNIQUE | 邮箱 |
| username | VARCHAR(100) | 用户名 |
| password_hash | VARCHAR(255) | 密码哈希 |
| plan_type | ENUM('free', 'pro') | 套餐类型 |
| is_active | BOOLEAN | 是否激活 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 3.2 链接表 (links)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK, AUTO_INCREMENT) | 链接ID |
| user_id | INT (FK) | 所属用户 |
| original_url | TEXT | 原URL |
| short_code | VARCHAR(20) UNIQUE | 短码（哈希生成） |
| custom_alias | VARCHAR(50) | 自定义短码 |
| domain | VARCHAR(255) | 域名 |
| is_custom | BOOLEAN | 是否自定义短码 |
| created_at | DATETIME | 创建时间 |
| expires_at | DATETIME | 过期时间 |
| is_active | BOOLEAN | 是否启用 |
| tags | JSON | 标签 |

### 3.3 点击统计表 (link_stats)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK, AUTO_INCREMENT) | 统计ID |
| link_id | INT (FK) | 链接ID |
| clicked_at | DATETIME | 点击时间 |
| country | VARCHAR(100) | 国家 |
| city | VARCHAR(100) | 城市 |
| device | ENUM('desktop','mobile','tablet') | 设备类型 |
| browser | VARCHAR(100) | 浏览器 |
| os | VARCHAR(100) | 操作系统 |
| referer | TEXT | 来源 |

### 3.4 自定义域名表 (domains)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT (PK, AUTO_INCREMENT) | 域名ID |
| user_id | INT (FK) | 所属用户 |
| domain | VARCHAR(255) UNIQUE | 域名 |
| verification_token | VARCHAR(100) | 验证Token |
| verified_at | DATETIME | 验证时间 |
| is_active | BOOLEAN | 是否启用 |
| created_at | DATETIME | 创建时间 |

---

## 四、API 接口设计

### 4.1 认证模块
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/register | 用户注册 |
| POST | /api/auth/login | 用户登录，返回JWT |
| POST | /api/auth/refresh | 刷新Token |
| GET | /api/auth/me | 获取当前用户信息 |

### 4.2 链接模块
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/links | 创建短链接 |
| GET | /api/links | 获取用户的链接列表（分页、筛选） |
| GET | /api/links/{short_code} | 获取单个链接详情 |
| PUT | /api/links/{short_code} | 更新链接 |
| DELETE | /api/links/{short_code} | 删除链接 |
| POST | /api/links/batch | 批量创建链接 |

### 4.3 统计模块
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/links/{short_code}/stats | 获取链接统计 |
| GET | /api/links/{short_code}/stats/timeline | 时间线统计 |

### 4.4 域名模块
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/domains | 获取用户的域名列表 |
| POST | /api/domains | 添加自定义域名 |
| POST | /api/domains/verify | 验证域名所有权 |
| DELETE | /api/domains/{domain} | 删除域名 |

### 4.5 公开接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /{short_code} | 短链接跳转（公开，无需认证） |
| GET | /api/info/{short_code} | 获取链接信息（公开） |

---

## 五、前端页面结构

### 5.1 公共页面
| 路径 | 说明 |
|------|------|
| / | 首页，输入URL生成短链接（无需登录） |
| /login | 登录页 |
| /register | 注册页 |

### 5.2 用户仪表盘
| 路径 | 说明 |
|------|------|
| /dashboard | 个人中心概览 |
| /links | 链接列表管理 |
| /links/new | 创建链接页面 |
| /links/{short_code}/edit | 编辑链接 |
| /links/{short_code}/stats | 链接统计分析 |
| /domains | 自定义域名管理 |
| /settings | 用户设置 |

---

## 六、视觉风格

- **主色调**: 渐变蓝紫色系 (#6366F1 → #8B5CF6)
- **暗色模式**: 支持
- **布局**: 卡片式布局，圆角设计
- **动效**: 数字统计用计数动画，链接创建成功有成功动效
- **风格定位**: 现代动感，强调速度和易用性

---

## 七、短码生成策略

采用**哈希算法 + 冲突检测**方案：
1. 用户提交原URL
2. 计算URL的哈希值（SHA1）
3. 取哈希前8字符作为候选短码
4. 检查数据库是否存在冲突
5. 如有冲突，添加随机后缀重试（最多3次）
6. 用户可自定义短码（需唯一性检查）

---

## 八、项目目录结构（预估）

```
short-url-service/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── links.py
│   │   │   ├── stats.py
│   │   │   └── domains.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── link.py
│   │   │   ├── stat.py
│   │   │   └── domain.py
│   │   ├── schemas/
│   │   │   └── ...
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── stores/
│   │   ├── api/
│   │   └── App.vue
│   ├── package.json
│   └── vite.config.ts
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

---

## 九、验收标准

1. 用户可以注册、登录、登出
2. 登录用户可以创建短链接（自动生成或自定义短码）
3. 登录用户可以查看、编辑、删除自己的链接
4. 登录用户可以查看链接点击统计
5. 登录用户可以绑定自定义域名
6. 任何人可以通过短链接访问原URL
7. 公开用户可以看到链接的公开信息
8. 前端界面符合现代动感风格设计
9. 所有API接口有适当的错误处理
10. 数据库设计支持高并发点击统计
