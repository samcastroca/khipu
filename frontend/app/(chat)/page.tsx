import { auth } from "@/app/(auth)/auth";
import { AlertsTable } from "@/components/alerts-table";
import { RefreshButton } from "@/components/refresh-button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getEvents, getEventStats } from "@/lib/db/queries";
import { AlertCircle, AlertTriangle, Shield } from "lucide-react";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await auth();

  if (!session) {
    redirect("/api/auth/guest");
  }

  const [events, stats] = await Promise.all([
    getEvents(100, false), // All events
    getEventStats(),
  ]);

  return (
    <div className="flex h-[calc(100dvh-3.25rem)] flex-col bg-background">
      <div className="border-b bg-background px-4 py-3">
        <h1 className="text-2xl font-bold">Dashboard de Alertas</h1>
        <p className="text-muted-foreground text-sm">
          Monitoreo de amenazas detectadas por modelos ML
        </p>
      </div>

      <main className="flex-1 overflow-hidden p-4">
        <div className="mx-auto h-full max-w-7xl space-y-6 overflow-y-auto">
          {/* Stats Cards */}
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Total Eventos</CardTitle>
                <Shield className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total}</div>
                <p className="text-xs text-muted-foreground">
                  Eventos procesados
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Amenazas</CardTitle>
                <AlertCircle className="h-4 w-4 text-amber-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.threats}</div>
                <p className="text-xs text-muted-foreground">
                  Catalogadas como amenaza
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Críticas</CardTitle>
                <AlertTriangle className="h-4 w-4 text-red-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.critical}</div>
                <p className="text-xs text-muted-foreground">
                  Severidad crítica
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Alerts Table */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>Eventos</CardTitle>
              <RefreshButton />
            </CardHeader>
            <CardContent>
              <AlertsTable events={events} />
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
}
