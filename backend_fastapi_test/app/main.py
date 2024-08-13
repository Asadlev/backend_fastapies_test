from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, auth
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(SessionLocal)):
    db_author = db.query(models.Author).filter(models.Author.username == author.username).first()
    if db_author:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.hash_password(author.password)
    db_author = models.Author(username=author.username, password=hashed_password)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.get("/all", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(SessionLocal)):
    return db.query(models.Author).all()
