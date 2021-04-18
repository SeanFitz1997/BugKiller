import { PayloadAction } from "@reduxjs/toolkit";
import { ProjectBugResponse } from "../../../services/projects/types";
import { Project, ProjectState } from "./types";
import { findBugIndex, findProject, findProjectIndex } from "./utils";

export const setProjectsReducer = (
	projectState: ProjectState,
	action: PayloadAction<Project[]>
) => {
	projectState.projects = action.payload;
};

export const addCreatedProjectReducer = (
	projectState: ProjectState,
	action: PayloadAction<Project>
) => {
	const project = action.payload;
	projectState.projects.push(project);
};

export const removeDeletedProjectReducer = (
	projectState: ProjectState,
	action: PayloadAction<Project>
) => {
	const index = findProjectIndex(projectState, action.payload.id);
	if (index !== null) {
		projectState.projects.splice(index, 1);
	}
};

export const addCreatedProjectBugReducer = (
	projectState: ProjectState,
	action: PayloadAction<ProjectBugResponse>
) => {
	const { projectId, bug } = action.payload;
	const project = findProject(projectState, projectId);
	project?.bugs.push(bug);
};

export const removeDeletedProjectBugReducer = (
	projectState: ProjectState,
	action: PayloadAction<ProjectBugResponse>
) => {
	const { projectId, bug } = action.payload;
	const project = findProject(projectState, projectId);
	if (project) {
		const bugIndex = findBugIndex(project, bug.id);
		if (bugIndex !== null) {
			project.bugs.splice(bugIndex, 1);
		}
	}
};

export const updateResolvedProjectBugReducer = (
	projectState: ProjectState,
	action: PayloadAction<ProjectBugResponse>
) => {
	const { projectId, bug } = action.payload;
	const project = findProject(projectState, projectId);
	if (project) {
		const bugIndex = findBugIndex(project, bug.id);
		if (bugIndex !== null) {
			project.bugs[bugIndex] = bug;
		}
	}
};
