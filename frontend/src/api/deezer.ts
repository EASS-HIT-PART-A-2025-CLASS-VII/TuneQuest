export async function fetchDeezerGenres(album: string, artist: string): Promise<string[]> {
  try {
    const res = await fetch(`http://localhost:8000/deezer/genres?album=${encodeURIComponent(album)}&artist=${encodeURIComponent(artist)}`);
    if (!res.ok) throw new Error("Failed to fetch genres");
    const data = await res.json();

    // Replace this with genre name logic later
    return data.genre ? [String(data.genre)] : [];
  } catch (err) {
    console.error("Deezer fetch error:", err);
    return [];
  }
}
