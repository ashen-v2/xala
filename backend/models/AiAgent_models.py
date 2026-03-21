from sqlmodel import SQLModel

class Prompt(SQLModel):
    data : str