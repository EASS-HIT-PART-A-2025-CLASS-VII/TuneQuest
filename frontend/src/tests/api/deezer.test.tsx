import { fetchWithService } from "@/utils/api";
import { test, vi, expect } from "vitest";
import { fetchDeezerGenres, fetchDeezerPreviewUrl } from "@/api/deezer";

vi.mock("@/utils/api", () => ({
  fetchWithService: vi.fn(),
}));

const mockedFetch = fetchWithService as unknown as ReturnType<typeof vi.fn>;

beforeEach(() => {
  mockedFetch.mockReset();
});

describe("fetchDeezerGenres", () => {
  test("returns genre if available", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ genre: "Rock" }),
    });

    const result = await fetchDeezerGenres("Some Album", "Some Artist");
    expect(result).toEqual(["Rock"]);
  });

  test("returns an empty array if genre is missing", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ genre: {} }),
    });

    const result = await fetchDeezerGenres("Some Album", "Some artist");
    expect(result).toEqual([]);
  });

  test("returns an ampty array if failed response", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: false,
    });
    const result = await fetchDeezerGenres("Some Album", "Some artist");
    expect(result).toEqual([]);
  });

  test("returns an empty array on thrown error", async () => {
    mockedFetch.mockResolvedValueOnce(new Error("network error"));
    const result = await fetchDeezerGenres("Some Album", "Some artist");
    expect(result).toEqual([]);
  });
});

describe("fetchDeezerPreviewUrl", () => {
  test("fetchDeezerPreviewUrl returns preview_url if available", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ preview_url: "http://example.com/preview.mp3" }),
    });

    const result = await fetchDeezerPreviewUrl("Track", "Artist");
    expect(result).toEqual(["http://example.com/preview.mp3"]);
  });

  test("fetchDeezerPreviewUrl returns empty array if preview_url missing", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({}),
    });

    const result = await fetchDeezerPreviewUrl("Track", "Artist");
    expect(result).toEqual([]);
  });

  test("fetchDeezerPreviewUrl returns empty array on failed response", async () => {
    mockedFetch.mockResolvedValueOnce({ ok: false });
    const result = await fetchDeezerPreviewUrl("Track", "Artist");
    expect(result).toEqual([]);
  });

  test("fetchDeezerPreviewUrl returns empty array on thrown error", async () => {
    mockedFetch.mockRejectedValueOnce(new Error("fetch failed"));
    const result = await fetchDeezerPreviewUrl("Track", "Artist");
    expect(result).toEqual([]);
  });
});
