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
    network_packet_size: int = Field(..., description="Tamaño del paquete de red", ge=0)
    protocol_type: str = Field(..., description="Tipo de protocolo (HTTP, HTTPS, FTP, SSH, etc.)")
    login_attempts: int = Field(..., description="Número de intentos de login", ge=0)
    session_duration: float = Field(..., description="Duración de la sesión en minutos", ge=0)
    encryption_used: str = Field(..., description="Tipo de encriptación (AES, RSA, None, Unknown)")
    ip_reputation_score: float = Field(..., description="Puntuación de reputación de IP (0-100)", ge=0, le=100)
    failed_logins: int = Field(..., description="Número de logins fallidos", ge=0)
    browser_type: str = Field(..., description="Tipo de navegador (Chrome, Firefox, Safari, Edge, etc.)")
    unusual_time_access: int = Field(..., description="Acceso en horario inusual (0=no, 1=sí)", ge=0, le=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "network_packet_size": 1200,
                "protocol_type": "HTTP",
                "login_attempts": 3,
                "session_duration": 15.8,
                "encryption_used": "AES",
                "ip_reputation_score": 73.2,
                "failed_logins": 1,
                "browser_type": "Chrome",
                "unusual_time_access": 0
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


class SuspiciousLogsRequest(BaseModel):
    """Request schema for suspicious network logs detection"""
    duration: float = Field(..., description="Duración de la conexión", ge=0)
    proto: str = Field(..., description="Protocolo (TCP, UDP, ICMP, etc.)")
    src_ip_addr: str = Field(..., description="Dirección IP de origen")
    src_pt: int = Field(..., description="Puerto de origen", ge=0, le=65535)
    dst_ip_addr: str = Field(..., description="Dirección IP de destino")
    dst_pt: float = Field(..., description="Puerto de destino", ge=0, le=65535)
    packets: int = Field(..., description="Número de paquetes", ge=0)
    bytes_str: str = Field(..., description="Bytes transferidos (e.g., '2.1 M', '500 K', '1234')")
    flags: str = Field(..., description="Flags TCP (e.g., '.AP...', 'S.....', etc.)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "duration": 81412.697,
                "proto": "TCP",
                "src_ip_addr": "EXT_SERVER",
                "src_pt": 8082,
                "dst_ip_addr": "OPENSTACK_NET",
                "dst_pt": 56978,
                "packets": 3057,
                "bytes_str": "2.1 M",
                "flags": ".AP..."
            }
        }
