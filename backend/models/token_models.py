from sqlmodel import SQLModel

class TokenBase(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    user_id: int
    is_verified: bool

class passwordReset(SQLModel):
    password_token: str
    password: str

class VerificationToken(SQLModel):
    email_token: str

