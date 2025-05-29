from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def create_item(db: Session, model, data):
    item = model(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_all_items(db: Session, model):
    return db.query(model).all()

def get_item_by_id(db: Session, model, item_id: int):
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

def update_item(db: Session, model, item_id: int, data):
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, model, item_id: int):
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}
