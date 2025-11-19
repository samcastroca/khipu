import { tool } from "ai";
import { z } from "zod";

const NEXT_PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL || "https://vibehack.onrender.com";

export const suspiciousLogsDetector = tool({
  description: `Analiza logs de red/tráfico de red para detectar actividad sospechosa usando ML (DecisionTree).
  
  IMPORTANTE: Esta herramienta REQUIERE TODOS los 9 parámetros para funcionar.
  
  Cuándo usar:
  - Usuario menciona "log de red", "tráfico", "conexión", "paquetes"
  - Datos de red con IPs, puertos, protocolos
  - Análisis de firewall o IDS
  
  Si el usuario NO proporciona TODOS los datos, debes:
  1. Usar valores por defecto razonables
  2. Inferir basándote en el contexto
  3. Ejemplo: si solo dice "conexión SSH desde 192.168.1.1", usar: duration="5", proto="tcp", src_ip_addr="192.168.1.1", src_pt="22", dst_ip_addr="10.0.0.1", dst_pt="22", packets="50", bytes_str="2500", flags="PA"`,
  
  parameters: z.object({
    duration: z.string().describe("Duración en segundos. Ej: '1.5', '0.001'. Si no se proporciona, infiere un valor razonable (1-5 seg típico)"),
    proto: z.string().describe("Protocolo. Ej: 'tcp', 'udp', 'icmp'. Si no se proporciona, usa 'tcp' como valor por defecto"),
    src_ip_addr: z.string().describe("IP origen. Ej: '192.168.1.100'. Si no se proporciona, usa una IP privada genérica"),
    src_pt: z.string().describe("Puerto origen. Ej: '80', '443', '22'. Si no se proporciona, infiere según contexto o usa puerto efímero"),
    dst_ip_addr: z.string().describe("IP destino. Ej: '10.0.0.1'. Si no se proporciona, usa una IP privada genérica"),
    dst_pt: z.string().describe("Puerto destino. Ej: '80', '443', '22'. Si no se proporciona, infiere según protocolo (80=HTTP, 443=HTTPS, 22=SSH)"),
    packets: z.string().describe("Cantidad paquetes. Ej: '100', '1000'. Si no se proporciona, usa un valor típico (50-200)"),
    bytes_str: z.string().describe("Bytes totales. Ej: '5000', '2.1 M'. Si no se proporciona, calcula aproximado (packets * 500)"),
    flags: z.string().describe("Flags TCP. Ej: 'S', 'PA', 'F'. Si no se proporciona, usa 'PA' para TCP normal o '' para UDP"),
  }),

  execute: async ({ duration, proto, src_ip_addr, src_pt, dst_ip_addr, dst_pt, packets, bytes_str, flags }) => {
    try {
      const url = `${NEXT_PUBLIC_API_URL}/api/v1/suspicious-logs/check-log`;
      const payload = { duration, proto, src_ip_addr, src_pt, dst_ip_addr, dst_pt, packets, bytes_str, flags };
      
      console.log('[suspiciousLogsDetector] Request URL:', url);
      console.log('[suspiciousLogsDetector] Request payload:', payload);
      
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(30000),
      });

      console.log('[suspiciousLogsDetector] Response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('[suspiciousLogsDetector] API Error:', response.status, errorText);
        throw new Error(`API Error: ${response.status} - ${errorText}`);
      }
      
      const data = await response.json();
      console.log('[suspiciousLogsDetector] Response data:', data);

      return {
        success: data.success,
        prediction: data.prediction,
        is_suspicious: data.is_suspicious,
        confidence: data.confidence,
        details: data.details,
        analyzed_log: { duration, proto, src_ip_addr, src_pt, dst_ip_addr, dst_pt, packets, bytes_str, flags },
        analyzed_at: new Date().toISOString(),
      };
    } catch (error) {
      console.error('[suspiciousLogsDetector] Error:', error);
      if (error instanceof Error) {
        if (error.name === "TimeoutError") {
          return { success: false, error: "timeout", prediction: "error", is_suspicious: false, confidence: 0, message: `El análisis tardó demasiado tiempo. ${error.message}` };
        }
        return { success: false, error: "network_error", prediction: "error", is_suspicious: false, confidence: 0, message: `Error de conexión: ${error.message}` };
      }
      return { success: false, error: "unknown", prediction: "error", is_suspicious: false, confidence: 0, message: "Ocurrió un error inesperado." };
    }
  },
});
