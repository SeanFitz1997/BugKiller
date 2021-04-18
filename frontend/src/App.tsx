import { useEffect } from "react";
import { Provider } from "react-redux";
import store from "./store";
import {
	addProjectBug,
	createProject,
	deleteProject,
	loadProjects,
	removeProjectBug,
	resolveProjectBug,
} from "./store/entities/project/asyncActions";
import ProjectList from "./components/ProjectList";

export default function App() {
	useEffect(() => {
		// Load projects
		store.dispatch(loadProjects());

		// Create new project
		store.dispatch(
			createProject({
				name: "A new project",
				manager: "MANAGER-ID",
			})
		);

		// Delete project
		store.dispatch(
			deleteProject({
				projectId: "2",
			})
		);

		// Add a bug project bug
		store.dispatch(
			addProjectBug({
				projectId: "1",
				title: "this is a test bug",
				description: "...",
			})
		);

		// Resolve a bug
		store.dispatch(
			resolveProjectBug({
				projectId: "1",
				bugId: "1",
				resolverId: "USER-1",
			})
		);

		// Remove project bug
		store.dispatch(
			removeProjectBug({
				projectId: "3",
				bugId: "1",
			})
		);
	}, []);

	return (
		<Provider store={store}>
			<div className="App">
				<h1>Redux Demo</h1>
				<ProjectList />
			</div>
		</Provider>
	);
}
