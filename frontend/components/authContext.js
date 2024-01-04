import { useState, createContext, useContext } from "react";

const AuthContext = createContext();

const AuthContextProvider = ({ children }) => {
  const getSession = () => {
    return JSON.parse(localStorage.getItem("session"));
  };

  const setSessionInLocalStorage = (token) => {
    localStorage.setItem("session", JSON.stringify(token));
    return true;
  };

  const auth = getSession();

  const [session, setSession] = useState(auth || "");

  const setAuth = (token) => {
    setSession(token);
    setSessionInLocalStorage(token);
  };

  const logout = () => {
    setAuth("");
  };

  const { user, token } = session;

  //Auth API logic here//




  return (
    <AuthContext.Provider value={{ user, token, setAuth }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContextProvider;

export const useAuth = () => {
  return useContext(AuthContext);
};

useEffect(() => {
    if (router.isReady) {
      const id3 = router.asPath;
      const origin =
        typeof window !== "undefined" && window.location.origin
          ? window.location.origin
          : "";

      console.log(id3);
    }
  }, [router]);

  const audience = "";
  const client_id = "";
  const redirect_uri = "";
  const authUrl =
    "" +
    "/authorize?" +
    `audience=${audience}&` +
    "response_type=token&" +
    `client_id=${client_id}&` +
    `redirect_uri=${redirect_uri}&` +
    "state=helpme123";


    <a href={authUrl}>Sign In</a>

    const router = useRouter();
    const [token, setToken] = useState(null);