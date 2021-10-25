import * as cdk from "@aws-cdk/core";
import { ApiStack } from "./stacks/apiStack";
import { LambdaStack } from "./stacks/lambdaStack";
import { DdbStack } from "./stacks/ddbStack";
import { AuthStack } from "./stacks/authStack";

export class BugKillerBackendApp extends cdk.Stack {
	/**
	 * TODO
	 */
	public readonly authStack: AuthStack;
	public readonly ddbStack: DdbStack;
	public readonly lambdaStack: LambdaStack;
	public readonly apiStack: ApiStack;

	constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
		super(scope, id, props);

		this.authStack = new AuthStack(this, "AuthStack");
		this.ddbStack = new DdbStack(this, "DdbStack");
		this.lambdaStack = new LambdaStack(this, "LambdaStack", {
			projectTable: this.ddbStack.projectTable,
			userProjectGsiName: this.ddbStack.userProjectGsiName,
		});
		this.apiStack = new ApiStack(this, "ApiStack", {
			apiLambdas: this.lambdaStack.apiLambdas,
			authUserPool: this.authStack.userPool,
		});
	}
}
