from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    Schema for user registration.

    Used to create a new user account.
    """
    username: str
    password: str


class UserLogin(BaseModel):
    """
    Schema for user authentication.

    Used to log in and receive JWT token.
    """
    username: str
    password: str


class Token(BaseModel):
    """
    Schema for JWT token response.

    Returned after successful authentication.
    """
    access_token: str
    token_type: str = "bearer"