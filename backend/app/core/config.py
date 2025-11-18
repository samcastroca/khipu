from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_title: str = "Cybersecurity AI API"
    api_description: str = "API para análisis de ciberseguridad con modelos ML y LangChain"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4"
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:3001"
    
    # Model Paths
    spam_model_path: str = "trained_models/spam_classifier.pkl"
    phishing_url_model_path: str = "trained_models/phishing_url_logistic_regression.pkl"
    suspicious_access_model_path: str = "trained_models/suspicious_access_classifier.pkl"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def get_cors_origins(self) -> list[str]:
        """Get CORS origins as list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
