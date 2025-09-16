import select
from fastapi import APIRouter, Depends, HTTPException
from app import db
from app.Schemas.medicamentScherma import MedicamentoCreate, MedicamentoUpdate
from app.Schemas.uniformeSchema import UniformeCreate, UniformeUpdate
from app.auth.dependencies import get_current_user
from app.db.db import get_db
from app.models.auth_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.medicament_model import Medicamento, medicamento_helper, obtener_medicamento
from app.models.uniformeModel import Uniforme, obtener_uniforme


router = APIRouter()
#Ruta para obtener todos los medicamentos
@router.get("/")
async def get_uniforme(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    uniforme = await obtener_uniforme(db)
    return uniforme

#Rutas Para Crear un Medicamento

@router.post("")
async def create_uniforme(data: UniformeCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_Uniforme = Uniforme(name=data.name)
    db.add(new_Uniforme)
    await db.commit()
    await db.refresh(new_Uniforme)
    return medicamento_helper(new_Uniforme)

@router.put("/{uniforme_id}")
async def update_uniforme(Uniforme_id: int , data:  UniformeUpdate , db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Uniforme).filter(Uniforme.id == Uniforme_id))
    uniforme = result.scalar_one_or_none()
    if not uniforme:
        raise HTTPException(status_code= 404, detail= "Uniforme No Encontrado")
    
#Ruta Para eliminar Un Id
@router.delete("/{uniforme_id}")
async def delete_uniforme(uniforme_id: int , db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Medicamento).filter(Medicamento.id == uniforme_id))
    uniforme = result.scalar_one_or_none()
    if not uniforme:
        raise HTTPException(status_code= 404 , detail= "Uniforme No encontrado")
    
    await db.delete(uniforme)
    await db.commit()
    return{"message": "Uniforme Borrado Con Existo"}
