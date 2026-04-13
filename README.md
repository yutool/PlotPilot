# PlotPilot · 墨枢

> AI 驱动的长篇小说创作平台 | 基于 DDD 架构的智能写作系统

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.5-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-teal.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 项目简介

PlotPilot（墨枢）是一个专业的 AI 小说创作平台，采用领域驱动设计（DDD）四层架构，支持从构思到成稿的全流程智能辅助。系统集成了知识图谱、人物关系网络、伏笔管理、文风分析等高级功能，为作者提供强大的创作工具链。

### 核心特性

- 🎯 **DDD 四层架构** - 清晰的领域边界，高内聚低耦合
- 🤖 **AI 智能生成** - 支持方舟 API / Anthropic Claude 多模型
- 📚 **Bible 设定系统** - 人物、地点、世界观统一管理
- 🕸️ **知识图谱** - 自动构建故事实体关系网络
- 📖 **故事线管理** - 多线索并行追踪与伏笔注册
- 🎭 **人物调度器** - 智能控制角色出场频率与重要性
- 📊 **实时分析** - 文风漂移检测、张力曲线、陈词滥调扫描
- 🔄 **自动驾驶模式** - 从大纲到成稿的全自动生成流程
- ✅ **完整测试覆盖** - 211+ 单元/集成测试
- 🚀 **现代化前端** - Vue 3 + Naive UI + ECharts 可视化

---

## 快速开始

### 环境要求

- **Python**: 3.9+
- **Node.js**: 16+
- **API Key**: 方舟 API 或 Anthropic API

### 安装步骤

#### 1. 克隆仓库

```bash
git clone <repository-url>
cd aitext
```

#### 2. 后端配置

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

**`.env` 配置示例：**

```bash
# 方舟 API（推荐）
ARK_API_KEY=your_ark_api_key
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3/chat/completions
ARK_MODEL=doubao-seed-2-0-mini-260215

# 或使用 Anthropic API
# ANTHROPIC_API_KEY=your_anthropic_key
# ANTHROPIC_BASE_URL=https://api.anthropic.com

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/aitext.log
```

#### 3. 前端配置

```bash
cd frontend
npm install
```

### 启动服务

#### 方式一：一键启动（推荐）

```bash
# 自动启动后端（8005端口）+ 前端（5173端口）
python run_server.py
```

#### 方式二：分别启动

```bash
# 终端 1 - 启动后端
python -m interfaces.main
# 或
uvicorn interfaces.main:app --reload --port 8005

# 终端 2 - 启动前端
cd frontend
npm run dev
```

### 访问应用

- **前端界面**: http://localhost:5173
- **API 文档**: http://localhost:8005/docs
- **ReDoc**: http://localhost:8005/redoc

---

## 系统架构

### DDD 四层架构

```
aitext/
├── domain/                 # 领域层 - 核心业务逻辑
│   ├── novel/             # 小说聚合根、章节实体、故事线
│   ├── bible/             # 设定库聚合根、人物、地点、世界设定
│   ├── cast/              # 人物关系图、角色调度
│   ├── knowledge/         # 知识图谱三元组
│   ├── ai/                # AI 服务接口定义
│   └── shared/            # 共享内核（基类、异常、事件）
│
├── application/           # 应用层 - 用例编排
│   ├── core/              # 小说/章节基础服务
│   ├── blueprint/         # 规划服务（宏观规划、幕级规划）
│   ├── engine/            # 生成引擎、自动驾驶守护进程
│   ├── world/             # Bible、知识图谱服务
│   ├── audit/             # 审阅、宏观重构服务
│   ├── analyst/           # 文风分析、张力分析服务
│   ├── workbench/         # 工作台服务（沙盒对话、故事线）
│   └── workflows/         # 工作流编排
│
├── infrastructure/        # 基础设施层 - 技术实现
│   ├── ai/                # LLM 客户端、向量存储、嵌入服务
│   │   ├── providers/     # 方舟/Anthropic 提供商
│   │   ├── llm_client.py  # 统一 LLM 客户端
│   │   └── local_embedding_service.py
│   └── persistence/       # 持久化实现
│       ├── database/      # SQLite 仓储
│       └── storage/       # 文件存储
│
└── interfaces/            # 接口层 - 外部接口
    └── api/               # REST API（FastAPI）
        └── v1/            # API 版本化
            ├── core/      # 小说/章节 API
            ├── world/     # Bible/知识图谱 API
            ├── blueprint/ # 规划 API
            ├── engine/    # 生成/自动驾驶 API
            ├── audit/     # 审阅 API
            ├── analyst/   # 分析 API
            └── workbench/ # 工作台 API
```

### 前端架构

```
frontend/
├── src/
│   ├── api/              # API 客户端封装
│   ├── components/       # Vue 组件
│   │   ├── autopilot/   # 自动驾驶面板
│   │   ├── charts/      # 图表组件
│   │   ├── graphs/      # 关系图可视化
│   │   ├── knowledge/   # 知识图谱面板
│   │   ├── panels/      # 功能面板
│   │   └── workbench/   # 工作台组件
│   ├── stores/          # Pinia 状态管理
│   ├── router/          # Vue Router 路由
│   ├── views/           # 页面视图
│   └── utils/           # 工具函数
└── package.json
```

---

## 核心模块详解

### 1. Domain 层（领域层）

| 模块 | 职责 | 核心实体 |
|------|------|---------|
| `novel/` | 小说聚合根管理 | Novel, Chapter, Storyline, ForeshadowingRegistry |
| `bible/` | 设定库管理 | Bible, Character, Location, WorldSetting |
| `cast/` | 人物关系网络 | CastGraph, CharacterRelation, AppearanceScheduler |
| `knowledge/` | 知识图谱 | Triple, ChapterSummary, StoryKnowledge |
| `ai/` | AI 服务抽象 | LLMService, PromptTemplate, TokenUsage |

### 2. Application 层（应用层）

| 模块 | 职责 | 核心服务 |
|------|------|---------|
| `core/` | 基础 CRUD | NovelService, ChapterService |
| `blueprint/` | 故事规划 | ContinuousPlanningService, BeatSheetService |
| `engine/` | AI 生成引擎 | HostedWriteService, AutopilotDaemon, ContextBuilder |
| `world/` | 世界构建 | BibleService, KnowledgeGraphService, CastService |
| `audit/` | 质量审计 | ChapterReviewService, MacroRefactorService, ClicheScanner |
| `analyst/` | 内容分析 | VoiceDriftService, TensionAnalyzer, StateExtractor |
| `workbench/` | 工作台 | SandboxDialogueService, StorylineService |

### 3. Infrastructure 层（基础设施层）

| 模块 | 职责 | 技术栈 |
|------|------|--------|
| `ai/llm_client.py` | LLM 统一客户端 | 方舟 SDK / Anthropic SDK |
| `ai/providers/` | 多提供商支持 | AnthropicProvider, MockProvider |
| `ai/local_embedding_service.py` | 向量嵌入 | sentence-transformers |
| `persistence/database/` | 数据持久化 | SQLite, 仓储模式 |

### 4. Interfaces 层（接口层）

| API 模块 | 端点前缀 | 功能 |
|---------|---------|------|
| `core/` | `/api/v1/novels`, `/api/v1/chapters` | 小说和章节管理 |
| `world/` | `/api/v1/bible`, `/api/v1/cast` | Bible 和人物关系 |
| `blueprint/` | `/api/v1/story-structure` | 故事规划 |
| `engine/` | `/api/v1/generate`, `/api/v1/autopilot` | AI 生成和自动驾驶 |
| `audit/` | `/api/v1/review`, `/api/v1/macro-refactor` | 审阅和重构 |
| `analyst/` | `/api/v1/voice-drift`, `/api/v1/foreshadow` | 分析和伏笔 |

---

## 核心优势

### 1. 架构优势

- **DDD 设计模式** - 清晰的领域边界，业务逻辑与技术实现分离
- **SOLID 原则** - 高内聚低耦合，易于扩展和维护
- **仓储模式** - 统一的数据访问接口，支持多种存储后端
- **依赖注入** - FastAPI 原生支持，便于测试和替换实现

### 2. AI 能力

- **多模型支持** - 方舟 API（豆包）、Anthropic Claude 无缝切换
- **上下文管理** - 智能预算分配，POV 防火墙防止信息泄露
- **流式生成** - SSE 实时输出，提升用户体验
- **向量检索** - 基于语义的知识召回，提高生成质量

### 3. 创作辅助

- **知识图谱** - 自动提取实体关系，构建故事世界
- **伏笔管理** - 注册、追踪、解决伏笔，避免遗漏
- **文风一致性** - 实时检测文风漂移，保持叙事风格
- **人物调度** - 基于重要性和出场频率的智能调度算法
- **张力分析** - 可视化情节张力曲线，优化节奏

### 4. 工程质量

- **完整测试** - 211+ 单元/集成测试，覆盖率 > 85%
- **类型安全** - 全面使用 Pydantic 和 TypeScript 类型注解
- **日志系统** - 结构化日志，支持多级别和文件轮转
- **错误处理** - 统一异常处理，友好的错误提示

---

## API 端点

### Novels API

```
POST   /api/v1/novels/                      创建小说
GET    /api/v1/novels/{novel_id}            获取小说详情
GET    /api/v1/novels/                      列出所有小说
PUT    /api/v1/novels/{novel_id}/stage      更新小说阶段
DELETE /api/v1/novels/{novel_id}            删除小说
GET    /api/v1/novels/{novel_id}/statistics 获取统计信息
```

### Chapters API

```
GET    /api/v1/chapters/{chapter_id}                    获取章节
PUT    /api/v1/chapters/{chapter_id}/content            更新章节内容
DELETE /api/v1/chapters/{chapter_id}                    删除章节
GET    /api/v1/chapters/novels/{novel_id}/chapters      列出小说章节
```

### Bible API

```
POST   /api/v1/bible/novels/{novel_id}/bible              创建 Bible
GET    /api/v1/bible/novels/{novel_id}/bible              获取 Bible
POST   /api/v1/bible/novels/{novel_id}/bible/characters   添加人物
POST   /api/v1/bible/novels/{novel_id}/bible/world-settings 添加世界设定
PUT    /api/v1/bible/novels/{novel_id}/bible/characters/{character_id} 更新人物
```

### Generation API

```
POST   /api/v1/novels/{novel_id}/generate-chapter-stream  流式生成章节
POST   /api/v1/novels/{novel_id}/hosted-write-stream      托管写作流
GET    /api/v1/autopilot/status                           自动驾驶状态
POST   /api/v1/autopilot/start                            启动自动驾驶
POST   /api/v1/autopilot/stop                             停止自动驾驶
```

### Knowledge Graph API

```
GET    /api/v1/knowledge-graph/novels/{novel_id}/triples  获取知识三元组
POST   /api/v1/knowledge-graph/novels/{novel_id}/sync     同步知识图谱
GET    /api/v1/knowledge-graph/novels/{novel_id}/graph    获取图谱可视化数据
```

完整 API 文档请访问：http://localhost:8005/docs

---

## 测试

### 运行测试

```bash
# 运行所有测试
pytest tests/unit/ tests/integration/ -v

# 运行特定模块测试
pytest tests/unit/domain/ -v
pytest tests/unit/application/ -v
pytest tests/integration/ -v

# 查看测试覆盖率
pytest tests/ --cov=. --cov-report=html
```

### 测试统计

- **总测试数**: 211+
- **通过率**: 100%
- **代码覆盖率**: > 85%
- **测试类型**: 单元测试 + 集成测试

---

## 部署

### 开发环境

```bash
# 后端开发模式（热重载）
uvicorn interfaces.main:app --reload --port 8005

# 前端开发模式
cd frontend && npm run dev
```

### 生产环境

#### 使用 Gunicorn + Uvicorn Workers

```bash
# 安装 gunicorn
pip install gunicorn

# 启动后端（4 个 worker）
gunicorn interfaces.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8005 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

#### 前端构建

```bash
cd frontend
npm run build

# 构建产物在 frontend/dist/
# 使用 Nginx 或其他静态服务器托管
```

#### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/aitext/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # SSE 支持
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 3600s;
    }

    # API 文档
    location /docs {
        proxy_pass http://127.0.0.1:8005/docs;
    }
}
```

### Docker 部署

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8005

# 启动命令
CMD ["gunicorn", "interfaces.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8005"]
```

```bash
# 构建镜像
docker build -t plotpilot:latest .

# 运行容器
docker run -d \
  -p 8005:8005 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --env-file .env \
  --name plotpilot \
  plotpilot:latest
```

### 环境变量配置

生产环境建议通过环境变量或密钥管理服务配置敏感信息：

```bash
export ARK_API_KEY="your_production_key"
export LOG_LEVEL="WARNING"
export LOG_FILE="/var/log/aitext/app.log"
```

---

## 配置说明

### 后端配置

**环境变量（`.env`）：**

```bash
# LLM 配置
ARK_API_KEY=                    # 方舟 API Key
ARK_BASE_URL=                   # 方舟 API 地址
ARK_MODEL=                      # 模型名称
ARK_TIMEOUT=120                 # 请求超时（秒）

# Anthropic 配置（可选）
ANTHROPIC_API_KEY=              # Anthropic API Key
ANTHROPIC_BASE_URL=             # Anthropic API 地址

# 应用配置
AITEXT_DEFAULT_CHAPTERS=100     # 默认章节数
AITEXT_DEFAULT_WORDS_PER_CHAPTER=3500  # 默认每章字数

# 日志配置
LOG_LEVEL=INFO                  # 日志级别：DEBUG, INFO, WARNING, ERROR
LOG_FILE=logs/aitext.log        # 日志文件路径
```

### 前端配置

**`frontend/vite.config.ts`：**

```typescript
export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8005',
        changeOrigin: true
      }
    }
  }
})
```

---

## 数据管理

### 数据目录结构

```
data/
├── aitext.db              # SQLite 主数据库
├── chromadb/              # 向量数据库
├── novels/                # 小说数据文件
├── bibles/                # Bible 快照
└── foreshadowings/        # 伏笔数据

logs/
└── aitext.log             # 应用日志
```

### 数据库备份

```bash
# 备份 SQLite 数据库
cp data/aitext.db data/aitext.db.backup

# 或使用 SQLite 命令
sqlite3 data/aitext.db ".backup data/aitext.db.backup"
```

### 日志管理

建议配置日志轮转，避免日志文件过大：

```bash
# 清理旧日志（保留最近 7 天）
find logs/ -name "*.log" -mtime +7 -delete

# 或使用 logrotate（Linux）
# /etc/logrotate.d/aitext
/path/to/aitext/logs/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

---

## 技术栈

### 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.9+ | 主语言 |
| FastAPI | 0.109+ | Web 框架 |
| Pydantic | 2.0+ | 数据验证 |
| SQLite | 3.x | 数据库 |
| sentence-transformers | 2.2+ | 向量嵌入 |
| pytest | 7.0+ | 测试框架 |

### 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | 3.5 | UI 框架 |
| TypeScript | 5.9 | 类型安全 |
| Vite | 8.0 | 构建工具 |
| Naive UI | 2.44 | 组件库 |
| Pinia | 3.0 | 状态管理 |
| ECharts | 6.0 | 数据可视化 |
| Vue Router | 4.6 | 路由管理 |

### AI 服务

- **方舟 API** - 字节跳动豆包模型
- **Anthropic Claude** - Claude 3.5 Sonnet / Opus

---

## 开发指南

### 添加新功能

1. **定义领域模型** - 在 `domain/` 中创建实体和值对象
2. **实现仓储接口** - 在 `infrastructure/persistence/` 中实现持久化
3. **编写应用服务** - 在 `application/` 中编排业务逻辑
4. **暴露 API 端点** - 在 `interfaces/api/v1/` 中创建路由
5. **编写测试** - 在 `tests/` 中添加单元和集成测试

### 代码规范

- **Python**: 遵循 PEP 8，使用类型注解
- **TypeScript**: 遵循 ESLint 规则
- **提交信息**: 使用语义化提交（Conventional Commits）

### 项目结构约定

- 每个聚合根一个目录
- 服务类以 `Service` 结尾
- 仓储接口以 `Repository` 结尾
- DTO 类以 `DTO` 结尾

---

## 已知限制

1. **向量检索未完全实现** - 部分场景仍使用简单文本匹配
2. **日志文件可能快速增长** - 建议配置日志轮转
3. **大文件服务类** - 部分服务类超过 1000 行，需要重构
4. **前端性能优化** - 大型知识图谱渲染可能较慢

---

## 文档

- [架构文档](docs/ARCHITECTURE.md)
- [系统架构分析](docs/system-architecture-analysis.md)
- [知识图谱设计](docs/knowledge_graph_auto_inference.md)
- [故事结构设计](docs/story_structure_complete_design.md)
- [人物调度器指南](docs/character-scheduler-simulator-guide.md)

---

## 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 联系方式

如有问题或建议，请创建 [Issue](../../issues)

---

**PlotPilot · 墨枢** - 让 AI 成为你的创作伙伴
