"use client";

import { createAuth0Client, type Auth0Client } from "@auth0/auth0-spa-js";
import { useEffect, useState } from "react";
import { loadRuntimeConfig } from "../runtime-config";
import "./front-desk.css";

type Destination = {
  destination_ref: string;
  route_purpose: "support" | "human_support" | "human_sales";
  destination_type: "support_worker" | "human_support_route" | "human_sales_route";
  channel_scope: string[];
  public_display: string;
  lifecycle_state: "draft" | "validated" | "active" | "suspended" | "withdrawn";
  configuration_version: number;
  health_state: "healthy" | "unknown";
  health_expires_at: string | null;
};

type HumanSalesRequest = {
  routing_request_ref: string;
  outcome: "handoff_requested";
  public_message: string;
  review_state: "new" | "reviewed" | "closed";
};

export default function FrontDeskAdminPage() {
  const [auth, setAuth] = useState<Auth0Client>();
  const [signedIn, setSignedIn] = useState(false);
  const [adminAccess, setAdminAccess] = useState(false);
  const [auth0Audience, setAuth0Audience] = useState("");
  const [apiBaseUrl, setApiBaseUrl] = useState("http://localhost:8080");
  const [destinations, setDestinations] = useState<Destination[] | null>(null);
  const [humanSalesRequests, setHumanSalesRequests] = useState<HumanSalesRequest[] | null>(null);
  const [notice, setNotice] = useState("Sign in with a Front Desk administrator account to manage test destinations.");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    void loadRuntimeConfig().then(async (config) => {
      const client = await createAuth0Client({
        domain: config.auth0Domain,
        clientId: config.auth0ClientId,
        cacheLocation: "localstorage",
        authorizationParams: {
          audience: config.auth0Audience,
          redirect_uri: window.location.origin + "/front-desk-admin",
          scope: "openid profile platform.front-desk.configure",
        },
      });
      if (window.location.search.includes("code=") && window.location.search.includes("state=")) {
        await client.handleRedirectCallback();
        window.history.replaceState({}, document.title, "/front-desk-admin");
      }
      setApiBaseUrl(config.apiBaseUrl);
      setAuth0Audience(config.auth0Audience);
      setAuth(client);
      setSignedIn(await client.isAuthenticated());
    }).catch(() => setNotice("Administrator sign-in could not be initialized."));
  }, []);

  useEffect(() => {
    if (auth && signedIn) void loadDestinations();
  }, [auth, signedIn]);

  async function getAdminToken() {
    if (!auth) throw new Error("auth_not_ready");
    return auth.getTokenSilently({
      authorizationParams: {
        audience: auth0Audience,
        redirect_uri: window.location.origin + "/front-desk-admin",
        scope: "openid profile platform.front-desk.configure",
      },
    });
  }

  async function loadDestinations() {
    if (!auth || !signedIn) return;
    setBusy(true);
    try {
      const token = await getAdminToken();
      const [destinationResponse, requestResponse] = await Promise.all([
        fetch(`${apiBaseUrl}/v1/front-desk/destinations`, { headers: { Authorization: `Bearer ${token}` } }),
        fetch(`${apiBaseUrl}/v1/front-desk/human-sales-requests`, { headers: { Authorization: `Bearer ${token}` } }),
      ]);
      const [destinationResult, requestResult] = await Promise.all([
        destinationResponse.json(), requestResponse.json(),
      ]);
      if (destinationResponse.status === 403 || requestResponse.status === 403) {
        setDestinations(null);
        setHumanSalesRequests(null);
        setAdminAccess(false);
        setNotice("You are signed in, but this account does not have Front Desk administrator access. Return to Support or sign in with an administrator account.");
        return;
      }
      if (!destinationResponse.ok || !requestResponse.ok || !Array.isArray(destinationResult.destinations) || !Array.isArray(requestResult.requests)) throw new Error("front_desk_list_failed");
      setDestinations(destinationResult.destinations as Destination[]);
      setHumanSalesRequests(requestResult.requests as HumanSalesRequest[]);
      setAdminAccess(true);
      setNotice(destinationResult.destinations.length ? "Test-only destinations loaded." : "No test-only destinations yet.");
    } catch {
      setDestinations(null);
      setHumanSalesRequests(null);
      setAdminAccess(false);
      setNotice("Destination settings could not be reached.");
    } finally {
      setBusy(false);
    }
  }

  function signInForAdministration() {
    void auth?.loginWithRedirect({
      authorizationParams: {
        audience: auth0Audience,
        scope: "openid profile platform.front-desk.configure",
      },
    });
  }

  async function createDraft(
    routePurpose: "support" | "human_support" | "human_sales",
    destinationType: "support_worker" | "human_support_route" | "human_sales_route",
  ) {
    if (!auth) return;
    setBusy(true);
    try {
      const token = await getAdminToken();
      const response = await fetch(`${apiBaseUrl}/v1/front-desk/destinations`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify({ route_purpose: routePurpose, destination_type: destinationType, channel_scope: ["web_chat"] }),
      });
      if (!response.ok) throw new Error("create_failed");
      setNotice(`${routePurpose === "support" ? "Support" : routePurpose === "human_sales" ? "Human Sales" : "Human Support"} route draft created. Validate it before activation.`);
      await loadDestinations();
    } catch {
      setNotice(`The ${routePurpose === "support" ? "Support" : routePurpose === "human_sales" ? "Human Sales" : "Human Support"} route draft could not be created.`);
    } finally {
      setBusy(false);
    }
  }

  async function transition(destination: Destination, operation: "validate" | "activate" | "renew" | "suspend" | "withdraw") {
    if (!auth) return;
    setBusy(true);
    try {
      const token = await getAdminToken();
      const response = await fetch(`${apiBaseUrl}/v1/front-desk/destinations/${encodeURIComponent(destination.destination_ref)}/${operation}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify({ expected_configuration_version: destination.configuration_version }),
      });
      if (response.status === 409) {
        setNotice("This destination changed. Reload it before taking another action.");
        await loadDestinations();
        return;
      }
      if (!response.ok) throw new Error("transition_failed");
      setNotice(`Destination ${operation}d. No external handoff or provider action was performed.`);
      await loadDestinations();
    } catch {
      setNotice("The destination change could not be confirmed.");
    } finally {
      setBusy(false);
    }
  }

  async function updateRequest(request: HumanSalesRequest, operation: "review" | "close") {
    if (!auth) return;
    setBusy(true);
    try {
      const token = await getAdminToken();
      const response = await fetch(`${apiBaseUrl}/v1/front-desk/human-sales-requests/${encodeURIComponent(request.routing_request_ref)}/${operation}`, {
        method: "POST", headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) throw new Error("review_failed");
      setNotice(`Human Sales request ${operation === "review" ? "marked reviewed" : "closed"}. No external action was performed.`);
      await loadDestinations();
    } catch {
      setNotice("The Human Sales request change could not be confirmed.");
    } finally {
      setBusy(false);
    }
  }

  return <main><section className="chat-shell admin-shell"><header><p>PLANWELL</p><h1>Front Desk routes</h1><span>Test-only setup</span>{signedIn && <button onClick={() => void loadDestinations()} disabled={busy}>{busy ? "Loading…" : "Refresh"}</button>}</header><div className="notice">{notice}<p><button onClick={signInForAdministration} disabled={!auth}>Sign in{signedIn ? " again" : ""} as Front Desk administrator</button></p></div>{signedIn && adminAccess && <div className="messages"><h2>Recorded Human Sales requests</h2>{humanSalesRequests?.length ? humanSalesRequests.map((request) => <div className="support" key={request.routing_request_ref}><small>Recorded · {request.outcome} · {request.review_state}</small><p>{request.public_message}</p><p>Request reference: {request.routing_request_ref}</p>{request.review_state === "new" && <button onClick={() => void updateRequest(request, "review")} disabled={busy}>Mark reviewed</button>}{request.review_state === "reviewed" && <button onClick={() => void updateRequest(request, "close")} disabled={busy}>Close request</button>}</div>) : humanSalesRequests && <p>No Human Sales requests have been recorded.</p>}<p><button onClick={() => void createDraft("support", "support_worker")} disabled={busy}>Create Support route draft</button></p><p><button className="secondary" onClick={() => void createDraft("human_support", "human_support_route")} disabled={busy}>Create Human Support route draft</button></p><p><button className="secondary" onClick={() => void createDraft("human_sales", "human_sales_route")} disabled={busy}>Create Human Sales route draft</button></p>{destinations?.map((destination) => <div className="support" key={destination.destination_ref}><small>{destination.public_display} · {destination.lifecycle_state} · version {destination.configuration_version}</small><p>Web chat only. Health: {destination.health_state}{destination.health_expires_at ? ` until ${new Date(destination.health_expires_at).toLocaleTimeString()}` : ""}.</p>{destination.lifecycle_state === "draft" && <button disabled={busy} onClick={() => void transition(destination, "validate")}>Validate</button>}{destination.lifecycle_state === "validated" && <button disabled={busy} onClick={() => void transition(destination, "activate")}>Activate</button>}{destination.lifecycle_state === "active" && <><button disabled={busy} onClick={() => void transition(destination, "renew")}>Renew health</button><button className="secondary" disabled={busy} onClick={() => void transition(destination, "suspend")}>Suspend</button><button className="secondary" disabled={busy} onClick={() => void transition(destination, "withdraw")}>Withdraw</button></>}{destination.lifecycle_state === "suspended" && <button disabled={busy} onClick={() => void transition(destination, "withdraw")}>Withdraw</button>}</div>)}{destinations?.length === 0 && <p>Create a draft to begin. Activation only affects the synthetic Front Desk route check.</p>}</div>}</section></main>;
}
