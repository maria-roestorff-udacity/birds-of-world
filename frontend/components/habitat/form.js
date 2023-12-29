import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Select from "react-select";
import Box from "@mui/system/Box";

const urlBase = process.env.NEXT_PUBLIC_BASEURL;

const HabitatForm = ({
  setHabitatsOptions = () => {},
  setBird = () => {},
  bird,
}) => {
  const router = useRouter();
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
    fetch(`${urlBase}/regions`)
      .then((res) => res.json())
      .then((data) => {
        if (data.regions) {
          const options = data.regions.map((item) => {
            return { value: item.id, label: item.name };
          });
          setRegionOptions(options);
        }
      })
      .catch((error) => setError(error.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (router.isReady) {
      const bird_id = router.query.id;
      if (bird_id) {
        setValue({ ...value, bird: bird_id });
      }
      const habitat_id = router.query.habitat;
      if (habitat_id) {
        fetch(`${urlBase}/habitats/${habitat_id}`)
          .then((res) => res.json())
          .then((data) => {
            const newValue = {
              name: data.habitat.name,
              region_id: data.habitat.region_id,
              bird: "",
            };
            setValue(newValue);
          })
          .catch((error) => setError(error.message))
          .finally(() => setLoading(false));
      }
    }
  }, [router]);

  useEffect(() => {
    if (regionOptions && value) {
      const intialRegion = regionOptions.filter(
        (habitat) => value.region_id == habitat.value
      );
      setSelectedRegion(intialRegion);
    }
  }, [regionOptions, value]);

  if (isLoading) return <p>Loading...</p>;

  const onSubmitHabitat = async (event) => {
    event.preventDefault();
    const id = router.query.habitat;

    setLoading(true);
    setError(null); // Clear previous errors when a new request starts

    const url = `${urlBase}/habitats${id ? `/${id}` : ""}`;
    const method = id ? "PUT" : "POST";

    try {
      const response = await fetch(url, {
        method,
        body: JSON.stringify(value),
        headers: { "Content-Type": "application/json" },
      });
      if (!response.ok) {
        throw new Error("Failed to submit the data. Please try again.");
      }
      // Handle response if necessary
      const res = await response.json();

      if (bird) {
        setHabitatsOptions((prev) => [
          ...prev,
          {
            value: res.habitat.id,
            label: res.habitat.name,
          },
        ]);
        setBird({ ...bird, habitats: [...bird.habitats, res.habitat.id] });
      }
    } catch (error) {
      // Capture the error message to display to the user
      setError(error.message);
      console.error(error);
    } finally {
      if (router.pathname == "/birds/form") {
        setSelectedRegion(null);
        const newValue = { ...value };
        newValue.name = "";
        newValue.region_id = "";
        setValue(newValue);
      }
      setLoading(false);
    }
  };

  return (
    <Box my={2}>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <form onSubmit={onSubmitHabitat}>
        <label htmlFor="name">Habitat name:</label>
        <input
          type="text"
          name="name"
          id="name"
          value={value.name}
          onChange={(e) => setValue({ ...value, name: e.target.value })}
          size="30"
          required
        />
        <br />
        <label htmlFor="regions">Global Region:</label>
        <Select
          inputId="regions"
          value={selectedRegion}
          options={regionOptions}
          onChange={(e) => {
            setSelectedRegion(e);
            setValue({ ...value, region_id: e.value });
          }}
          isSearchable
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Loading..." : "Add Habitat"}
        </button>
      </form>
    </Box>
  );
};
export default HabitatForm;
