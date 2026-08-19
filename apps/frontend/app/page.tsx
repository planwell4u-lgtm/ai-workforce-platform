"use client";

import { createAuth0Client, type Auth0Client } from "@auth0/auth0-spa-js";
import { Room, RoomEvent, Track } from "livekit-client";
import { FormEvent, useEffect, useRef, useState } from "react";
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
  const [escalatingConversationRef, setEscalatingConversationRef] = useState<string | null>(null);
  const [voiceSandboxStatus, setVoiceSandboxStatus] = useState("");
  const [voiceConsentPending, setVoiceConsentPending] = useState(false);
  const [voiceConnecting, setVoiceConnecting] = useState(false);
  const [voiceConnected, setVoiceConnected] = useState(false);
  const [voiceAgentTest, setVoiceAgentTest] = useState(false);
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
    setEscalatingConversationRef(conversation.conversation_ref);
    setTicketNotice("Creating Jira ticket…");
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
    } catch { setTicketNotice("Ticket service could not be reached.");
    } finally {
      setEscalatingConversationRef(null);
    }
  }
  function ticketLabel(conversation: AdminConversation) {
    if (escalatingConversationRef === conversation.conversation_ref) return "Creating ticket…";
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
        ? undefined
        : requestedRoomRef ? { room_ref: requestedRoomRef } : undefined;
      const response = await fetch(`${apiBaseUrl}${voiceAgentTest ? "/v1/livekit-cloud-agent-token" : "/v1/voice-sandbox-token"}`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
        body: requestBody ? JSON.stringify(requestBody) : undefined,
      });
      const result = await response.json();
      if (!response.ok || typeof result.url !== "string" || typeof result.token !== "string") throw new Error("token_request_failed");
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
      await stopVoiceSession(denied
        ? "Microphone permission was not granted. Nothing was shared; you can try again when ready."
        : "Voice could not start. Nothing is being shared; check the local services and try again.");
    }
  }
  async function signOut() {
    if (voiceRoomRef.current) await stopVoiceSession("Voice session ended before signing out.");
    await auth?.logout({ logoutParams: { returnTo: window.location.origin } });
  }
  return <main><section className="chat-shell"><header><p>PLANWELL</p><h1>Support chat</h1><span>Support ready</span><button className="secondary" onClick={startNewChat}>New chat</button>{signedIn && <button className="secondary" onClick={() => void loadAdminHistory()}>Admin</button>}{signedIn && (voiceConnected ? <button className="secondary" onClick={() => void stopVoiceSession()}>Stop voice</button> : <button className="secondary" disabled={voiceConnecting || voiceConsentPending} onClick={() => { setVoiceAgentTest(false); setVoiceConsentPending(true); setVoiceSandboxStatus("Voice uses your microphone only after you choose Enable microphone. Nothing is recorded."); }}>{voiceConnecting ? "Starting voice…" : "Start voice"}</button>)}{signedIn && !voiceConnected && <button className="secondary" disabled={voiceConnecting || voiceConsentPending} onClick={() => { setJoinVoiceRoomRef(""); setVoiceAgentTest(true); setVoiceConsentPending(true); setVoiceSandboxStatus("The configured Cloud voice agent will join a new private room only after you choose Enable microphone. Nothing is recorded."); }}>Test Cloud voice agent</button>}{signedIn ? <button onClick={() => void signOut()}>Sign out</button> : <button onClick={() => auth?.loginWithRedirect()}>Sign in</button>}</header><div className="notice">Do not share passwords or payment details here.</div>{voiceSandboxStatus && <p className="notice">{voiceSandboxStatus}</p>}{voiceRoomCode && <p className="notice">Voice room code: <code>{voiceRoomCode}</code></p>}{voiceConsentPending && <div className="notice"><p>{voiceAgentTest ? "Enable your microphone to begin the Cloud voice-agent test. The configured agent joins a new private room. It has no Planwell support data, tools, or recording." : "Enable your microphone to speak in this private local voice room. Other participants’ audio will play automatically. You can stop at any time; no recording is enabled."}</p><label>Join an existing local room (optional)<input value={joinVoiceRoomRef} onChange={(event) => setJoinVoiceRoomRef(event.target.value)} placeholder="Paste a voice room code" aria-label="Voice room code"/></label><button onClick={() => void startVoiceSession()}>{voiceAgentTest ? "Enable microphone and start Cloud agent" : "Enable microphone"}</button>{joinVoiceRoomRef.trim() && <button className="secondary" onClick={() => void startVoiceSession(false)}>Join without microphone</button>}<button className="secondary" onClick={() => { setVoiceConsentPending(false); setVoiceAgentTest(false); setVoiceSandboxStatus("Voice was not started. Nothing was shared."); }}>Cancel</button></div>}{adminConversations ? <div className="messages"><h2>Support activity</h2>{ticketNotice && <p>{ticketNotice}</p>}{adminConversations.length ? adminConversations.map((conversation) => <div className="support" key={conversation.conversation_ref}><small>Conversation {conversation.conversation_ref.slice(0, 12)} · {conversation.status}</small>{conversation.messages.map((message, index) => <p key={index}>{message.sender === "you" ? "Customer: " : "Support: "}{message.text}</p>)}{conversation.ticket_ref && <p>Saved Jira ticket: {conversation.ticket_ref}</p>}<button disabled={Boolean(conversation.ticket_ref) || escalatingConversationRef === conversation.conversation_ref} onClick={() => void escalate(conversation)}>{ticketLabel(conversation)}</button></div>) : <p>No administrator access or saved conversations yet.</p>}</div> : <><div className="messages">{messages.map((message, index) => <div className={message.sender} key={index}><small>{message.sender === "you" ? "You" : "Planwell Support"}</small><p>{message.text}</p></div>)}{sending && <div className="support"><small>Planwell Support</small><p>Sending…</p></div>}</div><form onSubmit={send}><input value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="Ask a support question" aria-label="Your question"/><button disabled={!signedIn || sending}>{sending ? "Sending…" : "Send"}</button></form></>}</section></main>;
}
