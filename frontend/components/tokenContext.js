import { useState, createContext, useEffect, useMemo, useContext } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useRouter } from "next/router";

const TokenContext = createContext();

const TokenContextProvider = ({ children }) => {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();
  const router = useRouter();
  const [token, setToken] = useState(null);

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
        } catch (e) {
          // Handle errors such as `login_required` and `consent_required` by re-prompting for a login
          console.error(e);
          router.push("/")
          // loginWithRedirect();
        }
      })();
    }
  }, [getAccessTokenSilently]);

  const contextValue = useMemo(
    () => ({
      token,
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
