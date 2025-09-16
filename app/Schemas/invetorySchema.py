from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria: str  # 'uniforme' o 'medicamento'
    stock_actual: int = 0
    stock_minimo: int = 10
    precio_unitario: Optional[float] = None

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    stock_minimo: Optional[int] = None
    precio_unitario: Optional[float] = None
    activo: Optional[bool] = None

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    categoria: str
    stock_actual: int
    stock_minimo: int
    precio_unitario: Optional[float]
    activo: bool
    fecha_creacion: Optional[str]

class MovimientoCreate(BaseModel):
    producto_id: int
    empleado_id: int
    tipo_movimiento: str  # 'entrada', 'salida', 'ajuste', 'devolucion'
    cantidad: int
    motivo: Optional[str] = None
    firma_digital: Optional[str] = None

class MovimientoResponse(BaseModel):
    id: int
    producto_id: int
    empleado_id: int
    tipo_movimiento: str
    cantidad: int
    motivo: Optional[str]
    fecha_movimiento: Optional[str]
    usuario_registro: str
    confirmado: bool
    firma_digital: Optional[str]

class EmpleadoCreate(BaseModel):
    spn: str
    nombre: str
    apellido: str
    area: str
    cargo: Optional[str] = None
    fecha_ingreso: Optional[datetime] = None

class EmpleadoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    area: Optional[str] = None
    cargo: Optional[str] = None
    activo: Optional[bool] = None

class EmpleadoResponse(BaseModel):
    id: int
    spn: str
    nombre: str
    apellido: str
    area: str
    cargo: Optional[str]
    activo: bool
    fecha_ingreso: Optional[str]

class ConfirmarEntrega(BaseModel):
    movimiento_id: int
    firma_digital: str
