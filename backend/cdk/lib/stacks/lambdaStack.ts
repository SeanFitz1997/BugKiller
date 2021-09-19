import * as cdk from "@aws-cdk/core";
import * as lambda from "@aws-cdk/aws-lambda";
import * as dynamodb from "@aws-cdk/aws-dynamodb";
import * as path from "path";
import { Duration } from "@aws-cdk/core";
import { snakeCaseToTitleCase } from "../utils";

export interface BugKillerApiLambdas {
	getUsersProjects: lambda.Function;
	createProject: lambda.Function;
	updateProject: lambda.Function;
	deleteProject: lambda.Function;
	createBug: lambda.Function;
	deleteBug: lambda.Function;
}

export interface LambdaStackProps extends cdk.NestedStackProps {
	projectTable: dynamodb.Table;
	userProjectGsiName: string;
}

export class LambdaStack extends cdk.NestedStack {
	/**
	 * TODO
	 */
	public readonly apiLambdas: BugKillerApiLambdas;

	private static readonly HANDLER_CODE_PATH = path.join(
		__dirname,
		"..",
		"..",
		"..",
		"app"
	);

	constructor(scope: cdk.Construct, id: string, props: LambdaStackProps) {
		super(scope, id, props);
		const { projectTable } = props;

		const defaultEnvironmentVariables = {
			PROJECT_TABLE_NAME: projectTable.tableName,
			USER_PROJECT_GSI_NAME: props.userProjectGsiName,
		};

		this.apiLambdas = {
			getUsersProjects: this.createApiLambda(
				"get_user_projects_handler",
				defaultEnvironmentVariables
			),
			createProject: this.createApiLambda(
				"create_project_handler",
				defaultEnvironmentVariables
			),
			updateProject: this.createApiLambda(
				"update_project_handler",
				defaultEnvironmentVariables
			),
			deleteProject: this.createApiLambda(
				"delete_project_handler",
				defaultEnvironmentVariables
			),
			createBug: this.createApiLambda(
				"create_bug_handler",
				defaultEnvironmentVariables
			),
			deleteBug: this.createApiLambda(
				"delete_bug_handler",
				defaultEnvironmentVariables
			),
		};

		projectTable.grantFullAccess(this.apiLambdas.getUsersProjects);
		projectTable.grantFullAccess(this.apiLambdas.createProject);
		projectTable.grantFullAccess(this.apiLambdas.updateProject);
		projectTable.grantFullAccess(this.apiLambdas.deleteProject);
		projectTable.grantFullAccess(this.apiLambdas.createBug);
		projectTable.grantFullAccess(this.apiLambdas.deleteBug);
	}

	private createApiLambda(
		handlerFunctionName: string,
		environmentVariables?: { [env: string]: string }
	): lambda.Function {
		return new lambda.Function(
			this,
			this.createLambdaNameFromHandler(handlerFunctionName),
			{
				handler: `lambda_handlers.${handlerFunctionName}`,
				code: lambda.Code.fromAsset(LambdaStack.HANDLER_CODE_PATH),
				timeout: Duration.seconds(30),
				runtime: lambda.Runtime.PYTHON_3_8,
				environment: environmentVariables,
			}
		);
	}

	private createLambdaNameFromHandler(handlerFunctionName: string): string {
		/**
		 * TODO
		 */
		return snakeCaseToTitleCase(
			handlerFunctionName.replace("_handler", "")
		);
	}
}
