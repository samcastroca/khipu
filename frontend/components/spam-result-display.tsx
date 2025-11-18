"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
    AlertCircle,
    CheckCircle2,
    Copy,
    Mail,
    ShieldAlert,
    ShieldCheck,
    TrendingUp,
    XCircle,
} from "lucide-react";
import { useState } from "react";

interface SpamResultDisplayProps {
  success: boolean;
  prediction: string;
  is_spam: boolean;
  confidence?: number;
  details?: {
    detected_patterns?: string[];
    risk_level?: string;
    [key: string]: any;
  };
  email_preview?: string;
  error?: string;
  message?: string;
}

export function SpamResultDisplay({
  success,
  prediction,
  is_spam,
  confidence,
  details,
  email_preview,
  error,
  message,
}: SpamResultDisplayProps) {
  const [copied, setCopied] = useState(false);

  const handleCopyReport = () => {
    const report = `
ANÁLISIS DE SPAM - MODELO ML

Resultado: ${is_spam ? "SPAM DETECTADO" : "EMAIL LEGÍTIMO"}
Predicción: ${prediction}
${confidence ? `Confianza: ${(confidence * 100).toFixed(1)}%` : ""}

${details?.detected_patterns ? `PATRONES DETECTADOS:\n${details.detected_patterns.map((p: string, i: number) => `${i + 1}. ${p}`).join("\n")}\n` : ""}
${details?.risk_level ? `Nivel de Riesgo: ${details.risk_level.toUpperCase()}\n` : ""}
${email_preview ? `\nVISTA PREVIA DEL EMAIL:\n${email_preview}...\n` : ""}
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
              "El modelo de detección de spam no está disponible temporalmente. Continuaré ayudándote con análisis manual."}
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

  const isSpam = is_spam;
  const confidencePercent = confidence ? (confidence * 100).toFixed(1) : null;

  return (
    <Card
      className={`border-2 ${
        isSpam
          ? "border-red-200 bg-red-50 dark:border-red-900 dark:bg-red-950/20"
          : "border-green-200 bg-green-50 dark:border-green-900 dark:bg-green-950/20"
      }`}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            {isSpam ? (
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
                {isSpam ? "Spam Detectado" : "Email Legítimo"}
              </h3>
              <div className="mt-1 flex items-center gap-2">
                <Badge
                  variant="outline"
                  className={
                    isSpam
                      ? "border-red-300 bg-red-100 text-red-800 dark:border-red-800 dark:bg-red-900/30 dark:text-red-200"
                      : "border-green-300 bg-green-100 text-green-800 dark:border-green-800 dark:bg-green-900/30 dark:text-green-200"
                  }
                >
                  <Mail className="mr-1 size-3" />
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
            isSpam
              ? "border-red-200 bg-red-100/50 dark:border-red-800 dark:bg-red-900/20"
              : "border-green-200 bg-green-100/50 dark:border-green-800 dark:bg-green-900/20"
          }`}
        >
          <div className="flex items-start gap-2">
            {isSpam ? (
              <XCircle className="mt-0.5 size-5 shrink-0 text-red-600 dark:text-red-400" />
            ) : (
              <CheckCircle2 className="mt-0.5 size-5 shrink-0 text-green-600 dark:text-green-400" />
            )}
            <div>
              <p className="font-medium">
                {isSpam
                  ? "Este email ha sido clasificado como spam"
                  : "Este email parece ser legítimo"}
              </p>
              <p className="mt-1 text-sm opacity-80">
                {isSpam
                  ? "El modelo ML detectó patrones característicos de correo no deseado o malicioso"
                  : "El modelo ML no encontró indicadores significativos de spam"}
              </p>
            </div>
          </div>
        </div>

        {/* Patrones detectados */}
        {details?.detected_patterns &&
          Array.isArray(details.detected_patterns) &&
          details.detected_patterns.length > 0 && (
            <>
              <Separator />
              <div>
                <h4 className="mb-2 font-medium">Patrones Detectados</h4>
                <div className="space-y-2">
                  {details.detected_patterns.map((pattern: string, index: number) => (
                    <div
                      key={index}
                      className="flex items-start gap-2 rounded-md bg-white/50 p-2 text-sm dark:bg-gray-900/30"
                    >
                      <AlertCircle className="mt-0.5 size-4 shrink-0 text-orange-500" />
                      <span>{pattern}</span>
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

        {/* Vista previa del email */}
        {email_preview && (
          <>
            <Separator />
            <div>
              <h4 className="mb-2 font-medium">Vista Previa</h4>
              <div className="rounded-md bg-white/50 p-3 text-sm font-mono dark:bg-gray-900/30">
                <p className="line-clamp-3 text-xs opacity-70">
                  {email_preview}...
                </p>
              </div>
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
