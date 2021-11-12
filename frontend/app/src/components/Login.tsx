import { useContext, useState } from "react";
import { UserContext } from "../providers/UserProvider";
import authClient from "../services/auth/authClient";

const Login = () => {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const { setCurrentUser } = useContext(UserContext);

	const handleSubmit = (e: React.SyntheticEvent): void => {
		e.preventDefault();
		authClient.logIn(email, password).then((_) => {
			setCurrentUser(authClient.getCurrentUser());
		});
	};

	return (
		<form onSubmit={handleSubmit}>
			<h1>Login</h1>
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

export default Login;
