import { useEffect, useState, useRef } from "react";
import { v4 as uuidv4 } from "uuid";
import styles from "./Companion.module.css";
import { TrackCard, AlbumCard, ArtistCard } from "@/components/features/Cards";
import { FiSend, FiRefreshCw } from "react-icons/fi";
import { ImSpinner2 } from "react-icons/im";
import shared from "@/styles/shared.module.css";
import type { Message } from "@/types/ai/AITypes";
import { fetchWithService } from "@/utils/api";

export default function Companion() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [regenerate, setRegenerate] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const token = localStorage.getItem("access_token");

  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "auto" });
    }
  }, [messages]);

  useEffect(() => {
    async function fetchHistory() {
      try {
        const response = await fetchWithService("/ai/companion", "BACKEND", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) throw new Error("Failed to load history");
        const history = await response.json();
        console.log(history);
        const formattedMessages: Message[] = [];

        for (const entry of history) {
          formattedMessages.push({
            id: uuidv4(),
            sender: "user",
            content: entry.prompt,
          });

          const responseData = entry.response;
          const tracksIds = responseData.results.tracks
            .map((item: any) => item.id)
            .join(",");
          const artistsIds = responseData.results.artists
            .map((item: any) => item.id)
            .join(",");
          const albumsIds = responseData.results.albums
            .map((item: any) => item.id)
            .join(",");

          const [trackRes, artistRes, albumRes] = await Promise.all([
            fetchWithService(
              `/spotify/tracks?ids=${tracksIds}`,
              "MUSIC_SERVICE"
            ),
            fetchWithService(
              `/spotify/artists?ids=${artistsIds}`,
              "MUSIC_SERVICE"
            ),
            fetchWithService(
              `/spotify/albums?ids=${albumsIds}`,
              "MUSIC_SERVICE"
            ),
          ]);

          if (trackRes.ok && artistRes.ok && albumRes.ok) {
            const [trackData, artistData, albumData] = await Promise.all([
              trackRes.json(),
              artistRes.json(),
              albumRes.json(),
            ]);

            formattedMessages.push({
              id: uuidv4(),
              sender: "ai",
              content: {
                tracks: trackData.tracks,
                artists: artistData.artists,
                albums: albumData.albums,
              },
            });
          } else {
            formattedMessages.push({
              id: uuidv4(),
              sender: "ai",
              content: JSON.stringify(responseData),
            });
          }
        }

        setMessages(formattedMessages);
      } catch (err) {
        console.error(err);
        setError("Failed to load chat history.");
      }
    }
    fetchHistory();
  }, [token]);

  const handleSubmit = async (prompt?: string) => {
    const messageContent = prompt ?? input.trim();
    if (!messageContent || loading) return;
    setLoading(true);

    const newMessage: Message = {
      id: uuidv4(),
      sender: "user",
      content: messageContent,
    };

    setMessages((prev) => [...prev, newMessage]);
    setRegenerate(messageContent);
    setInput("");

    try {
      const response = await fetchWithService("/ai/companion", "BACKEND", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
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
        fetchWithService(`/spotify/tracks?ids=${tracksIds}`, "MUSIC_SERVICE"),
        fetchWithService(`/spotify/artists?ids=${artistsIds}`, "MUSIC_SERVICE"),
        fetchWithService(`/spotify/albums?ids=${albumsIds}`, "MUSIC_SERVICE"),
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
      setLoading(false);
    } catch (error) {
      console.error("Error fetching AI response:", error);
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("An unknown error occurred.");
      }
    }
  };

  const handleEnter = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSubmit(input);
    }
  };

  const handleRegenerate = () => {
    if (!regenerate.trim()) return;

    setMessages((prevMessages) => {
      const updated = [...prevMessages];
      const lastMsg = updated[updated.length - 1];

      if (lastMsg?.sender === "ai") {
        updated.pop();
      }

      if (updated[updated.length - 1]?.sender === "user") {
        updated.pop();
      }

      return updated;
    });

    setInput(regenerate);
    handleSubmit(regenerate);
  };

  return (
    <div className={styles.container}>
      <div className={styles.chatBox}>
        <h2>Chat With a Friend</h2>
        {error && <p className={styles.error}>Error: {error}</p>}
        <div className={styles.messages}>
          {messages.map((msg) => (
            <div key={msg.id} className={styles[msg.sender]}>
              {typeof msg.content === "string" ? (
                <p>{msg.content}</p>
              ) : (
                <>
                  {msg.content.tracks?.length > 0 && (
                    <>
                      <p>Tracks</p>
                      <div className={styles.cards}>
                        {msg.content.tracks.map((track: any) => (
                          <div key={track.id} className={styles.card}>
                            <TrackCard track={track} />
                          </div>
                        ))}
                      </div>
                    </>
                  )}
                  {msg.content.artists?.length > 0 && (
                    <>
                      <p>Artists</p>
                      <div className={styles.cards}>
                        {msg.content.artists.map((artist: any) => (
                          <div key={artist.id} className={styles.card}>
                            <ArtistCard artist={artist} />
                          </div>
                        ))}
                      </div>
                    </>
                  )}
                  {msg.content.albums?.length > 0 && (
                    <>
                      <p>Albums</p>
                      <div className={styles.cards}>
                        {msg.content.albums.map((album: any) => (
                          <div key={album.id} className={styles.card}>
                            <AlbumCard album={album} />
                          </div>
                        ))}
                      </div>
                    </>
                  )}
                </>
              )}
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        {loading && (
          <div className={shared.loading}>
            <ImSpinner2 />
          </div>
        )}
      </div>
      <div className={styles.userInput}>
        <input
          type="text"
          className={styles.inputBox}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleEnter}
        />
        <button
          className={styles.sendButton}
          onClick={() => handleSubmit(input)}
          disabled={loading}
        >
          <FiSend />
        </button>
        <button
          className={styles.regenerateButton}
          onClick={handleRegenerate}
          disabled={loading}
        >
          <FiRefreshCw />
        </button>
      </div>
    </div>
  );
}
