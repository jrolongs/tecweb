import os

import httpx
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL", "vigipro.co@gmail.com")
BREVO_SENDER_NAME = os.getenv("BREVO_SENDER_NAME", "Tecweb")
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
HTTP_TIMEOUT = 15


async def send_email(to_email: str, body: str, subject: str = "Mensaje desde FastAPI") -> dict:
    if not BREVO_API_KEY:
        raise RuntimeError("BREVO_API_KEY no configurada")

    payload = {
        "sender": {"name": BREVO_SENDER_NAME, "email": BREVO_SENDER_EMAIL},
        "to": [{"email": to_email}],
        "subject": subject,
        "textContent": body,
    }
    headers = {
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
        "accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        response = await client.post(BREVO_API_URL, json=payload, headers=headers)

    if response.status_code >= 400:
        raise RuntimeError(f"Brevo respondió {response.status_code}: {response.text}")

    return {"status": "success", "message": f"Correo enviado a {to_email}"}


async def send_otp_email(to_email: str, code: str) -> dict:
    body = (
        f"Tu código de verificación es: {code}\n\n"
        "Este código expira en 5 minutos.\n"
        "Si no solicitaste este código, ignora este mensaje."
    )
    return await send_email(to_email, body, subject="Código de verificación")
