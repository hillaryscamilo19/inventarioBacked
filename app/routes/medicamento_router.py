from app.Schemas.medicamentScherma import MedicamentoCreate
from app.models.auth_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.medicament_model import obtener_medicamento


router = APIRouter()


#Ruta para obtener todos los medicamentos
@router.get("/")
async def get_medicamento(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    medicamento = await obtener_medicamento(db)
    return medicamento

#Rutas Para Crear un Medicamento

@router.post("")
async def create_medicamento(data: MedicamentoCreate, db: AsyncSession = Depends(get_db), )