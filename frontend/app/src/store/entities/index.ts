import { combineReducers } from "@reduxjs/toolkit";
import projectsReducer from "./project";

const entitiesReducer = combineReducers({
	projects: projectsReducer,
});

export default entitiesReducer;
export type EntitiesState = ReturnType<typeof entitiesReducer>;
