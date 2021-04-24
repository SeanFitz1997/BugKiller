import * as s3 from "@aws-cdk/aws-s3";
import * as cdk from "@aws-cdk/core";

export interface AppStackProps extends cdk.NestedStackProps {}

export interface GithubProps {
	username: string;
	repository: string;
	branch: string;
	token: string;
}

export interface PipelineStackProps extends cdk.NestedStackProps {
	github: GithubProps;
	websiteBucket: s3.IBucket;
}

export interface BuildPhase {
	[key: string]: {
		commands: string[];
	};
}

export enum BuildPhaseNames {
	INSTALL = "install",
	PRE_BUILD = "pre_build",
	BUILD = "build",
	POST_BUILD = "post_build",
}
