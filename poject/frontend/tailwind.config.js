module.exports = {
    content: [
      "./poject/frontend/src/**/*.{html,js}", // Scans all HTML and JS files in the src folder
      "./poject/frontend/src/components/**/*.{html,js}", // Includes components folder
    ],
    theme: {
      extend: {
        colors: {
          primary: "#1E40AF", // Custom primary color for buttons and links
          secondary: "#64748B", // Custom secondary color for text
        },
      },
    },
    plugins: [
      require('@tailwindcss/forms'), // Enables Tailwind forms plugin
      // Add more plugins or UI libraries like daisyUI if needed:
      // require('daisyui')
    ],
  };
  