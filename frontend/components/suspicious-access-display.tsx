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

interface SuspiciousAccessDisplayProps {
  success: boolean;
  prediction: string;
  is_suspicious: boolean;
  confidence?: number;
  details?: {
    anomaly_factors?: string[];
    risk_level?: string;
    [key: string]: any;
  };
  analyzed_params?: {
    network_packet_size?: number;
    protocol_type?: string;
    login_attempts?: number;
    session_duration?: number;
    encryption_used?: string;
    ip_reputation_score?: number;
    failed_logins?: number;
    browser_type?: string;
    unusual_time_access?: number;
  };
  error?: string;
  message?: string;
}

export function SuspiciousAccessDisplay({
  success,
  prediction,
  is_suspicious,
  confidence,
  details,
  analyzed_params,
  error,
  message,
}: SuspiciousAccessDisplayProps) {
  const [copied, setCopied] = useState(false);

  const handleCopyReport = () => {
    const report = `
ANÁLISIS DE ACCESO SOSPECHOSO - MODELO ML

Resultado: ${is_suspicious ? "ACCESO SOSPECHOSO DETECTADO" : "ACCESO NORMAL"}
Predicción: ${prediction}
${confidence ? `Confianza: ${(confidence * 100).toFixed(1)}%` : ""}

${analyzed_params ? `PARÁMETROS ANALIZADOS:
- Tamaño de paquete: ${analyzed_params.network_packet_size} bytes
- Protocolo: ${analyzed_params.protocol_type}
- Intentos de login: ${analyzed_params.login_attempts}
- Duración de sesión: ${analyzed_params.session_duration} min
- Encriptación: ${analyzed_params.encryption_used}
- Reputación IP: ${analyzed_params.ip_reputation_score}/100
- Logins fallidos: ${analyzed_params.failed_logins}
- Navegador: ${analyzed_params.browser_type}
- Horario inusual: ${analyzed_params.unusual_time_access ? "Sí" : "No"}
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
  const confidencePercent = confidence ? (confidence * 100).toFixed(1) : null;

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
                  ? "Este acceso presenta comportamiento anómalo"
                  : "Este acceso presenta comportamiento normal"}
              </p>
              <p className="mt-1 text-sm opacity-80">
                {isSuspicious
                  ? "El modelo ML detectó patrones inconsistentes con actividad legítima"
                  : "El modelo ML no encontró indicadores significativos de actividad maliciosa"}
              </p>
            </div>
          </div>
        </div>

        {/* Parámetros analizados */}
        {analyzed_params && (
          <>
            <Separator />
            <div>
              <h4 className="mb-3 flex items-center gap-2 font-medium">
                <Activity className="size-4" />
                Parámetros de Acceso
              </h4>
              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Tamaño de paquete</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_params.network_packet_size} bytes
                  </p>
                </div>
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Protocolo</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_params.protocol_type}
                  </p>
                </div>
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Intentos de login</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_params.login_attempts}
                  </p>
                </div>
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Logins fallidos</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_params.failed_logins}
                  </p>
                </div>
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Duración de sesión</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_params.session_duration} min
                  </p>
                </div>
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Encriptación</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_params.encryption_used}
                  </p>
                </div>
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Reputación IP</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_params.ip_reputation_score}/100
                  </p>
                </div>
                <div className="rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Navegador</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_params.browser_type}
                  </p>
                </div>
                <div className="col-span-2 rounded-md bg-white/50 p-2.5 dark:bg-gray-900/30">
                  <p className="text-xs opacity-60">Horario inusual</p>
                  <p className="mt-0.5 font-mono text-sm font-medium">
                    {analyzed_params.unusual_time_access ? "Sí" : "No"}
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
                <li>• Verificar la legitimidad del acceso con el usuario</li>
                <li>• Revisar logs completos de la sesión</li>
                <li>• Considerar bloqueo temporal de la IP</li>
                <li>• Escalar a equipo de respuesta a incidentes</li>
                <li>• Monitorear actividad futura desde este origen</li>
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
