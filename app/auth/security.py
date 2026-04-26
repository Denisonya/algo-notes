from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

from app.core.settings import settings

# Создаем объект для работы с хешированием паролей, используем алгоритм bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.

    :param password: Plain password
    :return: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify password.

    :param password: Plain password
    :param hashed: Hashed password
    :return: True if valid
    """
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict) -> str:
    """
    Create JWT token.

    :param data: Payload data
    :return: JWT token
    """
    # Копируем payload, чтобы не изменять исходный словарь
    payload = data.copy()

    # Время истечения токена
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_expire_minutes
    )

    # Добавляем в payload стандартное поле expiration time
    payload.update({"exp": expire})

    # Кодируем payload в JWT токен
    return jwt.encode(
        payload,
        settings.jwt_secret,  # секретный ключ подписи
        algorithm=settings.jwt_algorithm  # алгоритм шифрования
    )
