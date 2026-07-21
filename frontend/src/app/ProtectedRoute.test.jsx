import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";
import ProtectedRoute from "./ProtectedRoute";

vi.mock("../features/auth/AuthContext", () => ({ useAuth: () => ({ ready: true, user: { role: "manager" } }) }));

test("renders protected content for an allowed role", () => {
  render(<MemoryRouter><ProtectedRoute roles={["manager"]}><p>Farm content</p></ProtectedRoute></MemoryRouter>);
  expect(screen.getByText("Farm content")).toBeInTheDocument();
});

