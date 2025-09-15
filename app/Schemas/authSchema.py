from xmlrpc.client import boolean
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Schema para crear un usuario
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    area: str
    is_active: bool
    email: EmailStr
    sap_last_sync: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

# Schema para login
class UserLogin(BaseModel):
    username: str
    password: str

# Schema para respuesta de usuario
class UserResponse(BaseModel):
    username: str = Field(..., title="username")

    class Config:
        orm_mode = True

# Roles de usuario (puedes usar Enum)
from enum import Enum

class UserRoleEnum(str, Enum):
    admin = "Administrador"
    delivery = "Encargado de entrega"
    audit = "Personal Auditoria"
    employee = "Empleado"
