from typing import Annotated

import requests
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from ..database.config import SessionLocal
from ..models.models import GithubProfile
from ..models.schemas import GithubProfileBase

router = APIRouter(
    prefix="/github",
    tags=["github"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def get_access_token(authorization: str = Header(...)):
    """Custom dependency to extract access token from request headers."""
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        return token
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")

@router.post("/create-repo")
async def create_github_repo(repo_name: str, access_token: str = Depends(get_access_token)):
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "private": False  # Set to True if you want to create a private repository
        # Other optional parameters: description, homepage, private, visibility, auto_init
    }
    response = requests.post("https://api.github.com/user/repos", headers=headers, json=data)
    
    if response.status_code == 201:
        return {"message": "Repository created successfully!"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
