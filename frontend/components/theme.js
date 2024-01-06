import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    primary: {
      main: "#AB003C",
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          position: "relative",
          background: "linear-gradient(45deg, #D1C4E9 30%, #AB003C 90%)",
          zIndex: 1,
          "&:hover::before": {
            opacity: 1,
          },
          "&::before": {
            content: "''",
            position: "absolute",
            top: 0,
            right: 0,
            bottom: 0,
            left: 0,
            background: "linear-gradient(45deg, #D1C4E9 5%, #AB003C 95%)",
            transition: "opacity 0.15s linear",
            zIndex: -1,
            opacity: 0,
          },
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
      paddingTop: "2rem",
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
