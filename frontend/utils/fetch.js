const urlBase = process.env.NEXT_PUBLIC_BASEURL;

export const onSubmit = async (id, resource, value, setLoading, setError) => {
  setLoading(true);
  setError(null); // Clear previous errors when a new request starts

  const url = `${urlBase}/${resource}${id ? `/${id}` : ""}`;
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
    // const data = await response.json();
  } catch (error) {
    // Capture the error message to display to the user
    setError(error.message);
    console.error(error);
  } finally {
    setLoading(false);
  }
};

export const fetchOptions = async (resource, setError, setLoading) => {
  return await fetch(`${urlBase}/${resource}`)
    .then((res) => res.json())
    .then((data) => {
      if (data[resource]) {
        const options = data[resource].map((item) => {
          return { value: item.id, label: item.name };
        });
        return options;
      }
    })
    .catch((error) => setError(error.message))
    .finally(() => setLoading(false));
};
