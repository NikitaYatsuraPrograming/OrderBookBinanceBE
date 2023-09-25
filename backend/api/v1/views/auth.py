from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login")
async def login():
    return {'code': 200}
