# 后端运行说明

## 环境要求
- Python 3.9+
- SQLite（内置，无需安装）

## 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

## 启动服务

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API 文档

启动后访问：http://localhost:8000/docs

## 核心接口一览

### 商品管理
- `GET /api/products` - 商品列表（支持 category/material/color/keyword 筛选）
- `POST /api/products` - 新增商品
- `GET /api/products/{id}` - 获取商品详情
- `PUT /api/products/{id}` - 更新商品
- `DELETE /api/products/{id}` - 删除商品（库存为0时可用）
- `POST /api/products/upload-image/{id}` - 上传商品图片

### 入库管理
- `GET /api/in-records` - 入库记录列表
- `POST /api/in-records` - 新增进库记录（支持自动创建商品）

### 出库管理
- `GET /api/out-records` - 出库记录列表
- `POST /api/out-records` - 新增出库记录（FIFO批次扣减）

### 库存管理
- `GET /api/stocks` - 库存列表
- `GET /api/stocks/check-alerts` - 扫描并生成库存预警
- `GET /api/stocks/alerts` - 预警列表

### 看板数据
- `GET /api/dashboard/today` - 今日数据（销售额/订单数/出库量 及对比昨日变化）
- `GET /api/dashboard/stats` - 统计周期数据（period: day/week/month）

### 供应商管理
- `GET /api/suppliers` - 供应商列表
- `POST /api/suppliers` - 新增供应商
- `PUT /api/suppliers/{id}` - 更新供应商
- `DELETE /api/suppliers/{id}` - 删除供应商
- `GET /api/suppliers/{id}/products` - 供应商商品统计

### 语音录入（AI）
- `POST /api/voice/parse` - 解析语音文本，返回结构化数据
- `POST /api/voice/in-record` - 语音直接入库（一步完成）
  - 示例语音："入库珍珠项链10件单价200"
- `POST /api/voice/upload` - 上传语音文件并转写（需要 whisper）

## 数据库

SQLite 数据库文件：`backend/jewelry_inventory.db`

表结构：products / batches / stocks / in_records / out_records / alert_records / suppliers

## 前端对接

前端运行在 5173 端口时，后端需配置 CORS 允许跨域（已配置 allow_origins=["*"]）。
