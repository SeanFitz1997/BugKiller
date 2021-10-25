import * as cdk from "@aws-cdk/core";
import * as cognito from "@aws-cdk/aws-cognito";
import * as apigateway from "@aws-cdk/aws-apigateway";
import { BugKillerApiLambdas } from "./lambdaStack";

interface ApiStackProps extends cdk.NestedStackProps {
	apiLambdas: BugKillerApiLambdas;
	authUserPool: cognito.UserPool;
	// authUserPoolClient: cognito.UserPoolClient;
}

export class ApiStack extends cdk.NestedStack {
	/**
	 * TODO
	 */
	public readonly apiGateway: apigateway.RestApi;

	private static readonly API_NAME = "BugKillerApi";

	constructor(scope: cdk.Construct, id: string, props: ApiStackProps) {
		super(scope, id, props);
		const { apiLambdas, authUserPool } = props;

		const apiGwAuthorizer = this.createApiGwAuthorizer(authUserPool);
		this.apiGateway = this.createApiGateway(apiLambdas, apiGwAuthorizer);
	}

	private createApiGwAuthorizer(
		userPool: cognito.UserPool
	): apigateway.CognitoUserPoolsAuthorizer {
		return new apigateway.CognitoUserPoolsAuthorizer(
			this,
			ApiStack.API_NAME + "Authorizer",
			{
				cognitoUserPools: [userPool],
			}
		);
	}

	private createApiGateway(
		apiLambdas: BugKillerApiLambdas,
		apiAuthorizer: apigateway.CognitoUserPoolsAuthorizer
	): apigateway.RestApi {
		// Create API
		const api = new apigateway.RestApi(this, ApiStack.API_NAME, {
			restApiName: ApiStack.API_NAME,
			description: "TODO",
		});
		const authOptions = {
			authorizer: apiAuthorizer,
			authorizationType: apigateway.AuthorizationType.COGNITO,
		};

		// /projects
		const projects = api.root.addResource("projects");
		projects.addMethod(
			"GET",
			new apigateway.LambdaIntegration(apiLambdas.getUsersProjects),
			authOptions
		);
		projects.addMethod(
			"POST",
			new apigateway.LambdaIntegration(apiLambdas.createProject),
			authOptions
		);

		// /projects/{projectId}
		const projectId = projects.addResource("{projectId}");
		projectId.addMethod(
			"PATCH",
			new apigateway.LambdaIntegration(apiLambdas.updateProject),
			authOptions
		);
		projectId.addMethod(
			"DELETE",
			new apigateway.LambdaIntegration(apiLambdas.deleteProject),
			authOptions
		);

		// /bugs
		const bugs = api.root.addResource("bugs");
		bugs.addMethod(
			"POST",
			new apigateway.LambdaIntegration(apiLambdas.createBug),
			authOptions
		);

		// /bugs/{bugId}
		const bugId = bugs.addResource("{bugId}");
		bugId.addMethod(
			"DELETE",
			new apigateway.LambdaIntegration(apiLambdas.deleteBug),
			authOptions
		);

		return api;
	}
}
