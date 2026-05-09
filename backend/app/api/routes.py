from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
import os
import shutil

from ..models import get_db, Product, InRecord, OutRecord, Stock, AlertRecord, Supplier, Batch
from ..schemas import (
    ProductCreate, ProductResponse,
    InRecordCreate, InRecordResponse,
    OutRecordCreate, OutRecordResponse,
    StockResponse, AlertResponse,
    DashboardToday, DashboardStats,
    SupplierCreate, SupplierResponse
)

router = APIRouter(prefix="/api")

# ========== 商品管理 ==========
@router.get("/products", response_model=List[ProductResponse])
def get_products(
    category: Optional[str] = None,
    material: Optional[str] = None,
    color: Optional[str] = None,
    keyword: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    if material:
        query = query.filter(Product.material == material)
    if color:
        query = query.filter(Product.color == color)
    if keyword:
        query = query.filter(Product.name.contains(keyword))
    return query.offset(skip).limit(limit).all()

@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product

@router.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # 自动创建库存记录
    stock = Stock(product_id=db_product.id, quantity=0)
    db.add(stock)
    db.commit()
    
    return db_product

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db_product.updated_at = datetime.now()
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    # 检查库存是否为0
    stock = db.query(Stock).filter(Stock.product_id == product_id).first()
    if stock and stock.quantity > 0:
        raise HTTPException(status_code=400, detail=f"库存不为0（当前库存：{stock.quantity}），无法删除")
    
    db.delete(db_product)
    db.commit()
    return {"message": "删除成功"}

@router.post("/products/upload-image/{product_id}")
def upload_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传商品图片"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="仅支持 jpeg/png/webp/gif 图片格式")
    
    # 生成文件名
    ext = os.path.splitext(file.filename)[1].lower()
    if not ext:
        ext = ".jpg"
    filename = f"product_{product_id}_{int(datetime.now().timestamp())}{ext}"
    filepath = os.path.join("uploads", filename)
    
    # 保存文件
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 更新商品图片URL
    product.image_url = f"/uploads/{filename}"
    product.updated_at = datetime.now()
    db.commit()
    db.refresh(product)
    
    return {"image_url": product.image_url, "message": "上传成功"}

# ========== 入库管理 ==========
def generate_batch_no(db: Session) -> str:
    """生成批次号：BYYYYMMDD001"""
    today = datetime.now().strftime("%Y%m%d")
    prefix = f"B{today}"
    
    # 查找今天最大的批次号
    last_batch = db.query(Batch).filter(Batch.batch_no.like(f"{prefix}%")).order_by(Batch.batch_no.desc()).first()
    
    if last_batch:
        last_no = int(last_batch.batch_no[-3:])
        new_no = last_no + 1
    else:
        new_no = 1
    
    return f"{prefix}{new_no:03d}"

@router.get("/in-records", response_model=List[InRecordResponse])
def get_in_records(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(InRecord)
    if start_date:
        query = query.filter(InRecord.created_at >= start_date)
    if end_date:
        query = query.filter(InRecord.created_at <= end_date)
    return query.order_by(InRecord.created_at.desc()).offset(skip).limit(limit).all()

@router.post("/in-records", response_model=InRecordResponse)
def create_in_record(record: InRecordCreate, db: Session = Depends(get_db)):
    # 如果商品不存在，自动创建商品
    product = db.query(Product).filter(Product.id == record.product_id).first()
    if not product:
        # 自动创建商品（使用最小信息）
        product = Product(
            id=record.product_id,
            name=f"未命名商品-{record.product_id}",
            category="未分类"
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        
        # 创建库存记录
        stock = Stock(product_id=product.id, quantity=0)
        db.add(stock)
        db.commit()
    
    # 生成批次号
    batch_no = generate_batch_no(db)
    batch = Batch(
        product_id=record.product_id,
        supplier_id=record.product_id,  # 简化处理
        batch_no=batch_no,
        quantity=record.quantity,
        cost_price=record.cost_price or 0.0
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    
    # 创建入库记录（关联批次）
    db_record = InRecord(
        product_id=record.product_id,
        batch_id=batch.id,
        quantity=record.quantity,
        cost_price=record.cost_price,
        operator=record.operator,
        note=record.note
    )
    db.add(db_record)
    db.commit()
    
    # 更新库存
    stock = db.query(Stock).filter(Stock.product_id == record.product_id).first()
    if stock:
        stock.quantity += record.quantity
        stock.batch_id = batch.id
        stock.updated_at = datetime.now()
    db.commit()
    db.refresh(db_record)
    return db_record

# ========== 出库管理 ==========
@router.get("/out-records", response_model=List[OutRecordResponse])
def get_out_records(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(OutRecord)
    if start_date:
        query = query.filter(OutRecord.created_at >= start_date)
    if end_date:
        query = query.filter(OutRecord.created_at <= end_date)
    return query.order_by(OutRecord.created_at.desc()).offset(skip).limit(limit).all()

@router.post("/out-records", response_model=OutRecordResponse)
def create_out_record(record: OutRecordCreate, db: Session = Depends(get_db)):
    # 检查库存
    stock = db.query(Stock).filter(Stock.product_id == record.product_id).first()
    if not stock or stock.quantity < record.quantity:
        raise HTTPException(
            status_code=400, 
            detail=f"库存不足（当前库存：{stock.quantity if stock else 0}，需要：{record.quantity}）"
        )
    
    # FIFO: 获取最早的批次
    batches = db.query(Batch).filter(
        Batch.product_id == record.product_id,
        Batch.quantity > 0
    ).order_by(Batch.created_at.asc()).all()
    
    remaining = record.quantity
    total_cost = 0.0
    used_batches = []
    
    for batch in batches:
        if remaining <= 0:
            break
        take = min(batch.quantity, remaining)
        batch.quantity -= take
        remaining -= take
        total_cost += take * (batch.cost_price or 0)
        used_batches.append({"batch_id": batch.id, "quantity": take})
    
    # 创建出库记录（使用第一个批次）
    db_record = OutRecord(
        product_id=record.product_id,
        batch_id=used_batches[0]["batch_id"] if used_batches else None,
        quantity=record.quantity,
        sale_price=record.sale_price,
        operator=record.operator,
        note=record.note
    )
    db.add(db_record)
    db.commit()
    
    # 扣减库存
    stock.quantity -= record.quantity
    stock.updated_at = datetime.now()
    db.commit()
    db.refresh(db_record)
    return db_record

# ========== 库存管理 ==========
@router.get("/stocks", response_model=List[StockResponse])
def get_stocks(
    category: Optional[str] = None,
    alert_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Stock).join(Product)
    if category:
        query = query.filter(Product.category == category)
    return query.all()

@router.get("/stocks/{product_id}", response_model=StockResponse)
def get_stock(product_id: int, db: Session = Depends(get_db)):
    stock = db.query(Stock).filter(Stock.product_id == product_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="库存记录不存在")
    return stock

@router.get("/stocks/check-alerts")
def check_stock_alerts(db: Session = Depends(get_db)):
    """扫描库存并生成预警"""
    alerts_created = []
    
    # 1. 库存低于 min_stock 预警
    stocks = db.query(Stock).join(Product).all()
    for stock in stocks:
        if stock.quantity < stock.product.min_stock:
            # 检查是否已有未读的低库存预警
            existing = db.query(AlertRecord).filter(
                AlertRecord.product_id == stock.product_id,
                AlertRecord.alert_type == "stock_low",
                AlertRecord.is_read == False
            ).first()
            
            if not existing:
                alert = AlertRecord(
                    product_id=stock.product_id,
                    alert_type="stock_low",
                    message=f"库存不足：{stock.product.name} 当前库存 {stock.quantity}，低于安全库存 {stock.product.min_stock}",
                    is_read=False
                )
                db.add(alert)
                alerts_created.append({
                    "type": "stock_low",
                    "product_id": stock.product_id,
                    "message": alert.message
                })
    
    # 2. 30天无销售滞销预警
    thirty_days_ago = datetime.now() - timedelta(days=30)
    products_with_sales = db.query(OutRecord.product_id).filter(
        OutRecord.created_at >= thirty_days_ago
    ).distinct().all()
    products_with_sales_ids = [p[0] for p in products_with_sales]
    
    all_products = db.query(Product).all()
    for product in all_products:
        if product.id not in products_with_sales_ids:
            # 检查是否已有未读的滞销预警
            existing = db.query(AlertRecord).filter(
                AlertRecord.product_id == product.id,
                AlertRecord.alert_type == "slow_selling",
                AlertRecord.is_read == False
            ).first()
            
            if not existing:
                alert = AlertRecord(
                    product_id=product.id,
                    alert_type="slow_selling",
                    message=f"滞销预警：{product.name} 近30天无销售记录",
                    is_read=False
                )
                db.add(alert)
                alerts_created.append({
                    "type": "slow_selling",
                    "product_id": product.id,
                    "message": alert.message
                })
    
    db.commit()
    return {"alerts_created": len(alerts_created), "details": alerts_created}

@router.get("/stocks/alerts", response_model=List[AlertResponse])
def get_alerts(
    alert_type: Optional[str] = None,
    is_read: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(AlertRecord)
    if alert_type:
        query = query.filter(AlertRecord.alert_type == alert_type)
    if is_read is not None:
        query = query.filter(AlertRecord.is_read == is_read)
    return query.order_by(AlertRecord.created_at.desc()).all()

@router.put("/stocks/alerts/{alert_id}/read")
def mark_alert_read(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(AlertRecord).filter(AlertRecord.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="预警记录不存在")
    alert.is_read = True
    db.commit()
    return {"message": "已标记为已读"}

# ========== 看板数据 ==========
@router.get("/dashboard/today")
def get_dashboard_today(db: Session = Depends(get_db)):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)
    
    # 今日数据
    today_records = db.query(OutRecord).filter(OutRecord.created_at >= today).all()
    today_sales = sum(r.sale_price * r.quantity for r in today_records if r.sale_price)
    today_orders = len(today_records)
    today_out = sum(r.quantity for r in today_records)
    
    # 昨日数据（用于计算变化）
    yesterday_records = db.query(OutRecord).filter(
        OutRecord.created_at >= yesterday,
        OutRecord.created_at < today
    ).all()
    yesterday_sales = sum(r.sale_price * r.quantity for r in yesterday_records if r.sale_price)
    yesterday_orders = len(yesterday_records)
    yesterday_out = sum(r.quantity for r in yesterday_records)
    
    # 计算变化百分比
    sales_change = ((today_sales - yesterday_sales) / yesterday_sales * 100) if yesterday_sales else 0
    orders_change = ((today_orders - yesterday_orders) / yesterday_orders * 100) if yesterday_orders else 0
    out_change = ((today_out - yesterday_out) / yesterday_out * 100) if yesterday_out else 0
    
    return DashboardToday(
        today_sales=round(today_sales, 2),
        today_orders=today_orders,
        today_out=today_out,
        sales_change=round(sales_change, 1),
        orders_change=round(orders_change, 1),
        out_change=round(out_change, 1)
    )

@router.get("/dashboard/stats")
def get_dashboard_stats(period: str = "day", db: Session = Depends(get_db)):
    now = datetime.now()
    if period == "day":
        start = now - timedelta(days=7)
    elif period == "week":
        start = now - timedelta(weeks=4)
    elif period == "month":
        start = now - timedelta(days=30)
    else:
        start = now - timedelta(days=7)
    
    records = db.query(OutRecord).filter(OutRecord.created_at >= start).all()
    total_sales = sum(r.sale_price * r.quantity for r in records if r.sale_price)
    total_orders = len(records)
    
    # 热销排行（近7天）
    seven_days_ago = now - timedelta(days=7)
    recent_records = db.query(OutRecord).filter(OutRecord.created_at >= seven_days_ago).all()
    
    product_sales = {}
    for r in recent_records:
        if r.product_id not in product_sales:
            product_sales[r.product_id] = {"quantity": 0, "sales": 0.0}
        product_sales[r.product_id]["quantity"] += r.quantity
        if r.sale_price:
            product_sales[r.product_id]["sales"] += r.sale_price * r.quantity
    
    # 获取商品名称
    top_products = []
    for pid, data in sorted(product_sales.items(), key=lambda x: x[1]["quantity"], reverse=True)[:5]:
        product = db.query(Product).filter(Product.id == pid).first()
        top_products.append({
            "product_id": pid,
            "name": product.name if product else "未知商品",
            "quantity": data["quantity"],
            "sales": round(data["sales"], 2)
        })
    
    # 滞销排行（30天无销售）
    thirty_days_ago = now - timedelta(days=30)
    recent_product_ids = db.query(OutRecord.product_id).filter(
        OutRecord.created_at >= thirty_days_ago
    ).distinct().all()
    recent_product_ids = [p[0] for p in recent_product_ids]
    
    slow_products = []
    all_stocks = db.query(Stock).join(Product).filter(Stock.quantity > 0).all()
    for stock in all_stocks:
        if stock.product_id not in recent_product_ids:
            # 查找最后销售日期
            last_sale = db.query(OutRecord).filter(
                OutRecord.product_id == stock.product_id
            ).order_by(OutRecord.created_at.desc()).first()
            
            slow_products.append({
                "product_id": stock.product_id,
                "name": stock.product.name if stock.product else "未知商品",
                "quantity": stock.quantity,
                "last_sale": last_sale.created_at.strftime("%Y-%m-%d") if last_sale else "从未销售"
            })
    
    # 按库存数量排序，取前5
    slow_products = sorted(slow_products, key=lambda x: x["quantity"], reverse=True)[:5]
    
    return {
        "period": period,
        "total_sales": round(total_sales, 2),
        "total_orders": total_orders,
        "top_products": top_products,
        "slow_products": slow_products
    }

# ========== 供应商管理 ==========
@router.get("/suppliers", response_model=List[SupplierResponse])
def get_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Supplier).offset(skip).limit(limit).all()

@router.get("/suppliers/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    return supplier

@router.post("/suppliers", response_model=SupplierResponse)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    db_supplier = Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@router.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
def update_supplier(supplier_id: int, supplier: SupplierCreate, db: Session = Depends(get_db)):
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    for key, value in supplier.dict().items():
        setattr(db_supplier, key, value)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@router.delete("/suppliers/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    db.delete(db_supplier)
    db.commit()
    return {"message": "删除成功"}

@router.get("/suppliers/{supplier_id}/products")
def get_supplier_products(supplier_id: int, db: Session = Depends(get_db)):
    """获取供应商关联的商品统计"""
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="供应商不存在")
    
    products = db.query(Product).filter(Product.supplier_id == supplier_id).all()
    total_products = len(products)
    total_stock = db.query(func.sum(Stock.quantity)).filter(
        Stock.product_id.in_([p.id for p in products])
    ).scalar() or 0
    
    return {
        "supplier_id": supplier_id,
        "supplier_name": supplier.name,
        "total_products": total_products,
        "total_stock": total_stock,
        "products": [{"id": p.id, "name": p.name, "category": p.category} for p in products]
    }