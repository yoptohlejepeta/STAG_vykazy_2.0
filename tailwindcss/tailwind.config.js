/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["../templates/**/*.html"],
    theme: {
      extend: {},
    },
    plugins: [
      require('daisyui')
    ],
    daisyui: {
      themes: ["dark", "retro", "coffee", "cupcake", "bumblebee"],
    },
    theme: {
      fontFamily: {
        // roboto
        sans: ['Roboto', 'sans-serif'],
      },
  },
  }