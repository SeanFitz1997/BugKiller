import { StoreState } from "../../../../store";
import {
	Bug,
	Project,
	ProjectState,
} from "../../../../store/entities/project/types";
import {
	getProjectState,
	findProjectIndex,
	findProject,
	findBug,
	findBugIndex,
} from "../../../../store/entities/project/utils";

describe("projects utils", () => {
	/* Note: This test data should be read only */

	const bug1: Bug = Object.freeze({
		id: "1",
		title: "Bug1",
		description: "Test",
		tags: [],
		resolved: null,
	});

	const bug2: Bug = Object.freeze({
		id: "2",
		title: "Bug2",
		description: "Test",
		tags: [],
		resolved: null,
	});

	const project1: Project = Object.freeze({
		id: "1",
		name: "Project1",
		manager: "M",
		bugs: [bug1, bug2],
		team: [],
	});

	const project2: Project = Object.freeze({
		id: "2",
		name: "Project2",
		manager: "M",
		bugs: [],
		team: [],
	});

	const project3: Project = Object.freeze({
		id: "3",
		name: "Project3",
		manager: "M",
		bugs: [],
		team: [],
	});

	const projectState: ProjectState = Object.freeze({
		isLoading: false,
		lastFetched: null,
		projects: [project1, project2, project3],
	});

	const storeState: StoreState = Object.freeze({
		entities: {
			projects: projectState,
		},
	});

	describe("getProjectState", () => {
		it("should return project state", () => {
			expect(getProjectState(storeState)).toBe(projectState);
		});
	});

	describe("findProjectIndex", () => {
		it("should return the index of the project when it is in the project state", () => {
			expect(
				findProjectIndex(projectState, project1.id)
			).toBeGreaterThanOrEqual(0);
		});

		it("should return null when the project is not in the project state", () => {
			expect(findProjectIndex(projectState, "X")).toBeNull();
		});
	});

	describe("findProject", () => {
		it("should return the project if it is in the project state", () => {
			expect(findProject(projectState, project1.id)).toBe(project1);
		});

		it("should return null of the project is not in the project state", () => {
			expect(findProject(projectState, "X")).toBeNull();
		});
	});

	describe("findBugIndex", () => {
		it("should return the index of the bug if it is in the project", () => {
			expect(findBugIndex(project1, bug1.id)).toBeGreaterThanOrEqual(0);
		});

		it("should return null if the bug is not in the project", () => {
			expect(findBugIndex(project1, "X")).toBeNull();
		});
	});

	describe("findBug", () => {
		it("should return the bug if it is in the project", () => {
			expect(findBug(projectState, project1.id, bug1.id)).toBe(bug1);
		});

		it("should return null if the bug is not in the project", () => {
			expect(findBug(projectState, project1.id, "X")).toBeNull();
		});

		it("should return null if the project does not exist", () => {
			expect(findBug(projectState, "X", "X")).toBeNull();
		});
	});
});

export {};
