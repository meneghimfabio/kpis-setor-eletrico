import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from app.core.config import settings
from app.api.routes_executive import router as executive_router
from app.api.routes_sin import router as sin_router
from app.api.routes_ccee import router as ccee_router
from app.api.routes_transmissao import router as transmissao_router
from app.api.routes_distribuicao import router as distribuicao_router
from app.api.routes_perdas_mmgd import router as perdas_mmgd_router
from app.api.routes_atendimento import router as atendimento_router
from app.api.routes_financeiro_proret import router as financeiro_proret_router
from app.api.routes_alerts import router as alerts_router
from app.api.routes_ingestion import router as ingestion_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API do Painel do Setor Elétrico Brasileiro com suporte a BigQuery (kpisetoreletrico)",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(executive_router, prefix=settings.API_V1_STR)
app.include_router(sin_router, prefix=settings.API_V1_STR)
app.include_router(ccee_router, prefix=settings.API_V1_STR)
app.include_router(transmissao_router, prefix=settings.API_V1_STR)
app.include_router(distribuicao_router, prefix=settings.API_V1_STR)
app.include_router(perdas_mmgd_router, prefix=settings.API_V1_STR)
app.include_router(atendimento_router, prefix=settings.API_V1_STR)
app.include_router(financeiro_proret_router, prefix=settings.API_V1_STR)
app.include_router(alerts_router, prefix=settings.API_V1_STR)
app.include_router(ingestion_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "gcp_project": settings.GCP_PROJECT_ID
    }

# Check for static frontend distribution
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
if not os.path.exists(STATIC_DIR):
    STATIC_DIR = "/app/static"

if os.path.exists(STATIC_DIR):
    assets_dir = os.path.join(STATIC_DIR, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Don't intercept API or health endpoints
        if full_path.startswith("api") or full_path.startswith("health") or full_path.startswith("docs") or full_path.startswith("openapi"):
            return None
        file_path = os.path.join(STATIC_DIR, full_path)
        if full_path and os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        index_file = os.path.join(STATIC_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "Painel do Setor Elétrico Brasileiro API"}
else:
    @app.get("/")
    def root():
        return {
            "message": "API do Painel do Setor Elétrico Brasileiro",
            "docs": f"{settings.API_V1_STR}/docs",
            "gcp_project": settings.GCP_PROJECT_ID
        }
