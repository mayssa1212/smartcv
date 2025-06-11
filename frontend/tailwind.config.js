/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        poppins: ['Poppins', 'Arial', 'sans-serif'],
      },
      colors: {
        pastelPink: "#FBC2EB",
        pastelAccent: "#6C63FF",
        pastelLavender: "#B5ADF6",
        pastelBlue: "#8FD6E7",
        pastelYellow: "#FEE2A0",
      },
    },
  },
  plugins: [],
}