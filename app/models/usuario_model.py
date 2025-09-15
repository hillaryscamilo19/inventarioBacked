import datetime
from fastapi import HTTPException
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload
from app.db.base import Base

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"extend_existing": True}  # ⚠️ Agregar esto
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(Integer)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    status = Column(Boolean)
    created_at = Column("createdat", DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column("updatedat", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)



def usuario_helper(usuario) -> dict:
    return {
        "id": usuario.id,
        "fullname": usuario.fullname,
        "email": usuario.email,
        "role": usuario.role,
        "username": usuario.username,
        "status": usuario.status,
        "createdAt": usuario.created_at,
        "updatedAt": usuario.updated_at
    }

async def obtener_usuarios(db: AsyncSession):
    result = await db.execute(
        select(User)
        .options(selectinload(User.fullname), selectinload(User.id))
    )
    usuarios = result.scalars().all()
    return [usuario_helper(u) for u in usuarios]

async def update_fields(user: User, updated_data: dict, db: AsyncSession):
    allowed_fields = {
        "status", "fullname", "email", "role", "username"
    }

    disallowed_fields = {"created_at", "createdat", "createdAt", "id"}  # Puedes agregar más si es necesario

    # Validar que no se esté intentando modificar campos no permitidos
    for key in updated_data:
        if key in disallowed_fields:
            raise HTTPException(status_code=400, detail=f"No puedes modificar el campo '{key}'")

    # Aplicar los cambios permitidos
    for key, value in updated_data.items():
        if key in allowed_fields:
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user
