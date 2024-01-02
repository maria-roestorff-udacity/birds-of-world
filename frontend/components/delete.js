import React, { useState } from "react";
import { useRouter } from "next/router";

const urlBase = process.env.NEXT_PUBLIC_BASEURL;

const DeleteResource = ({ resource = "habitat" }) => {
  const router = useRouter();
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onDelete = async (event) => {
    event.preventDefault();
    const id = router.query[resource];
    setLoading(true);
    setError(null); // Clear previous errors when a new request starts

    try {
      const response = await fetch(`${urlBase}/${resource}s/${id}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
      });
      if (!response.ok) throw new Error("Delete Failed. Please try again.");
    } catch (error) {
      // Capture the error message to display to the user
      setError(error.message);
      console.error(error);
    } finally {
      setLoading(false);
      router.push("/birds");
    }
  };

  return (
    <>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <button type="button" disabled={isLoading} onClick={onDelete}>
        {isLoading ? "Loading..." : `Delete ${resource}`}
      </button>
    </>
  );
};
export default DeleteResource;
