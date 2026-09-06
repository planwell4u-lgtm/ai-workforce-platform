"use client";

import { createAuth0Client, type Auth0Client } from "@auth0/auth0-spa-js";
import { FormEvent, useEffect, useState } from "react";
import { loadRuntimeConfig } from "../runtime-config";

type ManagedUser = { email: string | null; name: string | null; permissions: string[] };
type AccessChange = { occurred_at: string; changed_by: string; user_email: string | null; permissions: string[] };

export default function AccessManagementPage() {
  const [auth, setAuth] = useState<Auth0Client>();
  const [signedIn, setSignedIn] = useState(false);
  const [accountEmail, setAccountEmail] = useState("");
  const [audience, setAudience] = useState("");
  const [apiBaseUrl, setApiBaseUrl] = useState("");
  const [email, setEmail] = useState("");
  const [user, setUser] = useState<ManagedUser | null>(null);
  const [notice, setNotice] = useState("Sign in with the owner account to manage workspace access.");
  const [busy, setBusy] = useState(false);
  const [history, setHistory] = useState<AccessChange[] | null>(null);
  const [ownerAuthorized, setOwnerAuthorized] = useState<boolean | null>(null);

  useEffect(() => { void loadRuntimeConfig().then(async (config) => {
    const client = await createAuth0Client({ domain: config.auth0Domain, clientId: config.auth0ClientId, cacheLocation: "localstorage", authorizationParams: {
      audience: config.auth0Audience, redirect_uri: `${window.location.origin}/access-management`, scope: "openid profile email platform.owner platform.front-desk.configure",
    }});
    if (window.location.search.includes("code=") && window.location.search.includes("state=")) {
      await client.handleRedirectCallback(); window.history.replaceState({}, document.title, "/access-management");
    }
    setAuth(client); setAudience(config.auth0Audience); setApiBaseUrl(config.apiBaseUrl);
    const isAuthenticated = await client.isAuthenticated();
    setSignedIn(isAuthenticated);
    if (isAuthenticated) {
      const account = await client.getUser();
      setAccountEmail(account?.email ?? account?.name ?? "Signed-in account");
      try {
        const accessToken = await client.getTokenSilently({ authorizationParams: { audience: config.auth0Audience, scope: "openid profile email platform.owner platform.front-desk.configure" } });
        const response = await fetch(`${config.apiBaseUrl}/v1/access-management?history=1`, { headers: { Authorization: `Bearer ${accessToken}` } });
        setOwnerAuthorized(response.ok);
        if (!response.ok) setNotice("This account is not allowed to manage workspace access.");
      } catch {
        setOwnerAuthorized(false); setNotice("This account is not allowed to manage workspace access.");
      }
    } else {
      setOwnerAuthorized(false);
    }
  }).catch(() => setNotice("Access Management could not be initialized.")); }, []);

  async function token() {
    if (!auth) throw new Error("not_ready");
    return auth.getTokenSilently({ authorizationParams: { audience, scope: "openid profile email platform.owner platform.front-desk.configure" } });
  }
  async function signIn() {
    if (!auth) return;
    await auth.loginWithRedirect({ authorizationParams: {
      audience, redirect_uri: `${window.location.origin}/access-management`, scope: "openid profile email platform.owner platform.front-desk.configure",
    }});
  }
  function signOut() {
    if (!auth) return;
    void auth.logout({ logoutParams: { returnTo: window.location.origin + "/access-management" } });
  }
  async function find(event: FormEvent) {
    event.preventDefault(); setBusy(true); setNotice("");
    try {
      const response = await fetch(`${apiBaseUrl}/v1/access-management?email=${encodeURIComponent(email.trim())}`, { headers: { Authorization: `Bearer ${await token()}` } });
      const result = await response.json();
      if (response.status === 403) throw new Error("forbidden");
      if (response.status === 404) { setUser(null); setNotice("No Auth0 user was found with that email address."); return; }
      if (!response.ok || !result.user) throw new Error("failed");
      setUser(result.user); setNotice("User found. Select the roles this person should have.");
    } catch (error) { setUser(null); setNotice(error instanceof Error && error.message === "forbidden" ? "This account is not allowed to manage access." : "The access service is temporarily unavailable."); } finally { setBusy(false); }
  }
  async function loadHistory() {
    if (!auth || !signedIn) return;
    try {
      const response = await fetch(`${apiBaseUrl}/v1/access-management?history=1`, { headers: { Authorization: `Bearer ${await token()}` } });
      const result = await response.json();
      if (!response.ok || !Array.isArray(result.changes)) throw new Error("failed");
      setHistory(result.changes as AccessChange[]);
    } catch { setNotice("Access history could not be loaded."); }
  }
  async function save(permission: string, enabled: boolean) {
    if (!user) return; setBusy(true); setNotice("");
    const permissions = enabled ? [...new Set([...user.permissions, permission])] : user.permissions.filter((item) => item !== permission);
    try {
      const response = await fetch(`${apiBaseUrl}/v1/access-management`, { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${await token()}` }, body: JSON.stringify({ email, permissions }) });
      const result = await response.json();
      if (response.status === 403) throw new Error("forbidden");
      if (response.status === 400 && result.error === "cannot_remove_last_owner") {
        setNotice("Cannot remove the last remaining Workspace Owner. At least one active owner must be preserved.");
        return;
      }
      if (!response.ok || !result.user) throw new Error("failed");
      setUser(result.user); setNotice("Access updated. The user may need to sign out and sign in again before their new role appears.");
      await loadHistory();
    } catch (error) { setNotice(error instanceof Error && error.message === "forbidden" ? "This account is not allowed to manage access." : "Access could not be updated. Nothing else was changed in this screen."); } finally { setBusy(false); }
  }
  const has = (permission: string) => Boolean(user?.permissions.includes(permission));
  return <main style={{ maxWidth: 820, margin: "36px auto", padding: 24, fontFamily: "Arial, sans-serif", color: "#102a43" }}>
    <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 16, borderBottom: "1px solid #d9e2ec", paddingBottom: 18 }}><a href="/" style={{ fontWeight: 800, color: "#007a99", textDecoration: "none" }}>PLANWELL</a><nav style={{ display: "flex", gap: 16 }}><a href="/support">Support</a><a href="/front-desk-admin">Front Desk</a></nav>{signedIn ? <span style={{ display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap", justifyContent: "end" }}><small style={{ color: "#486581" }}>{accountEmail}</small><button onClick={signOut} style={{ padding: "10px 14px", border: 0, borderRadius: 8, background: "#007a99", color: "white", fontWeight: 700 }}>Sign out</button></span> : <button onClick={() => void signIn()} disabled={!auth} style={{ padding: "10px 14px", border: 0, borderRadius: 8, background: "#007a99", color: "white", fontWeight: 700 }}>Sign in as owner</button>}</header>
    <section style={{ marginTop: 42 }}><p style={{ color: "#007a99", fontWeight: 700, letterSpacing: 1 }}>OWNER SETTINGS</p><h1>Access Management</h1>{ownerAuthorized === null ? <p>Checking workspace access…</p> : !ownerAuthorized ? <><p>This account is not allowed to manage workspace access.</p><a href="/support" style={{ color: "#007a99", fontWeight: 700 }}>Return to Support</a></> : <><p>Give an existing signed-in user access to Support, Front Desk administration, or Workspace Owner. This is limited to Planwell workspace roles.</p>
      <form onSubmit={find} style={{ display: "flex", gap: 10, marginTop: 26 }}><input type="email" required disabled={!signedIn} value={email} onChange={(event) => setEmail(event.target.value)} placeholder="User email address" style={{ flex: 1, padding: 13, border: "1px solid #9fb3c8", borderRadius: 8 }} /><button disabled={busy || !signedIn} style={{ padding: "12px 18px", border: 0, borderRadius: 8, background: "#007a99", color: "white", fontWeight: 700 }}>{busy ? "Working…" : "Find user"}</button></form>
      <p aria-live="polite" style={{ minHeight: 28, marginTop: 18, color: "#486581" }}>{notice}</p>
      {user && <section style={{ marginTop: 20, border: "1px solid #d9e2ec", borderRadius: 12, padding: 22, background: "#f8fbfd" }}><h2 style={{ marginTop: 0 }}>{user.name || "Planwell user"}</h2><p>{user.email}</p><Role label="Workspace Owner" description="Full administrative authority to manage workspace access, roles, and governance." checked={has("platform.owner")} disabled={busy} onChange={(checked) => void save("platform.owner", checked)} /><Role label="Front Desk administrator" description="Manage test-only Front Desk routing destinations." checked={has("platform.front-desk.configure")} disabled={busy} onChange={(checked) => void save("platform.front-desk.configure", checked)} /><Role label="Support" description="Use approved support chat and the voice-agent test." checked={has("agent.context.read")} disabled={busy} onChange={(checked) => void save("agent.context.read", checked)} /></section>}
      {signedIn && <section style={{ marginTop: 32, borderTop: "1px solid #d9e2ec", paddingTop: 22 }}><div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16 }}><h2 style={{ margin: 0 }}>Recent access changes</h2><button onClick={() => void loadHistory()} disabled={busy} style={{ padding: "9px 13px", border: "1px solid #9fb3c8", borderRadius: 8, background: "white", color: "#007a99", fontWeight: 700 }}>Refresh history</button></div>{history === null ? <p>Refresh to view the latest owner-managed changes.</p> : history.length === 0 ? <p>No changes have been recorded yet.</p> : <div style={{ marginTop: 16, display: "grid", gap: 10 }}>{history.map((change, index) => <article key={`${change.occurred_at}-${index}`} style={{ padding: 14, border: "1px solid #d9e2ec", borderRadius: 8 }}><strong>{change.user_email || "User"}</strong><br/><small>{new Date(change.occurred_at).toLocaleString()} · Changed by {change.changed_by}</small><br/><span>{change.permissions.length ? change.permissions.map((permission) => permission === "platform.owner" ? "Workspace Owner" : permission === "platform.front-desk.configure" ? "Front Desk administrator" : permission === "agent.context.read" ? "Support" : permission).join(", ") : "All Planwell roles removed"}</span></article>)}</div>}</section>}
    </>}</section>
  </main>;
}

function Role({ label, description, checked, disabled, onChange }: { label: string; description: string; checked: boolean; disabled: boolean; onChange: (checked: boolean) => void }) {
  return <label style={{ display: "flex", gap: 14, padding: "16px 0", borderTop: "1px solid #d9e2ec", cursor: "pointer" }}><input type="checkbox" checked={checked} disabled={disabled} onChange={(event) => onChange(event.target.checked)} style={{ width: 20, height: 20 }} /><span><strong>{label}</strong><br /><small>{description}</small></span></label>;
}
