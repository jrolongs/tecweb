import secrets
import string
from datetime import datetime, timedelta

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.db_models import OtpCode, AuthToken
from app.services.email_service import send_otp_email

OTP_TTL_MINUTES = 5
TOKEN_TTL_HOURS = 8


def _generate_code() -> str:
    return "".join(secrets.choice(string.digits) for _ in range(6))


async def request_otp(email: str, db: Session) -> dict:
    code = _generate_code()
    expires_at = datetime.utcnow() + timedelta(minutes=OTP_TTL_MINUTES)

    otp = OtpCode(email=email, code=code, expires_at=expires_at, used=False)
    db.add(otp)
    db.commit()

    await send_otp_email(email, code)
    return {"status": "success", "message": f"Código enviado a {email}"}


def verify_otp(email: str, code: str, db: Session) -> dict:
    otp = (
        db.query(OtpCode)
        .filter(OtpCode.email == email, OtpCode.code == code, OtpCode.used == False)
        .order_by(OtpCode.id.desc())
        .first()
    )

    if not otp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Código inválido")

    if otp.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Código expirado")

    otp.used = True

    token_value = secrets.token_urlsafe(32)
    token = AuthToken(
        token=token_value,
        email=email,
        expires_at=datetime.utcnow() + timedelta(hours=TOKEN_TTL_HOURS),
    )
    db.add(token)
    db.commit()

    return {"token": token_value, "email": email}


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")

    token_value = authorization.split(" ", 1)[1].strip()
    token = db.query(AuthToken).filter(AuthToken.token == token_value).first()

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    if token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")

    return token.email
