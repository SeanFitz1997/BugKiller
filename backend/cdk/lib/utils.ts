export function snakeCaseToTitleCase(str: string): string {
	/**
	 * TODO
	 */
	return str
		.split("_")
		.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
		.join("");
}
