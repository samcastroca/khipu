# Backend - Cybersecurity AI API

API de FastAPI con LangChain para análisis de ciberseguridad usando modelos de ML entrenados.

## Características

- 🔒 **Clasificación de Spam**: Detecta correos spam/phishing
- 🌐 **Detección de URLs Phishing**: Analiza URLs sospechosas
- 🚨 **Detección de Accesos Sospechosos**: Identifica intentos de acceso anómalos
- 🤖 **Agente Inteligente**: Usa GPT con LangChain para seleccionar el modelo apropiado

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI principal
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py        # Router principal de la API
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── spam.py      # Endpoint clasificación spam
│   │       ├── phishing.py  # Endpoint detección phishing
│   │       ├── suspicious.py # Endpoint accesos sospechosos
│   │       └── agent.py     # Endpoint agente inteligente
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuración de la app
│   │   └── dependencies.py  # Dependencias compartidas
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── requests.py      # Esquemas de request
│   │   └── responses.py     # Esquemas de response
│   ├── services/
│   │   ├── __init__.py
│   │   ├── spam_service.py
│   │   ├── phishing_service.py
│   │   └── suspicious_service.py
│   └── agents/
│       ├── __init__.py
│       ├── cybersecurity_agent.py  # Agente principal
│       └── tools.py                # Herramientas para el agente
├── trained_models/          # Modelos ML entrenados
├── requirements.txt
├── .env.example
└── README.md
```

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
copy .env.example .env
# Editar .env con tu API key de OpenAI
```

4. Colocar modelos entrenados en `trained_models/`

## Uso

Iniciar el servidor:
```bash
uvicorn app.main:app --reload
```

La API estará disponible en: `http://localhost:8000`

Documentación interactiva: `http://localhost:8000/docs`

## Endpoints

### Clasificación de Spam
```
POST /api/v1/spam/classify
```

### Detección de Phishing URL
```
POST /api/v1/phishing/check-url
```

### Detección de Acceso Sospechoso
```
POST /api/v1/suspicious/check-access
```

### Agente Inteligente
```
POST /api/v1/agent/analyze
```

## Tecnologías

- FastAPI
- LangChain
- OpenAI GPT
- Scikit-learn
- Pydantic
