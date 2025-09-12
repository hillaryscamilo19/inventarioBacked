from pydantic import BaseModel, Field
from django.contrib.auth.models import AbstractUser

class User(BaseModel):
    firt_name: str
    last_name: str
    area:str
    position: str
    employee_id: str
    phone: str
    is_active:str
    email: str
    sap_last_sync: str

class Config:
    arbitrary_type_allwed = True
    orm_mode: True

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str = Field(..., title="username")
    class config: 
        orm_mode: True

class UserRole(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('delivery', 'Encargado de entrega'),
        ('audit','Personal Auditoria'),
        ('Employee','Empleado')
    ]