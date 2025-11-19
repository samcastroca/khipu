"use client";

import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { Event } from "@/lib/db/schema";
import { Activity, Link as LinkIcon, Mail, Network } from "lucide-react";

interface AlertsTableProps {
  events: Event[];
}

export function AlertsTable({ events }: AlertsTableProps) {

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "email":
        return <Mail className="h-4 w-4" />;
      case "url":
        return <LinkIcon className="h-4 w-4" />;
      case "network_access":
        return <Network className="h-4 w-4" />;
      case "suspicious_logs":
        return <Activity className="h-4 w-4" />;
      default:
        return <Network className="h-4 w-4" />;
    }
  };

  const getSeverityColor = (severity: string | null) => {
    switch (severity) {
      case "critical":
        return "destructive";
      case "high":
        return "destructive";
      case "medium":
        return "default";
      case "low":
        return "secondary";
      default:
        return "secondary";
    }
  };

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Tipo</TableHead>
            <TableHead>Severidad</TableHead>
            <TableHead>Confianza</TableHead>
            <TableHead>Fecha</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {events.length === 0 ? (
            <TableRow>
              <TableCell colSpan={4} className="text-center text-muted-foreground">
                No hay alertas registradas
              </TableCell>
            </TableRow>
          ) : (
            events.map((event) => (
              <TableRow key={event.id}>
                <TableCell>
                  <div className="flex items-center gap-2">
                    {getTypeIcon(event.type)}
                    <span className="capitalize">{event.type.replace("_", " ")}</span>
                  </div>
                </TableCell>
                <TableCell>
                  <Badge variant={getSeverityColor(event.severity)}>
                    {event.severity || "unknown"}
                  </Badge>
                </TableCell>
                <TableCell>
                  {event.confidence
                    ? `${(parseFloat(event.confidence) * 100).toFixed(2)}%`
                    : "N/A"}
                </TableCell>
                <TableCell>
                  {new Date(event.createdAt).toLocaleString("es-ES", {
                    year: "numeric",
                    month: "short",
                    day: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  );
}
