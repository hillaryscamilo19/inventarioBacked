from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import Base
from datetime import datetime, date
from typing import Optional

from app.models.inventory_model import movimiento_helper

class ReporteGenerado(Base):
    __tablename__ = "reportes_generados"
    
    id = Column(Integer, primary_key=True)
    tipo_reporte = Column(String, nullable=False)  # 'inventario', 'movimientos', 'entregas', 'auditoria'
    parametros = Column(Text)  # JSON con parámetros del reporte
    archivo_path = Column(String)
    generado_por = Column(String, nullable=False)
    fecha_generacion = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="completado")  # 'procesando', 'completado', 'error'

class AlertaStock(Base):
    __tablename__ = "alertas_stock"
    
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, nullable=False)
    tipo_alerta = Column(String, nullable=False)  # 'stock_bajo', 'stock_agotado'
    mensaje = Column(String, nullable=False)
    fecha_alerta = Column(DateTime, default=datetime.utcnow)
    leida = Column(Boolean, default=False)
    usuario_notificado = Column(String)

# Helper functions
def reporte_helper(reporte) -> dict:
    return {
        "id": reporte.id,
        "tipo_reporte": reporte.tipo_reporte,
        "parametros": reporte.parametros,
        "archivo_path": reporte.archivo_path,
        "generado_por": reporte.generado_por,
        "fecha_generacion": reporte.fecha_generacion.isoformat() if reporte.fecha_generacion else None,
        "estado": reporte.estado
    }

def alerta_helper(alerta) -> dict:
    return {
        "id": alerta.id,
        "producto_id": alerta.producto_id,
        "tipo_alerta": alerta.tipo_alerta,
        "mensaje": alerta.mensaje,
        "fecha_alerta": alerta.fecha_alerta.isoformat() if alerta.fecha_alerta else None,
        "leida": alerta.leida,
        "usuario_notificado": alerta.usuario_notificado
    }

# Query functions para reportes
async def obtener_reportes(db: AsyncSession, usuario: str = None):
    query = select(ReporteGenerado)
    if usuario:
        query = query.where(ReporteGenerado.generado_por == usuario)
    
    result = await db.execute(query.order_by(ReporteGenerado.fecha_generacion.desc()))
    reportes = result.scalars().all()
    return [reporte_helper(r) for r in reportes]

async def obtener_alertas_activas(db: AsyncSession):
    result = await db.execute(
        select(AlertaStock).where(AlertaStock.leida == False)
        .order_by(AlertaStock.fecha_alerta.desc())
    )
    alertas = result.scalars().all()
    return [alerta_helper(a) for a in alertas]

# Funciones para generar estadísticas
async def obtener_estadisticas_inventario(db: AsyncSession):
    from app.models.inventory_model import Producto, MovimientoInventario
    
    # Total productos
    total_productos = await db.execute(select(func.count(Producto.id)).where(Producto.activo == True))
    total_productos = total_productos.scalar()
    # Productos con stock bajo
    stock_bajo = await db.execute(
        select(func.count(Producto.id)).where(
            Producto.stock_actual <= Producto.stock_minimo,
            Producto.activo == True
        )
    )
    stock_bajo = stock_bajo.scalar()
    # Movimientos del mes actual
    inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    movimientos_mes = await db.execute(
        select(func.count(MovimientoInventario.id)).where(
            MovimientoInventario.fecha_movimiento >= inicio_mes
        )
    )
    movimientos_mes = movimientos_mes.scalar()
    return {
        "total_productos": total_productos,
        "productos_stock_bajo": stock_bajo,
        "movimientos_mes_actual": movimientos_mes,
        "fecha_actualizacion": datetime.now().isoformat()
    }

async def obtener_movimientos_por_periodo(db: AsyncSession, fecha_inicio: date, fecha_fin: date):
    from app.models.inventory_model import MovimientoInventario, Producto, Empleado
    
    result = await db.execute(
        select(MovimientoInventario, Producto.nombre, Empleado.nombre, Empleado.apellido)
        .join(Producto, MovimientoInventario.producto_id == Producto.id)
        .join(Empleado, MovimientoInventario.empleado_id == Empleado.id)
        .where(
            MovimientoInventario.fecha_movimiento >= fecha_inicio,
            MovimientoInventario.fecha_movimiento <= fecha_fin
        )
        .order_by(MovimientoInventario.fecha_movimiento.desc())
    )
    
    movimientos = []
    for row in result:
        movimiento, producto_nombre, empleado_nombre, empleado_apellido = row
        movimientos.append({
            **movimiento_helper(movimiento),
            "producto_nombre": producto_nombre,
            "empleado_nombre": f"{empleado_nombre} {empleado_apellido}"
        })
    
    return movimientos
