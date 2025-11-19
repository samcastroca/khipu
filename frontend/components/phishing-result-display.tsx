"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
  AlertCircle,
  AlertTriangle,
  CheckCircle2,
  Copy,
  ExternalLink,
  Link2,
  ShieldAlert,
  ShieldCheck,
  TrendingUp,
} from "lucide-react";
import { useState } from "react";

interface PhishingResultDisplayProps {
  success: boolean;
  url: string;
  prediction: string;
  is_phishing: boolean;
  confidence?: number;
  details?: {
    risk_level?: string;
    suspicious_features?: string[];
    [key: string]: any;
  };
  error?: string;
  message?: string;
}

export function PhishingResultDisplay({
  success,
  url,
  prediction,
  is_phishing,
  confidence,
  details,
  error,
  message,
}: PhishingResultDisplayProps) {
  const [copied, setCopied] = useState(false);

  const handleCopyReport = () => {
    const report = `
ANÁLISIS DE PHISHING - MODELO ML

URL Analizada: ${url}
Resultado: ${is_phishing ? "PHISHING DETECTADO" : "URL SEGURA"}
Predicción: ${prediction}
${confidence ? `Confianza: ${(confidence * 100).toFixed(2)}%` : ""}

${details?.suspicious_features ? `CARACTERÍSTICAS SOSPECHOSAS:\n${details.suspicious_features.map((f: string, i: number) => `${i + 1}. ${f}`).join("\n")}\n` : ""}
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
              "El modelo de detección de phishing no está disponible temporalmente. Continuaré ayudándote con análisis manual."}
          </p>
          {error && (
            <p className="mt-2 text-xs text-yellow-600 dark:text-yellow-400">
              Error: {error === "timeout" ? "Tiempo de espera agotado" : "Error de conexión"}
            </p>
          )}
          {url && (
            <div className="mt-3 rounded-md bg-white/50 p-2 dark:bg-gray-900/30">
              <p className="break-all text-xs font-mono opacity-70">{url}</p>
            </div>
          )}
        </CardContent>
      </Card>
    );
  }

  const isPhishing = is_phishing;
  const confidencePercent = confidence ? (confidence * 100).toFixed(2) : null;

  return (
    <Card
      className={`border-2 ${
        isPhishing
          ? "border-red-200 bg-red-50 dark:border-red-900 dark:bg-red-950/20"
          : "border-green-200 bg-green-50 dark:border-green-900 dark:bg-green-950/20"
      }`}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            {isPhishing ? (
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
                {isPhishing ? "Phishing Detectado" : "URL Segura"}
              </h3>
              <div className="mt-1 flex items-center gap-2">
                <Badge
                  variant="outline"
                  className={
                    isPhishing
                      ? "border-red-300 bg-red-100 text-red-800 dark:border-red-800 dark:bg-red-900/30 dark:text-red-200"
                      : "border-green-300 bg-green-100 text-green-800 dark:border-green-800 dark:bg-green-900/30 dark:text-green-200"
                  }
                >
                  <Link2 className="mr-1 size-3" />
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
        {/* URL analizada */}
        <div className="rounded-lg border border-gray-200 bg-white/50 p-3 dark:border-gray-800 dark:bg-gray-900/30">
          <div className="mb-1 flex items-center gap-2 text-sm font-medium">
            <ExternalLink className="size-4" />
            <span>URL Analizada</span>
          </div>
          <p className="break-all font-mono text-xs opacity-70">{url}</p>
        </div>

        {/* Resultado principal */}
        <div
          className={`rounded-lg border p-4 ${
            isPhishing
              ? "border-red-200 bg-red-100/50 dark:border-red-800 dark:bg-red-900/20"
              : "border-green-200 bg-green-100/50 dark:border-green-800 dark:bg-green-900/20"
          }`}
        >
          <div className="flex items-start gap-2">
            {isPhishing ? (
              <AlertTriangle className="mt-0.5 size-5 shrink-0 text-red-600 dark:text-red-400" />
            ) : (
              <CheckCircle2 className="mt-0.5 size-5 shrink-0 text-green-600 dark:text-green-400" />
            )}
            <div>
              <p className="font-medium">
                {isPhishing
                  ? "Esta URL ha sido identificada como phishing"
                  : "Esta URL parece ser segura"}
              </p>
              <p className="mt-1 text-sm opacity-80">
                {isPhishing
                  ? "El modelo ML detectó características típicas de sitios fraudulentos"
                  : "El modelo ML no encontró indicadores significativos de phishing"}
              </p>
            </div>
          </div>
        </div>

        {/* Características sospechosas */}
        {details?.suspicious_features &&
          Array.isArray(details.suspicious_features) &&
          details.suspicious_features.length > 0 && (
            <>
              <Separator />
              <div>
                <h4 className="mb-2 font-medium">Características Sospechosas</h4>
                <div className="space-y-2">
                  {details.suspicious_features.map((feature: string, index: number) => (
                    <div
                      key={index}
                      className="flex items-start gap-2 rounded-md bg-white/50 p-2 text-sm dark:bg-gray-900/30"
                    >
                      <AlertCircle className="mt-0.5 size-4 shrink-0 text-orange-500" />
                      <span>{feature}</span>
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

        {/* Advertencia de seguridad */}
        {isPhishing && (
          <>
            <Separator />
            <div className="rounded-md border border-red-300 bg-red-50 p-3 dark:border-red-800 dark:bg-red-900/20">
              <p className="text-sm font-medium text-red-900 dark:text-red-100">
                ⚠️ Recomendaciones de Seguridad
              </p>
              <ul className="mt-2 space-y-1 text-xs text-red-800 dark:text-red-200">
                <li>• No ingreses información personal o credenciales</li>
                <li>• No descargues archivos desde este sitio</li>
                <li>• Reporta esta URL a tu equipo de seguridad</li>
                <li>• Verifica la legitimidad con el supuesto remitente</li>
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
