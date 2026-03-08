export async function fetcher(url: string) {
  const res = await fetch(url)

  if (!res.ok) {
    throw new Error("API error")
  }

  const data = await res.json()

  // handle pagination automatically
  if (data.results) return data.results

  return data
}