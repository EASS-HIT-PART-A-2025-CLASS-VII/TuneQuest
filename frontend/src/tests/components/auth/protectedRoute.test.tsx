import { render, screen } from "@testing-library/react";
import ProtectedRoute from "@/components/auth/ProtectedRoute";
import { useUser } from "@/contexts/UserContext";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";

vi.mock("@/contexts/UserContext", () => ({
  useUser: vi.fn(),
}));

describe("ProtectedRoute", () => {
  test("renders children if user is logged in", () => {
    (useUser as any).mockReturnValue({
      user: { id: "123", name: "Test User" },
    });

    render(
      <MemoryRouter>
        <ProtectedRoute>
          <div>Protected Content</div>
        </ProtectedRoute>
      </MemoryRouter>
    );

    expect(screen.getByText("Protected Content")).toBeInTheDocument();
  });

  test("redirects to /login if user is not logged in", () => {
    (useUser as any).mockReturnValue({ user: null });

    render(
      <MemoryRouter>
        <ProtectedRoute>
          <div>Protected Content</div>
        </ProtectedRoute>
      </MemoryRouter>
    );

    expect(screen.queryByText("Protected Content")).not.toBeInTheDocument();
  });
});
