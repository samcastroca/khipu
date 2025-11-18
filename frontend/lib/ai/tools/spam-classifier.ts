import { tool } from "ai";
import { z } from "zod";

export const spamClassifier = tool({
  description:
    "Clasifica correos electrónicos como spam o legítimos usando un modelo de Machine Learning entrenado. Úsala cuando el usuario proporcione el contenido de un email o mensaje para analizar si es spam, phishing o legítimo. Analiza el texto completo del mensaje.",
  inputSchema: z.object({
    email_text: z
      .string()
      .min(1)
      .describe(
        "Texto completo del correo electrónico o mensaje a analizar. Incluye asunto, cuerpo y cualquier otro contenido relevante."
      ),
  }),
  execute: async ({ email_text }) => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      if (!apiUrl) {
        return {
          success: false,
          error: "API no configurada",
          prediction: "error",
          is_spam: false,
          message:
            "No se pudo conectar con el servicio de análisis. Continuaré ayudándote con análisis manual.",
        };
      }

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);

      const response = await fetch(`${apiUrl}/api/v1/spam/classify`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email_text }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      return {
        success: true,
        prediction: data.prediction,
        is_spam: data.is_spam,
        confidence: data.confidence,
        details: data.details,
        email_preview: email_text.substring(0, 200),
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
        is_spam: false,
        message:
          "El servicio de análisis no está disponible en este momento. Puedo ayudarte a analizar el email manualmente basándome en patrones comunes de spam.",
      };
    }
  },
});
