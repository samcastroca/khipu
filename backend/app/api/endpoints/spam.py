from fastapi import APIRouter, Depends, HTTPException
from app.schemas.requests import SpamClassificationRequest
from app.schemas.responses import SpamClassificationResponse, ErrorResponse
from app.services.spam_service import SpamClassifierService
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/spam", tags=["Spam Classification"])

# Global service instance
spam_service = None


def get_spam_service():
    """Dependency to get spam service"""
    global spam_service
    if spam_service is None:
        settings = get_settings()
        spam_service = SpamClassifierService(settings.spam_model_path)
    return spam_service


@router.post(
    "/classify",
    response_model=SpamClassificationResponse,
    summary="Classify email as spam or legitimate",
    description="Analyzes email content and determines if it's spam using a trained ML model"
)
async def classify_spam(
    request: SpamClassificationRequest,
    service: SpamClassifierService = Depends(get_spam_service)
):
    """
    Classify an email as spam or legitimate
    
    - **email_text**: The content of the email to analyze
    
    Returns classification result with confidence score
    """
    try:
        result = service.classify(request.email_text)
        
        return SpamClassificationResponse(
            success=True,
            prediction=result["prediction"],
            confidence=result["confidence"],
            is_spam=result["is_spam"],
            details=result.get("details")
        )
        
    except Exception as e:
        logger.error(f"Error in spam classification endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/health",
    summary="Check spam classifier health",
    description="Verify if the spam classification service is running"
)
async def health_check(service: SpamClassifierService = Depends(get_spam_service)):
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "spam_classifier",
        "model_loaded": service.model is not None
    }
