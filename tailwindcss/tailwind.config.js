/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["../app/templates/**/*.html"],
    theme: {
      extend: {},
    },
    plugins: [
      require('daisyui')
    ],
    daisyui: {
      themes: ["emerald",
        {
          streamlit: {
            "primary": "#F63366",
            "secondary": "#F3A4B5",
            "accent": "#007bff",
            "neutral": "#333333",
            "base-100": "#ffffff",
            "info": "#17a2b8",
            "success": "#28a745",
            "warning": "#ffc107",
            "error": "#dc3545",
          },
        },
      ],
    },
    theme: {
      fontFamily: {
        // roboto
        sans: ['Roboto', 'sans-serif'],
      },
  },
  }