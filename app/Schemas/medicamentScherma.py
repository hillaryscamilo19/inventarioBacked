from pydantic import BaseModel

class MedicamentoCreate(BaseModel):
   name: str
   Medicamento_id: str

class MedicamentoUpdate(BaseModel):
    name: str
    Medicamento_id: str


class MedicantoEntrega(BaseModel):
    employee_id: str
    Area_id: str
    Medicamento_id: str
    Cantidad: int
    Firma: str