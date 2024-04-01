from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database.config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class GithubProfile(Base):
    __tablename__ = 'github_profiles'

    id = Column(Integer, primary_key=True, index=True)
    github_name = Column(String)
    github_login = Column(String, unique=True)
    github_email = Column(String, unique=True)
    github_bio = Column(String, unique=True)
    github_company = Column(String)
    github_url = Column(String)
    github_html_url = Column(String)
    
    posts = relationship("Post", back_populates="github_profile")
    repositories = relationship("Repositories", back_populates="github_profile")

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), default='')
    content = Column(String(256), default='')
    github_profile_id = Column(Integer, ForeignKey("github_profiles.id"))

    github_profile = relationship("GithubProfile", back_populates="posts")

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
        

class GithubRepositorie(Base):
    __tablename__ = 'repositories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), default='')
    description = Column(String(256), default='')
    github_url = Column(String, default='')
    github_profile_id = Column(Integer, ForeignKey("github_profiles.id"))

    github_profile = relationship("GithubProfile", back_populates="repositories")

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
        