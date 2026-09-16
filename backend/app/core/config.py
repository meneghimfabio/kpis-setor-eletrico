from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Painel do Setor Elétrico Brasileiro"
    API_V1_STR: str = "/api/v1"
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "kpisetoreletrico")
    
    # BigQuery Datasets
    DATASET_SIN: str = "operacao_sin"
    DATASET_CCEE: str = "mercado_ccee"
    DATASET_TRANSMISSAO: str = "transmissao"
    DATASET_DISTRIBUICAO: str = "distribuicao_qualidade"
    DATASET_PERDAS_MMGD: str = "perdas_mmgd"
    DATASET_ATENDIMENTO: str = "atendimento_cliente"
    DATASET_FINANCEIRO: str = "financeiro_ativos"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000",
        "*"
    ]
    
    # Cache TTL in seconds
    CACHE_TTL_SECONDS: int = 300
    
    class Config:
        case_sensitive = True

settings = Settings()
