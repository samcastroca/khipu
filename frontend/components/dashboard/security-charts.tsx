"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BarChart3 } from "lucide-react";

export function SecurityCharts() {
  // Datos de ejemplo para las barras
  const data = [
    { day: "Lun", threats: 12 },
    { day: "Mar", threats: 19 },
    { day: "Mié", threats: 8 },
    { day: "Jue", threats: 15 },
    { day: "Vie", threats: 24 },
    { day: "Sáb", threats: 6 },
    { day: "Dom", threats: 4 },
  ];

  const maxThreats = Math.max(...data.map((d) => d.threats));

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BarChart3 className="size-5" />
          Amenazas por Día
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex h-[200px] items-end justify-between gap-2">
          {data.map((item) => (
            <div key={item.day} className="flex flex-1 flex-col items-center gap-2">
              <div
                className="w-full rounded-t bg-primary transition-all hover:bg-primary/80"
                style={{
                  height: `${(item.threats / maxThreats) * 100}%`,
                }}
              />
              <div className="text-center">
                <p className="font-medium text-xs">{item.threats}</p>
                <p className="text-muted-foreground text-xs">{item.day}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
