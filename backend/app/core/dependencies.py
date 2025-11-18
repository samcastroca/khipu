from functools import lru_cache
from app.core.config import get_settings, Settings


@lru_cache()
def get_settings_dependency() -> Settings:
    """Dependency for getting settings"""
    return get_settings()
