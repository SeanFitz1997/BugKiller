import { createAsyncThunk } from "@reduxjs/toolkit";
import { Project } from "./types";
import projectClient from "../../../services/projects/MockProjectClient";
import {
	CreateProjectPayload,
	DeleteProjectPayload,
	ProjectBugResponse,
	AddProjectBugPayload,
	ResolveProjectBugPayload,
	RemoveProjectBugPayload,
} from "../../../services/projects/types";

export const loadProjects = createAsyncThunk<Project[]>(
	"projects/loadProjects",
	async () => {
		return await projectClient.loadProjects();
	}
);

export const createProject = createAsyncThunk<Project, CreateProjectPayload>(
	"projects/createProject",
	async (payload) => {
		return await projectClient.createProject(payload);
	}
);

export const deleteProject = createAsyncThunk<Project, DeleteProjectPayload>(
	"projects/deleteProject",
	async (payload) => {
		return await projectClient.deleteProject(payload);
	}
);

export const addProjectBug = createAsyncThunk<
	ProjectBugResponse,
	AddProjectBugPayload
>("projects/addProjectBug", async (payload) => {
	return await projectClient.addProjectBug(payload);
});

export const removeProjectBug = createAsyncThunk<
	ProjectBugResponse,
	RemoveProjectBugPayload
>("projects/removeProjectBug", async (payload) => {
	return projectClient.removeProjectBug(payload);
});

export const resolveProjectBug = createAsyncThunk<
	ProjectBugResponse,
	ResolveProjectBugPayload
>("projects/resolveProjectBug", async (payload) => {
	return await projectClient.resolveProjectBug(payload);
});
