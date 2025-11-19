from fastapi import APIRouter, Depends, HTTPException
from app.schemas.requests import PhishingURLRequest
from app.schemas.responses import PhishingURLResponse, ErrorResponse
from app.services.phishing_service import PhishingURLService
from app.core.config import get_settings
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/phishing", tags=["Phishing Detection"])

# Global service instance
phishing_service = None


def get_phishing_service():
    """Dependency to get phishing service"""
    global phishing_service
    if phishing_service is None:
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        model_path = base_dir / "trained_models" / "phishing_url_logistic_regression.pkl"
        phishing_service = PhishingURLService(str(model_path))
    return phishing_service


@router.post(
    "/check-url",
    response_model=PhishingURLResponse,
    summary="Check if URL is a phishing attempt",
    description="Analyzes a URL and determines if it's a phishing attempt using a trained ML model"
)
async def check_phishing_url(
    request: PhishingURLRequest,
    service: PhishingURLService = Depends(get_phishing_service)
):
    """
    Check if a URL is a phishing attempt
    
    - **url**: The URL to analyze
    
    Returns detection result with confidence score
    """
    try:
        result = service.check_url(request.url)
        
        return PhishingURLResponse(
            success=True,
            prediction=result["prediction"],
            confidence=result["confidence"],
            is_phishing=result["is_phishing"],
            details=result.get("details")
        )
        
    except Exception as e:
        logger.error(f"Error in phishing detection endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/health",
    summary="Check phishing detector health",
    description="Verify if the phishing detection service is running"
)
async def health_check(service: PhishingURLService = Depends(get_phishing_service)):
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "phishing_detector",
        "model_loaded": service.model is not None
    }
