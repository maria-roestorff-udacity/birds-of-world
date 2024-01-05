import Link from "next/link";
import React, { useState, useEffect } from "react";
import Grid from "@mui/system/Unstable_Grid";
import Stack from "@mui/system/Stack";
import { useToken } from "../../components/tokenContext";

const urlBase = process.env.NEXT_PUBLIC_BASEURL;

const Birds = () => {
  const [data, setData] = useState(null);
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { token } = useToken();

  useEffect(() => {
    if (token) {
      setLoading(true);
      fetch(`${urlBase}/birds`, {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => res.json())
        .then((data) => {
          setData(data);
        })
        .catch((error) => setError(error.message))
        .finally(() => setLoading(false));
    }
  }, [token]);

  if (isLoading) return <p>Loading...</p>;
  if (!data || !data?.birds) return <p>No profile data</p>;

  return (
    <div>
      <h1>Birds Of The World</h1>
      <Link href="birds/form" passHref>
        <button type="button">Add a new Bird</button>
      </Link>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <Grid container spacing={2}>
        <Grid xs={2}>
          <h2>Name</h2>
        </Grid>
        <Grid xs={3} ml={1}>
          <h2>Image</h2>
        </Grid>
        <Grid xs={3} ml={1}>
          <h2>Habitats</h2>
        </Grid>
        <Grid xs={3} ml={1}>
          <h2>Regions</h2>
        </Grid>
      </Grid>
      {data?.birds.map((bird) => (
        <Grid container spacing={3} mb={1.5} key={`${bird?.common_name}`}>
          <Grid xs={2} style={{ border: "1px solid #80808075" }}>
            <h3>{bird?.common_name}</h3>
            <br />
            <h5 style={{ fontStyle: "italic" }}>{bird?.species}</h5>
            <Link href={`birds/form?bird=${bird?.id}`}>Edit Bird</Link>
          </Grid>
          <Grid xs={3} style={{ border: "1px solid #80808075" }}>
            <img
              src={bird?.image_link}
              alt="External Image"
              style={{ width: "100%" }}
            />
          </Grid>
          <Grid xs={3} style={{ border: "1px solid #80808075" }}>
            <Stack component="ul" spacing={1}>
              {bird?.habitats.map((habitat) => (
                <li key={`${bird.common_name}-${habitat?.id}`}>
                  <Link href={`habitats?habitat=${habitat?.id}`}>
                    {habitat?.name}
                  </Link>
                </li>
              ))}
            </Stack>
          </Grid>
          <Grid
            container
            spacing={0}
            xs={4}
            style={{ border: "1px solid #80808075" }}
          >
            {bird.regions.map((region) => {
              const size = 12 / bird.regions.length;
              return (
                <Grid
                  key={`${bird.common_name}-${region.name}`}
                  xs={size > 4 ? size : 4}
                >
                  <img
                    src={region.image}
                    alt="External Image"
                    style={{ width: "100%" }}
                  />
                </Grid>
              );
            })}
          </Grid>
        </Grid>
      ))}
    </div>
  );
};
export default Birds;
