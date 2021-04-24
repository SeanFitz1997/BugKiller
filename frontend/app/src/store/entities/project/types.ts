/*=== State ===*/

export interface ProjectState {
	projects: Project[];
	isLoading: boolean;
	lastFetched: null | Date;
}

/*=== Entities ===*/

export interface Project {
	id: string;
	name: string;
	manager: string;
	team: string[];
	bugs: Bug[];
}

export interface Bug {
	id: string;
	title: string;
	description: string;
	tags: Tags;
	resolved: BugResolution | null;
}

export interface BugResolution {
	resolverId: string;
	resolvedAt: number;
}

type Tags = string[];

/*=== Selector Filters ===*/

export interface BugSelectorFilter {
	isResolved?: boolean;
	tags?: Tags;
}
