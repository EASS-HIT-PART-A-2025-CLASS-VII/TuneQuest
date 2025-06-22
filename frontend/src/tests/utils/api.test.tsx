import { test, expect, vi, beforeEach } from "vitest";
import { fetchWithService } from "../../utils/api";
import { API_URLS } from "../../config/api";

const mockFetch = vi.fn();
beforeEach(() => {
  vi.stubGlobal("fetch", mockFetch);
  mockFetch.mockReset();
});

test("fetchWithService constructs correct URL for BACKEND service", async () => {
  mockFetch.mockResolvedValueOnce({
    ok: true,
    json: () => Promise.resolve({}),
  });

  const path = "/some-endpoint";
  const service = "BACKEND";
  const options = { method: "GET", headers: { "X-Custom": "test" } };

  await fetchWithService(path, service, options);

  expect(mockFetch).toHaveBeenCalledOnce;
  expect(mockFetch).toHaveBeenCalledWith(`${API_URLS.BACKEND}${path}`, options);
});

test("fetchWithService constructs correct URL for MUSIC_SERVICE", async () => {
  mockFetch.mockResolvedValueOnce({
    ok: true,
    json: () => Promise.resolve({}),
  });

  const path = "/tracks/123";
  const service = "MUSIC_SERVICE";
  const options = { method: "POST", body: JSON.stringify({ data: "foo" }) };

  await fetchWithService(path, service, options);

  expect(mockFetch).toHaveBeenCalledOnce;
  expect(mockFetch).toHaveBeenCalledWith(
    `${API_URLS.MUSIC_SERVICE}${path}`,
    options
  );
});
