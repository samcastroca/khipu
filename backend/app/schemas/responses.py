from pydantic import BaseModel, Field
from typing import Optional, Any, Dict


class PredictionResponse(BaseModel):
    """Base response schema for predictions"""
    success: bool = Field(..., description="Si la predicción fue exitosa")
    prediction: str = Field(..., description="Resultado de la predicción")
    confidence: Optional[float] = Field(None, description="Confianza de la predicción (0-1)")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalles adicionales")


class SpamClassificationResponse(PredictionResponse):
    """Response schema for spam classification"""
    is_spam: bool = Field(..., description="Si el correo es spam")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "prediction": "spam",
                "confidence": 0.95,
                "is_spam": True,
                "details": {
                    "risk_level": "high",
                    "detected_patterns": ["suspicious_links", "urgency_language"]
                }
            }
        }


class PhishingURLResponse(PredictionResponse):
    """Response schema for phishing URL detection"""
    is_phishing: bool = Field(..., description="Si la URL es phishing")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "prediction": "phishing",
                "confidence": 0.87,
                "is_phishing": True,
                "details": {
                    "risk_level": "high",
                    "suspicious_features": ["domain_age", "ssl_certificate"]
                }
            }
        }


class SuspiciousAccessResponse(PredictionResponse):
    """Response schema for suspicious access detection"""
    is_suspicious: bool = Field(..., description="Si el acceso es sospechoso")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "prediction": "suspicious",
                "confidence": 0.78,
                "is_suspicious": True,
                "details": {
                    "risk_level": "medium",
                    "anomaly_factors": ["unusual_location", "unusual_time"]
                }
            }
        }


class AgentAnalysisResponse(BaseModel):
    """Response schema for AI agent analysis"""
    success: bool = Field(..., description="Si el análisis fue exitoso")
    response: str = Field(..., description="Respuesta del agente")
    tools_used: list[str] = Field(default_factory=list, description="Herramientas utilizadas")
    results: Optional[Dict[str, Any]] = Field(None, description="Resultados de las herramientas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "response": "El correo analizado tiene una probabilidad del 95% de ser spam.",
                "tools_used": ["spam_classifier"],
                "results": {
                    "spam_classification": {
                        "is_spam": True,
                        "confidence": 0.95
                    }
                }
            }
        }


class ErrorResponse(BaseModel):
    """Response schema for errors"""
    success: bool = Field(False, description="Siempre False en errores")
    error: str = Field(..., description="Mensaje de error")
    detail: Optional[str] = Field(None, description="Detalle adicional del error")
