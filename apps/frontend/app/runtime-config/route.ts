export const dynamic = "force-dynamic";

function runtimeValue(name: string, legacyName: string, fallback = ""): string {
  return process.env[name] ?? process.env[legacyName] ?? fallback;
}

export function GET(): Response {
  return Response.json(
    {
      auth0Domain: runtimeValue("AUTH0_DOMAIN", "VITE_AUTH0_DOMAIN"),
      auth0ClientId: runtimeValue("AUTH0_CLIENT_ID", "VITE_AUTH0_CLIENT_ID"),
      auth0Audience: runtimeValue("AUTH0_AUDIENCE", "VITE_AUTH0_AUDIENCE"),
      apiBaseUrl: runtimeValue("API_BASE_URL", "VITE_API_BASE_URL", "http://localhost:8080"),
    },
    { headers: { "Cache-Control": "no-store" } },
  );
}
