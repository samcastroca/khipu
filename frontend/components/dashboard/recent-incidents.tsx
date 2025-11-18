"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Clock } from "lucide-react";

interface Incident {
  id: string;
  title: string;
  category: string;
  status: "resolved" | "investigating" | "open";
  timestamp: string;
}

const statusColors = {
  resolved: "text-green-500",
  investigating: "text-yellow-500",
  open: "text-red-500",
};

const statusLabels = {
  resolved: "Resuelto",
  investigating: "Investigando",
  open: "Abierto",
};

export function RecentIncidents() {
  const incidents: Incident[] = [
    {
      id: "1",
      title: "Intento de acceso no autorizado",
      category: "Intrusión",
      status: "investigating",
      timestamp: "Hace 30 min",
    },
    {
      id: "2",
      title: "Correo de phishing bloqueado",
      category: "Ing. Social",
      status: "resolved",
      timestamp: "Hace 2 horas",
    },
    {
      id: "3",
      title: "Descarga de malware prevenida",
      category: "Malware",
      status: "resolved",
      timestamp: "Hace 4 horas",
    },
    {
      id: "4",
      title: "Comportamiento anómalo detectado",
      category: "Anomalía",
      status: "open",
      timestamp: "Hace 6 horas",
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Clock className="size-5" />
          Incidentes Recientes
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {incidents.map((incident) => (
            <div
              key={incident.id}
              className="flex items-start justify-between rounded-lg border p-3"
            >
              <div className="flex-1">
                <p className="font-medium text-sm">{incident.title}</p>
                <div className="mt-1 flex items-center gap-2">
                  <span className="rounded bg-muted px-2 py-0.5 text-xs">
                    {incident.category}
                  </span>
                  <span
                    className={`text-xs font-medium ${statusColors[incident.status]}`}
                  >
                    {statusLabels[incident.status]}
                  </span>
                </div>
              </div>
              <p className="text-muted-foreground text-xs">
                {incident.timestamp}
              </p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
