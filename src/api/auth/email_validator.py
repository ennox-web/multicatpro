from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr

from api.auth.config import (
    MAIL_USERNAME,
    MAIL_PASSWORD,
    MAIL_FROM,
    MAIL_PORT,
    MAIL_SERVER,
    TEST_EMAIL
)


class EmailSchema(BaseModel):
    email: EmailStr


email_conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email():
    message = MessageSchema(
        subject="Fastapi-Mail Test",
        recipients=[TEST_EMAIL],
        body="<p>Testing from MultiCatPro!</p>",
        subtype=MessageType.html,
    )
    fm = FastMail(email_conf)
    await fm.send_message(message=message)
    print("Email Sent!")
