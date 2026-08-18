export type RuntimeConfig = {
  auth0Domain: string;
  auth0ClientId: string;
  auth0Audience: string;
  apiBaseUrl: string;
};

const buildDefaults: RuntimeConfig = {
  auth0Domain: import.meta.env.VITE_AUTH0_DOMAIN ?? "",
  auth0ClientId: import.meta.env.VITE_AUTH0_CLIENT_ID ?? "",
  auth0Audience: import.meta.env.VITE_AUTH0_AUDIENCE ?? "",
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8080",
};

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
    return response.ok && isRuntimeConfig(config) ? config : buildDefaults;
  } catch {
    return buildDefaults;
  }
}
