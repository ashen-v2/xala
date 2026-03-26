from sqlmodel import Field, SQLModel

class Prompt(SQLModel):
    data: str = Field(min_length=1, max_length=700)