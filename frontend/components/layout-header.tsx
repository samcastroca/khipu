"use client";

import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { useWindowSize } from "usehooks-ts";
import { PlusIcon } from "./icons";
import { SidebarToggle } from "./sidebar-toggle";
import { useSidebar } from "./ui/sidebar";

export function LayoutHeader() {
  const router = useRouter();
  const { open } = useSidebar();
  const { width: windowWidth } = useWindowSize();

  return (
    <header className="sticky top-0 z-10 flex items-center gap-2 border-b bg-background/95 px-2 py-1.5 backdrop-blur supports-backdrop-filter:bg-background/60 md:px-2">
      <SidebarToggle />
      {(!open || windowWidth < 768) && (
        <Button
          className="h-8 px-2 md:h-fit md:px-2"
          onClick={() => {
            router.push("/");
            router.refresh();
          }}
          variant="outline"
        >
          <PlusIcon />
          <span className="md:sr-only">Nuevo chat</span>
        </Button>
      )}
    </header>
  );
}
