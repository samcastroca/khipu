import { auth } from "@/app/(auth)/auth";
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
    <div className="flex h-[calc(100dvh-3.25rem)] flex-col bg-background">
      <div className="border-b bg-background px-4 py-3">
        <h1 className="text-2xl font-bold">Panel de Ciberseguridad</h1>
        <p className="text-muted-foreground text-sm">
          Monitoreo y prevención de amenazas con IA
        </p>
      </div>

      <main className="flex-1 overflow-hidden p-4">
        <div className="mx-auto h-full max-w-7xl space-y-6 overflow-y-auto">
          <DashboardStats />

          <ThreatAlerts />

          <SecurityCharts />

        </div>
      </main>
    </div>
  );
}
