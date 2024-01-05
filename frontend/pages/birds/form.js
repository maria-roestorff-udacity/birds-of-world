import Link from "next/link";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Box from "@mui/system/Box";
import HabitatForm from "../../components/habitat/form";
import AsyncSelect from "react-select/async";
import DeleteResource from "../../components/delete";
import { useToken } from "../../components/tokenContext";

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
            const newValue = {
              common_name: data?.bird?.common_name,
              species: data?.bird?.species,
              image_link: data?.bird?.image_link,
              habitats: data?.bird?.habitats.map((h) => h?.id),
            };
            const options = data?.bird?.habitats.map((h) => {
              return { value: h?.id, label: h?.name };
            });
            setValue(newValue);
            setSelectedHabitats(options);
          })
          .catch((error) => setError(error.message))
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
          const options = data?.habitats.map((h) => {
            return { value: h?.id, label: h?.name };
          });
          return options;
        }
      })
      .catch((error) => {
        setError(error.message);
        console.error(error);
      });

  const onSubmitBird = async (event) => {
    event.preventDefault();
    const id = router?.query?.bird;

    setLoading(true);
    setError(null);

    const url = `${urlBase}/birds${id ? `/${id}` : ""}`;
    const method = id ? "PATCH" : "POST";
    let res;

    try {
      const response = await fetch(url, {
        method,
        body: JSON.stringify(value),
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      res = await response.json();
      const defaultMessage = "Submission Failed, please try again.";
      if (!res.success) throw new Error(res?.message || defaultMessage);
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

  if (isLoading) return <p>Loading...</p>;

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
          <label htmlFor="habitats">Search for Habitats:</label>
          <AsyncSelect
            inputId="habitats"
            instanceId="habitats"
            value={selectedHabitats}
            onChange={onSelect}
            cacheOptions
            isMulti
            loadOptions={promiseHabitatOptions}
            noOptionsMessage={() => "Search Again"}
            required
          />
          <button type="submit" disabled={isLoading}>
            {isLoading
              ? "Loading..."
              : `${router?.query?.bird ? "Update" : "Add"} Bird`}
          </button>
        </form>
        <DeleteResource resource="bird" />
      </Box>
      <p style={{ fontStyle: "italic" }}>
        HINT: Cant find your Habitat? Add a new habitat below:
      </p>
      <HabitatForm
        setSelectedHabitats={setSelectedHabitats}
        setBird={setValue}
        bird={value}
      />
    </div>
  );
};
export default BirdsForm;
