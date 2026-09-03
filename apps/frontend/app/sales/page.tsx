"use client";

import { createAuth0Client, type Auth0Client } from "@auth0/auth0-spa-js";
import { FormEvent, useEffect, useState } from "react";
import { loadRuntimeConfig } from "../runtime-config";
import "./sales.css";

type Message = { sender: "you" | "sales"; text: string };

export default function SalesPage() {
  const [auth, setAuth] = useState<Auth0Client>();
  const [signedIn, setSignedIn] = useState(false);
  const [audience, setAudience] = useState("");
  const [apiBaseUrl, setApiBaseUrl] = useState("http://localhost:8080");
  const [question, setQuestion] = useState("");
  const [conversationRef, setConversationRef] = useState<string | null>(null);
  const [routeOfferRef, setRouteOfferRef] = useState<string | null>(null);
  const [routeNotice, setRouteNotice] = useState("");
  const [routing, setRouting] = useState(false);
  const [leadName, setLeadName] = useState("");
  const [leadEmail, setLeadEmail] = useState("");
  const [leadConsent, setLeadConsent] = useState(false);
  const [leadIdempotencyRef, setLeadIdempotencyRef] = useState<string | null>(null);
  const [leadNotice, setLeadNotice] = useState("");
  const [creatingLead, setCreatingLead] = useState(false);
  const [messages, setMessages] = useState<Message[]>([{ sender: "sales", text: "Hello. I can help with approved fictional catalog information." }]);

  useEffect(() => {
    void loadRuntimeConfig().then(async (config) => {
      const client = await createAuth0Client({ domain: config.auth0Domain, clientId: config.auth0ClientId, cacheLocation: "localstorage", authorizationParams: { audience: config.auth0Audience, redirect_uri: `${window.location.origin}/sales`, scope: "openid profile agent.context.read integration.crm.lead.create" } });
      if (window.location.search.includes("code=") && window.location.search.includes("state=")) {
        await client.handleRedirectCallback();
        window.history.replaceState({}, document.title, "/sales");
      }
      setAudience(config.auth0Audience); setApiBaseUrl(config.apiBaseUrl); setAuth(client); setSignedIn(await client.isAuthenticated());
    });
  }, []);

  async function send(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!auth || !signedIn || !question.trim()) return;
    const text = question.trim(); setQuestion(""); setMessages((items) => [...items, { sender: "you", text }]);
    try {
      const token = await auth.getTokenSilently({ authorizationParams: { audience, scope: "openid profile agent.context.read" } });
      const response = await fetch(`${apiBaseUrl}/v1/sales-answers`, { method: "POST", headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" }, body: JSON.stringify({ agent_ref: "sales-worker", session_ref: "sales-demo", question: text }) });
      const result = await response.json();
      if (typeof result.conversation_ref === "string") setConversationRef(result.conversation_ref);
      if (result.human_sales_recommended === true) setRouteNotice("Human Sales may be available for this request. This does not collect contact details or confirm availability.");
      setMessages((items) => [...items, { sender: "sales", text: result.answer ?? "I could not reach the secure sales service. Please try again." }]);
    } catch { setMessages((items) => [...items, { sender: "sales", text: "I could not reach the secure sales service. Please try again." }]); }
  }

  async function routeToHumanSales(action: "offer" | "request") {
    if (!auth || !conversationRef || (action === "request" && !routeOfferRef)) return;
    setRouting(true);
    try {
      const token = await auth.getTokenSilently({ authorizationParams: { audience, scope: "openid profile agent.context.read" } });
      const body = action === "offer"
        ? { conversation_ref: conversationRef, route_purpose: "human_sales", event_ref: crypto.randomUUID(), route_action: "offer" }
        : { conversation_ref: conversationRef, route_purpose: "human_sales", event_ref: crypto.randomUUID(), route_action: "request", offer_ref: routeOfferRef };
      const response = await fetch(`${apiBaseUrl}/v1/conversation-routing-requests`, { method: "POST", headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const result = await response.json();
      if (!response.ok) throw new Error("route_failed");
      setRouteNotice(typeof result.public_message === "string" ? result.public_message : "Human Sales is not available through this channel right now.");
      setRouteOfferRef(result.outcome === "handoff_offered" && typeof result.routing_request_ref === "string" ? result.routing_request_ref : null);
    } catch { setRouteNotice("We could not confirm Human Sales availability. Please try again."); setRouteOfferRef(null); }
    finally { setRouting(false); }
  }

  async function createLead() {
    if (!auth || !signedIn || !leadName.trim() || !leadEmail.trim() || !leadConsent) return;
    setCreatingLead(true); setLeadNotice("");
    const idempotencyRef = leadIdempotencyRef ?? crypto.randomUUID();
    if (!leadIdempotencyRef) setLeadIdempotencyRef(idempotencyRef);
    try {
      const token = await auth.getTokenSilently({ authorizationParams: { audience, scope: "openid profile agent.context.read integration.crm.lead.create" } });
      const response = await fetch(`${apiBaseUrl}/v1/sales-leads`, { method: "POST", headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" }, body: JSON.stringify({ name: leadName.trim(), email: leadEmail.trim(), consent: true, idempotency_ref: idempotencyRef }) });
      const result = await response.json();
      if (!response.ok || result.outcome !== "succeeded") throw new Error("lead_failed");
      setLeadNotice("Your contact request was sent to Sales."); setLeadName(""); setLeadEmail(""); setLeadConsent(false); setLeadIdempotencyRef(null);
    } catch { setLeadNotice("We could not submit your contact request. Please try again later."); }
    finally { setCreatingLead(false); }
  }

  return <main><section className="chat-shell"><header><p>PLANWELL</p><h1>Sales chat</h1><span>Test-only catalog</span>{signedIn ? <button onClick={() => auth?.logout({ logoutParams: { returnTo: `${window.location.origin}/sales` } })}>Sign out</button> : <button onClick={() => auth?.loginWithRedirect()}>Sign in</button>}</header><div className="notice">Fictional catalog only. Do not share payment or contact details.</div><div className="messages">{messages.map((message, index) => <div className={message.sender === "you" ? "you" : "support"} key={index}><small>{message.sender === "you" ? "You" : "Planwell Sales"}</small><p>{message.text}</p></div>)}</div>{conversationRef && routeNotice && <div className="notice"><p>{routeNotice}</p>{routeOfferRef ? <button disabled={routing} onClick={() => void routeToHumanSales("request")}>{routing ? "Checking…" : "Request Human Sales route"}</button> : <button className="secondary" disabled={routing} onClick={() => void routeToHumanSales("offer")}>{routing ? "Checking…" : "Check Human Sales availability"}</button>}</div>}<form onSubmit={send}><input value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask about the fictional catalog" aria-label="Sales question"/><button disabled={!signedIn}>Send</button></form><section className="notice"><h2>Contact Sales</h2><p>Only use this form if you want Planwell to create a lead in HubSpot.</p><input value={leadName} onChange={(event) => { setLeadName(event.target.value); setLeadIdempotencyRef(null); }} placeholder="Full name" aria-label="Full name"/><input value={leadEmail} onChange={(event) => { setLeadEmail(event.target.value); setLeadIdempotencyRef(null); }} placeholder="Email" type="email" aria-label="Email"/><label><input type="checkbox" checked={leadConsent} onChange={(event) => setLeadConsent(event.target.checked)}/> I consent to Planwell creating a Sales lead in HubSpot.</label><button type="button" onClick={() => void createLead()} disabled={creatingLead || !signedIn || !leadName.trim() || !leadEmail.trim() || !leadConsent}>{creatingLead ? "Submitting…" : "Create HubSpot lead"}</button>{leadNotice && <p>{leadNotice}</p>}</section></section></main>;
}
