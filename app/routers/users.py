from typing import Annotated

import requests
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database.config import SessionLocal
from ..models.models import User
from ..models.schemas import UserBase

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/users/', status_code=status.HTTP_200_OK)
async def index(db: db_dependency, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def find_one(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details='User not found')
    return user


@router.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()

@router.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Update the user attributes
    db_user.username = user.username
    
    # Commit the changes to the database
    db.commit()
    
    return db_user

@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_one(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(user)
    db.commit()

@router.get("/users/{username}/github", status_code=status.HTTP_200_OK)
async def get_user_github_data(username):
     # GitHub API endpoint for fetching user information
    url = f"https://api.github.com/users/{username}"

    # Send GET request to the GitHub API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        user_info = response.json()
        
        # Extract username and email from the response
        github_username = user_info.get('login')
        github_email = user_info.get('email')

        return {"username": github_username, "email": github_email}
    else:
        # If the request was not successful, print an error message
        print(f"Failed to fetch user information: {response.status_code}")
        return None, None