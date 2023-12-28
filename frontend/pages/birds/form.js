import Link from "next/link";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Select from "react-select";
import Box from "@mui/system/Box";
import { onSubmit } from "../../utils/fetch";
import HabitatForm from "../../components/habitat/form";

const BirdsForm = () => {
  const router = useRouter();

  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [habitatsOptions, setHabitatsOptions] = useState(null);
  const [selectedHabitats, setSelectedHabitats] = useState(null);
  const [value, setValue] = useState({
    common_name: "",
    species: "",
    bird_image_link: "",
    habitats: "",
  });
  const urlBase = "http://127.0.0.1:5000";

  useEffect(() => {
    fetch(`${urlBase}/habitats`)
      .then((res) => res.json())
      .then((data) => {
        if (data["habitats"]) {
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
      const id = router.query.id;
      if (id) {
        fetch(`${urlBase}/birds/${id}`)
          .then((res) => res.json())
          .then((data) => {
            const newValue = {
              common_name: data.bird.common_name,
              species: data.bird.species,
              bird_image_link: data.bird.bird_image_link,
              habitats: data.bird.habitats,
            };

            if (habitatsOptions) {
              const intialHabitats = habitatsOptions.filter((habitat) =>
                data.bird.habitats.includes(habitat.value)
              );
              setSelectedHabitats(intialHabitats);
            }
            setValue(newValue);
          })
          .catch((error) => setError(error.message))
          .finally(() => setLoading(false));
      }
    }
  }, [router, habitatsOptions]);

  if (isLoading) return <p>Loading...</p>;

  const onSubmitBird = async (event) => {
    event.preventDefault();
    const id = router.query.id;
    await onSubmit(id, "birds", value, setLoading, setError);
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
          <label htmlFor="bird_image_link">Link for bird Image:</label>
          <input
            type="text"
            name="bird_image_link"
            id="bird_image_link"
            value={value.bird_image_link}
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
      <p>HINT: Cant find your Habitat? Add a new habitat below</p>
      <HabitatForm />
    </div>
  );
};
export default BirdsForm;
