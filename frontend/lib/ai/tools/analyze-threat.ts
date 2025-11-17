import { tool } from "ai";
import { z } from "zod";

export const analyzeThreat = () =>
  tool({
    description:
      "Analiza contenido sospechoso (correos, URLs, archivos) y clasifica el tipo de amenaza con su nivel de riesgo",
    inputSchema: z.object({
      content: z.string().describe("El contenido a analizar"),
      type: z
        .enum(["email", "url", "file", "behavior"])
        .describe("Tipo de contenido a analizar"),
      threatType: z
        .enum([
          "phishing",
          "malware",
          "intrusion",
          "social_engineering",
          "anomaly",
          "safe",
        ])
        .describe("Tipo de amenaza detectada"),
      riskLevel: z
        .enum(["critical", "high", "medium", "low"])
        .describe("Nivel de riesgo"),
      evidence: z
        .array(z.string())
        .describe("Lista de evidencias que indican la amenaza"),
      recommendations: z
        .array(z.string())
        .describe("Recomendaciones de acción"),
    }),
    execute: async ({
      content,
      type,
      threatType,
      riskLevel,
      evidence,
      recommendations,
    }) => {
      // Aquí se guardaría el análisis en la base de datos
      return {
        success: true,
        analysis: {
          content,
          type,
          threatType,
          riskLevel,
          evidence,
          recommendations,
          timestamp: new Date().toISOString(),
        },
      };
    },
  });
