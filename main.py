from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, github, posts, projects, users

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with the list of allowed origins if needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(github.router)
app.include_router(posts.router)
