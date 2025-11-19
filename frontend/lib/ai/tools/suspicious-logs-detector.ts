import { tool } from "ai";
import { z } from "zod";

const NEXT_PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL || "https://vibehack.onrender.com";

export const suspiciousLogsDetector = tool({
  description: `Analiza logs de red/tráfico de red para detectar actividad sospechosa usando ML (DecisionTree).
  
  Cuándo usar:
  - Usuario menciona "log de red", "tráfico", "conexión", "paquetes"
  - Datos de red con IPs, puertos, protocolos
  - Análisis de firewall o IDS
  
  Si el usuario NO proporciona todos los datos, la herramienta usa valores por defecto razonables.`,
  
  inputSchema: z.object({
    duration: z.string().default("1").describe("Duración en segundos. Ej: '1.5', '0.001'. Por defecto: '1'"),
    proto: z.string().default("tcp").describe("Protocolo. Ej: 'tcp', 'udp', 'icmp'. Por defecto: 'tcp'"),
    src_ip_addr: z.string().default("192.168.1.100").describe("IP origen. Ej: '192.168.1.100'. Por defecto: '192.168.1.100'"),
    src_pt: z.string().default("50000").describe("Puerto origen. Ej: '80', '443', '22'. Por defecto: '50000'"),
    dst_ip_addr: z.string().default("10.0.0.1").describe("IP destino. Ej: '10.0.0.1'. Por defecto: '10.0.0.1'"),
    dst_pt: z.string().default("80").describe("Puerto destino. Ej: '80', '443', '22'. Por defecto: '80'"),
    packets: z.string().default("100").describe("Cantidad paquetes. Ej: '100', '1000'. Por defecto: '100'"),
    bytes_str: z.string().default("5000").describe("Bytes totales. Ej: '5000', '2.1 M'. Por defecto: '5000'"),
    flags: z.string().default("PA").describe("Flags TCP. Ej: 'S', 'PA', 'F'. Por defecto: 'PA'"),
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
