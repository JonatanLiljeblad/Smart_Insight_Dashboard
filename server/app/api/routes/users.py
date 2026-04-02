from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.schemas.user import UserOut

router = APIRouter()


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: UserOut = Depends(get_current_user)):
    return current_user
