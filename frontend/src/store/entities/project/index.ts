import { ActionReducerMapBuilder, createSlice } from "@reduxjs/toolkit";
import {
	addProjectBug,
	createProject,
	deleteProject,
	loadProjects,
	removeProjectBug,
	resolveProjectBug,
} from "./asyncActions";
import {
	setProjectsReducer,
	addCreatedProjectReducer,
	removeDeletedProjectBugReducer,
	addCreatedProjectBugReducer,
	removeDeletedProjectReducer,
	updateResolvedProjectBugReducer,
} from "./reducers";
import { ProjectState } from "./types";

const INITIAL_STATE: ProjectState = {
	projects: [],
	isLoading: false,
	lastFetched: null,
};

const slice = createSlice({
	name: "projects",
	initialState: INITIAL_STATE,
	reducers: {},
	extraReducers: (builder: ActionReducerMapBuilder<ProjectState>) => {
		builder.addCase(loadProjects.fulfilled, setProjectsReducer);
		builder.addCase(createProject.fulfilled, addCreatedProjectReducer);
		builder.addCase(deleteProject.fulfilled, removeDeletedProjectReducer);
		builder.addCase(addProjectBug.fulfilled, addCreatedProjectBugReducer);
		builder.addCase(
			removeProjectBug.fulfilled,
			removeDeletedProjectBugReducer
		);
		builder.addCase(
			resolveProjectBug.fulfilled,
			updateResolvedProjectBugReducer
		);
	},
});

export default slice.reducer;
