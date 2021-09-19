import * as cdk from "@aws-cdk/core";
import * as dynamodb from "@aws-cdk/aws-dynamodb";

export class DdbStack extends cdk.NestedStack {
	/**
	 * TODO
	 */
	public readonly projectTable: dynamodb.Table;
	public readonly userProjectGsiName = "UserProjectGsi";

	constructor(
		scope: cdk.Construct,
		id: string,
		props?: cdk.NestedStackProps
	) {
		super(scope, id, props);

		this.projectTable = this.createProjectTable();

		this.projectTable.addGlobalSecondaryIndex(
			this.createUserProjectGsiProps()
		);
	}

	private createProjectTable(): dynamodb.Table {
		return new dynamodb.Table(this, "ProjectTable", {
			partitionKey: {
				name: "projectId",
				type: dynamodb.AttributeType.STRING,
			},
			sortKey: {
				name: "ProjectBugManagerMemberId",
				type: dynamodb.AttributeType.STRING,
			},
			billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
			pointInTimeRecovery: true,
		});
	}

	private createUserProjectGsiProps(): dynamodb.GlobalSecondaryIndexProps {
		return {
			indexName: this.userProjectGsiName,
			partitionKey: {
				name: "ProjectBugManagerMemberId",
				type: dynamodb.AttributeType.STRING,
			},
		};
	}
}
