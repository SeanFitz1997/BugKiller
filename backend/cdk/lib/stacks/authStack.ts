import * as cdk from "@aws-cdk/core";
import * as cognito from "@aws-cdk/aws-cognito";

export class AuthStack extends cdk.NestedStack {
	/**
	 * TODO
	 */
	userPool: cognito.UserPool;
	userPoolClient: cognito.UserPoolClient;

	constructor(
		scope: cdk.Construct,
		id: string,
		props?: cdk.NestedStackProps
	) {
		super(scope, id, props);

		this.userPool = this.createBugKillerUserPool();
		this.userPoolClient = this.createBugKillerUserPoolClient(this.userPool);
	}

	private createBugKillerUserPool(): cognito.UserPool {
		const userPoolName = "BugKillerUserPool";
		return new cognito.UserPool(this, userPoolName, {
			userPoolName: userPoolName,
			removalPolicy: cdk.RemovalPolicy.DESTROY,
			selfSignUpEnabled: true,
			signInAliases: { email: true },
			autoVerify: { email: true },
			passwordPolicy: {
				minLength: 6,
				requireLowercase: false,
				requireDigits: true,
				requireUppercase: true,
				requireSymbols: false,
			},
			accountRecovery: cognito.AccountRecovery.EMAIL_ONLY,
		});
	}

	private createBugKillerUserPoolClient(
		userPool: cognito.UserPool
	): cognito.UserPoolClient {
		return new cognito.UserPoolClient(this, "BugKillerUserPoolClient", {
			userPool,
			authFlows: {
				adminUserPassword: true,
				userPassword: true,
				custom: true,
				userSrp: true,
			},
			supportedIdentityProviders: [
				cognito.UserPoolClientIdentityProvider.COGNITO,
			],
		});
	}
}
