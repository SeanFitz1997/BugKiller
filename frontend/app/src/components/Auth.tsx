import { useContext } from "react";
import { UserContext } from "../providers/UserProvider";
import Login from "./Login";
import SignUp from "./SignUp";

const Auth = () => {
	const { currentUser } = useContext(UserContext);
	return (
		<>
			{currentUser ? (
				<p>Logged in</p>
			) : (
				<>
					{" "}
					<SignUp />
					<Login />
				</>
			)}
		</>
	);
};

export default Auth;
