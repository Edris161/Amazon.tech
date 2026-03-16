const API_BASE = "http://127.0.0.1:8000/api";

export async function fetchAPI(endpoint: string) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API Error: ${res.status} - ${text}`);
  }

  return res.json();
}