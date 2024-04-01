import os
from typing import Annotated, Optional

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..database.config import SessionLocal
from ..models.models import GithubProfile
from ..models.schemas import GithubProfileBase

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/login")
async def login():
    github_client_id = os.getenv("GITHUB_CLIENT_ID")
    github_redirect_url = os.getenv("GITHUB_REDIRECT_URI")
    # github_redirect_url = "http://localhost:5137"
    return RedirectResponse(url=f"https://github.com/login/oauth/authorize?client_id={github_client_id}&redirect_uri={github_redirect_url}&scope=repo")

@router.get("/oauth/callback", status_code=status.HTTP_201_CREATED)
async def oauth_callback( db: db_dependency, code: Optional[str] = Query(None)):
    if code is None:
        raise HTTPException(status_code=400, detail="Authorization code not provided")

    # Exchange authorization code for access token
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": os.getenv("GITHUB_CLIENT_ID"),
            "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
            "code": code,
            "redirect_uri": os.getenv("GITHUB_REDIRECT_URI")
        },
        headers={"Accept": "application/json"}
    )
    
    access_token = response.json().get("access_token")
    frontend_redirect_url = f"http://localhost:5173/oauth/callback?access_token={access_token}"
    print(response.json())
    
    # Fetch user information from GitHub
    user_info = get_github_user_info(access_token)
    # Add user information to the database
    github_profile = GithubProfile(
        github_name=user_info.get("name"),
        github_login=user_info.get("login"),
        github_email=user_info.get("email"),
        github_bio=user_info.get("bio"),
        github_company=user_info.get("company"),
        github_url=user_info.get("url"),
        github_html_url=user_info.get("html_url")
    )

    existing_profile = db.query(GithubProfile).filter(GithubProfile.github_login == user_info.get("login")).first()

    if existing_profile:
        return {
            "githubUser" : existing_profile,
            "accessToken" : access_token
        }

    github_user = db.add(github_profile)
    db.commit()
    # return get_github_user_info(response.json().get("access_token"))
    return {
        "githubUser" : github_user,
        "accessToken" : access_token
    }

    # return RedirectResponse(url=frontend_redirect_url)
    # returns the token
    # access_token = response.json().get("access_token")

    # Use the access token to authenticate requests to GitHub API
    # Store the access token securely and associate it with the user
    # return {"access_token": access_token}

@router.get("/user")
def get_github_user_info(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.github.com/user", headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch user information from GitHub")