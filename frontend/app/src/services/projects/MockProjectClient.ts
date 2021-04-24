import { v4 as uuid4 } from "uuid";
import { Bug, Project } from "../../store/entities/project/types";
import {
	AddProjectBugPayload,
	CreateProjectPayload,
	DeleteProjectPayload,
	ProjectBugResponse,
	ProjectsClient,
	RemoveProjectBugPayload,
	ResolveProjectBugPayload,
} from "./types";

class MockProjectClient implements ProjectsClient {
	private projects: Project[] = this.generateInitialProjects(10);

	public async loadProjects() {
		return this.projects;
	}

	public async createProject({
		manager,
		name,
		team = [],
	}: CreateProjectPayload): Promise<Project> {
		const project: Project = {
			id: uuid4(),
			name,
			manager,
			team,
			bugs: [],
		};
		this.projects = [...this.projects, project];
		return project;
	}

	public async deleteProject({
		projectId,
	}: DeleteProjectPayload): Promise<Project> {
		const index = this.getProjectIndex(projectId);
		const project = this.projects[index];
		this.projects.splice(index, 1);
		return project;
	}

	public async addProjectBug({
		projectId,
		title,
		description,
		tags = [],
	}: AddProjectBugPayload): Promise<ProjectBugResponse> {
		const project = this.getProject(projectId);
		const bug: Bug = {
			id: uuid4(),
			title,
			description,
			tags,
			resolved: null,
		};
		project.bugs.push(bug);
		return { projectId, bug };
	}

	public async resolveProjectBug({
		projectId,
		bugId,
		resolverId,
	}: ResolveProjectBugPayload): Promise<ProjectBugResponse> {
		const project = this.getProject(projectId);
		const bug = this.getProjectBug(project, bugId);
		bug.resolved = {
			resolverId,
			resolvedAt: 0,
		};
		return { projectId, bug };
	}

	public async removeProjectBug({
		projectId,
		bugId,
	}: RemoveProjectBugPayload): Promise<ProjectBugResponse> {
		const project = this.getProject(projectId);
		const index = this.getProjectBugIndex(project, bugId);
		const bug = project.bugs[index];
		project.bugs.splice(index, 1);
		return { projectId, bug };
	}

	private generateInitialProjects(n: number): Project[] {
		const projects: Project[] = [];
		for (let i = 0; i < n; i++) {
			const bug: Bug = {
				id: "1",
				title: "test bug",
				description: "test bug",
				tags: [],
				resolved: null,
			};
			const project: Project = {
				id: `${i}`,
				name: `Project ${i}`,
				manager: "M",
				bugs: [bug],
				team: [],
			};
			projects.push(project);
		}
		return projects;
	}

	private getProjectIndex(projectId: string): number {
		const index = this.projects.findIndex(
			(project) => project.id === projectId
		);
		if (index >= 0) {
			return index;
		}
		throw Error(`No project with id: ${projectId}`);
	}

	private getProject(projectId: string): Project {
		return this.projects[this.getProjectIndex(projectId)];
	}

	private getProjectBugIndex(project: Project, bugId: string): number {
		const index = project.bugs.findIndex((bug) => bug.id === bugId);
		if (index >= 0) {
			return index;
		}
		throw Error(`No bug with id: ${bugId} in project: ${project.id}`);
	}

	private getProjectBug(project: Project, bugId: string): Bug {
		return project.bugs[this.getProjectBugIndex(project, bugId)];
	}
}

export default new MockProjectClient();
