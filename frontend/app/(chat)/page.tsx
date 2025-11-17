import { auth } from "@/app/(auth)/auth";
import { RecentIncidents } from "@/components/dashboard/recent-incidents";
import { SecurityCharts } from "@/components/dashboard/security-charts";
import { DashboardStats } from "@/components/dashboard/stats";
import { ThreatAlerts } from "@/components/dashboard/threat-alerts";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await auth();

  if (!session) {
    redirect("/api/auth/guest");
  }

  return (
    <div className="flex h-dvh flex-col bg-background">
      <header className="sticky top-0 z-10 flex items-center justify-between border-b bg-background px-4 py-3">
        <div>
          <h1 className="text-2xl font-bold">Panel de Ciberseguridad</h1>
          <p className="text-muted-foreground text-sm">
            Monitoreo y prevención de amenazas con IA
          </p>
        </div>
      </header>

      <main className="flex-1 overflow-auto p-4">
        <div className="mx-auto max-w-7xl space-y-6">
          {/* Estadísticas principales */}
          <DashboardStats />

          {/* Alertas de amenazas activas */}
          <ThreatAlerts />

          <div className="grid gap-6 lg:grid-cols-2">
            {/* Gráficas de seguridad */}
            <SecurityCharts />

            {/* Incidentes recientes */}
            <RecentIncidents />
          </div>
        </div>
      </main>
    </div>
  );
}
