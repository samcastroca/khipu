"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  Activity,
  AlertCircle,
  AlertTriangle,
  CheckCircle2,
  Copy,
  Network,
  ShieldAlert,
  ShieldCheck,
  TrendingUp,
} from "lucide-react";
import { useState } from "react";

interface SuspiciousLogsResultDisplayProps {
  success: boolean;
  prediction: string;
  is_suspicious: boolean;
  confidence?: number;
  details?: {
    anomaly_factors?: string[];
    risk_level?: string;
    [key: string]: any;
  };
  analyzed_log?: {
    duration: string;
    proto: string;
    src_ip_addr: string;
    src_pt: string;
    dst_ip_addr: string;
    dst_pt: string;
    packets: string;
    bytes_str: string;
    flags: string;
  };
  error?: string;
  message?: string;
}

export function SuspiciousLogsResultDisplay({
  success,
  prediction,
  is_suspicious,
  confidence,
  details,
  analyzed_log,
  error,
  message,
}: SuspiciousLogsResultDisplayProps) {
  const [copied, setCopied] = useState(false);

  const handleCopyReport = () => {
    const report = `
ANÁLISIS DE LOG DE RED SOSPECHOSO - MODELO ML

Resultado: ${is_suspicious ? "ACTIVIDAD SOSPECHOSA DETECTADA" : "ACTIVIDAD NORMAL"}
Predicción: ${prediction}
${confidence ? `Confianza: ${(confidence * 100).toFixed(2)}%` : ""}

${analyzed_log ? `DATOS DEL LOG:
- Origen: ${analyzed_log.src_ip_addr}:${analyzed_log.src_pt}
- Destino: ${analyzed_log.dst_ip_addr}:${analyzed_log.dst_pt}
- Protocolo: ${analyzed_log.proto}
- Duración: ${analyzed_log.duration.toFixed(2)}s
- Paquetes: ${analyzed_log.packets}
- Bytes: ${analyzed_log.bytes_str}
- Flags: ${analyzed_log.flags}
` : ""}
${details?.anomaly_factors ? `FACTORES DE ANOMALÍA:\n${details.anomaly_factors.map((f: string, i: number) => `${i + 1}. ${f}`).join("\n")}\n` : ""}
${details?.risk_level ? `Nivel de Riesgo: ${details.risk_level.toUpperCase()}\n` : ""}
Analizado: ${new Date().toLocaleString("es-ES")}
    `.trim();

    navigator.clipboard.writeText(report);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Si hay error, mostrar mensaje amigable
  if (!success) {
    return (
      <Card className="border-yellow-200 bg-yellow-50 dark:border-yellow-900 dark:bg-yellow-950/20">
        <CardHeader className="pb-3">
          <div className="flex items-center gap-2">
            <AlertCircle className="size-5 text-yellow-600 dark:text-yellow-400" />
            <h3 className="font-semibold text-yellow-900 dark:text-yellow-100">
              Servicio de Análisis No Disponible
            </h3>
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-yellow-800 dark:text-yellow-200">
            {message ||
              "El modelo de detección de accesos sospechosos no está disponible temporalmente. Continuaré ayudándote con análisis manual."}
          </p>
          {error && (
            <p className="mt-2 text-xs text-yellow-600 dark:text-yellow-400">
              Error: {error === "timeout" ? "Tiempo de espera agotado" : "Error de conexión"}
            </p>
          )}
        </CardContent>
      </Card>
    );
  }

  const isSuspicious = is_suspicious;
  const confidencePercent = confidence ? (confidence * 100).toFixed(2) : null;

  return (
    <Card
      className={`border-2 ${
        isSuspicious
          ? "border-red-200 bg-red-50 dark:border-red-900 dark:bg-red-950/20"
          : "border-green-200 bg-green-50 dark:border-green-900 dark:bg-green-950/20"
      }`}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            {isSuspicious ? (
              <div className="rounded-lg bg-red-100 p-2 dark:bg-red-900/30">
                <ShieldAlert className="size-6 text-red-600 dark:text-red-400" />
              </div>
            ) : (
              <div className="rounded-lg bg-green-100 p-2 dark:bg-green-900/30">
                <ShieldCheck className="size-6 text-green-600 dark:text-green-400" />
              </div>
            )}
            <div>
              <h3 className="text-lg font-semibold">
                {isSuspicious ? "Acceso Sospechoso Detectado" : "Acceso Normal"}
              </h3>
              <div className="mt-1 flex items-center gap-2">
                <Badge
                  variant="outline"
                  className={
                    isSuspicious
                      ? "border-red-300 bg-red-100 text-red-800 dark:border-red-800 dark:bg-red-900/30 dark:text-red-200"
                      : "border-green-300 bg-green-100 text-green-800 dark:border-green-800 dark:bg-green-900/30 dark:text-green-200"
                  }
                >
                  <Network className="mr-1 size-3" />
                  {prediction}
                </Badge>
                {confidencePercent && (
                  <Badge
                    variant="secondary"
                    className="bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300"
                  >
                    <TrendingUp className="mr-1 size-3" />
                    {confidencePercent}% confianza
                  </Badge>
                )}
              </div>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={handleCopyReport}
            className="shrink-0"
          >
            {copied ? (
              <CheckCircle2 className="size-4 text-green-600" />
            ) : (
              <Copy className="size-4" />
            )}
          </Button>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Resultado principal */}
        <div
          className={`rounded-lg border p-4 ${
            isSuspicious
              ? "border-red-200 bg-red-100/50 dark:border-red-800 dark:bg-red-900/20"
              : "border-green-200 bg-green-100/50 dark:border-green-800 dark:bg-green-900/20"
          }`}
        >
          <div className="flex items-start gap-2">
            {isSuspicious ? (
              <AlertTriangle className="mt-0.5 size-5 shrink-0 text-red-600 dark:text-red-400" />
            ) : (
              <CheckCircle2 className="mt-0.5 size-5 shrink-0 text-green-600 dark:text-green-400" />
            )}
            <div>
              <p className="font-medium">
                {isSuspicious
                  ? "Este log de red presenta comportamiento anómalo"
                  : "Este log de red presenta comportamiento normal"}
              </p>
              <p className="mt-1 text-sm opacity-80">
                {isSuspicious
                  ? "El modelo ML detectó patrones inconsistentes con tráfico legítimo"
                  : "El modelo ML no encontró indicadores significativos de actividad sospechosa"}
              </p>
            </div>
          </div>
        </div>

        {/* Log de red analizado */}
        {analyzed_log && (
          <>
            <Separator />
            <div>
              <h4 className="mb-3 flex items-center gap-2 font-medium">
                <Activity className="size-4" />
                Datos del Log de Red
              </h4>
              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">IP Origen</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_log.src_ip_addr}:{analyzed_log.src_pt}
                  </p>
                </div>
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">IP Destino</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_log.dst_ip_addr}:{analyzed_log.dst_pt}
                  </p>
                </div>
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Protocolo</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_log.proto}
                  </p>
                </div>
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Duración</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_log.duration}
                  </p>
                </div>
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Paquetes</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_log.packets}
                  </p>
                </div>
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Bytes</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_log.bytes_str}
                  </p>
                </div>
                <div className="col-span-2 rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Flags</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_log.flags}
                  </p>
                </div>
              </div>
            </div>
          </>
        )}

        {/* Factores de anomalía */}
        {details?.anomaly_factors &&
          Array.isArray(details.anomaly_factors) &&
          details.anomaly_factors.length > 0 && (
            <>
              <Separator />
              <div>
                <h4 className="mb-2 font-medium">Factores de Anomalía</h4>
                <div className="space-y-2">
                  {details.anomaly_factors.map((factor: string, index: number) => (
                    <div
                      key={index}
                      className="flex items-start gap-2 rounded-md bg-white/50 p-2 text-sm dark:bg-gray-900/30"
                    >
                      <AlertCircle className="mt-0.5 size-4 shrink-0 text-orange-500" />
                      <span>{factor}</span>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

        {/* Nivel de riesgo */}
        {details?.risk_level && (
          <>
            <Separator />
            <div className="flex items-center justify-between rounded-md bg-white/50 p-3 dark:bg-gray-900/30">
              <span className="text-sm font-medium">Nivel de Riesgo</span>
              <Badge
                variant="outline"
                className={
                  details.risk_level === "high"
                    ? "border-red-400 bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300"
                    : details.risk_level === "medium"
                      ? "border-yellow-400 bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300"
                      : "border-blue-400 bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300"
                }
              >
                {details.risk_level.toUpperCase()}
              </Badge>
            </div>
          </>
        )}

        {/* Recomendaciones de seguridad */}
        {isSuspicious && (
          <>
            <Separator />
            <div className="rounded-md border border-red-300 bg-red-50 p-3 dark:border-red-800 dark:bg-red-900/20">
              <p className="text-sm font-medium text-red-900 dark:text-red-100">
                ⚠️ Acciones Recomendadas
              </p>
              <ul className="mt-2 space-y-1 text-xs text-red-800 dark:text-red-200">
                <li>• Analizar patrones de tráfico desde la IP origen</li>
                <li>• Verificar legitimidad del protocolo y puertos utilizados</li>
                <li>• Revisar flags TCP/UDP para detectar anomalías</li>
                <li>• Considerar bloqueo temporal de la IP origen</li>
                <li>• Escalar a equipo de respuesta a incidentes</li>
              </ul>
            </div>
          </>
        )}

        {/* Footer con timestamp */}
        <div className="pt-2 text-center text-xs opacity-50">
          Análisis realizado con modelo ML • {new Date().toLocaleString("es-ES")}
        </div>
      </CardContent>
    </Card>
  );
}
