from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List, Dict, Any

class ReporteCreate(BaseModel):
    tipo_reporte: str  # 'inventario', 'movimientos', 'entregas', 'auditoria'
    parametros: Optional[Dict[str, Any]] = None

class ReporteResponse(BaseModel):
    id: int
    tipo_reporte: str
    parametros: Optional[str]
    archivo_path: Optional[str]
    generado_por: str
    fecha_generacion: Optional[str]
    estado: str

class AlertaResponse(BaseModel):
    id: int
    producto_id: int
    tipo_alerta: str
    mensaje: str
    fecha_alerta: Optional[str]
    leida: bool
    usuario_notificado: Optional[str]

class EstadisticasInventario(BaseModel):
    total_productos: int
    productos_stock_bajo: int
    movimientos_mes_actual: int
    fecha_actualizacion: str

class FiltroMovimientos(BaseModel):
    fecha_inicio: date
    fecha_fin: date
    producto_id: Optional[int] = None
    empleado_id: Optional[int] = None
    tipo_movimiento: Optional[str] = None

class MovimientoReporte(BaseModel):
    id: int
    producto_id: int
    producto_nombre: str
    empleado_id: int
    empleado_nombre: str
    tipo_movimiento: str
    cantidad: int
    motivo: Optional[str]
    fecha_movimiento: Optional[str]
    confirmado: bool

class MarcarAlertaLeida(BaseModel):
    alerta_id: int
