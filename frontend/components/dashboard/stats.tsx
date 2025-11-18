"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, AlertTriangle, Shield, Users } from "lucide-react";

export function DashboardStats() {
  const stats = [
    {
      title: "Amenazas Detectadas",
      value: "47",
      change: "+12% vs ayer",
      icon: AlertTriangle,
      trend: "up",
      color: "text-red-500",
    },
    {
      title: "Sistemas Protegidos",
      value: "156",
      change: "100% operativos",
      icon: Shield,
      trend: "stable",
      color: "text-green-500",
    },
    {
      title: "Eventos Analizados",
      value: "2,847",
      change: "+8% esta semana",
      icon: Activity,
      trend: "up",
      color: "text-blue-500",
    },
    {
      title: "Usuarios Monitoreados",
      value: "1,234",
      change: "En 5 países",
      icon: Users,
      trend: "stable",
      color: "text-purple-500",
    },
  ];

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => (
        <Card key={stat.title}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="font-medium text-sm">{stat.title}</CardTitle>
            <stat.icon className={`size-4 ${stat.color}`} />
          </CardHeader>
          <CardContent>
            <div className="font-bold text-2xl">{stat.value}</div>
            <p className="text-muted-foreground text-xs">{stat.change}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
