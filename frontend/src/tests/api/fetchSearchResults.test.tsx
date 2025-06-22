import { fetchWithService } from "@/utils/api";
import { test, vi, expect } from "vitest";
import {
  fetchSearchResults,
  fetchAlbumSearchResults,
} from "@/api/fetchSearchResults";

vi.mock("@/utils/api", () => ({
  fetchWithService: vi.fn(),
}));

const mockedFetch = fetchWithService as unknown as ReturnType<typeof vi.fn>;

beforeEach(() => {
  mockedFetch.mockReset();
});

describe("fetchSearchResults", () => {
  test("returns data on success", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        tracks: { items: ["track1"] },
        artists: { items: ["artist1"] },
        albums: { items: ["album1"] },
      }),
    });

    const result = await fetchSearchResults("query");
    expect(result).toEqual({
      tracks: ["track1"],
      artists: ["artist1"],
      albums: ["album1"],
    });
  });

  test("returns empty arrays if nested data missing", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    });

    const result = await fetchSearchResults("query");
    expect(result).toEqual({
      tracks: [],
      artists: [],
      albums: [],
    });
  });

  test("returns empty arrays on bad response", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: false,
    });
    const result = await fetchSearchResults("query");
    expect(result).toEqual({
      tracks: [],
      artists: [],
      albums: [],
    });
  });

  test("returns empty arrays on fetch error", async () => {
    mockedFetch.mockRejectedValueOnce(new Error("network error"));
    const result = await fetchSearchResults("query");
    expect(result).toEqual({
      tracks: [],
      artists: [],
      albums: [],
    });
  });
});

describe("fetchAlbumSearchResults", () => {
  test("returns data on success", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        albums: { items: ["album1"] },
      }),
    });

    const result = await fetchAlbumSearchResults("query");
    expect(result).toEqual({
      albums: ["album1"],
    });
  });

  test("returns an empty array if nested data missing", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    });

    const result = await fetchAlbumSearchResults("query");
    expect(result).toEqual({
      albums: [],
    });
  });

  test("returns empty arrays on bad response", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: false,
    });
    const result = await fetchAlbumSearchResults("query");
    expect(result).toEqual({
      albums: [],
    });
  });

  test("returns an empty array on fetch error", async () => {
    mockedFetch.mockRejectedValueOnce(new Error("network error"));
    const result = await fetchAlbumSearchResults("query");
    expect(result).toEqual({ albums: [] });
  });
});
