from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Importamos routers de las diferentes rutas de la aplicación 
from app.routes.usuario_router import router as usuario_router
from app.routes.uniforme_router import router as uniforme_router
from app.routes.medicamento_router import router as medicamento_router
from app.routes.inventario_router import router as inventario_router
from app.routes.reporte_router import router as reporte_router
from app.routes.auth_router import router as auth_router
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Configuramos la plantilla de Jinja2 para servir HTML desde la carpeta 'templates'
templates = Jinja2Templates(directory="templates")
# Creamos la instancia principal de la aplicación FastAPI
app = FastAPI ()
# Incluimos los routers para cada módulo, asignándoles un prefijo y tags para documentación
app.include_router(auth_router, prefix="", tags=["Login"])
app.include_router(medicamento_router, prefix="/medicamento", tags=["Medicamento"])
app.include_router(uniforme_router, prefix="/uniforme", tags=["Uniforme"])
app.include_router(usuario_router, prefix="/usuarios", tags=["Usuario"])
app.include_router(auth_router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(uniforme_router, prefix="/api/uniformes", tags=["Uniformes"])
app.include_router(inventario_router, prefix="/api/inventario", tags=["Inventario"])
app.include_router(reporte_router, prefix="/api/reportes", tags=["Reportes"])

# Configuración CORS para permitir peticiones desde los orígenes listados
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3000",  
    "https://localhost:3000",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:4200",
    "http://10.0.0.15:4200",
    "https://localhost:3000",
]

# Añadimos middleware de CORS para gestionar acceso desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"], # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"], # Permitir todos los headers
)