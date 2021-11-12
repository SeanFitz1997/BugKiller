import { useState } from "react";
import authClient from "../services/auth/authClient";

const SignUp = () => {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	const handleSubmit = (e: React.SyntheticEvent): void => {
		e.preventDefault();
		authClient.signUp(email, password);
	};

	return (
		<form onSubmit={handleSubmit}>
			<h1>Sign Up</h1>
			<input
				title="Email"
				value={email}
				onChange={(e) => setEmail(e.target.value)}
			/>
			<input
				title="Password"
				value={password}
				onChange={(e) => setPassword(e.target.value)}
			/>
			<input type="submit" />
		</form>
	);
};

export default SignUp;
