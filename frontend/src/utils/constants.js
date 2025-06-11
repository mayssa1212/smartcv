// Constantes globales pour l'application SmartCV

// URL de base de l'API
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// Thèmes de couleurs disponibles
export const COLOR_THEMES = {
  PASTEL: {
    primary: "#A0E9E0",
    secondary: "#FBC2EB",
    accent: "#FEE2A0",
    text: "#B5ADF6",
  },
  PROFESSIONAL: {
    primary: "#2C3E50",
    secondary: "#3498DB",
    accent: "#1ABC9C",
    text: "#34495E",
  },
  MODERN: {
    primary: "#6C63FF",
    secondary: "#FF6584",
    accent: "#43CBFF",
    text: "#30336B",
  },
};

// Polices disponibles
export const FONTS = [
  "Poppins",
  "Roboto",
  "Open Sans",
  "Montserrat",
  "Lato",
];

// Étapes du guide interactif
export const GUIDE_STEPS = [
  "personal_info",
  "education",
  "experience",
  "skills",
  "summary",
];
