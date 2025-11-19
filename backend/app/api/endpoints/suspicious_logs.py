from fastapi import APIRouter, Depends, HTTPException
from app.schemas.requests import SuspiciousLogsRequest
from app.schemas.responses import SuspiciousAccessResponse, ErrorResponse
from app.services.suspicious_logs_service import SuspiciousLogsService
from app.core.config import get_settings
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/suspicious-logs", tags=["Suspicious Network Logs Detection"])

# Global service instance
suspicious_logs_service = None


def get_suspicious_logs_service():
    """Dependency to get suspicious logs service"""
    global suspicious_logs_service
    if suspicious_logs_service is None:
        # Get absolute path to model
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        model_path = base_dir / "trained_models" / "suspicious_logs.pkl"
        suspicious_logs_service = SuspiciousLogsService(str(model_path))
    return suspicious_logs_service


@router.post(
    "/check-log",
    response_model=SuspiciousAccessResponse,
    summary="Check if network log is suspicious",
    description="Analyzes network log data and determines if it's an attack using a trained DecisionTree model"
)
async def check_suspicious_log(
    request: SuspiciousLogsRequest,
    service: SuspiciousLogsService = Depends(get_suspicious_logs_service)
):
    """
    Check if network log entry is suspicious/attack
    
    - **duration**: Duration of connection
    - **proto**: Protocol (TCP, UDP, ICMP, etc.)
    - **src_ip_addr**: Source IP address identifier
    - **src_pt**: Source port
    - **dst_ip_addr**: Destination IP address identifier
    - **dst_pt**: Destination port
    - **packets**: Number of packets
    - **bytes_str**: Bytes transferred (e.g., "2.1 M", "500 K", "1234")
    - **flags**: TCP flags (e.g., ".AP...", "S.....", etc.)
    
    Returns detection result with confidence score
    """
    try:
        result = service.check_log(
            duration=request.duration,
            proto=request.proto,
            src_ip_addr=request.src_ip_addr,
            src_pt=request.src_pt,
            dst_ip_addr=request.dst_ip_addr,
            dst_pt=request.dst_pt,
            packets=request.packets,
            bytes_str=request.bytes_str,
            flags=request.flags
        )
        
        return SuspiciousAccessResponse(
            success=True,
            prediction=result["prediction"],
            confidence=result["confidence"],
            is_suspicious=result["is_suspicious"],
            details=result.get("details")
        )
        
    except Exception as e:
        logger.error(f"Error in suspicious logs detection endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/health",
    summary="Check suspicious logs detector health",
    description="Verify if the suspicious logs detection service is running"
)
async def health_check(service: SuspiciousLogsService = Depends(get_suspicious_logs_service)):
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "suspicious_logs_detector",
        "model_loaded": service.pipeline is not None
    }
