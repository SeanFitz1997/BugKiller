export class MissingEnvironmentVariableError extends Error {
	constructor(variableName: string) {
		const msg = `Missing required environment variable ${variableName}`;
		super(msg);
	}
}
