"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertCircle, FileWarning, Link2, Mail } from "lucide-react";

type ThreatLevel = "critical" | "high" | "medium" | "low";

interface Threat {
  id: string;
  type: string;
  description: string;
  level: ThreatLevel;
  timestamp: string;
  icon: typeof AlertCircle;
}

const threatLevelColors: Record<ThreatLevel, string> = {
  critical: "bg-red-500 text-white",
  high: "bg-orange-500 text-white",
  medium: "bg-yellow-500 text-black",
  low: "bg-blue-500 text-white",
};

export function ThreatAlerts() {
  const threats: Threat[] = [
    {
      id: "1",
      type: "Phishing",
      description: "Intento de phishing detectado en correo corporativo",
      level: "critical",
      timestamp: "Hace 5 minutos",
      icon: Mail,
    },
    {
      id: "2",
      type: "URL Maliciosa",
      description: "Click en enlace sospechoso desde red interna",
      level: "high",
      timestamp: "Hace 15 minutos",
      icon: Link2,
    },
    {
      id: "3",
      type: "Archivo Sospechoso",
      description: "Descarga de archivo con firma desconocida",
      level: "medium",
      timestamp: "Hace 1 hora",
      icon: FileWarning,
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AlertCircle className="size-5 text-red-500" />
          Alertas Activas
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {threats.map((threat) => (
            <div
              key={threat.id}
              className="flex items-start gap-3 rounded-lg border p-3"
            >
              <threat.icon className="mt-0.5 size-5 text-muted-foreground" />
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <p className="font-medium text-sm">{threat.type}</p>
                  <Badge className={threatLevelColors[threat.level]}>
                    {threat.level.toUpperCase()}
                  </Badge>
                </div>
                <p className="text-muted-foreground text-sm">
                  {threat.description}
                </p>
                <p className="mt-1 text-muted-foreground text-xs">
                  {threat.timestamp}
                </p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
