import Router from "next/router";
import { Auth0Provider } from "@auth0/auth0-react";

const onRedirectCallback = (appState) => {
  // Use Next.js's Router.replace method to replace the url
  Router.replace(appState?.returnTo || "/");
};

console.log();

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
      ge
    >
      <Component {...pageProps} />
    </Auth0Provider>
  );
}
