import React, { createContext, useContext, useState, useMemo } from "react";
import type { ReactNode } from "react";

interface User {
  fullName: string;
  username: string;
  email: string;
}

interface UserContextType {
  readonly user: User | null;
  readonly setUser: React.Dispatch<React.SetStateAction<User | null>>;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

type UserProviderProps = {
  readonly children: ReactNode;
};

export function UserProvider({ children }: UserProviderProps) {
  const [user, setUser] = useState<User | null>({
    fullName: "John Doe",
    username: "johndoe123",
    email: "john@example.com",
  });

  const value = useMemo(() => ({ user, setUser }), [user, setUser]);

  return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}

export function useUser(): UserContextType {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
}
