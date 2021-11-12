import React, { createContext, useEffect, useState } from "react";
import { CognitoUser } from "amazon-cognito-identity-js";
import authClient from "../services/auth/authClient";

interface UserProviderProps {
	children: React.ReactNode;
}

export interface UserContextData {
	currentUser: CognitoUser | null;
	setCurrentUser: (currentUser: CognitoUser | null) => void;
}

export const UserContext = createContext<UserContextData>({
	currentUser: null,
	setCurrentUser: (_) => {},
});

const UserProvider: React.FC<UserProviderProps> = ({ children }) => {
	const [currentUser, setCurrentUser] = useState<CognitoUser | null>(null);
	useEffect(() => setCurrentUser(authClient.getCurrentUser()), []);

	return (
		<UserContext.Provider value={{ currentUser, setCurrentUser }}>
			{children}
		</UserContext.Provider>
	);
};

export default UserProvider;
