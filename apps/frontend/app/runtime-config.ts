export type RuntimeConfig = {
  auth0Domain: string;
  auth0ClientId: string;
  auth0Audience: string;
  apiBaseUrl: string;
};

// These identifiers configure the public browser client; they are not secrets.
// Keeping them here makes authenticated API calls resilient if a privacy
// extension blocks the optional runtime-config request.
const publicAuth0Defaults = {
  auth0Domain: "dev-h2h8kguiy88hhun1.us.auth0.com",
  auth0ClientId: "xjPSQEmZMR1FamltWXJj8KJlX9uT2u6D",
  auth0Audience: "https://my-saas-app/",
};

function buildDefaults(): RuntimeConfig {
  const apiBaseUrl =
    typeof window !== "undefined" && window.location.hostname !== "localhost"
      ? `${window.location.origin}/api`
      : "http://localhost:8080";
  return {
    auth0Domain: import.meta.env.VITE_AUTH0_DOMAIN ?? publicAuth0Defaults.auth0Domain,
    auth0ClientId: import.meta.env.VITE_AUTH0_CLIENT_ID ?? publicAuth0Defaults.auth0ClientId,
    auth0Audience: import.meta.env.VITE_AUTH0_AUDIENCE ?? publicAuth0Defaults.auth0Audience,
    apiBaseUrl: import.meta.env.VITE_API_BASE_URL ?? apiBaseUrl,
  };
}

function isRuntimeConfig(value: unknown): value is RuntimeConfig {
  if (typeof value !== "object" || value === null) return false;
  const config = value as Record<string, unknown>;
  return ["auth0Domain", "auth0ClientId", "auth0Audience", "apiBaseUrl"].every(
    (key) => typeof config[key] === "string",
  );
}

export async function loadRuntimeConfig(): Promise<RuntimeConfig> {
  try {
    const response = await fetch("/runtime-config", { cache: "no-store" });
    const config: unknown = await response.json();
    return response.ok && isRuntimeConfig(config) ? config : buildDefaults();
  } catch {
    return buildDefaults();
  }
}
