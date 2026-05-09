from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact = Column(String(100))
    address = Column(Text)
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    
    products = relationship("Product", back_populates="supplier")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    material = Column(String(50))
    color = Column(String(50))
    unit = Column(String(20), default="件")
    cost_price = Column(Float, default=0.0)
    sale_price = Column(Float, default=0.0)
    min_stock = Column(Integer, default=10)
    image_url = Column(String(500))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    supplier = relationship("Supplier", back_populates="products")
    batches = relationship("Batch", back_populates="product")
    stock = relationship("Stock", back_populates="product", uselist=False)

class Batch(Base):
    __tablename__ = "batches"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    batch_no = Column(String(50), unique=True)
    quantity = Column(Integer, default=0)
    cost_price = Column(Float, default=0.0)
    production_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    
    product = relationship("Product", back_populates="batches")

class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True)
    batch_id = Column(Integer, ForeignKey("batches.id"))
    quantity = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    product = relationship("Product", back_populates="stock")

class InRecord(Base):
    __tablename__ = "in_records"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    batch_id = Column(Integer, ForeignKey("batches.id"))
    quantity = Column(Integer, nullable=False)
    cost_price = Column(Float)
    operator = Column(String(50))
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

class OutRecord(Base):
    __tablename__ = "out_records"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    batch_id = Column(Integer, ForeignKey("batches.id"))
    quantity = Column(Integer, nullable=False)
    sale_price = Column(Float)
    operator = Column(String(50))
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

class AlertRecord(Base):
    __tablename__ = "alert_records"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    alert_type = Column(String(20))  # stock_low, slow_selling, expired
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

# 数据库连接
DATABASE_URL = "sqlite:///./jewelry_inventory.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
