import { PayloadAction } from "@reduxjs/toolkit";
import {
	addCreatedProjectBugReducer,
	addCreatedProjectReducer,
	removeDeletedProjectBugReducer,
	removeDeletedProjectReducer,
	setProjectsReducer,
	updateResolvedProjectBugReducer,
} from "../../../../store/entities/project/reducers";
import {
	Project,
	ProjectState,
} from "../../../../store/entities/project/types";
import {
	testProjectAction,
	testProjectState,
	testSetProjectsAction,
	testProject,
	testBug,
	testBugAction,
	testResolveBugAction,
	testBugResolution,
} from "./sharedTestData";

describe("project reducers", () => {
	describe("setProjectsReducer", () => {
		it("should set projects list when given a list of projects", () => {
			const state: ProjectState = { ...testProjectState };

			setProjectsReducer(state, testSetProjectsAction);
			expect(state.projects).toEqual([testProject]);
		});
	});

	describe("addCreatedProjectReducer", () => {
		it("should add created project to state", () => {
			const state: ProjectState = { ...testProjectState };

			addCreatedProjectReducer(state, testProjectAction);
			expect(state.projects).toEqual([testProject]);
		});
	});

	describe("removeDeletedProjectReducer", () => {
		const state: ProjectState = {
			...testProjectState,
			projects: [testProject],
		};

		it("should remove deleted project from the state", () => {
			removeDeletedProjectReducer(state, testProjectAction);
			expect(state.projects).toEqual([]);
		});

		it("should not remove the project if it does not exist in the state", () => {
			const action: PayloadAction<Project> = {
				...testProjectAction,
				payload: { ...testProject, id: "X" },
			};

			const state: ProjectState = {
				...testProjectState,
				projects: [testProject],
			};

			removeDeletedProjectReducer(state, action);
			expect(state.projects).toEqual([testProject]);
		});
	});

	describe("addCreatedProjectBugReducer", () => {
		it("should add create bug to the project", () => {
			const state: ProjectState = {
				...testProjectState,
				projects: [testProject],
			};

			addCreatedProjectBugReducer(state, testBugAction);
			expect(state.projects[0].bugs).toEqual([testBug]);
		});
	});

	describe("removeDeletedProjectBugReducer", () => {
		it("should remove deleted bug from the project", () => {
			const state: ProjectState = {
				...testProjectState,
				projects: [{ ...testProject, bugs: [testBug] }],
			};

			removeDeletedProjectBugReducer(state, testBugAction);
			expect(state.projects[0].bugs).toEqual([]);
		});

		it("should not remove the bug if it is not in the project", () => {
			const action: PayloadAction<ProjectBugResponse> = {
				...testBugAction,
				payload: {
					...testBugAction.payload,
					bug: { ...testBug, id: "X" },
				},
			};
			const state: ProjectState = {
				...testProjectState,
				projects: [{ ...testProject, bugs: [testBug] }],
			};

			removeDeletedProjectBugReducer(state, action);
			expect(state.projects[0].bugs).toEqual([testBug]);
		});

		it("should not remove the bug if the project does not exists", () => {
			const action: PayloadAction<ProjectBugResponse> = {
				...testBugAction,
				payload: { ...testBugAction.payload, projectId: "X" },
			};
			const state: ProjectState = {
				...testProjectState,
				projects: [{ ...testProject, bugs: [testBug] }],
			};

			removeDeletedProjectBugReducer(state, action);
			expect(state.projects[0].bugs).toEqual([testBug]);
		});
	});

	describe("updateResolvedProjectBugReducer", () => {
		it("should update the project bug when it is testResolution", () => {
			const state: ProjectState = {
				...testProjectState,
				projects: [{ ...testProject, bugs: [{ ...testBug }] }],
			};

			updateResolvedProjectBugReducer(state, testResolveBugAction);
			expect(state.projects[0].bugs[0].resolved).toEqual(
				testBugResolution
			);
		});
		it("should not update the project bug if it is not in the project", () => {
			const action: PayloadAction<ProjectBugResponse> = {
				...testResolveBugAction,
				payload: {
					...testResolveBugAction.payload,
					bug: { ...testBug, id: "X" },
				},
			};

			const state: ProjectState = {
				...testProjectState,
				projects: [{ ...testProject, bugs: [{ ...testBug }] }],
			};

			updateResolvedProjectBugReducer(state, action);
			expect(state.projects[0].bugs[0].resolved).toBeNull();
		});

		it("should not update the project bug if the project does not exist", () => {
			const action: PayloadAction<ProjectBugResponse> = {
				...testResolveBugAction,
				payload: {
					...testResolveBugAction.payload,
					projectId: "X",
				},
			};

			const state: ProjectState = {
				...testProjectState,
				projects: [{ ...testProject, bugs: [{ ...testBug }] }],
			};

			updateResolvedProjectBugReducer(state, action);
			expect(state.projects[0].bugs[0].resolved).toBeNull();
		});
	});
});

export {};
