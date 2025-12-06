from pydantic import BaseModel


class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    email: str


class ClienteCreate(ClienteBase):
    pass


class Cliente(ClienteBase):
    id: int

    class Config:
        orm_mode = True
