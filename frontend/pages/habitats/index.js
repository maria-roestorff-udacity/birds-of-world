import Link from "next/link";
import React from "react";
import HabitatForm from "../../components/habitat/form";
import DeleteResource from "../../components/delete";

const Habitat = () => {
  return (
    <div>
      <h1>Birds Of The World.</h1> <Link href="/birds">Back to Birds</Link>
      <h2>Fill in the Habitat Form</h2>
      <HabitatForm edit />
      <DeleteResource />
    </div>
  );
};
export default Habitat;
