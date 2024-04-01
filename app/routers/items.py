from fastapi import APIRouter

router = APIRouter(
    prefix="/items"
)

# @router.get("/items")
# async def index():
#     return []

@router.get("/items")
async def find_all(skip: int=0, count: int=10, page: int=1):
    return {
        "meta":{"skip" : skip, "count": count, "page": page},
        "results" : []
    }