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
import FavoriteBorderSharpIcon from "@mui/icons-material/FavoriteBorderSharp";
import { useToken } from "../../components/tokenContext";

const urlBase = process.env.NEXT_PUBLIC_BASEURL;
const fallbackBird =
  "https://tse1.mm.bing.net/th/id/OIP.VnKF_9XCsYHFrI4TZGritgHaFE?rs=1&pid=ImgDetMain";

const Birds = () => {
  const [data, setData] = useState(null);
  const [regions, setRegions] = useState(null);
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { token, ownerRole } = useToken();
  const [page, setPage] = useState(1);

  useEffect(() => {
    if (token) {
      setLoading(true);
      fetch(`${urlBase}/habitats?page=${page || 1}`, {
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

  useEffect(() => {
    if (token) {
      setLoading(true);
      fetch(`${urlBase}/regions`, {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => res.json())
        .then((respData) => {
          const regionsMap = {};
          respData?.regions?.forEach?.((region) => {
            regionsMap[region.id] = region;
          });
          setRegions(regionsMap);
        })
        .catch((e) => setError(e.message))
        .finally(() => setLoading(false));
    }
  }, [token]);

  const handlePageChange = (event, value) => {
    setPage(value);
  };

  if (isLoading) return <CircularProgress color="secondary" />;
  if (!data || !data?.habitats)
    return <Alert severity="warning">No habitat data</Alert>;

  console.log('data', data)

  return (
    <Container maxWidth="lg">
      <Typography variant="h1" gutterBottom>
        Birds Of The World.
      </Typography>
      <Stack direction="row" justifyContent="space-between" pb={2}>
        {ownerRole && (
          <Link href="/habitats/form" passHref>
            <Button endIcon={<AddCircleOutlineIcon />}>Add a new Habitat</Button>
          </Link>
        )}
        <Link href="/birds" passHref>
          <Button endIcon={<FavoriteBorderSharpIcon />}>View Birds</Button>
        </Link>
        <Link href="/" passHref>
          <Button endIcon={<HomeIcon />}>Home</Button>
        </Link>
      </Stack>
      {error && <Alert severity="error">{error}</Alert>}
      <Stack direction="row" justifyContent="center" pb={2}>
        <Grid container spacing={0} width={600}>
          <Grid xs={8}>
            <Typography variant="h3">Habitat</Typography>
          </Grid>
          <Grid xs={4}>
            <Typography variant="h3">Region</Typography>
          </Grid>
        </Grid>
      </Stack>
      <Stack direction="row" justifyContent="center" pb={2}>
        <Box
          sx={{
            borderTop: "1px solid",
            borderRight: "1px solid",
            borderColor: "grey.600",
          }}
          width={600}
        >
          {data?.habitats?.map?.((habitat) => (
            <Grid
              container
              spacing={0}
              key={`${habitat?.name}`}
              sx={{
                borderBottom: "1px solid",
                borderColor: "grey.600",
              }}
              height={185}
            >
              <Grid
                xs={8}
                sx={{
                  borderLeft: "1px solid",
                  borderColor: "grey.600",
                }}
                height={185}
              >
                <Stack p={1} spacing={2}>
                  {ownerRole ? (
                      <Tooltip title="Edit Habitat" placement="top-start">
                        <Link href={`habitats/form?habitat=${habitat?.id}`}>
                          <Typography
                            variant="h4"
                            sx={{ display: "inline" }}
                          >
                            {habitat?.name}
                          </Typography>
                        </Link>
                      </Tooltip>
                    ) : (
                      <Typography variant="h4">{habitat?.name}</Typography>
                    )}
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
                height={185}
              >
                {!regions?.[habitat?.region_id] ? null : (
                  <Grid
                    key={`${habitat?.name}-${regions[habitat.region_id]?.name}`}
                    xs={12}
                  >
                    <img
                      src={regions[habitat.region_id]?.image_link}
                      style={{ width: "100%", maxWidth: 180 }}
                      title={regions[habitat.region_id]?.name}
                    />
                  </Grid>
                )}
              </Grid>
            </Grid>
          ))}
        </Box>
      </Stack>
      <Pagination
        color="primary"
        variant="outlined"
        count={Math.ceil(data?.total_habitats / 10) || 10}
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
