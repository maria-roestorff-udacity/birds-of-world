import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    primary: {
      main: "#6573C3",
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          background: "linear-gradient(45deg, #D1C4E9 30%, #AB003C 90%)",
          border: 0,
          borderRadius: 3,
          boxShadow: "0 3px 5px 2px rgba(255, 105, 135, .3)",
          color: "white",
          height: 48,
          padding: "0 30px",
        },
      },
    },
  },
  typography: {
    h1: {
      fontSize: "3rem",
    },
    h2: {
      fontSize: "2.5rem",
    },
    h3: {
      fontSize: "2rem",
      paddingTop: "1rem",
      paddingBottom: "0.5rem",
      paddingLeft: "2px",
    },
    h4: {
      fontSize: "1.2rem",
    },
    h5: {
      fontSize: "0.9rem",
      fontStyle: "italic",
    },
  },
});
