import { PayloadAction } from "@reduxjs/toolkit";
import { StoreState } from "../../../../store";
import {
	ProjectState,
	Project,
	Bug,
	BugResolution,
} from "../../../../store/entities/project/types";

/* Note: This is to prevent a test failure due to 
	"Your test suite must contain at least one test." 
*/
test.skip("Workaround", () => 1);

/* Note: This test data should be read only */

const ACTION = Object.freeze("ACTION");
const MANAGER_ID = Object.freeze("M");
const USER_ID = Object.freeze("U");
const DESCRIPTION = Object.freeze("test description");
const PROJECT_TITLE = Object.freeze("test project");
const BUG_TITLE = Object.freeze("test bug");

/*=== State ===*/

export const testProjectState: ProjectState = Object.freeze({
	isLoading: false,
	lastFetched: null,
	projects: [],
});

export const testStoreState: StoreState = Object.freeze({
	entities: {
		projects: testProjectState,
	},
});

/*=== Entities ===*/

export const testProject: Project = Object.freeze({
	id: "1",
	name: PROJECT_TITLE,
	manager: MANAGER_ID,
	bugs: [],
	team: [],
});

export const testBug: Bug = Object.freeze({
	id: "1",
	title: BUG_TITLE,
	description: DESCRIPTION,
	resolved: null,
	tags: [],
});

export const testBugResolution: BugResolution = Object.freeze({
	resolvedAt: 0,
	resolverId: USER_ID,
});

/*=== Actions ===*/

export const testSetProjectsAction: PayloadAction<Project[]> = Object.freeze({
	type: ACTION,
	payload: [testProject],
});

export const testProjectAction: PayloadAction<Project> = Object.freeze({
	type: ACTION,
	payload: testProject,
});

export const testBugAction: PayloadAction<ProjectBugResponse> = Object.freeze({
	type: ACTION,
	payload: {
		projectId: testProject.id,
		bug: testBug,
	},
});

export const testResolveBugAction: PayloadAction<ProjectBugResponse> = Object.freeze(
	{
		type: ACTION,
		payload: {
			projectId: testProject.id,
			bug: {
				...testBug,
				resolved: {
					resolvedAt: 0,
					resolverId: USER_ID,
				},
			},
		},
	}
);
