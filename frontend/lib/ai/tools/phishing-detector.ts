import { tool } from "ai";
import { z } from "zod";

export const phishingDetector = tool({
  description:
    "Detecta si una URL es un intento de phishing usando un modelo de Machine Learning entrenado. Úsala cuando el usuario proporcione una URL o enlace sospechoso para verificar si es seguro o fraudulento. Analiza características de la URL como dominio, estructura y patrones maliciosos.",
  inputSchema: z.object({
    url: z
      .string()
      .min(1)
      .describe(
        "URL completa a analizar. Puede ser un enlace HTTP/HTTPS o dominio. Ejemplos: 'http://suspicious-site.com/login', 'paypa1.com', 'https://secure-bank-login.xyz'"
      ),
  }),
  execute: async ({ url }) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      if (!apiUrl) {
        return {
          success: false,
          error: "API no configurada",
          prediction: "error",
          is_phishing: false,
          message:
            "No se pudo conectar con el servicio de análisis. Continuaré ayudándote con análisis manual de la URL.",
        };
      }

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);

      const response = await fetch(`${apiUrl}/api/v1/phishing/check-url`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      return {
        success: true,
        url: url,
        prediction: data.prediction,
        is_phishing: data.is_phishing,
        confidence: data.confidence,
        details: data.details,
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
        is_phishing: false,
        url: url,
        message:
          "El servicio de análisis no está disponible en este momento. Puedo ayudarte a analizar la URL manualmente basándome en indicadores comunes de phishing.",
      };
    }
  },
});
