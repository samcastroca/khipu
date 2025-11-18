from pydantic import BaseModel, Field
from typing import Optional


class SpamClassificationRequest(BaseModel):
    """Request schema for spam classification"""
    email_text: str = Field(..., description="Texto del correo electrónico a analizar", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email_text": "Congratulations! You've won $1,000,000. Click here to claim your prize!"
            }
        }


class PhishingURLRequest(BaseModel):
    """Request schema for phishing URL detection"""
    url: str = Field(..., description="URL a analizar", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "http://suspicious-website.com/login"
            }
        }


class SuspiciousAccessRequest(BaseModel):
    """Request schema for suspicious access detection"""
    user_id: Optional[str] = Field(None, description="ID del usuario")
    ip_address: str = Field(..., description="Dirección IP del acceso")
    timestamp: Optional[str] = Field(None, description="Timestamp del acceso")
    action: str = Field(..., description="Acción realizada")
    location: Optional[str] = Field(None, description="Ubicación del acceso")
    device: Optional[str] = Field(None, description="Dispositivo usado")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "ip_address": "192.168.1.1",
                "timestamp": "2025-01-15T14:30:00",
                "action": "login_attempt",
                "location": "Unknown",
                "device": "Unknown Device"
            }
        }


class AgentAnalysisRequest(BaseModel):
    """Request schema for AI agent analysis"""
    query: str = Field(..., description="Consulta en lenguaje natural", min_length=1)
    context: Optional[dict] = Field(None, description="Contexto adicional para el análisis")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "¿Este correo es spam? 'Get rich quick! Click here now!'",
                "context": {}
            }
        }
