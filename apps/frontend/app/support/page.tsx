"use client";

import { createAuth0Client, type Auth0Client } from "@auth0/auth0-spa-js";
import { Room, RoomEvent, Track } from "livekit-client";
import { FormEvent, useCallback, useEffect, useRef, useState } from "react";
import { loadRuntimeConfig } from "../runtime-config";
import "./support.css";

type ChatMessage = { sender: "support" | "you"; text: string };
type AdminConversation = {
  conversation_ref: string;
  messages: ChatMessage[];
  status: string;
  ticket_ref: string | null;
  ticket_outcome: "succeeded" | "failed" | "uncertain" | null;
  ticket_reason: string | null;
};

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    { sender: "support", text: "Hello. I can help with approved Planwell support information." },
  ]);
  const [question, setQuestion] = useState("");
  const [auth, setAuth] = useState<Auth0Client>();
  const [signedIn, setSignedIn] = useState(false);
  const [accountLabel, setAccountLabel] = useState("");
  const [identityProvider, setIdentityProvider] = useState("");
  const [auth0Audience, setAuth0Audience] = useState("");
  const [sequence, setSequence] = useState(1);
  const [sessionRef, setSessionRef] = useState(() => {
    const existing = typeof window === "undefined" ? null : window.localStorage.getItem("planwell-support-session");
    const session = existing ?? `web-chat-${crypto.randomUUID()}`;
    if (!existing && typeof window !== "undefined") window.localStorage.setItem("planwell-support-session", session);
    return session;
  });
  const [sending, setSending] = useState(false);
  const [conversationRef, setConversationRef] = useState<string | null>(null);
  const [routeOfferRef, setRouteOfferRef] = useState<string | null>(null);
  const [routePurpose, setRoutePurpose] = useState<"support" | "human_support">("support");
  const [routeNotice, setRouteNotice] = useState("");
  const [routing, setRouting] = useState(false);
  const [adminConversations, setAdminConversations] = useState<AdminConversation[] | null>(null);
  const [ticketNotice, setTicketNotice] = useState("");
  const [apiBaseUrl, setApiBaseUrl] = useState("/api");
  const [escalatingConversationRef, setEscalatingConversationRef] = useState<string | null>(null);
  const [voiceSandboxStatus, setVoiceSandboxStatus] = useState("");
  const [voiceConsentPending, setVoiceConsentPending] = useState(false);
  const [voiceConnecting, setVoiceConnecting] = useState(false);
  const [voiceConnected, setVoiceConnected] = useState(false);
  const [voiceAgentTest, setVoiceAgentTest] = useState(false);
  const [cloudSupportQuery, setCloudSupportQuery] = useState("");
  const [voiceRoomCode, setVoiceRoomCode] = useState("");
  const [joinVoiceRoomRef, setJoinVoiceRoomRef] = useState("");
  const voiceRoomRef = useRef<Room>();
  const voiceMicrophoneRef = useRef<MediaStreamTrack>();
  const voicePlaybackElementsRef = useRef<HTMLMediaElement[]>([]);
  useEffect(() => {
    void loadRuntimeConfig().then(async (config) => {
      const client = await createAuth0Client({
        domain: config.auth0Domain,
        clientId: config.auth0ClientId,
        cacheLocation: "localstorage",
        authorizationParams: {
          audience: config.auth0Audience,
          redirect_uri: `${window.location.origin}/support`,
          scope: "openid profile email agent.context.read operator.status.read integration.support-ticket.create",
        },
      });
      if (window.location.search.includes("code=") && window.location.search.includes("state=")) {
        await client.handleRedirectCallback();
        window.history.replaceState({}, document.title, window.location.pathname);
      }
      setApiBaseUrl(config.apiBaseUrl);
      setAuth0Audience(config.auth0Audience);
      setAuth(client);
      const isAuthenticated = await client.isAuthenticated();
      setSignedIn(isAuthenticated);
      if (isAuthenticated) {
        const user = await client.getUser();
        setAccountLabel(user?.email ?? user?.name ?? "");
        setIdentityProvider(user?.sub?.startsWith("google-oauth2|") ? "Google" : "");
      }
    });
  }, []);
  const getSupportToken = useCallback(async () => {
    if (!auth) throw new Error("auth_not_ready");
    return auth.getTokenSilently({
      authorizationParams: {
        audience: auth0Audience,
        scope: "openid profile email agent.context.read operator.status.read integration.support-ticket.create",
      },
    });
  }, [auth, auth0Audience]);
  function signInForSupport() {
    void auth?.loginWithRedirect({
      authorizationParams: {
        audience: auth0Audience,
        redirect_uri: `${window.location.origin}/support`,
        scope: "openid profile email agent.context.read operator.status.read integration.support-ticket.create",
      },
    });
  }
  useEffect(() => {
    if (!auth || !signedIn) return;
    async function restoreHistory() {
      try {
        const token = await getSupportToken();
        const response = await fetch(`${apiBaseUrl}/v1/support-answers?session_ref=${encodeURIComponent(sessionRef)}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const result = await response.json();
        if (typeof result.conversation_ref === "string") setConversationRef(result.conversation_ref);
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
  }, [apiBaseUrl, auth, getSupportToken, sessionRef, signedIn]);
  async function send(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!question.trim() || !auth || !signedIn) return;
    const text = question.trim();
    setMessages((current) => [...current, { sender: "you", text }]);
    setQuestion("");
    setSending(true);
    try {
      const token = await getSupportToken();
      const response = await fetch(`${apiBaseUrl}/v1/support-answers`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify({ agent_ref: "customer-support-worker", session_ref: sessionRef, event_ref: crypto.randomUUID(), sequence, question: text }),
      });
      const result = await response.json();
      setSequence((value) => value + 1);
      if (typeof result.conversation_ref === "string") setConversationRef(result.conversation_ref);
      setMessages((current) => [...current, { sender: "support", text: result.answer ?? "I could not find an approved answer for that question." }]);
    } catch {
      setMessages((current) => [...current, { sender: "support", text: "I could not reach the secure support service. Please try again." }]);
    } finally {
      setSending(false);
    }
  }
  async function offerRoute(purpose: "support" | "human_support") {
    if (!auth || !conversationRef) return;
    setRouting(true);
    setRoutePurpose(purpose);
    const display = purpose === "support" ? "Support" : "Human Support";
    setRouteNotice(`Checking whether ${display} is available…`);
    try {
      const token = await getSupportToken();
      const response = await fetch(`${apiBaseUrl}/v1/conversation-routing-requests`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify({ conversation_ref: conversationRef, route_purpose: purpose, event_ref: crypto.randomUUID(), route_action: "offer" }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error("route_offer_failed");
      setRouteNotice(typeof result.public_message === "string" ? result.public_message : `${display} is not available through this channel right now.`);
      setRouteOfferRef(result.outcome === "route_offered" && typeof result.routing_request_ref === "string" ? result.routing_request_ref : null);
    } catch {
      setRouteOfferRef(null);
      setRouteNotice(`We could not confirm ${display} availability. Please try again.`);
    } finally {
      setRouting(false);
    }
  }
  async function offerSupportRoute() {
    await offerRoute("support");
  }
  async function requestSupportRoute() {
    if (!auth || !conversationRef || !routeOfferRef) return;
    setRouting(true);
    const display = routePurpose === "support" ? "Support" : "Human Support";
    setRouteNotice(`Rechecking ${display} availability…`);
    try {
      const token = await getSupportToken();
      const response = await fetch(`${apiBaseUrl}/v1/conversation-routing-requests`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify({ conversation_ref: conversationRef, route_purpose: routePurpose, event_ref: crypto.randomUUID(), route_action: "request", offer_ref: routeOfferRef }),
      });
      const result = await response.json();
      if (!response.ok) throw new Error("route_request_failed");
      setRouteNotice(typeof result.public_message === "string" ? result.public_message : "We could not confirm the request. Please try again.");
      setRouteOfferRef(null);
    } catch {
      setRouteNotice("We could not confirm the request. Please try again.");
    } finally {
      setRouting(false);
    }
  }
  async function loadAdminHistory() {
    if (!auth || !signedIn) return;
    try {
      const token = await getSupportToken();
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
    setEscalatingConversationRef(conversation.conversation_ref);
    setTicketNotice("Creating Jira ticket…");
    try {
      const token = await getSupportToken();
      const summary = conversation.messages.map((message) => `${message.sender}: ${message.text}`).join(" ").slice(0, 240);
      const response = await fetch(`${apiBaseUrl}/v1/support-tickets`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: JSON.stringify({ conversation_ref: conversation.conversation_ref, idempotency_ref: conversation.conversation_ref, summary }),
      });
      const result = await response.json();
      if (result.ticket_ref) {
        setAdminConversations((current) => current?.map((item) =>
          item.conversation_ref === conversation.conversation_ref
            ? { ...item, ticket_ref: result.ticket_ref, ticket_outcome: result.outcome ?? "succeeded" }
            : item,
        ) ?? null);
      }
      if (result.outcome === "succeeded" && result.ticket_ref) setTicketNotice(`Ticket created: ${result.ticket_ref}`);
      else if (result.outcome === "uncertain") setTicketNotice(`Jira could not confirm the ticket result${result.reason ? ` (${result.reason})` : ""}. Do not retry; check Jira first.`);
      else setTicketNotice(`Jira rejected the ticket request${result.reason ? ` (${result.reason})` : ""}. No ticket was created.`);
    } catch { setTicketNotice("Ticket service could not be reached.");
    } finally {
      setEscalatingConversationRef(null);
    }
  }
  function ticketLabel(conversation: AdminConversation) {
    if (escalatingConversationRef === conversation.conversation_ref) return "Creating ticket…";
    if (conversation.ticket_ref) return `Ticket ${conversation.ticket_ref} created`;
    if (conversation.ticket_outcome === "uncertain") return "Ticket outcome unknown";
    if (conversation.ticket_outcome === "failed") return "Ticket creation failed";
    return "Escalate to ticket";
  }
  function startNewChat() {
    const next = `web-chat-${crypto.randomUUID()}`;
    window.localStorage.setItem("planwell-support-session", next);
    setSessionRef(next);
    setSequence(1);
    setConversationRef(null);
    setRouteOfferRef(null);
    setRouteNotice("");
    setMessages([{ sender: "support", text: "Hello. I can help with approved Planwell support information." }]);
  }
  function clearVoicePlayback() {
    for (const element of voicePlaybackElementsRef.current) element.remove();
    voicePlaybackElementsRef.current = [];
  }
  async function stopVoiceSession(notice = "Voice session ended. Your microphone is no longer shared.") {
    const room = voiceRoomRef.current;
    const microphone = voiceMicrophoneRef.current;
    if (room && microphone) room.localParticipant.unpublishTrack(microphone);
    microphone?.stop();
    clearVoicePlayback();
    await room?.disconnect();
    voiceRoomRef.current = undefined;
    voiceMicrophoneRef.current = undefined;
    setVoiceRoomCode("");
    setVoiceConnected(false);
    setVoiceConnecting(false);
    setVoiceConsentPending(false);
    setVoiceSandboxStatus(notice);
  }
  async function startVoiceSession(shareMicrophone = true) {
    if (!auth || !signedIn) return;
    setVoiceConsentPending(false);
    setVoiceConnecting(true);
    setVoiceSandboxStatus("Connecting your private voice room…");
    try {
      const token = await auth.getTokenSilently();
      const requestedRoomRef = joinVoiceRoomRef.trim();
      const requestBody = voiceAgentTest
        ? { support_query: cloudSupportQuery.trim() }
        : requestedRoomRef ? { room_ref: requestedRoomRef } : undefined;
      const response = await fetch(`${apiBaseUrl}${voiceAgentTest ? "/v1/livekit-cloud-agent-token" : "/v1/voice-sandbox-token"}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: requestBody ? JSON.stringify(requestBody) : undefined,
      });
      const result = await response.json();
      if (!response.ok || typeof result.url !== "string" || typeof result.token !== "string") {
        throw new Error(
          voiceAgentTest && response.status === 403
            ? "approved_context_unavailable"
            : typeof result.error === "string" ? result.error : "token_request_failed",
        );
      }
      const room = new Room();
      let cloudAgentJoined = false;
      let cloudAudioReceived = false;
      voiceRoomRef.current = room;
      room.on(RoomEvent.ParticipantConnected, () => {
        if (!voiceAgentTest) return;
        cloudAgentJoined = true;
        setVoiceSandboxStatus("Cloud voice agent joined the private room. It is ready to hear your question.");
      });
      room.on(RoomEvent.TrackSubscribed, (track) => {
        if (track.kind !== Track.Kind.Audio) return;
        if (voiceAgentTest) {
          cloudAudioReceived = true;
          setVoiceSandboxStatus("Cloud voice agent audio received. It should be playing now.");
        }
        const playback = track.attach();
        playback.autoplay = true;
        playback.setAttribute("aria-label", "Voice participant audio");
        document.body.appendChild(playback);
        voicePlaybackElementsRef.current.push(playback);
        void playback.play().catch(() => {
          setVoiceSandboxStatus("Cloud voice agent audio is ready, but your browser blocked playback. Click once anywhere on this page, then try the test again.");
        });
      });
      room.on(RoomEvent.Disconnected, () => {
        if (voiceRoomRef.current === room) {
          setVoiceConnected(false);
          setVoiceConnecting(false);
          setVoiceSandboxStatus("Voice connection ended unexpectedly. Nothing is being shared; you can try again.");
        }
      });
      await room.connect(result.url, result.token);
      if (voiceAgentTest) {
        window.setTimeout(() => {
          if (voiceRoomRef.current === room && !cloudAgentJoined) {
            setVoiceSandboxStatus("Waiting for the Cloud voice agent to join. If this remains, its deployment name or Cloud project settings need checking.");
          }
        }, 12000);
      }
      if (!shareMicrophone) {
        setVoiceConnected(true);
        setVoiceConnecting(false);
        setVoiceRoomCode(result.room_ref);
        setVoiceSandboxStatus("Connected as a listener. Audio from other participants will play automatically; your microphone is not shared.");
        return;
      }
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true },
        video: false,
      });
      const microphone = stream.getAudioTracks()[0];
      if (!microphone) throw new Error("microphone_unavailable");
      voiceMicrophoneRef.current = microphone;
      await room.localParticipant.publishTrack(microphone, {
        name: "customer-microphone",
        source: Track.Source.Microphone,
      });
      setVoiceConnected(true);
      setVoiceConnecting(false);
      setVoiceRoomCode(result.room_ref);
      setVoiceSandboxStatus(voiceAgentTest
        ? cloudAudioReceived
          ? "Cloud voice agent audio received. It should be playing now."
          : cloudAgentJoined
            ? "Cloud voice agent joined the private room. Ask your question now."
            : "Cloud voice agent test is live. Your microphone is shared only in this private room; the configured agent will join automatically."
        : "Voice is live. Your microphone is shared only in this room; audio from other participants will play automatically.");
    } catch (error) {
      const denied = error instanceof DOMException && error.name === "NotAllowedError";
      const unsupportedTopic = error instanceof Error && error.message === "approved_context_unavailable";
      await stopVoiceSession(denied
        ? "Microphone permission was not granted. Nothing was shared; you can try again when ready."
        : unsupportedTopic
          ? "That topic is not available for the voice test. Try the approved topic: order tracking. Nothing was shared."
        : "Voice could not start. Nothing is being shared; check the local services and try again.");
    }
  }
  async function signOut() {
    if (voiceRoomRef.current) await stopVoiceSession("Voice session ended before signing out.");
    await auth?.logout({ logoutParams: { returnTo: window.location.origin } });
  }
  return <main><section className="chat-shell"><header><p>PLANWELL</p><h1>Support chat</h1><span>{signedIn ? accountLabel ? `${identityProvider ? `Signed in with ${identityProvider} as` : "Signed in as"} ${accountLabel}` : "Signed in — email unavailable. Sign in again to show it." : "Support ready"}</span><button className="secondary" onClick={startNewChat}>New chat</button>{signedIn && <button className="secondary" onClick={() => void loadAdminHistory()}>Admin</button>}{signedIn && <button className="secondary" onClick={signInForSupport}>Sign in again for Support</button>}{signedIn && (voiceConnected ? <button className="secondary" onClick={() => void stopVoiceSession()}>Stop voice</button> : <button className="secondary" disabled={voiceConnecting || voiceConsentPending} onClick={() => { setVoiceAgentTest(false); setVoiceConsentPending(true); setVoiceSandboxStatus("Voice uses your microphone only after you choose Enable microphone. Nothing is recorded."); }}>{voiceConnecting ? "Starting voice…" : "Start voice"}</button>)}{signedIn && !voiceConnected && <button className="secondary" disabled={voiceConnecting || voiceConsentPending} onClick={() => { setJoinVoiceRoomRef(""); setVoiceAgentTest(true); setVoiceConsentPending(true); setVoiceSandboxStatus("The configured Cloud voice agent will receive only the approved FAQ context for the support topic you provide."); }}>Test Cloud voice agent</button>}{signedIn ? <button onClick={() => void signOut()}>Sign out</button> : <button onClick={() => auth?.loginWithRedirect()}>Sign in</button>}</header><div className="notice">Do not share passwords or payment details here.</div>{voiceSandboxStatus && <p className="notice">{voiceSandboxStatus}</p>}{voiceRoomCode && <p className="notice">Voice room code: <code>{voiceRoomCode}</code></p>}{voiceConsentPending && <div className="notice"><p>{voiceAgentTest ? "Provide a support topic, then enable your microphone. The configured Cloud voice agent receives only one matching approved FAQ excerpt; no recording or actions are enabled." : "Enable your microphone to speak in this private local voice room. Other participants’ audio will play automatically. You can stop at any time; no recording is enabled."}</p>{voiceAgentTest && <label>Support topic<input value={cloudSupportQuery} onChange={(event) => setCloudSupportQuery(event.target.value)} placeholder="For example: order tracking" aria-label="Support topic"/></label>}<label>Join an existing local room (optional)<input value={joinVoiceRoomRef} onChange={(event) => setJoinVoiceRoomRef(event.target.value)} placeholder="Paste a voice room code" aria-label="Voice room code"/></label><button disabled={voiceAgentTest && !cloudSupportQuery.trim()} onClick={() => void startVoiceSession()}>{voiceAgentTest ? "Enable microphone and start Cloud agent" : "Enable microphone"}</button>{joinVoiceRoomRef.trim() && <button className="secondary" onClick={() => void startVoiceSession(false)}>Join without microphone</button>}<button className="secondary" onClick={() => { setVoiceConsentPending(false); setVoiceAgentTest(false); setVoiceSandboxStatus("Voice was not started. Nothing was shared."); }}>Cancel</button></div>}{adminConversations ? <div className="messages"><h2>Support activity</h2>{ticketNotice && <p>{ticketNotice}</p>}{adminConversations.length ? adminConversations.map((conversation) => <div className="support" key={conversation.conversation_ref}><small>Conversation {conversation.conversation_ref.slice(0, 12)} · {conversation.status}</small>{conversation.messages.map((message, index) => <p key={index}>{message.sender === "you" ? "Customer: " : "Support: "}{message.text}</p>)}{conversation.ticket_ref && <p>Saved Jira ticket: {conversation.ticket_ref}</p>}<button disabled={Boolean(conversation.ticket_ref) || escalatingConversationRef === conversation.conversation_ref} onClick={() => void escalate(conversation)}>{ticketLabel(conversation)}</button></div>) : <p>No administrator access or saved conversations yet.</p>}</div> : <><div className="messages">{messages.map((message, index) => <div className={message.sender} key={index}><small>{message.sender === "you" ? "You" : "Planwell Support"}</small><p>{message.text}</p></div>)}{sending && <div className="support"><small>Planwell Support</small><p>Sending…</p></div>}</div>{conversationRef && <div className="notice"><p>{routeNotice || "You can ask the Front Desk to check whether Support is available. This does not transfer your chat."}</p>{routeOfferRef ? <button disabled={routing} onClick={() => void requestSupportRoute()}>{routing ? "Checking…" : "Request Support route"}</button> : <button className="secondary" disabled={routing} onClick={() => void offerSupportRoute()}>{routing ? "Checking…" : "Check Support availability"}</button>}</div>}<form onSubmit={send}><input value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask a support question" aria-label="Your question"/><button disabled={!signedIn || sending}>{sending ? "Sending…" : "Send"}</button></form></>}</section></main>;
}
