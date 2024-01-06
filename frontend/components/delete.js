import React, { useState } from "react";
import { useRouter } from "next/router";
import { useToken } from "./tokenContext";
import Button from "@mui/material/Button";
import DeleteForeverIcon from "@mui/icons-material/DeleteForever";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";

const urlBase = process.env.NEXT_PUBLIC_BASEURL;

const DeleteResource = ({ resource = "habitat" }) => {
  const router = useRouter();
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { token, ownerRole } = useToken();

  const onDelete = async (event) => {
    event.preventDefault();
    const id = router.query[resource];
    setLoading(true);
    setError(null); // Clear previous errors when a new request starts

    try {
      const response = await fetch(`${urlBase}/${resource}s/${id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error("Delete Failed. Please try again.");
      }
      router.push("/birds");
    } catch (e) {
      // Capture the error message to display to the user
      setError(e.message);
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ marginTop: "1.2rem" }}>
      {error && <Alert severity="error">{error}</Alert>}
      <Button
        endIcon={<DeleteForeverIcon />}
        disabled={isLoading || !router.query[resource]}
        onClick={onDelete}
      >
        {isLoading ? "Loading..." : `Delete ${resource}`}
      </Button>
    </Box>
  );
};
export default DeleteResource;
