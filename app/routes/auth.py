from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


class RequestOtpBody(BaseModel):
    email: EmailStr


class VerifyOtpBody(BaseModel):
    email: EmailStr
    code: str


@router.post("/request-otp")
async def request_otp(body: RequestOtpBody, db: Session = Depends(get_db)):
    return await auth_service.request_otp(body.email, db)


@router.post("/verify-otp")
def verify_otp(body: VerifyOtpBody, db: Session = Depends(get_db)):
    return auth_service.verify_otp(body.email, body.code, db)
