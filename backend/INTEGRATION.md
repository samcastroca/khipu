# 🔗 Guía de Integración Frontend-Backend

## 📡 Conectar Next.js Frontend con FastAPI Backend

### Configuración del Backend

El backend ya está configurado con CORS. Solo asegúrate de que en tu `.env`:

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Configuración en Next.js

#### 1. Crear archivo de configuración de API

```typescript
// frontend/lib/api/cybersecurity.ts

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface SpamClassificationRequest {
  email_text: string;
}

export interface SpamClassificationResponse {
  success: boolean;
  prediction: string;
  confidence: number;
  is_spam: boolean;
  details: {
    risk_level: string;
    detected_patterns?: string[];
  };
}

export interface PhishingURLRequest {
  url: string;
}

export interface PhishingURLResponse {
  success: boolean;
  prediction: string;
  confidence: number;
  is_phishing: boolean;
  details: {
    risk_level: string;
    suspicious_features?: string[];
  };
}

export interface SuspiciousAccessRequest {
  user_id?: string;
  ip_address: string;
  timestamp?: string;
  action: string;
  location?: string;
  device?: string;
}

export interface SuspiciousAccessResponse {
  success: boolean;
  prediction: string;
  confidence: number;
  is_suspicious: boolean;
  details: {
    risk_level: string;
    anomaly_factors?: string[];
  };
}

export interface AgentAnalysisRequest {
  query: string;
  context?: Record<string, any>;
}

export interface AgentAnalysisResponse {
  success: boolean;
  response: string;
  tools_used: string[];
  results?: Record<string, any>;
}

// Función para clasificar spam
export async function classifySpam(
  request: SpamClassificationRequest
): Promise<SpamClassificationResponse> {
  const response = await fetch(`${API_BASE_URL}/spam/classify`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }

  return response.json();
}

// Función para detectar phishing
export async function checkPhishingURL(
  request: PhishingURLRequest
): Promise<PhishingURLResponse> {
  const response = await fetch(`${API_BASE_URL}/phishing/check-url`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }

  return response.json();
}

// Función para detectar accesos sospechosos
export async function checkSuspiciousAccess(
  request: SuspiciousAccessRequest
): Promise<SuspiciousAccessResponse> {
  const response = await fetch(`${API_BASE_URL}/suspicious/check-access`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }

  return response.json();
}

// Función para usar el agente AI
export async function analyzeWithAgent(
  request: AgentAnalysisRequest
): Promise<AgentAnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/agent/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }

  return response.json();
}

// Función de health check
export async function checkAPIHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/../health`);
  
  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }

  return response.json();
}
```

#### 2. Agregar variable de entorno en Next.js

```env
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

#### 3. Ejemplo de uso en un componente

```typescript
// frontend/components/spam-checker.tsx
'use client';

import { useState } from 'react';
import { classifySpam } from '@/lib/api/cybersecurity';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card } from '@/components/ui/card';

export function SpamChecker() {
  const [emailText, setEmailText] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCheck = async () => {
    if (!emailText.trim()) {
      setError('Por favor ingresa un texto de correo');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await classifySpam({ email_text: emailText });
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error al analizar');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <Textarea
        placeholder="Pega el contenido del correo aquí..."
        value={emailText}
        onChange={(e) => setEmailText(e.target.value)}
        rows={6}
      />
      
      <Button onClick={handleCheck} disabled={loading}>
        {loading ? 'Analizando...' : 'Analizar Correo'}
      </Button>

      {error && (
        <Card className="p-4 border-red-500 bg-red-50">
          <p className="text-red-700">{error}</p>
        </Card>
      )}

      {result && (
        <Card className="p-4">
          <h3 className="text-lg font-semibold mb-2">Resultado:</h3>
          <div className="space-y-2">
            <p>
              <strong>Predicción:</strong>{' '}
              <span className={result.is_spam ? 'text-red-600' : 'text-green-600'}>
                {result.is_spam ? '🚨 SPAM' : '✅ Legítimo'}
              </span>
            </p>
            <p>
              <strong>Confianza:</strong> {(result.confidence * 100).toFixed(1)}%
            </p>
            <p>
              <strong>Nivel de Riesgo:</strong> {result.details.risk_level}
            </p>
            {result.details.detected_patterns && (
              <div>
                <strong>Patrones detectados:</strong>
                <ul className="list-disc list-inside">
                  {result.details.detected_patterns.map((pattern: string, i: number) => (
                    <li key={i}>{pattern}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </Card>
      )}
    </div>
  );
}
```

#### 4. Uso del Agente AI en el Chat

```typescript
// frontend/app/(chat)/actions.ts (agregar a tu archivo existente)

import { analyzeWithAgent } from '@/lib/api/cybersecurity';

// En tu función de submit message, puedes agregar:
export async function analyzeCybersecurityQuery(message: string) {
  try {
    const result = await analyzeWithAgent({
      query: message,
      context: {}
    });
    
    return {
      success: true,
      content: result.response,
      toolsUsed: result.tools_used
    };
  } catch (error) {
    console.error('Error analyzing query:', error);
    return {
      success: false,
      error: 'Error al analizar la consulta'
    };
  }
}
```

### 🔌 Endpoints Disponibles

| Endpoint | Método | Propósito |
|----------|--------|-----------|
| `/api/v1/spam/classify` | POST | Clasificar correos como spam |
| `/api/v1/phishing/check-url` | POST | Detectar URLs de phishing |
| `/api/v1/suspicious/check-access` | POST | Detectar accesos sospechosos |
| `/api/v1/agent/analyze` | POST | Análisis con agente AI |
| `/api/v1/spam/health` | GET | Health check del servicio spam |
| `/api/v1/phishing/health` | GET | Health check del servicio phishing |
| `/api/v1/suspicious/health` | GET | Health check del servicio suspicious |
| `/api/v1/agent/health` | GET | Health check del agente |
| `/api/v1/agent/tools` | GET | Listar herramientas disponibles |

### 🚀 Ejecutar ambos servidores

```powershell
# Terminal 1 - Backend
cd backend
.\venv\Scripts\Activate.ps1
python run.py

# Terminal 2 - Frontend
cd frontend
pnpm dev
```

### 📝 Notas Importantes

1. **Manejo de Errores**: Siempre usa try-catch al llamar las APIs
2. **Loading States**: Muestra indicadores de carga mientras esperas respuestas
3. **Validación**: Valida los inputs antes de enviarlos al backend
4. **Tipos**: Usa TypeScript para mayor seguridad de tipos
5. **Variables de Entorno**: Nunca hardcodees URLs, usa variables de entorno

### 🔍 Debugging

Para ver qué está pasando en las llamadas:

```typescript
// Agregar logging
console.log('Request:', request);
const response = await classifySpam(request);
console.log('Response:', response);
```

### 🎨 Ejemplos de UI

Puedes crear componentes para cada tipo de análisis:
- `SpamChecker.tsx` - Para clasificación de spam
- `PhishingChecker.tsx` - Para URLs de phishing
- `AccessMonitor.tsx` - Para accesos sospechosos
- `AIAnalyzer.tsx` - Para el agente AI

¡Listo para integrar! 🎉
