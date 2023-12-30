import Link from "next/link";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Select from "react-select";
import Box from "@mui/system/Box";
import HabitatForm from "../../components/habitat/form";

const urlBase = process.env.NEXT_PUBLIC_BASEURL;

const BirdsForm = () => {
  const router = useRouter();

  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [habitatsOptions, setHabitatsOptions] = useState(null);
  const [selectedHabitats, setSelectedHabitats] = useState(null);
  const [value, setValue] = useState({
    common_name: "",
    species: "",
    image_link: "",
    habitats: "",
  });

  useEffect(() => {
    fetch(`${urlBase}/habitats`)
      .then((res) => res.json())
      .then((data) => {
        if (data.habitats) {
          const options = data.habitats.map((habitat) => {
            return { value: habitat.id, label: habitat.name };
          });
          setHabitatsOptions(options);
        }
      })
      .catch((error) => setError(error.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (router.isReady) {
      const id = router.query.bird;
      if (id) {
        fetch(`${urlBase}/birds/${id}`)
          .then((res) => res.json())
          .then((data) => {
            const newValue = {
              common_name: data.bird.common_name,
              species: data.bird.species,
              image_link: data.bird.image_link,
              habitats: data.bird.habitats,
            };
            setValue(newValue);
          })
          .catch((error) => setError(error.message))
          .finally(() => setLoading(false));
      }
    }
  }, [router]);

  useEffect(() => {
    if (habitatsOptions && value) {
      const intialHabitats = habitatsOptions.filter((habitat) =>
        value.habitats.includes(habitat.value)
      );
      setSelectedHabitats(intialHabitats);
    }
  }, [habitatsOptions, value]);

  if (isLoading) return <p>Loading...</p>;

  const onSubmitBird = async (event) => {
    event.preventDefault();
    const id = router.query.bird;

    setLoading(true);
    setError(null); // Clear previous errors when a new request starts

    const url = `${urlBase}/birds${id ? `/${id}` : ""}`;
    const method = id ? "PUT" : "POST";
    let res;

    try {
      const response = await fetch(url, {
        method,
        body: JSON.stringify(value),
        headers: { "Content-Type": "application/json" },
      });
      if (!response.ok) {
        throw new Error("Failed to submit the data. Please try again.");
      }
      res = await response.json();
    } catch (error) {
      // Capture the error message to display to the user
      setError(error.message);
      console.error(error);
    } finally {
      setLoading(false);
      if (res) {
        router.push(`${router.pathname}/?bird=${res?.bird}`, undefined, {
          shallow: true,
        });
      }
    }
  };

  const onChange = (e) => {
    const name = e.target.name;
    const newValue = { ...value, [name]: e.target.value };
    setValue(newValue);
  };

  const onSelect = (e) => {
    setSelectedHabitats(e);
    const newHabitats = e.map((habitat) => habitat.value);
    const newValue = { ...value, habitats: newHabitats };
    setValue(newValue);
  };

  return (
    <div>
      <h1>Birds Of The World.</h1> <Link href="/birds">Back to Birds</Link>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <Box my={2}>
        <h2>Fill in the Bird Form</h2>
        <form onSubmit={onSubmitBird}>
          <label htmlFor="common_name">Common name:</label>
          <input
            type="text"
            name="common_name"
            id="common_name"
            value={value.common_name}
            onChange={onChange}
            size="30"
            required
          />
          <br />
          <label htmlFor="species">Species:</label>
          <input
            type="text"
            name="species"
            id="species"
            value={value.species}
            onChange={onChange}
            size="30"
            required
          />
          <br />
          <label htmlFor="image_link">Link for bird image:</label>
          <input
            type="text"
            name="image_link"
            id="image_link"
            value={value.image_link}
            onChange={onChange}
            size="80"
          />
          <br />
          <label htmlFor="habitats">Habitats:</label>
          <Select
            inputId="habitats"
            value={selectedHabitats}
            options={habitatsOptions}
            onChange={onSelect}
            isMulti
            isSearchable
          />
          <button type="submit" disabled={isLoading}>
            {isLoading ? "Loading..." : "Submit"}
          </button>
        </form>
      </Box>
      <p style={{ fontStyle: "italic" }}>
        HINT: Cant find your Habitat? Add a new habitat below:
      </p>
      <HabitatForm
        setHabitatsOptions={setHabitatsOptions}
        setBird={setValue}
        bird={value}
      />
    </div>
  );
};
export default BirdsForm;
