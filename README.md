# Khipu - Plataforma de Análisis de Ciberseguridad con IA  
  
Khipu es una plataforma de detección de amenazas cibernéticas desarrollada por estudiantes de la Universidad Nacional de Colombia Sede Manizales para una hackathon. El nombre "Khipu" honra los antiguos sistemas de registro y comunicación seguros de las culturas precolombinas.  

### Documentacion Tecnica:  [deepwiki.com/samcastroca/khipu](https://deepwiki.com/samcastroca/khipu)
  
## Capacidades Principales  
  
El sistema combina **4 modelos de Machine Learning** especializados con una interfaz conversacional de IA:  
  
1. **Clasificador de Spam** - Analiza correos electrónicos usando TF-IDF  
2. **Detector de Phishing** - Verifica URLs maliciosas con regresión logística  
3. **Detector de Accesos Sospechosos** - Analiza patrones de acceso a red con Gradient Boosting  
4. **Analizador de Logs de Red** - Detecta tráfico anómalo con Decision Tree  
  
## Arquitectura  
  
**Frontend**: Next.js 15 con TypeScript, Tailwind CSS y Vercel AI SDK  
  
**Backend**: FastAPI, LangChain, OpenAI GPT, Scikit-learn, Pydantic, servicios ML que exponen endpoints REST:  
- `/api/v1/spam/classify` - Clasificación de spam  
- `/api/v1/phishing/check-url` - Detección de phishing  
- `/api/v1/suspicious/check-access` - Análisis de accesos  
- `/api/v1/agent/analyze` - Agente conversacional (opcional)  
  
**Base de Datos**: PostgreSQL con Drizzle ORM  
  
**Modelos**: TF-IDF, Logistic Regression, Gradient Boosting, Decision Trees
  
## Interfaz de Usuario  
  
- **Dashboard**: Visualiza estadísticas de eventos de seguridad y alertas recientes  
- **Chat Inteligente**: Interfaz conversacional donde puedes analizar amenazas en lenguaje natural usando el asistente "Khipu"  
  
## Objetivo
Democratizar el acceso a herramientas de análisis de ciberseguridad mediante IA y Machine Learning.
