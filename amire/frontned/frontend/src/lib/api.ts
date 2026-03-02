const API_BASE = "http://127.0.0.1:8000/api";

export async function fetchAPI(endpoint: string) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch data");
  }

  return res.json();
}