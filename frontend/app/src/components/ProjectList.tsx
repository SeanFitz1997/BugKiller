import { useDispatch, useSelector } from "react-redux";
import {
	CreateProjectPayload,
	DeleteProjectPayload,
} from "../services/projects/types";
import {
	createProject,
	deleteProject,
} from "../store/entities/project/asyncActions";
import { getProjects } from "../store/entities/project/selectors";

/**
 * Just a demo
 */
const ProjectList = () => {
	const dispatch = useDispatch();
	const projects = useSelector(getProjects);

	const createProjectEvent: CreateProjectPayload = {
		name: "New Project",
		manager: "M",
	};

	const deleteProjectEvent: DeleteProjectPayload = {
		projectId: "1",
	};

	return (
		<div>
			<h1>Projects List</h1>
			<hr />
			<ul>
				{projects.map((project, i) => (
					<li key={i}>
						<pre>{JSON.stringify(project, null, 4)}</pre>
					</li>
				))}
			</ul>
			<hr />
			<button onClick={() => dispatch(createProject(createProjectEvent))}>
				Add project
			</button>
			<button onClick={() => dispatch(deleteProject(deleteProjectEvent))}>
				Delete project
			</button>
		</div>
	);
};

export default ProjectList;
