import {
	ISignUpResult,
	CognitoUserSession,
	CognitoUser,
} from "amazon-cognito-identity-js";

export interface IAuthClient {
	signUp: (email: string, password: string) => Promise<ISignUpResult>;
	logIn: (email: string, password: string) => Promise<CognitoUserSession>;
	logOut: () => void;
	getCurrentUser: () => CognitoUser | null;
}
