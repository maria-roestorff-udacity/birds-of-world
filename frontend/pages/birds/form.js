import Link from "next/link";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Box from "@mui/system/Box";
import HabitatForm from "../../components/habitat/form";
import AsyncSelect from "react-select/async";
import DeleteResource from "../../components/delete";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import HomeIcon from "@mui/icons-material/Home";
import FavoriteBorderSharpIcon from "@mui/icons-material/FavoriteBorderSharp";
import SaveOutlinedIcon from "@mui/icons-material/SaveOutlined";
import SearchIcon from "@mui/icons-material/Search";
import Alert from "@mui/material/Alert";
import TextField from "@mui/material/TextField";
import Tooltip from "@mui/material/Tooltip";
import { useToken } from "../../components/tokenContext";
import { styled } from "@mui/material/styles";

const urlBase = process.env.NEXT_PUBLIC_BASEURL;

const BirdsForm = () => {
  const router = useRouter();
  const { token } = useToken();

  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedHabitats, setSelectedHabitats] = useState(null);
  const [value, setValue] = useState({
    common_name: "",
    species: "",
    image_link: "",
    habitats: "",
  });

  useEffect(() => {
    if (router.isReady && token) {
      const id = router?.query?.bird;
      if (id) {
        setLoading(true);
        fetch(`${urlBase}/birds/${id}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.error) {
              throw new Error(
                `${
                  data.message ?? "failed to load data, please refresh page"
                } - Please return to the home page`
              );
            }
            const newValue = {
              common_name: data?.bird?.common_name,
              species: data?.bird?.species,
              image_link: data?.bird?.image_link,
              habitats: data?.bird?.habitats?.map?.((h) => h?.id),
            };
            const options = data?.bird?.habitats?.map?.((h) => {
              return { value: h?.id, label: h?.name };
            });
            setValue(newValue);
            setSelectedHabitats(options);
          })
          .catch((e) => setError(e.message))
          .finally(() => setLoading(false));
      }
    }
  }, [router, token]);

  const promiseHabitatOptions = (inputValue) =>
    fetch(`${urlBase}/habitats`, {
      method: "POST",
      body: JSON.stringify({ search: inputValue }),
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (!data?.success) throw new Error(data?.message || "Search Failed");
        if (data?.habitats) {
          const options = data?.habitats?.map?.((h) => {
            return { value: h?.id, label: h?.name };
          });
          return options;
        }
      })
      .catch((e) => {
        setError(e.message);
        console.error(e);
      });

  const onSubmitBird = async (event) => {
    event.preventDefault();
    const id = router?.query?.bird;

    setLoading(true);
    setError(null);

    const url = `${urlBase}/birds${id ? `/${id}` : ""}`;
    const method = id ? "PATCH" : "POST";

    try {
      const response = await fetch(url, {
        method,
        body: JSON.stringify(value),
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      const res = await response.json();
      const defaultMessage = "Submission Failed, please try again.";
      if (!res.success) {
        throw new Error(res?.message || defaultMessage);
      }
      if (res?.bird) {
        router.push(`${router.pathname}/?bird=${res?.bird}`, undefined, {
          shallow: true,
        });
      }
    } catch (e) {
      // Capture the error message to display to the user
      setError(e.message);
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const onChange = (e) => {
    const name = e.target.id;
    const newValue = { ...value, [name]: e.target.value };
    setValue(newValue);
  };

  const onSelect = (e) => {
    setSelectedHabitats(e);
    const newHabitats = e?.map?.((habitat) => habitat.value);
    const newValue = { ...value, habitats: newHabitats };
    setValue(newValue);
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h1" gutterBottom>
        Birds Of The World.
      </Typography>
      <Stack direction="row" justifyContent="space-between" pb={2}>
        <Link href="/birds" passHref>
          <Button endIcon={<FavoriteBorderSharpIcon />}>Back to Birds</Button>
        </Link>
        <Link href="/" passHref>
          <Button endIcon={<HomeIcon />}>Home</Button>
        </Link>
      </Stack>
      {error && <Alert severity="error">{error}</Alert>}
      <Box my={2}>
        <Typography variant="h2" gutterBottom>
          Fill in the Bird Form
        </Typography>
        <form onSubmit={onSubmitBird}>
          <Stack spacing={2}>
            <TextField
              id="common_name"
              label="Common name"
              value={value?.common_name}
              onChange={onChange}
              required
            />
            <TextField
              id="species"
              label="Species"
              value={value?.species}
              onChange={onChange}
              required
            />
            <Alert severity="info" style={{ fontStyle: "italic" }}>
              HINT: Go to your preferred image search engine. Filter for images
              in the public domain. Copy image link in the input field below.
            </Alert>
            <TextField
              id="image_link"
              label="Link for bird image"
              value={value?.image_link}
              onChange={onChange}
              required
            />
            <Item>
              <Stack direction="row">
                <Typography variant="caption" color="grey.700">
                  Search for Habitats*
                </Typography>
                <Tooltip title="Type to begin search" placement="right">
                  <SearchIcon />
                </Tooltip>
              </Stack>
              <AsyncSelect
                name="habitatsinput"
                inputId="habitatsinput"
                instanceId="habitats"
                value={selectedHabitats}
                onChange={onSelect}
                cacheOptions
                isMulti
                loadOptions={promiseHabitatOptions}
                noOptionsMessage={() => "Type to Search Again"}
                required
                placeholder="Type to Search..."
                className="react-select-container"
                classNamePrefix="react-select"
                theme={(theme) => ({
                  ...theme,
                  colors: {
                    ...theme.colors,
                    primary: "#AB003C",
                  },
                })}
              />
            </Item>
            <Button
              endIcon={<SaveOutlinedIcon />}
              type="submit"
              disabled={isLoading}
            >
              {isLoading
                ? "Loading..."
                : `${router?.query?.bird ? "Update" : "Add"} Bird`}
            </Button>
          </Stack>
        </form>
        <DeleteResource resource="bird" />
      </Box>

      <Alert severity="info" style={{ fontStyle: "italic" }}>
        HINT: Cant find your Habitat? Add a new habitat below:
      </Alert>

      <HabitatForm
        setSelectedHabitats={setSelectedHabitats}
        setBird={setValue}
        bird={value}
      />
    </Container>
  );
};
export default BirdsForm;

const Item = styled("div")({
  "& .react-select__menu": {
    zIndex: 1000,
  },
});
