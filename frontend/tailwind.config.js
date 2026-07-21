/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: { farm: { 50: "#f1f8f3", 100: "#dcefe1", 500: "#2f8550", 600: "#257044", 700: "#1d5937", 900: "#153c28" } },
      boxShadow: { card: "0 1px 3px rgba(20, 45, 29, .08), 0 8px 24px rgba(20, 45, 29, .05)" },
    },
  },
  plugins: [],
};
