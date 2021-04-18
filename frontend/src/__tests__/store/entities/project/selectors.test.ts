import { StoreState } from "../../../../store";
import {
	getProject,
	getProjectBugs,
	getProjects,
} from "../../../../store/entities/project/selectors";
import {
	Bug,
	Project,
	ProjectState,
} from "../../../../store/entities/project/types";
import {
	testBug,
	testBugResolution,
	testProject,
	testProjectState,
	testStoreState,
} from "./sharedTestData";

describe("project selectors", () => {
	describe("getProjects", () => {
		it("should get all projects", () => {
			const projectState: ProjectState = {
				...testProjectState,
				projects: [testProject],
			};

			const storeState: StoreState = {
				...testStoreState,
				entities: {
					projects: projectState,
				},
			};
			expect(getProjects(storeState)).toEqual([testProject]);
		});
	});

	describe("getProject", () => {
		it("should get project by id", () => {
			const projectState: ProjectState = {
				...testProjectState,
				projects: [testProject],
			};

			const storeState: StoreState = {
				...testStoreState,
				entities: {
					projects: projectState,
				},
			};

			getProject(testProject.id)(storeState);
		});

		it("should return null if the project does not exist", () => {
			expect(getProject("X")(testStoreState)).toBeNull();
		});
	});

	describe("getProjectBugs", () => {
		const bug1: Bug = { ...testBug, id: "1" };
		const bug2: Bug = { ...testBug, id: "2", tags: ["foo", "bar"] };
		const bug3: Bug = {
			...testBug,
			id: "3",
			resolved: testBugResolution,
			tags: ["test"],
		};

		const project: Project = { ...testProject, bugs: [bug1, bug2, bug3] };

		const projectState: ProjectState = {
			...testProjectState,
			projects: [project],
		};

		const storeState: StoreState = {
			...testStoreState,
			entities: {
				projects: projectState,
			},
		};

		it("should return all project bugs when given no filters", () => {
			const result = getProjectBugs(testProject.id)(storeState);
			expect(result).toEqual([bug1, bug2, bug3]);
		});

		it("gets bugs with all tags given in the tag filter", () => {
			const result = getProjectBugs(testProject.id, {
				tags: ["foo", "bar"],
			})(storeState);
			expect(result).toEqual([bug2]);
		});

		it("gets all resolved bugs when given resolved filter set to true", () => {
			const result = getProjectBugs(testProject.id, { isResolved: true })(
				storeState
			);
			expect(result).toEqual([bug3]);
		});

		it('gets all unresolved bugs with tag "test" when given these filters', () => {
			const result = getProjectBugs(testProject.id, {
				isResolved: true,
				tags: ["test"],
			})(storeState);
			expect(result).toEqual([bug3]);
		});

		it("returns an empty list when the project does not exist", () => {
			const result = getProjectBugs("X")(storeState);
			expect(result).toEqual([]);
		});
	});
});

export {};
