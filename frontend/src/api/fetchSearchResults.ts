export default async function fetchSearchResults(query: string) {
  try {
    const response = await fetch(
      `http://localhost:8000/spotify/search?query=${encodeURIComponent(query)}`,
      {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      }
    );

    if (!response.ok) return { tracks: [], artists: [], albums: [] };

    const data = await response.json();

    return {
      tracks: data.tracks?.items ?? [],
      artists: data.artists?.items ?? [],
      albums: data.albums?.items ?? [],
    };

  } catch (error) {
    console.error("Search error:", error);
    return { tracks: [], artists: [], albums: [] };
  }
}




