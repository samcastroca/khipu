"""
URL Tokenizer for phishing detection

This module must be separate to ensure it can be imported by joblib
when deserializing the TfidfVectorizer
"""


def tokenize_url(url: str) -> list:
    """
    Tokeniza una URL separándola en componentes significativos
    
    Esta función debe estar definida antes de cargar el vectorizador
    porque el TfidfVectorizer fue entrenado con este tokenizador personalizado.
    
    Ejemplo:
    'https://github.com/user/repo' → ['https', 'github', 'com', 'user', 'repo']
    
    Args:
        url: URL a tokenizar
        
    Returns:
        Lista de tokens
    """
    # Reemplazar caracteres especiales por espacios
    tokens = url.replace('/', ' ').replace('.', ' ').replace('?', ' ') \
                .replace('=', ' ').replace('&', ' ').replace('-', ' ') \
                .replace('_', ' ').replace(':', ' ')
    
    # Dividir en tokens
    return tokens.split()
