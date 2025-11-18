from fastapi import APIRouter, Depends, HTTPException
from app.schemas.requests import AgentAnalysisRequest
from app.schemas.responses import AgentAnalysisResponse, ErrorResponse
from app.agents.cybersecurity_agent import CybersecurityAgent
from app.services.spam_service import SpamClassifierService
from app.services.phishing_service import PhishingURLService
from app.services.suspicious_service import SuspiciousAccessService
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agent", tags=["AI Agent"])

# Global instances
agent = None
spam_service = None
phishing_service = None
suspicious_service = None


def get_agent():
    """Dependency to get cybersecurity agent"""
    global agent, spam_service, phishing_service, suspicious_service
    
    if agent is None:
        settings = get_settings()
        
        # Initialize services
        spam_service = SpamClassifierService(settings.spam_model_path)
        phishing_service = PhishingURLService(settings.phishing_url_model_path)
        suspicious_service = SuspiciousAccessService(settings.suspicious_access_model_path)
        
        # Initialize agent
        agent = CybersecurityAgent(
            openai_api_key=settings.openai_api_key,
            model_name=settings.openai_model
        )
        agent.initialize(spam_service, phishing_service, suspicious_service)
    
    return agent


@router.post(
    "/analyze",
    response_model=AgentAnalysisResponse,
    summary="Analyze cybersecurity query with AI agent",
    description="Uses GPT-powered agent to analyze cybersecurity queries and automatically select appropriate tools"
)
async def analyze_with_agent(
    request: AgentAnalysisRequest,
    agent: CybersecurityAgent = Depends(get_agent)
):
    """
    Analyze a cybersecurity query using AI agent
    
    The agent will:
    1. Understand your natural language query
    2. Determine which tools to use (spam classifier, phishing detector, suspicious access detector)
    3. Execute the appropriate analysis
    4. Provide a comprehensive response
    
    - **query**: Your question or request in natural language (Spanish or English)
    - **context**: Optional additional context for the analysis
    
    Examples:
    - "¿Este correo es spam? 'Get rich quick! Click here now!'"
    - "Analiza esta URL: http://suspicious-site.com/login"
    - "Revisa este acceso: IP 192.168.1.1, acción: login_attempt, ubicación: Unknown"
    """
    try:
        result = await agent.analyze(request.query, request.context)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["response"])
        
        return AgentAnalysisResponse(
            success=True,
            response=result["response"],
            tools_used=result["tools_used"],
            results={"intermediate_steps": str(result.get("intermediate_steps", []))}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in agent analysis endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/tools",
    summary="List available agent tools",
    description="Get list of tools available to the AI agent"
)
async def list_tools(agent: CybersecurityAgent = Depends(get_agent)):
    """List available tools for the agent"""
    return {
        "tools": agent.get_available_tools(),
        "description": {
            "spam_classifier": "Classifies emails as spam or legitimate",
            "phishing_url_detector": "Detects phishing URLs and malicious websites",
            "suspicious_access_detector": "Detects suspicious access attempts to systems"
        }
    }


@router.get(
    "/health",
    summary="Check AI agent health",
    description="Verify if the AI agent service is running"
)
async def health_check(agent: CybersecurityAgent = Depends(get_agent)):
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "cybersecurity_agent",
        "agent_initialized": agent.agent_executor is not None,
        "available_tools": agent.get_available_tools()
    }
