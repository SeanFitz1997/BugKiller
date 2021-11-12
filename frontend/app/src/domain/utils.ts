import { MissingEnvironmentVariableError } from "./errors";

export function getRequiredEnvironmentVariable(variableName: string): string {
	const variable = process.env[variableName];
	if (!variable) throw new MissingEnvironmentVariableError(variableName);
	return variable;
}
