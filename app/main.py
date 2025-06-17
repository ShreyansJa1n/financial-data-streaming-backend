from fastapi import FastAPI
from app.api.api import api_router
from fastapi import APIRouter

app = FastAPI()

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


router.include_router(api_router, tags=["prices"])

app.include_router(router)
