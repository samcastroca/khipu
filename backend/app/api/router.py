from fastapi import APIRouter
from app.api.endpoints import spam, phishing, suspicious, suspicious_logs
# from app.api.endpoints import agent  # Comentado temporalmente - requiere langchain

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(spam.router)
api_router.include_router(phishing.router)
api_router.include_router(suspicious.router)
api_router.include_router(suspicious_logs.router)
# api_router.include_router(agent.router)  # Comentado temporalmente
