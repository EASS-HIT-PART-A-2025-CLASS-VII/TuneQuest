import { render, screen, waitFor } from "@testing-library/react";
import fireEvent from "@testing-library/user-event";
import AiHomeButton from "@/components/common/AiHomeButton";
import { vi } from "vitest";
import { fetchWithService } from "@/utils/api";
import { MemoryRouter } from "react-router-dom";

// Mock API
vi.mock("@/utils/api", () => ({
  fetchWithService: vi.fn(),
}));

const mockedFetch = fetchWithService as unknown as ReturnType<typeof vi.fn>;

beforeEach(() => {
  mockedFetch.mockReset();
});

describe("AiHomeButton", () => {
  test("renders Ask AI button", () => {
    render(
      <MemoryRouter>
        <AiHomeButton />
      </MemoryRouter>
    );
    expect(screen.getByRole("button", { name: /ask ai/i })).toBeInTheDocument();
  });

  test("shows loading spinner on click", async () => {
    // 1. AI response
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        results: {
          tracks: [{ id: "123" }],
          albums: [{ id: "456" }],
          artists: [{ id: "789" }],
        },
      }),
    });

    // 2. Spotify tracks
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        tracks: [
          {
            id: "123",
            name: "Sample Track",
            album: {
              images: [{ url: "https://example.com/cover.jpg" }],
              name: "Sample Track Album",
            },
            artists: [{ name: "Sample Track Artist" }],
          },
        ],
      }),
    });

    // 3. Spotify artists
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        artists: [
          {
            id: "789",
            name: "Sample Artist",
            images: [{ url: "https://example.com/cover.jpg" }],
          },
        ],
      }),
    });

    // 4. Spotify albums
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        albums: [
          {
            id: "456",
            name: "Sample Album",
            images: [{ url: "https://example.com/cover.jpg" }],
            artists: [{ name: "Sample Album Artist" }],
            release_date: "2023-05-10",
            release_date_precision: "day",
          },
        ],
      }),
    });

    render(
      <MemoryRouter>
        <AiHomeButton />
      </MemoryRouter>
    );

    const button = screen.getByRole("button", { name: /ask ai/i });
    fireEvent.click(button);

    await waitFor(() => {
      expect(screen.getByTestId("loading-spinner")).toBeInTheDocument();
      expect(button).toBeDisabled();
    });

    // Now wait for the results to appear (meaning loading state has finished and content rendered)
    await waitFor(() => {
      expect(screen.queryByTestId("loading-spinner")).not.toBeInTheDocument(); // Spinner should be gone
      expect(button).not.toBeDisabled(); // Button should be re-enabled
      expect(screen.getByText("Sample Track")).toBeInTheDocument();
      expect(screen.getByText("Sample Artist")).toBeInTheDocument();
      expect(screen.getByText("Sample Album")).toBeInTheDocument();
    });
  });

  test("disables button while loading", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ results: [] }),
    });
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ tracks: [], albums: [], artists: [] }),
    });

    render(
      <MemoryRouter>
        <AiHomeButton />
      </MemoryRouter>
    );

    const button = screen.getByRole("button", { name: /ask ai/i });
    fireEvent.click(button);
    await waitFor(() => expect(button).toBeDisabled());

    await waitFor(() => expect(button).not.toBeDisabled());
  });

  test("shows error message on failure", async () => {
    mockedFetch.mockRejectedValueOnce(new Error("API Error"));

    render(
      <MemoryRouter>
        <AiHomeButton />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /ask ai/i }));

    await waitFor(() =>
      expect(screen.getByText(/api error/i)).toBeInTheDocument()
    );
  });
});
