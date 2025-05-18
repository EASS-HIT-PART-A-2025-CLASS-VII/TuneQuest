// ProtectedRoute.tsx
import { Navigate } from "react-router-dom";
import { useUser } from "../contexts/UserContext";
import React from "react";

interface Props {
  readonly children: React.JSX.Element;
}

export default function ProtectedRoute({ children }: Props) {
  const { user } = useUser();

  if (!user) {
    // Not logged in, redirect to login page
    return <Navigate to="/login" replace />;
  }

  return children;
}
