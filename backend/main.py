from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import create_tables
from app.api.routes import router
from app.api.voice import router as voice_router

app = FastAPI(
    title="饰品店 AI 库存管理系统",
    description="霓虹仓库 - 智能库存管理",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 初始化数据库
@app.on_event("startup")
async def startup():
    create_tables()
    logger.info("数据库初始化完成")

# 注册路由
app.include_router(router)
app.include_router(voice_router)

@app.get("/")
def root():
    return {
        "message": "🌐 霓虹仓库 API 服务运行中",
        "version": "1.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)