from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.Schemas.authSchema import UserCreate
from app.auth.dependencies import get_current_user
from app.db.db import get_db
from app.models.auth_model import User
from app.models.usuario_model import obtener_usuarios, update_fields, usuario_helper

router = APIRouter()


@router.get("/")
async def get_usuarios(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await obtener_usuarios(db)

#Rutas Para obtener usuario
@router.get("/{user_id}")
async def get_user_by_id( user_id: int,current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User)
        .filter(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return usuario_helper(user)
# Ruta para crear un usuario
@router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Verificar si el usuario ya existe
    result = await db.execute(select(User).filter(User.email == user.email))
    user_db = result.scalar_one_or_none()
    if user_db:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Crear el usuario
    user_db = User(**user.dict())
    db.add(user_db)
    await db.commit()
    await db.refresh(user_db)
    return usuario_helper(user_db)


# Ruta para actualizar un usuario
@router.put("/{user_id}")
async def update_user( user_id: int, updated_data: dict, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role not in (0, 1, 2):
        raise HTTPException(status_code=403, detail="No tienes permisos suficientes")

    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar usuario con datos permitidos
    updated_user = await update_fields(user, updated_data, db)

    # Recargar usuario con relaciones para evitar error de lazy load en async
    result = await db.execute(
        select(User)
        .options(selectinload(User.department), selectinload(User.supervision_departments))
        .filter(User.id == updated_user.id)
    )
    user_with_relations = result.scalar_one_or_none()

    return usuario_helper(user_with_relations)


# Ruta para eliminar un usuario
@router.delete("/{user_id}")
async def delete_user( user_id: int,current_user=Depends(get_current_user),
db: AsyncSession = Depends(get_db),):
    if current_user.role not in (0, 1):
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar usuarios")

    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    await db.delete(user)
    await db.commit()
    return {"message": "Usuario eliminado exitosamente"}
