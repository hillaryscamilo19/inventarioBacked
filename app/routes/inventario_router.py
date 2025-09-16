from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.db import get_db
from app.models.inventory_model import (
    Producto, MovimientoInventario, Empleado,
    obtener_productos, obtener_productos_stock_bajo, 
    obtener_movimientos, obtener_empleados,
    producto_helper, movimiento_helper, empleado_helper
)
from app.Schemas.invetorySchema import (
    ProductoCreate, ProductoUpdate, ProductoResponse,
    MovimientoCreate, MovimientoResponse,
    EmpleadoCreate, EmpleadoUpdate, EmpleadoResponse,
    ConfirmarEntrega
)
from app.auth.dependencies import get_current_user
from app.models.auth_model import User
from typing import List, Optional

router = APIRouter()

# Rutas para Productos
@router.get("/productos", response_model=List[ProductoResponse])
async def get_productos(
    categoria: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    productos = await obtener_productos(db, categoria)
    return productos

@router.post("/productos", response_model=ProductoResponse)
async def create_producto(
    data: ProductoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_producto = Producto(**data.dict())
    db.add(new_producto)
    await db.commit()
    await db.refresh(new_producto)
    return producto_helper(new_producto)

@router.put("/productos/{producto_id}", response_model=ProductoResponse)
async def update_producto(
    producto_id: int,
    data: ProductoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Producto).filter(Producto.id == producto_id))
    producto = result.scalar_one_or_none()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(producto, field, value)
    
    await db.commit()
    await db.refresh(producto)
    return producto_helper(producto)

@router.get("/productos/stock-bajo", response_model=List[ProductoResponse])
async def get_productos_stock_bajo(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    productos = await obtener_productos_stock_bajo(db)
    return productos

# Rutas para Movimientos
@router.get("/movimientos", response_model=List[MovimientoResponse])
async def get_movimientos(
    producto_id: Optional[int] = None,
    empleado_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    movimientos = await obtener_movimientos(db, producto_id, empleado_id)
    return movimientos

@router.post("/movimientos", response_model=MovimientoResponse)
async def create_movimiento(
    data: MovimientoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificar que el producto existe
    result = await db.execute(select(Producto).filter(Producto.id == data.producto_id))
    producto = result.scalar_one_or_none()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Crear movimiento
    new_movimiento = MovimientoInventario(
        **data.dict(),
        usuario_registro=current_user.username
    )
    db.add(new_movimiento)
    
    # Actualizar stock según tipo de movimiento
    if data.tipo_movimiento == "entrada":
        producto.stock_actual += data.cantidad
    elif data.tipo_movimiento == "salida":
        if producto.stock_actual < data.cantidad:
            raise HTTPException(status_code=400, detail="Stock insuficiente")
        producto.stock_actual -= data.cantidad
    elif data.tipo_movimiento == "ajuste":
        producto.stock_actual = data.cantidad
    
    await db.commit()
    await db.refresh(new_movimiento)
    return movimiento_helper(new_movimiento)

@router.post("/movimientos/confirmar")
async def confirmar_entrega(
    data: ConfirmarEntrega,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(MovimientoInventario).filter(MovimientoInventario.id == data.movimiento_id))
    movimiento = result.scalar_one_or_none()
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    
    movimiento.confirmado = True
    movimiento.firma_digital = data.firma_digital
    
    await db.commit()
    return {"message": "Entrega confirmada exitosamente"}

# Rutas para Empleados
@router.get("/empleados", response_model=List[EmpleadoResponse])
async def get_empleados(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    empleados = await obtener_empleados(db)
    return empleados

@router.post("/empleados", response_model=EmpleadoResponse)
async def create_empleado(
    data: EmpleadoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_empleado = Empleado(**data.dict())
    db.add(new_empleado)
    await db.commit()
    await db.refresh(new_empleado)
    return empleado_helper(new_empleado)

@router.put("/empleados/{empleado_id}", response_model=EmpleadoResponse)
async def update_empleado(
    empleado_id: int,
    data: EmpleadoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Empleado).filter(Empleado.id == empleado_id))
    empleado = result.scalar_one_or_none()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(empleado, field, value)
    
    await db.commit()
    await db.refresh(empleado)
    return empleado_helper(empleado)
