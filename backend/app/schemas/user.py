from pydantic import BaseModel


class UserCreate(BaseModel):

    name: str
    email: str
    password: str


class UserResponse(BaseModel):

    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):

    email: str

    password: str


class Token(BaseModel):

    access_token: str

    token_type: str


class TokenResponse(BaseModel):

    access_token: str

    refresh_token: str

    token_type: str


class RefreshTokenRequest(BaseModel):

    refresh_token: str
