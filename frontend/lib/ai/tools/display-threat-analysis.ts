import { tool } from "ai";
import { z } from "zod";

export const displayThreatAnalysis = tool({
  description:
    "Muestra análisis visual de amenazas de ciberseguridad. USA SIEMPRE que analices emails, URLs, archivos o contenido de seguridad. Proporciona evidencias objetivas y recomendaciones claras. IMPORTANTE: Debes proporcionar al menos 1 evidencia y 1 recomendación.",
  inputSchema: z.object({
    threatType: z
      .enum([
        "phishing",
        "malware",
        "intrusion",
        "social_engineering",
        "anomaly",
        "safe",
      ])
      .describe(
        "Tipo de amenaza: 'phishing' para emails falsos, 'malware' para software malicioso, 'intrusion' para intrusiones de red, 'social_engineering' para manipulación, 'anomaly' para comportamientos extraños, 'safe' si no hay amenaza"
      ),
    riskLevel: z
      .enum(["critical", "high", "medium", "low", "safe"])
      .describe(
        "Nivel de riesgo: 'critical' si hay peligro inmediato, 'high' si es muy sospechoso, 'medium' si tiene algunos indicadores, 'low' si tiene pocos indicadores, 'safe' si no hay amenaza"
      ),
    summary: z
      .string()
      .min(10)
      .describe(
        "Resumen objetivo del análisis en 2-3 oraciones. Describe QUÉ se encontró sin hacer juicios definitivos. Ejemplo: 'Se detectaron 3 indicadores sospechosos en el email analizado. El dominio del remitente difiere del mostrado y contiene errores ortográficos. Se recomienda verificación adicional antes de interactuar.'"
      ),
    evidence: z
      .array(z.string())
      .min(1)
      .describe(
        "Lista de evidencias OBJETIVAS encontradas. Mínimo 1, recomendado 4-10. Ejemplos: 'Dominio registrado hace 2 días', 'Remitente usa dominio diferente', 'Mensaje contiene errores ortográficos', 'URL redirige a otro dominio'"
      ),
    recommendations: z
      .array(z.string())
      .min(1)
      .describe(
        "Lista de recomendaciones de acción. Mínimo 1, recomendado 3-6. Ejemplos: 'Verificar legitimidad del remitente', 'Comprobar URL en bases de amenazas', 'Analizar encabezados del correo', 'No hacer clic en enlaces', 'Reportar al equipo de seguridad'"
      ),
    suspiciousIndicators: z
      .array(
        z.object({
          category: z.string().describe("Categoría del indicador"),
          finding: z.string().describe("Hallazgo específico"),
          significance: z
            .enum(["high", "medium", "low"])
            .describe("Importancia del hallazgo"),
        })
      )
      .optional()
      .describe(
        "Indicadores sospechosos categorizados para análisis detallado"
      ),
    details: z
      .object({
        sender: z
          .string()
          .optional()
          .describe("Email del remitente si es un correo"),
        subject: z.string().optional().describe("Asunto del correo"),
        url: z.string().optional().describe("URL analizada"),
        fileName: z
          .string()
          .optional()
          .describe("Nombre del archivo analizado"),
        ipAddress: z
          .string()
          .optional()
          .describe("Dirección IP"),
        domain: z.string().optional().describe("Dominio analizado"),
        registrationDate: z
          .string()
          .optional()
          .describe("Fecha de registro del dominio"),
        sslCertificate: z
          .string()
          .optional()
          .describe("Información del certificado SSL"),
      })
      .optional()
      .describe("Detalles técnicos adicionales del contenido analizado"),
    affectedSystems: z
      .array(z.string())
      .optional()
      .describe("Lista de sistemas o usuarios potencialmente afectados"),
  }),
  execute: async (input) => {
    return {
      type: "threat-analysis",
      analysis: {
        ...input,
        timestamp: new Date().toISOString(),
        analysisId: `threat-${Date.now()}`,
      },
    };
  },
});
