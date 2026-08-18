import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("server-renders the Planwell support chat", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);
  const html = await response.text();
  assert.match(html, /PLANWELL/);
  assert.match(html, /Support chat/);
  assert.match(html, /Do not share passwords or payment details here\./);
  assert.match(html, /Ask a support question/);
  assert.match(html, /Sign in/);
});

test("keeps voice consent, playback, and recovery explicit in browser code", async () => {
  const page = await readFile(new URL("../app/page.tsx", import.meta.url), "utf8");
  assert.match(page, /Start voice/);
  assert.match(page, /Enable microphone/);
  assert.match(page, /Stop voice/);
  assert.match(page, /getUserMedia/);
  assert.match(page, /TrackSubscribed/);
  assert.match(page, /Join an existing local room/);
  assert.match(page, /Join without microphone/);
  assert.match(page, /Voice room code/);
  assert.match(page, /Nothing was shared/);
  assert.match(page, /voice-sandbox-token/);
  assert.doesNotMatch(page, /LIVEKIT_API_SECRET/);
});
