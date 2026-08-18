"use client";

import { createAuth0Client, type Auth0Client } from "@auth0/auth0-spa-js";
import { FormEvent, useEffect, useState } from "react";
import { loadRuntimeConfig } from "./runtime-config";

type ChatMessage = { sender: "support" | "you"; text: string };
type AdminConversation = {
  conversation_ref: string;
  messages: ChatMessage[];
  status: string;
  ticket_ref: string | null;
};

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { sender: "support", text: "Hello. I can help with approved Planwell support information." },
  ]);
  const [question, setQuestion] = useState("");
  const [auth, setAuth] = useState<Auth0Client>();
  const [signedIn, setSignedIn] = useState(false);
  const [sequence, setSequence] = useState(1);
  const [sessionRef, setSessionRef] = useState(() => {
    const existing = typeof window === "undefined" ? null : window.localStorage.getItem("planwell-support-session");
    const session = existing ?? `web-chat-${crypto.randomUUID()}`;
    if (!existing && typeof window !== "undefined") window.localStorage.setItem("planwell-support-session", session);
    return session;
  });
  const [sending, setSending] = useState(false);
  const [adminConversations, setAdminConversations] = useState<AdminConversation[] | null>(null);
  const [ticketNotice, setTicketNotice] = useState("");
  const [apiBaseUrl, setApiBaseUrl] = useState("http://localhost:8080");
  useEffect(() => {
    void loadRuntimeConfig().then(async (config) => {
      const client = await createAuth0Client({
        domain: config.auth0Domain,
        clientId: config.auth0ClientId,
        authorizationParams: {
          audience: config.auth0Audience,
          redirect_uri: window.location.origin,
          scope: "openid profile agent.context.read operator.status.read integration.support-ticket.create",
        },
      });
      if (window.location.search.includes("code=") && window.location.search.includes("state=")) {
        await client.handleRedirectCallback();
        window.history.replaceState({}, document.title, window.location.pathname);
      }
      setApiBaseUrl(config.apiBaseUrl);
      setAuth(client);
      setSignedIn(await client.isAuthenticated());
    });
  }, []);
  useEffect(() => {
    if (!auth || !signedIn) return;
    async function restoreHistory() {
      try {
        const token = await auth.getTokenSilently();
        const response = await fetch(`${apiBaseUrl}/v1/support-answers?session_ref=${encodeURIComponent(sessionRef)}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const result = await response.json();
        if (!response.ok || !Array.isArray(result.messages) || result.messages.length === 0) return;
        const restored = result.messages.filter(
          (message: unknown): message is ChatMessage =>
            typeof message === "object" && message !== null &&
            (message as ChatMessage).sender !== undefined && typeof (message as ChatMessage).text === "string",
        );
        if (restored.length) {
          setMessages([{ sender: "support", text: "Hello. I can help with approved Planwell support information." }, ...restored]);
          setSequence(restored.filter((message) => message.sender === "you").length + 1);
        }
      } catch { /* The normal empty chat remains available. */ }
    }
    void restoreHistory();
  }, [apiBaseUrl, auth, sessionRef, signedIn]);
  async function send(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!question.trim() || !auth || !signedIn) return;
    const text = question.trim();
    setMessages((current) => [...current, { sender: "you", text }]);
    setQuestion("");
    setSending(true);
    try {
      const token = await auth.getTokenSilently();
      const response = await fetch(`${apiBaseUrl}/v1/support-answers`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify({ agent_ref: "support-agent", session_ref: sessionRef, event_ref: crypto.randomUUID(), sequence, question: text }),
      });
      const result = await response.json();
      setSequence((value) => value + 1);
      setMessages((current) => [...current, { sender: "support", text: result.answer ?? "I could not find an approved answer for that question." }]);
    } catch {
      setMessages((current) => [...current, { sender: "support", text: "I could not reach the secure support service. Please try again." }]);
    } finally {
      setSending(false);
    }
  }
  async function loadAdminHistory() {
    if (!auth || !signedIn) return;
    try {
      const token = await auth.getTokenSilently();
      const response = await fetch(`${apiBaseUrl}/v1/admin/conversations`, { headers: { Authorization: `Bearer ${token}` } });
      const result = await response.json();
      setAdminConversations(response.ok ? result.conversations : []);
    } catch {
      setAdminConversations([]);
    }
  }
  async function escalate(conversation: AdminConversation) {
    if (!auth) return;
    if (conversation.ticket_ref) {
      setTicketNotice(`Ticket ${conversation.ticket_ref} already created.`);
      return;
    }
    try {
      const token = await auth.getTokenSilently();
      const summary = conversation.messages.map((message) => `${message.sender}: ${message.text}`).join(" ");
      const response = await fetch(`${apiBaseUrl}/v1/support-tickets`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify({ conversation_ref: conversation.conversation_ref, idempotency_ref: conversation.conversation_ref, summary }),
      });
      const result = await response.json();
      if (response.ok && result.ticket_ref) {
        setAdminConversations((current) => current?.map((item) =>
          item.conversation_ref === conversation.conversation_ref
            ? { ...item, ticket_ref: result.ticket_ref }
            : item,
        ) ?? null);
      }
      setTicketNotice(response.ok ? `Ticket created: ${result.ticket_ref ?? "submitted"}` : "Ticket could not be created.");
    } catch { setTicketNotice("Ticket service could not be reached."); }
  }
  function ticketLabel(conversation: AdminConversation) {
    return conversation.ticket_ref
      ? `Ticket ${conversation.ticket_ref} created`
      : "Escalate to ticket";
  }
  function startNewChat() {
    const next = `web-chat-${crypto.randomUUID()}`;
    window.localStorage.setItem("planwell-support-session", next);
    setSessionRef(next);
    setSequence(1);
    setMessages([{ sender: "support", text: "Hello. I can help with approved Planwell support information." }]);
  }
  return <main><section className="chat-shell"><header><p>PLANWELL</p><h1>Support chat</h1><span>Support ready</span><button className="secondary" onClick={startNewChat}>New chat</button>{signedIn && <button className="secondary" onClick={() => void loadAdminHistory()}>Admin</button>}{signedIn ? <button onClick={() => auth?.logout({ logoutParams: { returnTo: window.location.origin } })}>Sign out</button> : <button onClick={() => auth?.loginWithRedirect()}>Sign in</button>}</header><div className="notice">Do not share passwords or payment details here.</div>{adminConversations ? <div className="messages"><h2>Support activity</h2>{ticketNotice && <p>{ticketNotice}</p>}{adminConversations.length ? adminConversations.map((conversation) => <div className="support" key={conversation.conversation_ref}><small>Conversation {conversation.conversation_ref.slice(0, 12)} · {conversation.status}</small>{conversation.messages.map((message, index) => <p key={index}>{message.sender === "you" ? "Customer: " : "Support: "}{message.text}</p>)}{conversation.ticket_ref && <p>Saved Jira ticket: {conversation.ticket_ref}</p>}<button disabled={Boolean(conversation.ticket_ref)} onClick={() => void escalate(conversation)}>{ticketLabel(conversation)}</button></div>) : <p>No administrator access or saved conversations yet.</p>}</div> : <><div className="messages">{messages.map((message, index) => <div className={message.sender} key={index}><small>{message.sender === "you" ? "You" : "Planwell Support"}</small><p>{message.text}</p></div>)}{sending && <div className="support"><small>Planwell Support</small><p>Sending…</p></div>}</div><form onSubmit={send}><input value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask a support question" aria-label="Your question"/><button disabled={!signedIn || sending}>{sending ? "Sending…" : "Send"}</button></form></>}</section></main>;
}
