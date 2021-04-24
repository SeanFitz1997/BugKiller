import {
	testProject,
	testBug,
} from "../../../__tests__/store/entities/project/sharedTestData";
import { ProjectsClient } from "../types";

const mockProjectClient: ProjectsClient = {
	loadProjects: async () => [testProject],
	createProject: async () => testProject,
	deleteProject: async () => testProject,
	addProjectBug: async () => ({
		projectId: testProject.id,
		bug: testBug,
	}),
	resolveProjectBug: async () => ({
		projectId: testProject.id,
		bug: testBug,
	}),
	removeProjectBug: async () => ({
		projectId: testProject.id,
		bug: testBug,
	}),
};

export default mockProjectClient;
