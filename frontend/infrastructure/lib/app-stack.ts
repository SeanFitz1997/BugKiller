import * as cdk from "@aws-cdk/core";
import * as s3 from "@aws-cdk/aws-s3";
import * as cloudfront from "@aws-cdk/aws-cloudfront";
import { AppStackProps } from "./types";
import { APP_NAME } from "./constants";

export default class AppStack extends cdk.NestedStack {
	readonly bucket: s3.IBucket;
	readonly distribution: cloudfront.CloudFrontWebDistribution;

	constructor(scope: cdk.Construct, id: string, props: AppStackProps) {
		super(scope, id, props);

		this.bucket = new s3.Bucket(this, `${APP_NAME}_AppBucket`, {
			websiteIndexDocument: "index.html",
			blockPublicAccess: new s3.BlockPublicAccess({
				restrictPublicBuckets: false,
			}),
		});

		const cloudFrontOAI = new cloudfront.OriginAccessIdentity(
			this,
			`${APP_NAME}_OAI`
		);

		this.distribution = new cloudfront.CloudFrontWebDistribution(
			this,
			`${APP_NAME}_Distribution`,
			{
				originConfigs: [
					{
						s3OriginSource: {
							s3BucketSource: this.bucket,
							originPath: "/frontend/build",
							originAccessIdentity: cloudFrontOAI,
						},
						behaviors: [{ isDefaultBehavior: true }],
					},
				],
			}
		);

		this.bucket.grantRead(cloudFrontOAI.grantPrincipal);
	}
}
