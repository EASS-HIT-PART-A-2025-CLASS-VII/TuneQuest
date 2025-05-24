export default async function fetchTracks(query: string) {
  try {
    const response = await fetch(
      `http://localhost:8000/spotify/search?query=${encodeURIComponent(query)}`,
      {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      }
    );

    if (!response.ok) return [];

    return await response.json();
  } catch (error) {
    console.error("Search error:", error);
    return [];
  }
}
