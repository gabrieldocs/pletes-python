from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database.config import SessionLocal
from ..models.models import Post
from ..models.schemas import PostBase

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

# Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/posts", status_code=status.HTTP_200_OK)
async def index(db: db_dependency, skip: int = 0, limit:int = 100):
    return db.query(Post).offset(skip).limit(limit).all()

@router.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db : db_dependency):
    db_post = Post(**post.model_dump())
    db.add(db_post)
    db.commit()