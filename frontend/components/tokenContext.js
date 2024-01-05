import { useState, createContext, useEffect, useMemo, useContext } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useRouter } from "next/router";
import * as jose from "jose";

const TokenContext = createContext();

const TokenContextProvider = ({ children }) => {
  const { getAccessTokenSilently, isAuthenticated, user } = useAuth0();
  const router = useRouter();
  const [token, setToken] = useState(null);
  const [ownerRole, setOwnerRole] = useState(false);

  useEffect(() => {
    if (!token) {
      (async () => {
        try {
          const getToken = await getAccessTokenSilently({
            authorizationParams: {
              audience: process.env.AUTH0_AUDIENCE,
            },
          });
          setToken(getToken);
          console.log(getToken);
          const claims = jose.decodeJwt(getToken);
          console.log(claims?.permissions);

          const ownerRolePer = [
            "delete:birds",
            "delete:habitats",
            "get:birds",
            "get:habitats",
            "get:regions",
            "patch:birds",
            "patch:habitats",
            "post:birds",
            "post:habitats",
          ];

          if (
            ownerRolePer.every((ownerRole) =>
              claims?.permissions.includes(ownerRole)
            )
          ) {
            setOwnerRole(true);
          }
        } catch (e) {
          // Handle errors such as `login_required` and `consent_required` by re-prompting for a login
          console.error(e);
          router.push("/");
          // loginWithRedirect();
        }
      })();
    }
  }, [getAccessTokenSilently]);

  const contextValue = useMemo(
    () => ({
      token,
      ownerRole,
    }),
    [token]
  );

  return (
    <TokenContext.Provider value={contextValue}>
      {children}
    </TokenContext.Provider>
  );
};

export default TokenContextProvider;

export const useToken = () => {
  return useContext(TokenContext);
};
