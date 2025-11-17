"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import {
    AlertCircle,
    AlertTriangle,
    CheckCircle,
    CheckCircle2,
    Copy,
    FileWarning,
    Mail,
    ShieldAlert,
    ShieldCheck,
    User,
} from "lucide-react";
import { useState } from "react";

type ThreatType =
  | "phishing"
  | "malware"
  | "intrusion"
  | "social_engineering"
  | "anomaly"
  | "safe";

type RiskLevel = "critical" | "high" | "medium" | "low" | "safe";

interface SuspiciousIndicator {
  category: string;
  finding: string;
  significance: "high" | "medium" | "low";
}

interface ThreatAnalysisProps {
  threatType: ThreatType;
  riskLevel: RiskLevel;
  summary: string;
  evidence: string[];
  recommendations: string[];
  suspiciousIndicators?: SuspiciousIndicator[];
  details?: {
    sender?: string;
    subject?: string;
    url?: string;
    fileName?: string;
    ipAddress?: string;
    domain?: string;
    registrationDate?: string;
    sslCertificate?: string;
  };
  affectedSystems?: string[];
}

const threatTypeConfig: Record<
  ThreatType,
  { label: string; icon: typeof AlertTriangle; color: string }
> = {
  phishing: { label: "Phishing", icon: Mail, color: "text-red-500" },
  malware: { label: "Malware", icon: FileWarning, color: "text-orange-500" },
  intrusion: { label: "Intrusión", icon: AlertTriangle, color: "text-red-600" },
  social_engineering: {
    label: "Ingeniería Social",
    icon: User,
    color: "text-yellow-600",
  },
  anomaly: { label: "Anomalía", icon: AlertCircle, color: "text-blue-500" },
  safe: { label: "Seguro", icon: CheckCircle, color: "text-green-500" },
};

const riskLevelConfig: Record<
  RiskLevel,
  { label: string; description: string; className: string; color: string }
> = {
  critical: {
    label: "Múltiples Indicadores Graves",
    description: "Se encontraron varios indicadores serios",
    className: "bg-red-100 text-red-900 dark:bg-red-950 dark:text-red-100",
    color: "text-red-600 dark:text-red-400",
  },
  high: {
    label: "Indicadores Serios",
    description: "Presencia de señales preocupantes",
    className: "bg-orange-100 text-orange-900 dark:bg-orange-950 dark:text-orange-100",
    color: "text-orange-600 dark:text-orange-400",
  },
  medium: {
    label: "Algunos Indicadores",
    description: "Elementos que requieren atención",
    className: "bg-yellow-100 text-yellow-900 dark:bg-yellow-950 dark:text-yellow-100",
    color: "text-yellow-600 dark:text-yellow-400",
  },
  low: {
    label: "Pocos Indicadores",
    description: "Señales menores detectadas",
    className: "bg-blue-100 text-blue-900 dark:bg-blue-950 dark:text-blue-100",
    color: "text-blue-600 dark:text-blue-400",
  },
  safe: {
    label: "Sin Indicadores",
    description: "No se detectaron señales de amenaza",
    className: "bg-green-100 text-green-900 dark:bg-green-950 dark:text-green-100",
    color: "text-green-600 dark:text-green-400",
  },
};

export function ThreatAnalysisDisplay({
  threatType,
  riskLevel,
  summary,
  evidence = [],
  recommendations = [],
  suspiciousIndicators = [],
  details,
  affectedSystems = [],
}: ThreatAnalysisProps) {
  const [copied, setCopied] = useState(false);
  const threatConfig = threatTypeConfig[threatType] || threatTypeConfig.anomaly;
  const riskConfig = riskLevelConfig[riskLevel] || riskLevelConfig.medium;
  const ThreatIcon = threatConfig.icon;

  const handleCopyReport = () => {
    const report = `
ANÁLISIS DE AMENAZA

Tipo: ${threatConfig.label}
Nivel de Indicadores: ${riskConfig.label}

RESUMEN:
${summary}

EVIDENCIAS ENCONTRADAS (${evidence.length}):
${evidence.map((e, i) => `${i + 1}. ${e}`).join("\n")}

${suspiciousIndicators && suspiciousIndicators.length > 0 ? `INDICADORES SOSPECHOSOS:\n${suspiciousIndicators.map((ind, i) => `${i + 1}. [${ind.significance.toUpperCase()}] ${ind.category}: ${ind.finding}`).join("\n")}\n\n` : ""}RECOMENDACIONES PARA VERIFICACIÓN:
${recommendations.map((r, i) => `${i + 1}. ${r}`).join("\n")}
${details && Object.values(details).some(v => v) ? `\n\nDETALLES TÉCNICOS:\n${Object.entries(details).filter(([_, v]) => v).map(([k, v]) => `${k}: ${v}`).join("\n")}` : ""}
    `.trim();

    navigator.clipboard.writeText(report);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getRiskIcon = () => {
    if (riskLevel === "safe") return <ShieldCheck className="size-4" />;
    if (riskLevel === "critical" || riskLevel === "high") return <ShieldAlert className="size-4" />;
    return <AlertCircle className="size-4" />;
  };

  return (
    <Card className="overflow-hidden">
      <CardHeader className="border-b space-y-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-start gap-3 flex-1">
            <div className={`mt-1 ${threatConfig.color}`}>
              <ThreatIcon className="size-6" />
            </div>
            <div className="space-y-3 flex-1">
              <div className="space-y-2">
                <div className="flex items-center gap-2 flex-wrap">
                  <h3 className="font-semibold text-lg">{threatConfig.label}</h3>
                  <Badge className={riskConfig.className}>
                    {getRiskIcon()}
                    <span className="ml-1">{riskConfig.label}</span>
                  </Badge>
                </div>
                <p className="text-xs text-muted-foreground">{riskConfig.description}</p>
              </div>
              <p className="text-sm leading-relaxed">{summary}</p>
            </div>
          </div>
          
          <Button
            size="icon"
            variant="ghost"
            className="size-8 shrink-0"
            onClick={handleCopyReport}
            title={copied ? "Copiado" : "Copiar análisis"}
          >
            {copied ? <CheckCircle2 className="size-4" /> : <Copy className="size-4" />}
          </Button>
        </div>
      </CardHeader>

      <CardContent className="space-y-6 pt-6">
        {/* Detalles Técnicos */}
        {details && Object.values(details).some(v => v) && (
          <div className="space-y-3">
            <h4 className="font-medium text-sm flex items-center gap-2">
              <FileWarning className="size-4" />
              Información Analizada
            </h4>
            <div className="grid gap-3 text-sm bg-muted/30 rounded-lg p-4">
              {details.sender && (
                <div className="grid grid-cols-[120px_1fr] gap-2">
                  <span className="text-muted-foreground font-medium">Remitente:</span>
                  <span className="font-mono text-xs break-all">{details.sender}</span>
                </div>
              )}
              {details.subject && (
                <div className="grid grid-cols-[120px_1fr] gap-2">
                  <span className="text-muted-foreground font-medium">Asunto:</span>
                  <span className="wrap-break-word">{details.subject}</span>
                </div>
              )}
              {details.url && (
                <div className="grid grid-cols-[120px_1fr] gap-2">
                  <span className="text-muted-foreground font-medium">URL:</span>
                  <span className="font-mono text-xs break-all">{details.url}</span>
                </div>
              )}
              {details.domain && (
                <div className="grid grid-cols-[120px_1fr] gap-2">
                  <span className="text-muted-foreground font-medium">Dominio:</span>
                  <span className="font-mono text-xs">{details.domain}</span>
                </div>
              )}
              {details.registrationDate && (
                <div className="grid grid-cols-[120px_1fr] gap-2">
                  <span className="text-muted-foreground font-medium">Registro:</span>
                  <span className="text-xs">{details.registrationDate}</span>
                </div>
              )}
              {details.fileName && (
                <div className="grid grid-cols-[120px_1fr] gap-2">
                  <span className="text-muted-foreground font-medium">Archivo:</span>
                  <span className="font-mono text-xs">{details.fileName}</span>
                </div>
              )}
              {details.ipAddress && (
                <div className="grid grid-cols-[120px_1fr] gap-2">
                  <span className="text-muted-foreground font-medium">Dirección IP:</span>
                  <span className="font-mono text-xs">{details.ipAddress}</span>
                </div>
              )}
              {details.sslCertificate && (
                <div className="grid grid-cols-[120px_1fr] gap-2">
                  <span className="text-muted-foreground font-medium">SSL:</span>
                  <span className="text-xs">{details.sslCertificate}</span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Indicadores Sospechosos */}
        {suspiciousIndicators && suspiciousIndicators.length > 0 && (
          <div className="space-y-3">
            <h4 className="font-medium text-sm flex items-center gap-2">
              <AlertCircle className="size-4" />
              Indicadores Detectados ({suspiciousIndicators.length})
            </h4>
            <div className="space-y-2">
              {suspiciousIndicators.map((indicator, index) => {
                const indicatorColor =
                  indicator.significance === "high"
                    ? "border-red-500 bg-red-50 dark:bg-red-950/30"
                    : indicator.significance === "medium"
                      ? "border-yellow-500 bg-yellow-50 dark:bg-yellow-950/30"
                      : "border-blue-500 bg-blue-50 dark:bg-blue-950/30";
                return (
                  <div key={index} className={`border-l-2 ${indicatorColor} p-3 rounded-r-lg text-sm`}>
                    <div className="font-medium text-xs text-muted-foreground mb-1">
                      {indicator.category}
                    </div>
                    <div>{indicator.finding}</div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Evidencias */}
        {evidence.length > 0 && (
          <div className="space-y-3">
            <h4 className="font-medium text-sm flex items-center gap-2">
              <AlertTriangle className={`size-4 ${riskConfig.color}`} />
              Hallazgos del Análisis ({evidence.length})
            </h4>
            <ul className="space-y-2.5">
              {evidence.map((item, index) => (
                <li key={index} className="flex gap-3 text-sm items-start">
                  <span className="text-muted-foreground shrink-0 font-medium">{index + 1}.</span>
                  <span className="leading-relaxed">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Recomendaciones */}
        {recommendations.length > 0 && (
          <div className="space-y-3">
            <h4 className="font-medium text-sm flex items-center gap-2">
              <ShieldCheck className="size-4 text-blue-600 dark:text-blue-400" />
              Pasos para Verificación
            </h4>
            <div className="bg-blue-50/50 dark:bg-blue-950/20 rounded-lg p-4 border border-blue-200 dark:border-blue-900">
              <ul className="space-y-3">
                {recommendations.map((item, index) => (
                  <li key={index} className="flex gap-3 text-sm items-start">
                    <span className="text-blue-600 dark:text-blue-400 shrink-0 font-semibold">{index + 1}.</span>
                    <span className="leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {/* Sistemas Afectados */}
        {affectedSystems.length > 0 && (
          <div className="space-y-2">
            <h4 className="font-medium text-sm">Sistemas Afectados</h4>
            <div className="flex flex-wrap gap-1.5">
              {affectedSystems.map((system, index) => (
                <Badge key={index} variant="secondary" className="text-xs font-mono">
                  {system}
                </Badge>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
