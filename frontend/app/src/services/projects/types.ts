import { Bug, Project } from "../../store/entities/project/types";

export interface ProjectsClient {
	loadProjects: () => Promise<Project[]>;
	createProject: (payload: CreateProjectPayload) => Promise<Project>;
	deleteProject: (payload: DeleteProjectPayload) => Promise<Project>;

	addProjectBug: (
		payload: AddProjectBugPayload
	) => Promise<ProjectBugResponse>;
	resolveProjectBug: (
		payload: ResolveProjectBugPayload
	) => Promise<ProjectBugResponse>;
	removeProjectBug: (
		payload: RemoveProjectBugPayload
	) => Promise<ProjectBugResponse>;
}

export interface ProjectBugResponse {
	projectId: string;
	bug: Bug;
}

export interface CreateProjectPayload {
	name: string;
	manager: string;
	team?: string[];
}

export interface DeleteProjectPayload {
	projectId: string;
}

export interface AddProjectBugPayload {
	title: string;
	description: string;
	projectId: string;
	tags?: string[];
}

export interface ResolveProjectBugPayload {
	projectId: string;
	bugId: string;
	resolverId: string;
}

export interface RemoveProjectBugPayload {
	projectId: string;
	bugId: string;
}
