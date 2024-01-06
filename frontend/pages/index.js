import Link from "next/link";
import { useAuth0 } from "@auth0/auth0-react";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import LogoutIcon from "@mui/icons-material/Logout";
import LoginIcon from "@mui/icons-material/Login";
import FavoriteBorderSharpIcon from "@mui/icons-material/FavoriteBorderSharp";
import FormatListBulletedSharpIcon from '@mui/icons-material/FormatListBulletedSharp';
import Alert from "@mui/material/Alert";

export default function Index() {
  const { loginWithRedirect, user, error, logout } = useAuth0();

  if (error) return <Alert severity="error">{error.message}</Alert>;

  return (
    <Container maxWidth="lg">
      <Typography variant="h1" style={{ textAlign: "center" }}>
        Welcome to Birds of The World
      </Typography>
      {user && (
        <Typography variant="h2" gutterBottom style={{ textAlign: "center" }}>
          {user.name}!
        </Typography>
      )}
      <Stack direction="row" spacing={2} justifyContent="center">
        {user ? (
          <>
            <Button
              onClick={() => {
                logout({
                  logoutParams: {
                    returnTo: window.location.origin,
                  },
                });
              }}
              endIcon={<LogoutIcon />}
            >
              Log out
            </Button>
            <Link href="/birds" passHref>
              <Button endIcon={<FavoriteBorderSharpIcon />}>View Birds</Button>
            </Link>
            <Link href="/habitats" passHref>
              <Button endIcon={<FormatListBulletedSharpIcon />}>View Habitats</Button>
            </Link>
          </>
        ) : (
          <Button onClick={() => loginWithRedirect()} endIcon={<LoginIcon />}>
            Log In
          </Button>
        )}
      </Stack>
    </Container>
  );
}
