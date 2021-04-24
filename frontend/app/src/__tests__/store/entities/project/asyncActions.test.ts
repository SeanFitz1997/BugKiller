jest.mock("../../../../services/projects/MockProjectClient");

import {
	loadProjects,
	createProject,
	deleteProject,
	addProjectBug,
	resolveProjectBug,
	removeProjectBug,
} from "../../../../store/entities/project/asyncActions";
import { testBug, testProject } from "./sharedTestData";

describe("project asyncActions", () => {
	const dispatch = jest.fn();
	const getState = jest.fn();

	describe("loadProjects", () => {
		it("returns a list of projects on success", async () => {
			const response = await loadProjects()(dispatch, getState, {});
			expect(response.payload).toEqual([testProject]);
		});
	});

	describe("createProject", () => {
		it("returns the created project on success", async () => {
			const response = await createProject({
				name: testProject.name,
				manager: testProject.manager,
			})(dispatch, getState, {});
			expect(response.payload).toEqual(testProject);
		});
	});

	describe("deleteProject", () => {
		it("returns the deleted project on success", async () => {
			const response = await deleteProject({
				projectId: testProject.id,
			})(dispatch, getState, {});
			expect(response.payload).toEqual(testProject);
		});
	});

	describe("addProjectBug", () => {
		it("returns the added bug on success", async () => {
			const { title, description } = testBug;
			const response = await addProjectBug({
				projectId: testProject.id,
				title,
				description,
			})(dispatch, getState, {});
			expect(response.payload).toEqual({
				projectId: testProject.id,
				bug: testBug,
			});
		});
	});

	describe("resolveProjectBug", () => {
		it("returns the resolved bug on success", async () => {
			const response = await resolveProjectBug({
				projectId: testProject.id,
				bugId: testBug.id,
				resolverId: "U",
			})(dispatch, getState, {});
			expect(response.payload).toEqual({
				projectId: testProject.id,
				bug: testBug,
			});
		});
	});

	describe("removeProjectBug", () => {
		it("returns the removed bug on success", async () => {
			const response = await removeProjectBug({
				projectId: testProject.id,
				bugId: testBug.id,
			})(dispatch, getState, {});
			expect(response.payload).toEqual({
				projectId: testProject.id,
				bug: testBug,
			});
		});
	});
});

export {};
