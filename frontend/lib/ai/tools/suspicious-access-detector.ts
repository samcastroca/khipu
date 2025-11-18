import { tool } from "ai";
import { z } from "zod";

export const suspiciousAccessDetector = tool({
  description:
    "Analiza accesos de red y detecta actividad sospechosa o ataques usando un modelo de Machine Learning entrenado. Úsala cuando el usuario proporcione logs de acceso, datos de tráfico de red, o información sobre sesiones. Acepta parámetros opcionales y usa valores por defecto inteligentes.",
  inputSchema: z.object({
    network_packet_size: z
      .number()
      .min(0)
      .default(1500)
      .describe("Tamaño del paquete de red en bytes. Por defecto: 1500"),
    protocol_type: z
      .string()
      .default("HTTP")
      .describe(
        "Tipo de protocolo usado (HTTP, HTTPS, FTP, SSH, etc.). Por defecto: HTTP"
      ),
    login_attempts: z
      .number()
      .min(0)
      .default(1)
      .describe("Número de intentos de login. Por defecto: 1"),
    session_duration: z
      .number()
      .min(0)
      .default(10)
      .describe("Duración de la sesión en minutos. Por defecto: 10"),
    encryption_used: z
      .string()
      .default("AES")
      .describe(
        "Tipo de encriptación (AES, RSA, None, Unknown). Por defecto: AES"
      ),
    ip_reputation_score: z
      .number()
      .min(0)
      .max(100)
      .default(50)
      .describe(
        "Puntuación de reputación de la IP (0-100, mayor es mejor). Por defecto: 50"
      ),
    failed_logins: z
      .number()
      .min(0)
      .default(0)
      .describe("Número de logins fallidos. Por defecto: 0"),
    browser_type: z
      .string()
      .default("Chrome")
      .describe(
        "Tipo de navegador (Chrome, Firefox, Safari, Edge, etc.). Por defecto: Chrome"
      ),
    unusual_time_access: z
      .number()
      .min(0)
      .max(1)
      .default(0)
      .describe("Acceso en horario inusual (0=no, 1=sí). Por defecto: 0"),
  }),
  execute: async (params) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      if (!apiUrl) {
        return {
          success: false,
          error: "API no configurada",
          prediction: "error",
          is_suspicious: false,
          message:
            "No se pudo conectar con el servicio de análisis. Continuaré ayudándote con análisis manual de acceso.",
        };
      }

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);

      const response = await fetch(
        `${apiUrl}/api/v1/suspicious/check-access`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(params),
          signal: controller.signal,
        }
      );

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      return {
        success: true,
        prediction: data.prediction,
        is_suspicious: data.is_suspicious,
        confidence: data.confidence,
        details: data.details,
        analyzed_params: params,
        analyzed_at: new Date().toISOString(),
      };
    } catch (error) {
      // Manejo silencioso de errores
      return {
        success: false,
        error:
          error instanceof Error
            ? error.name === "AbortError"
              ? "timeout"
              : "network"
            : "unknown",
        prediction: "error",
        is_suspicious: false,
        message:
          "El servicio de análisis no está disponible en este momento. Puedo ayudarte a analizar el acceso manualmente basándome en patrones comunes de ataques.",
      };
    }
  },
});
