from email.message import EmailMessage
from config import SMTP_USER, SMTP_HOST, SMTP_PORT, SMTP_PASSWORD

from celery import Celery
import smtplib

celery = Celery(
    'tasks',
    broker='redis://5.23.49.44:6379',
    backend='redis://5.23.49.44:6379'
)


def create_mail(username, user_email) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = f'Тестовое письмо для {username}'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(f'Здравствуй, {username} ! Вы у нас самый дорогой пользователь нашего приложения\n'
                      f'Мы высылаем вам это тестовое письмо для проверки работы Celery.')

    return email


@celery.task(bind=True, max_retries=3)
def send_email_to_one_user(self, username: str, user_email: str) -> None:
    try:
        email = create_mail(username, user_email)
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(email)
    except Exception as e:
        raise self.retry(exc=e)

