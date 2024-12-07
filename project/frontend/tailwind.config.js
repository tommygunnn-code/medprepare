module.exports = {
  content: [
    "./src/**/*.html",
    "./src/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: "#1E40AF",
        secondary: "#64748B",
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
};