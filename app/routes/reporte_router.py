from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.db import get_db
from app.models.reporte_model import (
    ReporteGenerado, AlertaStock, obtener_reportes, obtener_alertas_activas,
    obtener_estadisticas_inventario, obtener_movimientos_por_periodo,
    reporte_helper, alerta_helper
)
from app.Schemas.reporteSchema import (
    ReporteCreate, ReporteResponse, AlertaResponse,
    EstadisticasInventario, FiltroMovimientos, MovimientoReporte,
    MarcarAlertaLeida
)
from app.auth.dependencies import get_current_user
from app.models.auth_model import User
from typing import List
import json
import pandas as pd
import os
from datetime import datetime

router = APIRouter()

# Función para generar reportes en Excel
async def generar_reporte_excel(tipo_reporte: str, datos: List[dict], parametros: dict):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reporte_{tipo_reporte}_{timestamp}.xlsx"
    filepath = f"reports/{filename}"
    
    # Crear directorio si no existe
    os.makedirs("reports", exist_ok=True)
    
    # Crear DataFrame y guardar en Excel
    df = pd.DataFrame(datos)
    df.to_excel(filepath, index=False, sheet_name=tipo_reporte.title())
    
    return filepath

@router.get("/estadisticas", response_model=EstadisticasInventario)
async def get_estadisticas_inventario(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    estadisticas = await obtener_estadisticas_inventario(db)
    return estadisticas

@router.get("/alertas", response_model=List[AlertaResponse])
async def get_alertas_activas(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    alertas = await obtener_alertas_activas(db)
    return alertas

@router.post("/alertas/marcar-leida")
async def marcar_alerta_leida(
    data: MarcarAlertaLeida,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(AlertaStock).filter(AlertaStock.id == data.alerta_id))
    alerta = result.scalar_one_or_none()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    
    alerta.leida = True
    alerta.usuario_notificado = current_user.username
    await db.commit()
    
    return {"message": "Alerta marcada como leída"}

@router.post("/generar", response_model=ReporteResponse)
async def generar_reporte(
    data: ReporteCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Crear registro del reporte
    nuevo_reporte = ReporteGenerado(
        tipo_reporte=data.tipo_reporte,
        parametros=json.dumps(data.parametros) if data.parametros else None,
        generado_por=current_user.username,
        estado="procesando"
    )
    
    db.add(nuevo_reporte)
    await db.commit()
    await db.refresh(nuevo_reporte)
    
    # Generar reporte en background
    background_tasks.add_task(
        procesar_reporte, 
        nuevo_reporte.id, 
        data.tipo_reporte, 
        data.parametros or {}
    )
    
    return reporte_helper(nuevo_reporte)

async def procesar_reporte(reporte_id: int, tipo_reporte: str, parametros: dict):
    # Esta función se ejecuta en background
    # Aquí iría la lógica para generar el reporte específico
    pass

@router.get("/movimientos", response_model=List[MovimientoReporte])
async def get_reporte_movimientos(
    filtros: FiltroMovimientos = Depends(),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    movimientos = await obtener_movimientos_por_periodo(
        db, filtros.fecha_inicio, filtros.fecha_fin
    )
    return movimientos

@router.get("/", response_model=List[ReporteResponse])
async def get_reportes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reportes = await obtener_reportes(db, current_user.username)
    return reportes

@router.get("/descargar/{reporte_id}")
async def descargar_reporte(
    reporte_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(ReporteGenerado).filter(ReporteGenerado.id == reporte_id))
    reporte = result.scalar_one_or_none()
    if not reporte:
        raise HTTPException(status_code=404, detail="Reporte no encontrado")
    
    if not reporte.archivo_path or not os.path.exists(reporte.archivo_path):
        raise HTTPException(status_code=404, detail="Archivo de reporte no encontrado")
    
    return FileResponse(
        path=reporte.archivo_path,
        filename=f"reporte_{reporte.tipo_reporte}_{reporte.id}.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
