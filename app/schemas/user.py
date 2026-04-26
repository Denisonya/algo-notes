from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    """
    Base schema for User.

    Contains shared fields used across user schemas.
    """
    username: str


class UserCreate(UserBase):
    """
    Schema for user registration.

    Extends UserBase with password field.
    """
    password: str


class UserLogin(UserBase):
    """
    Schema for user authentication.

    Used to log in and receive JWT token.
    """
    password: str


class UserRead(UserBase):
    """
    Schema for user authentication.

    Used to log in and receive JWT token.
    """
    id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """
    Schema for JWT token response.

    Returned after successful authentication.
    """
    access_token: str
    token_type: str = "bearer"
