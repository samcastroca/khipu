from fastapi import APIRouter, Depends, HTTPException
from app.schemas.requests import SuspiciousAccessRequest
from app.schemas.responses import SuspiciousAccessResponse, ErrorResponse
from app.services.suspicious_service import SuspiciousAccessService
from app.core.config import get_settings
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/suspicious", tags=["Suspicious Access Detection"])

# Global service instance
suspicious_service = None


def get_suspicious_service():
    """Dependency to get suspicious access service"""
    global suspicious_service
    if suspicious_service is None:
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        model_path = base_dir / "trained_models" / "suspicious_access_classifier.pkl"
        suspicious_service = SuspiciousAccessService(str(model_path))
    return suspicious_service


@router.post(
    "/check-access",
    response_model=SuspiciousAccessResponse,
    summary="Check if network access is suspicious",
    description="Analyzes network access data and determines if it's an attack using a trained ML model"
)
async def check_suspicious_access(
    request: SuspiciousAccessRequest,
    service: SuspiciousAccessService = Depends(get_suspicious_service)
):
    """
    Check if network access is suspicious/attack
    
    - **network_packet_size**: Size of network packet
    - **protocol_type**: Protocol used (HTTP, HTTPS, FTP, SSH, etc.)
    - **login_attempts**: Number of login attempts
    - **session_duration**: Duration of session in minutes
    - **encryption_used**: Encryption type (AES, RSA, None, Unknown)
    - **ip_reputation_score**: IP reputation score (0-100)
    - **failed_logins**: Number of failed logins
    - **browser_type**: Browser type (Chrome, Firefox, Safari, Edge, etc.)
    - **unusual_time_access**: Binary flag for unusual access time (0 or 1)
    
    Returns detection result with confidence score
    """
    try:
        result = service.check_access(
            network_packet_size=request.network_packet_size,
            protocol_type=request.protocol_type,
            login_attempts=request.login_attempts,
            session_duration=request.session_duration,
            encryption_used=request.encryption_used,
            ip_reputation_score=request.ip_reputation_score,
            failed_logins=request.failed_logins,
            browser_type=request.browser_type,
            unusual_time_access=request.unusual_time_access
        )
        
        return SuspiciousAccessResponse(
            success=True,
            prediction=result["prediction"],
            confidence=result["confidence"],
            is_suspicious=result["is_suspicious"],
            details=result.get("details")
        )
        
    except Exception as e:
        logger.error(f"Error in suspicious access detection endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/health",
    summary="Check suspicious access detector health",
    description="Verify if the suspicious access detection service is running"
)
async def health_check(service: SuspiciousAccessService = Depends(get_suspicious_service)):
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "suspicious_access_detector",
        "model_loaded": service.pipeline is not None
    }
