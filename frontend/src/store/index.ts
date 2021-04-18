import { configureStore } from "@reduxjs/toolkit";
import { combineReducers } from "@reduxjs/toolkit";
import entitiesReducer from "./entities";

const rootReducer = combineReducers({
	entities: entitiesReducer,
});

export type StoreState = ReturnType<typeof rootReducer>;
export default configureStore({
	reducer: rootReducer,
});
