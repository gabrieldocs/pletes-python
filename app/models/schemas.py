from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    user_id: str

class UserBase(BaseModel):
    username: str

class GithubProfileBase(BaseModel):
    github_name: str 
    github_login: str 
    github_email: str 
    github_bio: str
    github_company: str
    github_url:str
    github_html_url: str