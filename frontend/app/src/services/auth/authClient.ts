import {
	ISignUpResult,
	CognitoUserSession,
	CognitoUserPool,
	CognitoUser,
	AuthenticationDetails,
} from "amazon-cognito-identity-js";
import { getRequiredEnvironmentVariable } from "../../domain/utils";
import { IAuthClient } from "./types";

export class AuthClient implements IAuthClient {
	private userPool: CognitoUserPool;

	constructor(userPool: CognitoUserPool) {
		this.userPool = userPool;
	}

	public async signUp(
		email: string,
		password: string
	): Promise<ISignUpResult> {
		return new Promise((resolve, reject) => {
			this.userPool.signUp(email, password, [], [], (error, data) => {
				if (error) reject(error);
				else if (data) resolve(data);
			});
		});
	}

	public async logIn(
		email: string,
		password: string
	): Promise<CognitoUserSession> {
		return new Promise((resolve, reject) => {
			const user = new CognitoUser({
				Username: email,
				Pool: this.userPool,
			});

			const authDetails = new AuthenticationDetails({
				Username: email,
				Password: password,
			});

			user.authenticateUser(authDetails, {
				onSuccess: (data) => resolve(data),
				onFailure: (error) => reject(error),
			});
		});
	}

	public logOut(): void {
		const currentUser = this.getCurrentUser();
		if (currentUser) {
			currentUser.signOut();
		}
	}

	public getCurrentUser(): CognitoUser | null {
		return this.userPool.getCurrentUser();
	}
}

function getUserPool(): CognitoUserPool {
	return new CognitoUserPool({
		UserPoolId: getRequiredEnvironmentVariable(
			"REACT_APP_COGNITO_USER_POOL_ID"
		),
		ClientId: getRequiredEnvironmentVariable("REACT_APP_COGNITO_CLIENT_ID"),
	});
}

export default new AuthClient(getUserPool());
