import { Navigate } from "react-router-dom";
import { useUser } from "@/contexts/UserContext";

interface ProtectedRouteProps {
  readonly children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { user } = useUser();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
