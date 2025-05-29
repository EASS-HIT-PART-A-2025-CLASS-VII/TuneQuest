import { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import styles from "./Companion.module.css";
import { TrackCard, AlbumCard, ArtistCard } from "../components/Cards";

type Message = {
  id: string;
  sender: "user" | "ai";
  content: string | AIResults;
};

type AIResults = {
  tracks: any[];
  artists: any[];
  albums: any[];
};

export default function Companion() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const handleSubmit = async () => {
    if (!input.trim()) return;

    const newMessage: Message = {
      id: uuidv4(),
      sender: "user",
      content: input,
    };

    setMessages([...messages, newMessage]);
    setInput("");

    try {
      const response = await fetch("http://localhost:8000/ai/companion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: newMessage.content }),
      });

      const data = await response.json();
      const tracksIds = data.results.tracks
        .map((item: any) => item.id)
        .join(",");
      const artistsIds = data.results.artists
        .map((item: any) => item.id)
        .join(",");
      const albumsIds = data.results.albums
        .map((item: any) => item.id)
        .join(",");

      const [trackRes, artistRes, albumRes] = await Promise.all([
        fetch(`http://localhost:8000/spotify/tracks?ids=${tracksIds}`),
        fetch(`http://localhost:8000/spotify/artists?ids=${artistsIds}`),
        fetch(`http://localhost:8000/spotify/albums?ids=${albumsIds}`),
      ]);

      if (!trackRes.ok || !artistRes.ok || !albumRes.ok) {
        throw new Error("One or more Spotify fetches failed");
      }
      const [trackData, artistData, albumData] = await Promise.all([
        trackRes.json(),
        artistRes.json(),
        albumRes.json(),
      ]);

      const aiMessage: Message = {
        id: uuidv4(),
        sender: "ai",
        content: {
          tracks: trackData.tracks,
          artists: artistData.artists,
          albums: albumData.albums,
        },
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error fetching AI response:", error);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.chatBox}>
        <h2>Chat With a Friend</h2>
        <div className={styles.messages}>
          {messages.map((msg) => (
            <div key={msg.id} className={styles[msg.sender]}>
              {typeof msg.content === "string" ? (
                <p>{msg.content}</p>
              ) : (
                <div className={styles.cards}>
                  <div className={styles.cards}>
                    {"tracks" in msg.content && (
                      <>
                        <p>Tracks</p>
                        {msg.content.tracks.map((track: any) => (
                          <div key={track.id} className={styles.card}>
                            <TrackCard key={track.id} track={track} />
                          </div>
                        ))}
                      </>
                    )}

                    {"artists" in msg.content && (
                      <>
                        <p>Artists</p>
                        {msg.content.artists.map((artist: any) => (
                          <div key={artist.id} className={styles.card}>
                            <ArtistCard key={artist.id} artist={artist} />
                          </div>
                        ))}
                      </>
                    )}
                    {"albums" in msg.content && (
                      <>
                        <p>Albums</p>
                        {msg.content.albums.map((album: any) => (
                          <div key={album.id} className={styles.card}>
                            <AlbumCard key={album.id} album={album} />
                          </div>
                        ))}
                      </>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
      <div>
        <input
          type="text"
          className={styles.inputBox}
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <input
          type="submit"
          className={styles.submitButton}
          onClick={handleSubmit}
          value="Send"
        />
      </div>
    </div>
  );
}
