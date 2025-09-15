# app/routes/auth_router.py
import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from passlib.context import CryptContext
import jwt

# Configuración de seguridad
SECRET_KEY = "supersecretkey"  # Cambiar en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# --- Schemas ---
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

# --- Usuario de prueba ---
fake_user_db = {
    "AnalistaRRHH": {
        "id": 1,
        "username": "AnalistaRRHH",
        "email": "ssusana@ssv.com.do",
        "hashed_password": pwd_context.hash("123456"),
        "role": "admin",
        "is_active": True,
    }
}

# --- Funciones de utilidad ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_minutes: Optional[int] = ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Endpoint de login ---
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_user_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    if not verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    if not user_dict["is_active"]:
        raise HTTPException(status_code=401, detail="Usuario inactivo")

    token = create_access_token(data={"sub": user_dict["username"]})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_dict["id"],
            "username": user_dict["username"],
            "email": user_dict["email"],
            "role": user_dict["role"],
        }
    }
