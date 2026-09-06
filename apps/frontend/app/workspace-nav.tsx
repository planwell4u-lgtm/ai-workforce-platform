"use client";

/* eslint-disable @next/next/no-html-link-for-pages */

import { usePathname } from "next/navigation";

const links = [
  ["Support", "/support"],
  ["Sales", "/sales"],
  ["Front Desk", "/front-desk-admin"],
] as const;

export function WorkspaceNav() {
  const pathname = usePathname();
  if (pathname === "/") return null;

  return (
    <nav className="workspace-nav" aria-label="Planwell navigation">
      <a className="workspace-nav-brand" href="/">PLANWELL</a>
      <div className="workspace-nav-links">
        <a href="/">Home</a>
        {links.map(([label, href]) => (
          <a key={href} href={href} aria-current={pathname === href ? "page" : undefined}>{label}</a>
        ))}
      </div>
    </nav>
  );
}
