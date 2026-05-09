from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# 分页响应
class PaginatedResponse(BaseModel):
    total: int
    items: List[dict]
    page: int
    page_size: int

# 供应商
class SupplierBase(BaseModel):
    name: str
    contact: Optional[str] = None
    address: Optional[str] = None
    note: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 商品
class ProductBase(BaseModel):
    name: str
    category: str
    material: Optional[str] = None
    color: Optional[str] = None
    unit: Optional[str] = "件"
    cost_price: Optional[float] = 0.0
    sale_price: Optional[float] = 0.0
    min_stock: Optional[int] = 10
    image_url: Optional[str] = None
    supplier_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 入库
class InRecordBase(BaseModel):
    product_id: int
    batch_id: Optional[int] = None
    quantity: int
    cost_price: Optional[float] = None
    operator: Optional[str] = None
    note: Optional[str] = None

class InRecordCreate(InRecordBase):
    pass

class InRecordResponse(InRecordBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 出库
class OutRecordBase(BaseModel):
    product_id: int
    batch_id: Optional[int] = None
    quantity: int
    sale_price: Optional[float] = None
    operator: Optional[str] = None
    note: Optional[str] = None

class OutRecordCreate(OutRecordBase):
    pass

class OutRecordResponse(OutRecordBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 库存
class StockResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    updated_at: datetime
    product: Optional[ProductResponse] = None
    
    class Config:
        from_attributes = True

# 预警
class AlertResponse(BaseModel):
    id: int
    product_id: int
    alert_type: str
    message: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# 看板数据
class DashboardToday(BaseModel):
    today_sales: float
    today_orders: int
    today_out: int
    sales_change: float
    orders_change: float
    out_change: float

class DashboardStats(BaseModel):
    period: str
    total_sales: float
    total_orders: int
    top_products: List[dict]
    slow_products: List[dict]

# AI 语音
class VoiceInput(BaseModel):
    audio_base64: str

class VoiceParseResult(BaseModel):
    text: str
    parsed: dict

# AI 图片
class ImageMatch(BaseModel):
    image_base64: str

class ImageMatchResult(BaseModel):
    matches: List[dict]