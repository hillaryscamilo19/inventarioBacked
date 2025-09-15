from pydantic import BaseModel

class UniformeCreate(BaseModel):
    name: str
    Uniforme_id: str

class UniformeUpdate(BaseModel): 
    name: str
    Uniforme_id: str

    
class UniformeEntrega(BaseModel):
    Area_id: str
    Medicamento_id: str
    Cantidad: int
    Firma: str