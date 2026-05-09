from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import base64
import tempfile
import os
from datetime import datetime

from ..models import get_db, Product, Stock, InRecord, Batch
from ..schemas import VoiceParseResult

router = APIRouter(prefix="/api")

def parse_voice_command(text: str) -> dict:
    """
    解析语音命令文本，返回结构化数据
    支持格式示例：
    - "入库 珍珠项链 10件 单价200"
    - "入库 银色耳环 5件"
    - "出库 黄金手镯 2件"
    """
    text = text.strip()
    
    # 判断是入库还是出库
    if text.startswith("入库") or text.startswith("进库") or text.startswith("进货"):
        action = "in"
        text = text[2:].strip()
    elif text.startswith("出库") or text.startswith("销货") or text.startswith("卖出"):
        action = "out"
        text = text[2:].strip()
    else:
        return {"action": "unknown", "raw": text}
    
    # 提取数量（件/个/条/对/枚 等）
    quantity = 1
    import re
    q_match = re.search(r"(\d+)\s*(?:件|个|条|对|枚|套|箱|包)", text)
    if q_match:
        quantity = int(q_match.group(1))
        text = re.sub(r"\d+\s*(?:件|个|条|对|枚|套|箱|包)", "", text).strip()
    
    # 提取单价
    price = None
    p_match = re.search(r"(?:单价|价格|每[件个条对枚套箱包])\s*[:：]?\s*(\d+(?:\.\d+)?)", text)
    if not p_match:
        p_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:元|块)", text)
    if p_match:
        price = float(p_match.group(1))
        text = re.sub(r"(?:单价|价格|每[件个条对枚套箱包])?\s*[:：]?\s*\d+(?:\.\d+)?\s*(?:元|块)?", "", text).strip()
        text = re.sub(r"\d+(?:\.\d+)?\s*(?:元|块)", "", text).strip()
    
    # 剩余文字作为商品名称
    product_name = text.strip()
    
    return {
        "action": action,
        "product_name": product_name,
        "quantity": quantity,
        "price": price
    }


@router.post("/voice/parse", response_model=VoiceParseResult)
def parse_voice(
    text: str,
    db: Session = Depends(get_db)
):
    """解析语音文本，返回结构化数据（不入库）"""
    parsed = parse_voice_command(text)
    return VoiceParseResult(text=text, parsed=parsed)


@router.post("/voice/in-record")
def voice_in_record(
    text: str,
    operator: str = "语音录入",
    db: Session = Depends(get_db)
):
    """语音录入入库（一步完成）"""
    from .routes import generate_batch_no
    
    parsed = parse_voice_command(text)
    
    if parsed["action"] != "in":
        raise HTTPException(status_code=400, detail="请说\"入库+商品名+数量\"，例如：入库珍珠项链10件")
    
    product_name = parsed["product_name"]
    quantity = parsed["quantity"]
    price = parsed.get("price") or 0.0
    
    # 查找或创建商品
    product = db.query(Product).filter(Product.name == product_name).first()
    if not product:
        product = Product(
            name=product_name,
            category="未分类",
            cost_price=price,
            sale_price=price * 1.5 if price else 0.0
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        
        # 创建库存记录
        stock = Stock(product_id=product.id, quantity=0)
        db.add(stock)
        db.commit()
    
    # 生成批次
    batch_no = generate_batch_no(db)
    batch = Batch(
        product_id=product.id,
        batch_no=batch_no,
        quantity=quantity,
        cost_price=price
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    
    # 创建入库记录
    record = InRecord(
        product_id=product.id,
        batch_id=batch.id,
        quantity=quantity,
        cost_price=price,
        operator=operator,
        note=f"语音录入：{text}"
    )
    db.add(record)
    
    # 更新库存
    stock = db.query(Stock).filter(Stock.product_id == product.id).first()
    stock.quantity += quantity
    stock.batch_id = batch.id
    stock.updated_at = datetime.now()
    
    db.commit()
    db.refresh(record)
    
    return {
        "message": f"入库成功",
        "product_name": product.name,
        "quantity": quantity,
        "price": price,
        "record_id": record.id,
        "batch_no": batch_no
    }


@router.post("/voice/upload")
async def upload_voice(
    file_bytes: bytes,
    db: Session = Depends(get_db)
):
    """
    上传语音文件并转写（需要 whisper 或外部 TTS API）
    这里返回占位，实际需要 whisper 本地推理或调用 API
    """
    # 保存临时文件
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
        f.write(file_bytes)
        tmp_path = f.name
    
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(tmp_path)
        text = result["text"]
        
        # 解析命令
        parsed = parse_voice_command(text)
        
        return {
            "text": text,
            "parsed": parsed,
            "confidence": result.get("confidence", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"语音识别失败: {str(e)}")
    finally:
        os.unlink(tmp_path)
