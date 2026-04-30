import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


async def send_email(to_email: str, body: str, subject: str = "Mensaje desde FastAPI") -> dict:
    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)

    return {"status": "success", "message": f"Correo enviado a {to_email}"}


async def send_otp_email(to_email: str, code: str) -> dict:
    body = (
        f"Tu código de verificación es: {code}\n\n"
        "Este código expira en 5 minutos.\n"
        "Si no solicitaste este código, ignora este mensaje."
    )
    return await send_email(to_email, body, subject="Código de verificación")