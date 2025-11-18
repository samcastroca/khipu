# 🚀 Inicio Rápido - Backend de Ciberseguridad

## 📋 Pasos para poner en marcha el backend

### 1️⃣ Crear y activar entorno virtual

```powershell
# Navegar al directorio backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Si hay error de políticas, ejecutar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2️⃣ Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3️⃣ Configurar variables de entorno

```powershell
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar .env y agregar tu API key de OpenAI
# OPENAI_API_KEY=tu_api_key_aqui
```

### 4️⃣ Preparar los modelos entrenados

Los modelos deben estar en la carpeta `trained_models/`:

```
trained_models/
├── spam_classifier.pkl
├── phishing_url_classifier.pkl
└── suspicious_access_classifier.pkl
```

Si aún no tienes los modelos entrenados, la API funcionará en **modo demo** con heurísticas simples.

### 5️⃣ Iniciar el servidor

```powershell
# Opción 1: Usando el script run.py
python run.py

# Opción 2: Usando uvicorn directamente
uvicorn app.main:app --reload
```

El servidor estará disponible en: **http://localhost:8000**

### 6️⃣ Probar la API

Abre tu navegador y visita:
- **Documentación interactiva**: http://localhost:8000/docs
- **Documentación alternativa**: http://localhost:8000/redoc

O ejecuta el script de prueba:

```powershell
python test_api.py
```

## 🔌 Endpoints Disponibles

### 1. Clasificación de Spam
```http
POST /api/v1/spam/classify
Content-Type: application/json

{
  "email_text": "Tu texto de correo aquí"
}
```

### 2. Detección de Phishing
```http
POST /api/v1/phishing/check-url
Content-Type: application/json

{
  "url": "http://ejemplo.com/login"
}
```

### 3. Detección de Acceso Sospechoso
```http
POST /api/v1/suspicious/check-access
Content-Type: application/json

{
  "user_id": "user_123",
  "ip_address": "192.168.1.1",
  "action": "login_attempt",
  "timestamp": "2025-01-15T14:30:00",
  "location": "Unknown",
  "device": "Chrome"
}
```

### 4. Agente Inteligente (requiere OpenAI API)
```http
POST /api/v1/agent/analyze
Content-Type: application/json

{
  "query": "¿Este correo es spam? 'Click aquí para ganar dinero'",
  "context": {}
}
```

## 🧪 Ejemplos con cURL

### Clasificar Spam
```powershell
curl -X POST "http://localhost:8000/api/v1/spam/classify" `
  -H "Content-Type: application/json" `
  -d '{\"email_text\":\"Win money now! Click here!\"}'
```

### Detectar Phishing
```powershell
curl -X POST "http://localhost:8000/api/v1/phishing/check-url" `
  -H "Content-Type: application/json" `
  -d '{\"url\":\"http://suspicious-site.com/login\"}'
```

### Analizar Acceso Sospechoso
```powershell
curl -X POST "http://localhost:8000/api/v1/suspicious/check-access" `
  -H "Content-Type: application/json" `
  -d '{\"ip_address\":\"192.168.1.1\",\"action\":\"failed_login\",\"location\":\"Unknown\"}'
```

## 📦 Guardar Modelos Entrenados

Cuando entrenes tus modelos, guárdalos así:

```python
import joblib

# Opción 1: Guardar modelo y vectorizador juntos (RECOMENDADO)
model_data = {
    'model': trained_model,
    'vectorizer': tfidf_vectorizer
}
joblib.dump(model_data, 'trained_models/spam_classifier.pkl')

# Opción 2: Guardar solo el modelo
joblib.dump(trained_model, 'trained_models/spam_classifier.pkl')
```

## 🔧 Solución de Problemas

### Error: "No module named 'app'"
```powershell
# Asegúrate de estar en el directorio backend
cd backend
python run.py
```

### Error: "openai_api_key required"
```powershell
# Verifica que el archivo .env existe y tiene tu API key
# El agente NO funcionará sin esta configuración
```

### Los modelos no cargan
```powershell
# Verifica que los archivos .pkl están en trained_models/
# La API funcionará en modo demo si no hay modelos
```

## 🌐 Integración con Frontend

Para conectar con el frontend Next.js, asegúrate de:

1. El backend esté corriendo en el puerto 8000
2. Las CORS estén configuradas en `.env`:
   ```
   CORS_ORIGINS=http://localhost:3000,http://localhost:3001
   ```

3. En el frontend, usa la URL base:
   ```typescript
   const API_BASE_URL = 'http://localhost:8000/api/v1';
   ```

## 📚 Estructura de Respuestas

Todas las respuestas siguen este formato:

```json
{
  "success": true,
  "prediction": "spam|legitimate|phishing|suspicious|normal",
  "confidence": 0.95,
  "is_spam": true,  // o is_phishing, is_suspicious
  "details": {
    "risk_level": "high|medium|low",
    // ... más detalles específicos
  }
}
```

## 🎯 Próximos Pasos

1. Entrena tus modelos de ML con los datos reales
2. Guarda los modelos en `trained_models/`
3. Configura tu API key de OpenAI para el agente
4. Integra con el frontend
5. ¡Disfruta tu API de ciberseguridad! 🎉
