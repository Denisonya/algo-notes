from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

from ..core.settings import settings

# Создаем объект для работы с хешированием паролей, используем алгоритм bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash user password.

    :param password: Plain password
    :return: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify password with stored hash.

    :param password: Plain password
    :param hashed: Hashed password from database
    :return: True if password is valid, else False
    """
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict) -> str:
    """
    Create JWT access token.

    :param data: Payload data
    :return: Encoded JWT token
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
