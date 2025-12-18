import Link from "next/link";
import { Home, Users2, List } from "lucide-react";
import Image from "next/image";

import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { logout } from "@/components/actions/logout-action";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen">
      <aside className="fixed inset-y-0 left-0 z-10 w-16 flex flex-col border-r bg-background p-4">
        <div className="flex flex-col items-center gap-8">
          <Link
            href="/"
            className="flex items-center justify-center rounded-full"
          >
            <Image
              src="/images/vinta.png"
              alt="Vinta"
              width={64}
              height={64}
              className="object-cover transition-transform duration-200 hover:scale-105"
            />
          </Link>
          <Link
            href="/dashboard"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
          >
            <List className="h-5 w-5" />
          </Link>
          <Link
            href="/customers"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
          >
            <Users2 className="h-5 w-5" />
          </Link>
        </div>
      </aside>
      <main className="ml-16 flex-1 min-w-0 relative">
        {children}
      </main>
    </div>
  );
}
