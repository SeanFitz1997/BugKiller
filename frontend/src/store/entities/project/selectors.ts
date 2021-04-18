import { createSelector } from "@reduxjs/toolkit";
import { BugSelectorFilter, ProjectState } from "./types";
import { getProjectState, findProject } from "./utils";

export const getProjects = createSelector(
	getProjectState,
	(projectState) => projectState.projects
);

export const getProject = (projectId: string) =>
	createSelector(getProjectState, (projectState: ProjectState) =>
		findProject(projectState, projectId)
	);

export const getProjectBugs = (
	projectId: string,
	filters: BugSelectorFilter = {}
) =>
	createSelector(getProjectState, (projectState) => {
		const project = findProject(projectState, projectId);
		if (project) {
			return Object.values(project.bugs).filter((bug) => {
				let result = true;

				// Resolve filter
				if ("isResolved" in filters) {
					result =
						result && filters.isResolved === Boolean(bug.resolved);
				}

				// Tag filter
				if ("tags" in filters) {
					const hasTags = filters.tags!.every((tag) =>
						bug.tags.find((bugTag) => bugTag === tag)
					);
					result = result && hasTags;
				}

				return result;
			});
		} else {
			return [];
		}
	});
