import * as cdk from "@aws-cdk/core";
import { APP_NAME } from "./constants";
import AppStack from "./app-stack";
import PipelineStack from "./pipeline-stack";

export class FrontEndStack extends cdk.Stack {
	frontEndAppStack: cdk.NestedStack;
	frontEndPipelineStack: cdk.NestedStack;

	constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
		super(scope, id, props);

		const usernameParam = new cdk.CfnParameter(this, "GithubUserName", {
			type: "String",
			default: "SeanFitz1997",
			description:
				"The GitHub username of the repo to retrieve source code from",
		});

		const repoParam = new cdk.CfnParameter(this, "RepoName", {
			type: "String",
			default: "BugKiller",
			description:
				"The name of the GitHub repo to retrieve source code from",
		});

		const branchParam = new cdk.CfnParameter(this, "BranchName", {
			type: "String",
			default: "main",
			description:
				"The name of the repo branch to retrieve source code from",
		});

		const tokenParam = new cdk.CfnParameter(this, "GithubToken", {
			type: "String",
			description: "The OAuth access token for the github user",
		});

		const frontEndAppStack = new AppStack(this, `${APP_NAME}-App`, {});
		const frontEndPipelineStack = new PipelineStack(
			this,
			`${APP_NAME}-Pipeline`,
			{
				github: {
					username: usernameParam.valueAsString,
					repository: repoParam.valueAsString,
					branch: branchParam.valueAsString,
					token: tokenParam.valueAsString,
				},
				websiteBucket: frontEndAppStack.bucket,
			}
		);
	}
}
