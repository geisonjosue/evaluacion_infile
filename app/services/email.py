import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAILS_FROM = os.getenv("EMAILS_FROM")
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")

def _send_email(to_email: str, subject: str, body: str, is_html: bool = True):
    msg = MIMEMultipart()
    msg["From"] = EMAILS_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html" if is_html else "plain"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(EMAILS_FROM, to_email, msg.as_string())

# Envio de confirmacion de cuenta
def send_confirmation_email(to_email: str, token: str):
    confirm_url = f"{FRONTEND_BASE_URL}/confirm/{token}"
    subject = "Confirma tu cuenta"
    body = f"""
    <h1>Bienvenido</h1>
    <p>Por favor confirma tu cuenta haciendo clic en el siguiente enlace:</p>
    <a href="{confirm_url}">{confirm_url}</a>
    """
    _send_email(to_email, subject, body)

# Envio de recuperacion de contraseña
def send_reset_password_email(to_email: str, token: str):
    reset_url = f"{FRONTEND_BASE_URL}/reset-password?token={token}"
    subject = "Recuperar contraseña"
    body = f"""
    <h1>Recuperar contraseña</h1>
    <p>Haz clic en el siguiente enlace para restablecer tu contraseña:</p>
    <a href="{reset_url}">{reset_url}</a>
    <p>Si no solicitaste este cambio, ignora este correo.</p>
    """
    _send_email(to_email, subject, body)
