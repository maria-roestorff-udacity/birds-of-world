import Router from "next/router";
import { Auth0Provider } from "@auth0/auth0-react";
import TokenContextProvider from "../components/tokenContext";

const onRedirectCallback = (appState) => {
  // Use Next.js's Router.replace method to replace the url
  Router.replace(appState?.returnTo || "/");
};

export default function MyApp({ Component, pageProps }) {
  return (
    <Auth0Provider
      domain={process.env.AUTH0_URL}
      clientId={process.env.AUTH0_CLIENT_ID}
      onRedirectCallback={onRedirectCallback}
      authorizationParams={{
        redirect_uri:
          typeof window !== "undefined" ? window.location.origin : undefined,
        prompt: "consent",
      }}
    >
      <TokenContextProvider>
        <Component {...pageProps} />
      </TokenContextProvider>
    </Auth0Provider>
  );
}
