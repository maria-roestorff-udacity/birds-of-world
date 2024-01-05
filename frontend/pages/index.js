import Link from "next/link";
import { useAuth0 } from "@auth0/auth0-react";

export default function Index() {
  const { loginWithRedirect, user, error, logout } = useAuth0();

  // const checkClaims = (claim) =>
  //   claim?.[`https://${process.env.AUTH0_URL}/jwt/claims`]?.ROLE?.includes(
  //     "ADMIN"
  //   );

  // const checkClaims = (claim) =>
  //   claim?.["https://my.app.io/jwt/claims"]?.ROLE?.includes("ADMIN");

  // console.log(user?.logins_count);

  if (error) return <div>{error.message}</div>;

  if (user) {
    return (
      <div>
        <h1>Welcome to Birds of The World {user.name}!</h1>

        <button
          onClick={() => {
            logout({
              logoutParams: {
                returnTo: window.location.origin,
              },
            });
          }}
        >
          Log out
        </button>
        <Link href="/birds">Birds</Link>
      </div>
    );
  }

  return <button onClick={() => loginWithRedirect()}>Log In</button>;
}
