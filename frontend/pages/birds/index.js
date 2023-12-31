import Link from "next/link";
import React, { useState, useEffect } from "react";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Unstable_Grid2";
import Stack from "@mui/material/Stack";
import Box from "@mui/material/Box";
import Pagination from "@mui/material/Pagination";
import Button from "@mui/material/Button";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import HomeIcon from "@mui/icons-material/Home";
import EditIcon from "@mui/icons-material/Edit";
import Alert from "@mui/material/Alert";
import Tooltip from "@mui/material/Tooltip";
import CircularProgress from "@mui/material/CircularProgress";
import FormatListBulletedSharpIcon from '@mui/icons-material/FormatListBulletedSharp';
import { useToken } from "../../components/tokenContext";

const urlBase = process.env.NEXT_PUBLIC_BASEURL;
const fallbackBird =
  "https://tse1.mm.bing.net/th/id/OIP.VnKF_9XCsYHFrI4TZGritgHaFE?rs=1&pid=ImgDetMain";

const Birds = () => {
  const [data, setData] = useState(null);
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { token, ownerRole } = useToken();
  const [page, setPage] = useState(1);

  useEffect(() => {
    if (token) {
      setLoading(true);
      fetch(`${urlBase}/birds?page=${page || 1}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => res.json())
        .then((data) => {
          setData(data);
        })
        .catch((e) => setError(e.message))
        .finally(() => setLoading(false));
    }
  }, [token, page]);

  const handlePageChange = (event, value) => {
    setPage(value);
  };

  if (isLoading) return <CircularProgress color="secondary" />;
  if (!data || !data?.birds)
    return <Alert severity="warning">No bird data</Alert>;

  return (
    <Container maxWidth="lg">
      <Typography variant="h1" gutterBottom>
        Birds Of The World.
      </Typography>
      <Stack direction="row" justifyContent="space-between" pb={2}>
        {ownerRole && (
          <Link href="/birds/form" passHref>
            <Button endIcon={<AddCircleOutlineIcon />}>Add a new Bird</Button>
          </Link>
        )}
        <Link href="/habitats" passHref>
          <Button endIcon={<FormatListBulletedSharpIcon />}>View Habitats</Button>
        </Link>
        <Link href="/" passHref>
          <Button endIcon={<HomeIcon />}>Home</Button>
        </Link>
      </Stack>
      {error && <Alert severity="error">{error}</Alert>}
      <Grid container spacing={0}>
        <Grid xs={2}>
          <Typography variant="h3">Name</Typography>
        </Grid>
        <Grid xs={3}>
          <Typography variant="h3">Image</Typography>
        </Grid>
        <Grid xs={3}>
          <Typography variant="h3">Habitats</Typography>
        </Grid>
        <Grid xs={3}>
          <Typography variant="h3">Regions</Typography>
        </Grid>
      </Grid>
      <Box
        sx={{
          borderTop: "1px solid",
          borderRight: "1px solid",
          borderColor: "grey.600",
        }}
      >
        {data?.birds?.map?.((bird) => (
          <Grid
            container
            spacing={0}
            key={`${bird?.common_name}`}
            sx={{
              borderBottom: "1px solid",
              borderColor: "grey.600",
            }}
          >
            <Grid
              xs={2}
              sx={{
                borderLeft: "1px solid",
                borderColor: "grey.600",
              }}
            >
              <Stack p={1} spacing={2}>
                <Typography variant="h4">{bird?.common_name}</Typography>
                <Typography variant="h5">{bird?.species}</Typography>
                {ownerRole && (
                  <Link href={`birds/form?bird=${bird?.id}`} passHref>
                    <Button endIcon={<EditIcon />}>Edit Bird</Button>
                  </Link>
                )}
              </Stack>
            </Grid>
            <Grid
              xs={3}
              sx={{
                borderLeft: "1px solid",
                borderColor: "grey.600",
              }}
            >
              <img
                src={bird?.image_link || fallbackBird}
                title={bird?.common_name}
                alt={bird?.common_name}
                style={{ width: "100%" }}
                onError={(e) => {
                  e.currentTarget.onerror = null;
                  e.currentTarget.src = fallbackBird;
                }}
              />
            </Grid>
            <Grid
              xs={3}
              sx={{
                borderLeft: "1px solid",
                borderColor: "grey.600",
              }}
            >
              <Stack component="ul" spacing={1}>
                {bird?.habitats?.map?.((habitat) => (
                  <li key={`${bird?.common_name}-${habitat?.id}`}>
                    {ownerRole ? (
                      <Tooltip title="Edit Habitat" placement="right">
                        <Link href={`habitats/form?habitat=${habitat?.id}`}>
                          <Typography
                            variant="body1"
                            sx={{ display: "inline" }}
                          >
                            {habitat?.name}
                          </Typography>
                        </Link>
                      </Tooltip>
                    ) : (
                      <Typography variant="body1">{habitat?.name}</Typography>
                    )}
                  </li>
                ))}
              </Stack>
            </Grid>
            <Grid
              container
              spacing={0}
              xs={4}
              sx={{
                borderLeft: "1px solid",
                borderLeftColor: "grey.600",
              }}
            >
              {bird?.regions?.map?.((region) => {
                const size = 12 / bird?.regions.length;
                return (
                  <Grid
                    key={`${bird?.common_name}-${region?.name}`}
                    xs={size > 6 ? size : 6}
                  >
                    <img
                      src={region?.image}
                      style={{ width: "100%", maxWidth: 180 }}
                      title={region?.name}
                    />
                  </Grid>
                );
              })}
            </Grid>
          </Grid>
        ))}
      </Box>
      <Pagination
        color="primary"
        variant="outlined"
        count={Math.ceil(data?.total_birds / 10) || 10}
        page={page}
        onChange={handlePageChange}
        sx={{ paddingTop: "1.2rem", paddingBottom: "1.2rem" }}
      />
      <Alert severity="info">
        Orthographic projection from Wikipedia Commons.
        <a
          href="/wiki/Commons:GNU_Free_Documentation_License,_version_1.2"
          title="Commons:GNU Free Documentation License, version 1.2"
        >
          GNU Free Documentation License.
        </a>
        <a
          href="https://en.wikipedia.org/wiki/en:Creative_Commons"
          title="w:en:Creative Commons"
        >
          Creative Commons.
        </a>
      </Alert>
    </Container>
  );
};
export default Birds;
