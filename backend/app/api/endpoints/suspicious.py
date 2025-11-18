from fastapi import APIRouter, Depends, HTTPException
from app.schemas.requests import SuspiciousAccessRequest
from app.schemas.responses import SuspiciousAccessResponse, ErrorResponse
from app.services.suspicious_service import SuspiciousAccessService
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/suspicious", tags=["Suspicious Access Detection"])

# Global service instance
suspicious_service = None


def get_suspicious_service():
    """Dependency to get suspicious access service"""
    global suspicious_service
    if suspicious_service is None:
        settings = get_settings()
        suspicious_service = SuspiciousAccessService(settings.suspicious_access_model_path)
    return suspicious_service


@router.post(
    "/check-access",
    response_model=SuspiciousAccessResponse,
    summary="Check if access attempt is suspicious",
    description="Analyzes access attempt data and determines if it's suspicious using a trained ML model"
)
async def check_suspicious_access(
    request: SuspiciousAccessRequest,
    service: SuspiciousAccessService = Depends(get_suspicious_service)
):
    """
    Check if an access attempt is suspicious
    
    - **user_id**: User identifier (optional)
    - **ip_address**: IP address of the access
    - **timestamp**: Timestamp of the access (optional)
    - **action**: Action performed (e.g., login_attempt, file_access)
    - **location**: Geographic location (optional)
    - **device**: Device information (optional)
    
    Returns detection result with confidence score
    """
    try:
        result = service.check_access(
            user_id=request.user_id,
            ip_address=request.ip_address,
            timestamp=request.timestamp,
            action=request.action,
            location=request.location,
            device=request.device
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
        "model_loaded": service.model is not None
    }
