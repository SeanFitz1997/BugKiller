import * as cdk from "@aws-cdk/core";
import * as apigateway from "@aws-cdk/aws-apigateway";
import { BugKillerApiLambdas } from "./lambdaStack";

interface ApiStackProps extends cdk.NestedStackProps {
	apiLambdas: BugKillerApiLambdas;
}

export class ApiStack extends cdk.NestedStack {
	/**
	 * TODO
	 */
	public readonly apiGateway: apigateway.RestApi;

	private static readonly API_NAME = "BugKillerApi";

	constructor(scope: cdk.Construct, id: string, props: ApiStackProps) {
		super(scope, id, props);

		this.apiGateway = this.createApiGateway(props.apiLambdas);
	}

	private createApiGateway(
		apiLambdas: BugKillerApiLambdas
	): apigateway.RestApi {
		// Create API
		const api = new apigateway.RestApi(this, ApiStack.API_NAME, {
			restApiName: ApiStack.API_NAME,
			description: "TODO",
		});

		// /projects
		const projects = api.root.addResource("projects");
		projects.addMethod(
			"GET",
			new apigateway.LambdaIntegration(apiLambdas.getUsersProjects)
		);
		projects.addMethod(
			"POST",
			new apigateway.LambdaIntegration(apiLambdas.createProject)
		);

		// /projects/{projectId}
		const projectId = projects.addResource("{projectId}");
		projectId.addMethod(
			"PATCH",
			new apigateway.LambdaIntegration(apiLambdas.updateProject)
		);
		projectId.addMethod(
			"DELETE",
			new apigateway.LambdaIntegration(apiLambdas.deleteProject)
		);

		// /bugs
		const bugs = api.root.addResource("bugs");
		bugs.addMethod(
			"POST",
			new apigateway.LambdaIntegration(apiLambdas.createBug)
		);

		// /bugs/{bugId}
		const bugId = bugs.addResource("{bugId}");
		bugId.addMethod(
			"DELETE",
			new apigateway.LambdaIntegration(apiLambdas.deleteBug)
		);

		return api;
	}
}
