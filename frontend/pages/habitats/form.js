import Link from "next/link";
import React from "react";
import HabitatForm from "../../components/habitat/form";
import DeleteResource from "../../components/delete";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import HomeIcon from "@mui/icons-material/Home";
import FavoriteBorderSharpIcon from "@mui/icons-material/FavoriteBorderSharp";
import FormatListBulletedSharpIcon from '@mui/icons-material/FormatListBulletedSharp';

const Habitat = () => {
  return (
    <Container maxWidth="lg">
      <Typography variant="h1" gutterBottom>
        Birds Of The World.
      </Typography>
      <Stack direction="row" justifyContent="space-between" pb={4}>
        <Link href="/birds" passHref>
          <Button endIcon={<FavoriteBorderSharpIcon />}>View all Birds</Button>
        </Link>
        <Link href="/habitats" passHref>
          <Button endIcon={<FormatListBulletedSharpIcon />}>View all Habitats</Button>
        </Link>
        <Link href="/" passHref>
          <Button endIcon={<HomeIcon />}>Home</Button>
        </Link>
      </Stack>
      <Typography variant="h2" gutterBottom>
        Fill in the Habitat Form
      </Typography>
      <HabitatForm edit />
      <DeleteResource />
    </Container>
  );
};
export default Habitat;
