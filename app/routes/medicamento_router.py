import select
from fastapi import APIRouter, Depends, HTTPException
from app import db
from app.Schemas.medicamentScherma import MedicamentoCreate, MedicamentoUpdate
from app.auth.dependencies import get_current_user
from app.db.db import get_db
from app.models.auth_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.medicament_model import Medicamento, medicamento_helper, obtener_medicamento


router = APIRouter()
#Ruta para obtener todos los medicamentos
@router.get("/")
async def get_medicamento(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    medicamento = await obtener_medicamento(db)
    return medicamento

#Rutas Para Crear un Medicamento

@router.post("")
async def create_medicamento(data: MedicamentoCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_Medicamento = Medicamento(name=data.name)
    db.add(new_Medicamento)
    await db.commit()
    await db.refresh(new_Medicamento)
    return medicamento_helper(new_Medicamento)

@router.put("/{medicamento_id}")
async def update_medicamento(medicamento_id: int , data:  MedicamentoUpdate , db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Medicamento).filter(Medicamento.id == medicamento_id))
    medicamento = result.scalar_one_or_none()
    if not medicamento:
        raise HTTPException(status_code= 404, detail= "Medicamento No Encontrado")
    
#Ruta Para eliminar Un Id
@router.delete("/{medicamento_id}")
async def delete_medicamento(medicamento_id: int , db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Medicamento).filter(Medicamento.id == medicamento_id))
    medicamento = result.scalar_one_or_none()
    if not medicamento:
        raise HTTPException(status_code= 404 , detail= "Medicamento No encontrado")
    
    await db.delete(medicamento)
    await db.commit()
    return{"message": "Medicamento Borrado Con Existo"}