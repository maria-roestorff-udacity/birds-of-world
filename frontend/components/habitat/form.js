import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Select from "react-select";
import Box from "@mui/system/Box";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import SaveOutlinedIcon from "@mui/icons-material/SaveOutlined";
import Alert from "@mui/material/Alert";
import { useToken } from "../tokenContext";
import { styled } from "@mui/material/styles";

const urlBase = process.env.NEXT_PUBLIC_BASEURL;

const HabitatForm = ({
  setSelectedHabitats = () => {},
  setBird = () => {},
  bird = null,
  edit = false,
}) => {
  const router = useRouter();
  const { token } = useToken();
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [regionOptions, setRegionOptions] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [value, setValue] = useState({
    name: "",
    region_id: "",
    bird: "",
  });

  useEffect(() => {
    if (token) {
      setLoading(true);
      fetch(`${urlBase}/regions`, {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then((res) => res.json())
        .then((data) => {
          if (data?.regions) {
            const options = data?.regions?.map?.((item) => {
              return { value: item?.id, label: item?.name };
            });
            setRegionOptions(options);
          }
        })
        .catch((error) => setError(error?.message))
        .finally(() => setLoading(false));
    }
  }, [token]);

  useEffect(() => {
    if (router.isReady) {
      const bird_id = router.query.bird;
      if (bird_id) {
        setValue({ ...value, bird: bird_id });
      }
      const habitat_id = router.query.habitat;
      if (habitat_id && token) {
        setLoading(true);
        fetch(`${urlBase}/habitats/${habitat_id}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
          .then((res) => res.json())
          .then((data) => {
            const newValue = {
              name: data?.habitat?.name,
              region_id: data?.habitat?.region_id,
              bird: "",
            };
            setValue(newValue);
          })
          .catch((error) => setError(error?.message))
          .finally(() => setLoading(false));
      }
    }
  }, [router, token]);

  useEffect(() => {
    if (regionOptions && value) {
      const intialRegion = regionOptions.filter(
        (habitat) => value.region_id == habitat.value
      );
      setSelectedRegion(intialRegion);
    }
  }, [regionOptions, value]);

  const onSubmitHabitat = async (event) => {
    event.preventDefault();
    const id = router.query.habitat;

    setLoading(true);
    setError(null); // Clear previous errors when a new request starts

    const url = `${urlBase}/habitats${id ? `/${id}` : ""}`;
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
      if (!response.ok) {
        throw new Error(
          "Failed to submit the data. Please try again, or search for your habitat to see if it already exists."
        );
      }
      // Handle response if necessary
      const res = await response.json();

      if (bird) {
        setSelectedHabitats((prev) => [
          ...(prev || []),
          {
            value: res.habitat.id,
            label: res.habitat.name,
          },
        ]);
        setBird({ ...bird, habitats: [...bird.habitats, res.habitat.id] });
      }

      if (router.pathname == "/birds/form") {
        setSelectedRegion(null);
        const newValue = { ...value };
        newValue.name = "";
        newValue.region_id = "";
        setValue(newValue);
      } else if (router.pathname == "/habitats" && res?.habitat?.id) {
        const dest = `${router.pathname}?habitat=${res?.habitat?.id}`;
        router.push(dest, undefined, {
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

  return (
    <Box my={2}>
      {error && <Alert severity="error">{error}</Alert>}
      <form onSubmit={onSubmitHabitat}>
        <Stack spacing={2}>
          <TextField
            id="name"
            label="Habitat name"
            value={value?.name}
            onChange={(e) => setValue({ ...value, name: e.target.value })}
            required
          />
          {/* <label htmlFor="regions">Global Region:</label> */}
          <Item>
            <Typography variant="caption" color="grey.700">
              Global Region*
            </Typography>
            <Select
              name="regionsInput"
              inputId="regionsInput"
              instanceId="regionsInstance"
              value={selectedRegion}
              options={regionOptions}
              onChange={(e) => {
                setSelectedRegion(e);
                setValue({ ...value, region_id: e.value });
              }}
              isSearchable
              required
              theme={(theme) => ({
                ...theme,
                colors: {
                  ...theme.colors,
                  primary: "#AB003C",
                },
              })}
              className="react-select-container"
              classNamePrefix="react-select"
            />
          </Item>
          <Button
            endIcon={<SaveOutlinedIcon />}
            type="submit"
            disabled={isLoading}
          >
            {isLoading
              ? "Loading..."
              : `${edit && router?.query?.habitat ? "Update" : "Add"} Habitat`}
          </Button>
        </Stack>
      </form>
    </Box>
  );
};
export default HabitatForm;

const Item = styled("div")({
  "& .react-select__menu": {
    zIndex: 1000,
  },
});
