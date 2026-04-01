from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, database

router = APIRouter(prefix="/todos", tags=["todos"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Todo)
def create(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@router.get("/", response_model=List[schemas.Todo])
def list_all(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@router.get("/{todo_id}", response_model=schemas.Todo)
def get_by_id(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo não encontrado")
    return db_todo


@router.put("/{todo_id}", response_model=schemas.Todo)
def update(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id, todo)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo não encontrado")
    return db_todo

@router.delete("/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo(db, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo não encontrado")
    return {"message": "Todo deletado com sucesso"}
