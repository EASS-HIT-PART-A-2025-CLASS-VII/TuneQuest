import { fetchWithService } from "@/utils/api";

export async function fetchSearchResults(query: string) {
  try {
    const response = await fetchWithService(
      `/spotify/search?query=${encodeURIComponent(query)}`,
      'MUSIC_SERVICE',
      { headers: { "Content-Type": "application/json" } }
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

export async function fetchAlbumSearchResults(query: string) {
  try {
    const response = await fetchWithService(
      `/spotify/search?query=${encodeURIComponent(query)}&type=album`,
      'MUSIC_SERVICE',
      { headers: { "Content-Type": "application/json" } }
    );

    if (!response.ok) return { albums: [] };

    const data = await response.json();
    return { albums: data.albums?.items ?? [] };

  } catch (error) {
    console.error("Album search error:", error);
    return { albums: [] };
  }
}




