from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Dict, Any, List
import logging

from app.agents.tools import (
    create_spam_classifier_tool,
    create_phishing_url_tool,
    create_suspicious_access_tool
)

logger = logging.getLogger(__name__)


class CybersecurityAgent:
    """AI Agent for cybersecurity analysis using LangChain"""
    
    def __init__(self, openai_api_key: str, model_name: str = "gpt-5-mini"):
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.llm = None
        self.agent_executor = None
        self.tools = []
    
    def initialize(self, spam_service, phishing_service, suspicious_service):
        """Initialize the agent with tools"""
        try:
            # Initialize LLM
            self.llm = ChatOpenAI(
                temperature=0,
                model_name=self.model_name,
                openai_api_key=self.openai_api_key
            )
            
            # Create tools
            self.tools = [
                create_spam_classifier_tool(spam_service.classify),
                create_phishing_url_tool(phishing_service.check_url),
                create_suspicious_access_tool(suspicious_service.check_access)
            ]
            
            # Create prompt
            prompt = ChatPromptTemplate.from_messages([
                ("system", self._get_system_prompt()),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])
            
            # Create agent
            agent = create_openai_functions_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=prompt
            )
            
            # Create agent executor
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True,
                max_iterations=5,
                return_intermediate_steps=True
            )
            
            logger.info("Cybersecurity agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing agent: {e}")
            raise
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent"""
        return """Eres un asistente experto en ciberseguridad que ayuda a analizar amenazas.

Tienes acceso a las siguientes herramientas:
1. spam_classifier: Para clasificar correos electrónicos como spam o legítimos
2. phishing_url_detector: Para detectar URLs de phishing y sitios maliciosos
3. suspicious_access_detector: Para detectar intentos de acceso sospechosos a sistemas

Tu trabajo es:
- Entender la consulta del usuario
- Determinar qué herramienta(s) usar
- Usar las herramientas apropiadamente
- Proporcionar una respuesta clara y útil en español

Cuando uses la herramienta suspicious_access_detector, formatea los datos como:
'ip:XXX.XXX.XXX.XXX,action:ACTION,location:LOCATION,device:DEVICE'

Siempre proporciona:
- Un resumen claro del análisis
- El nivel de riesgo detectado
- Recomendaciones si es necesario

Responde siempre en español de manera profesional y clara."""
    
    async def analyze(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze a cybersecurity query using the agent
        
        Args:
            query: User's natural language query
            context: Additional context for the analysis
            
        Returns:
            Dictionary with analysis results
        """
        try:
            if self.agent_executor is None:
                raise ValueError("Agent not initialized. Call initialize() first.")
            
            # Prepare input
            full_query = query
            if context:
                full_query += f"\n\nContexto adicional: {context}"
            
            # Run agent
            result = await self.agent_executor.ainvoke({
                "input": full_query
            })
            
            # Extract tools used
            tools_used = []
            if result.get("intermediate_steps"):
                for step in result["intermediate_steps"]:
                    if hasattr(step[0], 'tool'):
                        tools_used.append(step[0].tool)
            
            return {
                "success": True,
                "response": result.get("output", "No se pudo generar una respuesta"),
                "tools_used": tools_used,
                "intermediate_steps": result.get("intermediate_steps", [])
            }
            
        except Exception as e:
            logger.error(f"Error in agent analysis: {e}")
            return {
                "success": False,
                "response": f"Error en el análisis: {str(e)}",
                "tools_used": [],
                "intermediate_steps": []
            }
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return [tool.name for tool in self.tools]
