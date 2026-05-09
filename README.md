# 饰品店 AI 库存管理系统

## 技术栈
- **后端**: FastAPI + SQLite + Redis
- **前端**: React + TailwindCSS
- **AI**: Whisper (本地) + 第三方图像 API
- **风格**: 霓虹赛博朋克

## 目录结构
```
jewelry-inventory/
├── backend/          # FastAPI 后端
│   ├── app/
│   │   ├── api/      # API 路由
│   │   ├── models/   # 数据库模型
│   │   ├── services/ # 业务逻辑
│   │   └── ai/       # AI 能力
│   ├── requirements.txt
│   └── main.py
├── frontend/         # React 前端
│   ├── src/
│   ├── public/
│   └── package.json
├── ai-models/        # 本地 AI 模型
└── docs/            # 文档
```

## 快速启动

### 后端
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 前端
```bash
cd frontend
npm install
npm start
```

## 开发计划
- Sprint 0: 环境搭建 (2天)
- Sprint 1: MVP 核心功能 (5天)
- Sprint 2: V1.0 完整功能 (5天)
- Sprint 3: V1.5 智能化 (6天)
- Sprint 4: V2.0 扩展 (6天)
