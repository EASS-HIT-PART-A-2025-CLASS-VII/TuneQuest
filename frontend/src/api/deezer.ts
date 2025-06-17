import { fetchWithService } from "@/utils/api";

export async function fetchDeezerGenres(album: string, artist: string): Promise<string[]> {
  try {
    const res = await fetchWithService(`/deezer/genres?album=${encodeURIComponent(album)}&artist=${encodeURIComponent(artist)}`,'MUSIC_SERVICE');
    if (!res.ok) throw new Error("Failed to fetch genres");
    const data = await res.json();
    return data.genre ? [String(data.genre)] : [];
  } catch (err) {
    console.error("Deezer fetch error:", err);
    return [];
  }
}

export async function fetchDeezerPreviewUrl(track: string, artist: string): Promise<string[]> {
  try {
    const res = await fetchWithService(`/deezer/tracks?track=${encodeURIComponent(track)}&artist=${encodeURIComponent(artist)}`,'MUSIC_SERVICE');
    if (!res.ok) throw new Error("Failed to fetch preview url");
    const data = await res.json();
    return data.preview_url ? [String(data.preview_url)] : [];
  } catch (err) {
    console.error("Deezer fetch error:", err);
    return [];
  }
}
