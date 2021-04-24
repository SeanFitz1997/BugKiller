import * as cdk from "@aws-cdk/core";
import * as codepipeline from "@aws-cdk/aws-codepipeline";
import * as codepipelineActions from "@aws-cdk/aws-codepipeline-actions";
import * as s3 from "@aws-cdk/aws-s3";
import * as codebuild from "@aws-cdk/aws-codebuild";
import {
	BuildPhase,
	BuildPhaseNames,
	GithubProps,
	PipelineStackProps,
} from "./types";
import { APP_NAME } from "./constants";

export default class PipelineStack extends cdk.NestedStack {
	pipeline: codepipeline.Pipeline;

	constructor(scope: cdk.Construct, id: string, props: PipelineStackProps) {
		super(scope, id, props);

		const outputSource = new codepipeline.Artifact();
		const outputWebsite = new codepipeline.Artifact();
		this.pipeline = new codepipeline.Pipeline(
			this,
			`${APP_NAME}_Pipeline`,
			{
				pipelineName: `${APP_NAME}_Pipeline`,
				restartExecutionOnUpdate: true,
			}
		);

		this.pipeline.addStage(
			this.createSourceStage(props.github, outputSource)
		);

		this.pipeline.addStage(
			this.createBuildStage(outputSource, outputWebsite)
		);

		this.pipeline.addStage(
			this.createDeployStage(outputWebsite, props.websiteBucket)
		);
	}

	private createBuildPhase(
		phaseName: string,
		commands: string[],
		withIntroLog: boolean = true,
		withFinishedLog: boolean = true
	): BuildPhase {
		if (withIntroLog)
			commands = [`echo 'Starting Phase ${phaseName} ...'`, ...commands];

		if (withFinishedLog)
			commands = [...commands, `echo 'Finished Phase ${phaseName} ...'`];

		const phase: BuildPhase = {};
		phase[phaseName] = { commands };
		return phase;
	}

	private createSourceStage(
		github: GithubProps,
		outputSource: codepipeline.Artifact
	): codepipeline.StageOptions {
		return {
			stageName: "Source",
			actions: [
				new codepipelineActions.GitHubSourceAction({
					actionName: "Checkout",
					owner: github.username,
					repo: github.repository,
					branch: github.branch,
					oauthToken: cdk.SecretValue.plainText(github.token),
					output: outputSource,
					trigger: codepipelineActions.GitHubTrigger.WEBHOOK,
				}),
			],
		};
	}

	private createBuildStage(
		outputSource: codepipeline.Artifact,
		outputWebsite: codepipeline.Artifact
	): codepipeline.StageOptions {
		const phases: BuildPhase = {
			...this.createBuildPhase(BuildPhaseNames.INSTALL, [
				"echo 'Listing files ...'",
				"find .",
				"cd frontend",
				"echo 'Installing dependencies ...'",
				"npm install -D",
			]),
			...this.createBuildPhase(BuildPhaseNames.PRE_BUILD, [
				"echo 'Running tests ...'",
				"npm test -- --watchAll=false",
			]),
			...this.createBuildPhase(BuildPhaseNames.BUILD, [
				"echo 'Building site ...'",
				"npm run build",
			]),
		};

		return {
			stageName: "Build",
			actions: [
				new codepipelineActions.CodeBuildAction({
					actionName: `Build`,
					input: outputSource,
					outputs: [outputWebsite],
					project: new codebuild.PipelineProject(this, `Build`, {
						projectName: APP_NAME,
						buildSpec: codebuild.BuildSpec.fromObject({
							version: "0.2",
							phases,
							artifacts: {
								files: ["frontend/**/*"],
								base_directory: "build",
							},
							cache: {
								paths: ["./frontend/node_modules/**/*"],
							},
						}),
					}),
				}),
			],
		};
	}

	private createDeployStage(
		outputWebsite: codepipeline.Artifact,
		bucketWebsite: s3.IBucket
	): codepipeline.StageOptions {
		return {
			stageName: "Deploy",
			actions: [
				new codepipelineActions.S3DeployAction({
					actionName: "Deploy",
					input: outputWebsite,
					bucket: bucketWebsite,
				}),
			],
		};
	}
}
