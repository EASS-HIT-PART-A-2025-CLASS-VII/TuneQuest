import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import AiButton from "@/components/common/AiButton";
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

describe("AiButton", () => {
  test("renders Ask AI button", () => {
    render(
      <MemoryRouter>
        <AiButton type="track" name="test track" />
      </MemoryRouter>
    );
    expect(screen.getByRole("button", { name: /ask ai/i })).toBeInTheDocument();
  });

  test("shows loading spinner on click", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ results: [{ id: "123" }] }),
    });
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        tracks: [
          {
            id: "123",
            name: "Sample Track",
            album: {
              images: [{ url: "https://example.com/cover.jpg" }],
              name: "Sample Album",
            },
            artists: [{ name: "Sample Artist" }],
          },
        ],
      }),
    });

    render(
      <MemoryRouter>
        <AiButton type="track" name="Test Track" />
      </MemoryRouter>
    );

    const button = screen.getByRole("button", { name: /ask ai/i });
    fireEvent.click(button);

    await waitFor(() =>
      expect(screen.getByTestId("loading-spinner")).toBeInTheDocument()
    );
    await waitFor(() =>
      expect(screen.getByText("Sample Track")).toBeInTheDocument()
    );
  });

  test("disables button while loading", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ results: [] }),
    });
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ tracks: [] }),
    });

    render(
      <MemoryRouter>
        <AiButton type="track" name="Test Track" />
      </MemoryRouter>
    );

    const button = screen.getByRole("button", { name: /ask ai/i });
    fireEvent.click(button);

    expect(button).toBeDisabled();

    await waitFor(() => expect(button).not.toBeDisabled());
  });

  test("shows error message on failure", async () => {
    mockedFetch.mockRejectedValueOnce(new Error("API Error"));

    render(
      <MemoryRouter>
        <AiButton type="track" name="Test Track" />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /ask ai/i }));

    await waitFor(() =>
      expect(screen.getByText(/api error/i)).toBeInTheDocument()
    );
  });

  test("shows artist card when type is 'artist'", async () => {
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ results: [{ id: "123" }] }),
    });
    mockedFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        artists: [
          {
            id: "123",
            name: "Sample Artist",
            images: [{ url: "https://example.com/sample.jpg" }],
          },
        ],
      }),
    });

    render(
      <MemoryRouter>
        <AiButton type="artist" name="Test Artist" />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /ask ai/i }));

    await waitFor(() =>
      expect(screen.getByText("Sample Artist")).toBeInTheDocument()
    );
  });
});
