from sqlalchemy.orm import relationship, selectinload
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import Base
from datetime import datetime

class Producto(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    categoria = Column(String, nullable=False)  # 'uniforme' o 'medicamento'
    stock_actual = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=10)
    precio_unitario = Column(Float)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    movimientos = relationship("MovimientoInventario", back_populates="producto")

class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"
    
    id = Column(Integer, primary_key=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    empleado_id = Column(Integer, ForeignKey("empleados.id"))
    tipo_movimiento = Column(String, nullable=False)  # 'entrada', 'salida', 'ajuste', 'devolucion'
    cantidad = Column(Integer, nullable=False)
    motivo = Column(String)
    fecha_movimiento = Column(DateTime, default=datetime.utcnow)
    usuario_registro = Column(String, nullable=False)
    confirmado = Column(Boolean, default=False)
    firma_digital = Column(String)
    
    # Relaciones
    producto = relationship("Producto", back_populates="movimientos")
    empleado = relationship("Empleado", back_populates="movimientos")

class Empleado(Base):
    __tablename__ = "empleados"
    
    id = Column(Integer, primary_key=True)
    spn = Column(String, unique=True, nullable=False)  # Para integración SAP
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    area = Column(String, nullable=False)
    cargo = Column(String)
    activo = Column(Boolean, default=True)
    fecha_ingreso = Column(DateTime)
    
    # Relaciones
    movimientos = relationship("MovimientoInventario", back_populates="empleado")

# Helper functions
def producto_helper(producto) -> dict:
    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "categoria": producto.categoria,
        "stock_actual": producto.stock_actual,
        "stock_minimo": producto.stock_minimo,
        "precio_unitario": producto.precio_unitario,
        "activo": producto.activo,
        "fecha_creacion": producto.fecha_creacion.isoformat() if producto.fecha_creacion else None
    }

def movimiento_helper(movimiento) -> dict:
    return {
        "id": movimiento.id,
        "producto_id": movimiento.producto_id,
        "empleado_id": movimiento.empleado_id,
        "tipo_movimiento": movimiento.tipo_movimiento,
        "cantidad": movimiento.cantidad,
        "motivo": movimiento.motivo,
        "fecha_movimiento": movimiento.fecha_movimiento.isoformat() if movimiento.fecha_movimiento else None,
        "usuario_registro": movimiento.usuario_registro,
        "confirmado": movimiento.confirmado,
        "firma_digital": movimiento.firma_digital
    }

def empleado_helper(empleado) -> dict:
    return {
        "id": empleado.id,
        "spn": empleado.spn,
        "nombre": empleado.nombre,
        "apellido": empleado.apellido,
        "area": empleado.area,
        "cargo": empleado.cargo,
        "activo": empleado.activo,
        "fecha_ingreso": empleado.fecha_ingreso.isoformat() if empleado.fecha_ingreso else None
    }

# Query functions
async def obtener_productos(db: AsyncSession, categoria: str = None):
    query = select(Producto).where(Producto.activo == True)
    if categoria:
        query = query.where(Producto.categoria == categoria)
    
    result = await db.execute(query)
    productos = result.scalars().all()
    return [producto_helper(p) for p in productos]

async def obtener_productos_stock_bajo(db: AsyncSession):
    result = await db.execute(
        select(Producto).where(
            Producto.stock_actual <= Producto.stock_minimo,
            Producto.activo == True
        )
    )
    productos = result.scalars().all()
    return [producto_helper(p) for p in productos]

async def obtener_movimientos(db: AsyncSession, producto_id: int = None, empleado_id: int = None):
    query = select(MovimientoInventario).options(
        selectinload(MovimientoInventario.producto),
        selectinload(MovimientoInventario.empleado)
    )
    
    if producto_id:
        query = query.where(MovimientoInventario.producto_id == producto_id)
    if empleado_id:
        query = query.where(MovimientoInventario.empleado_id == empleado_id)
    
    result = await db.execute(query)
    movimientos = result.scalars().all()
    return [movimiento_helper(m) for m in movimientos]

async def obtener_empleados(db: AsyncSession):
    result = await db.execute(
        select(Empleado).where(Empleado.activo == True)
    )
    empleados = result.scalars().all()
    return [empleado_helper(e) for e in empleados]
