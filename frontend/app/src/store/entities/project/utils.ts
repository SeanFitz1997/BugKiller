import { StoreState } from "../..";
import { Project, ProjectState } from "./types";

export const getProjectState = (state: StoreState) => state.entities.projects;

export const findProjectIndex = (projectState: ProjectState, id: string) => {
	const index = projectState.projects.findIndex(
		(project) => project.id === id
	);
	return index >= 0 ? index : null;
};

export const findProject = (projectState: ProjectState, projectId: string) => {
	const index = findProjectIndex(projectState, projectId);
	return index !== null ? projectState.projects[index] : null;
};

export const findBugIndex = (project: Project, bugId: string) => {
	const index = project.bugs.findIndex((bug) => bug.id === bugId);
	return index >= 0 ? index : null;
};

export const findBug = (
	projectState: ProjectState,
	projectId: string,
	bugId: string
) => {
	let bug = null;
	const project = findProject(projectState, projectId);
	if (project) {
		const bugIndex = findBugIndex(project, bugId);
		if (bugIndex !== null) {
			bug = project.bugs[bugIndex];
		}
	}
	return bug;
};
