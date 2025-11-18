import { AppSidebar } from "@/components/app-sidebar";
import { DataStreamProvider } from "@/components/data-stream-provider";
import { LayoutHeader } from "@/components/layout-header";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import Script from "next/script";
import { auth } from "../(auth)/auth";

export const experimental_ppr = true;

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();

  return (
    <>
      <Script
        src="https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js"
        strategy="beforeInteractive"
      />
      <DataStreamProvider>
        <SidebarProvider defaultOpen={true}>
          <AppSidebar user={session?.user} />
          <SidebarInset className="flex h-dvh flex-col overflow-hidden">
            <LayoutHeader />
            {children}
          </SidebarInset>
        </SidebarProvider>
      </DataStreamProvider>
    </>
  );
}
