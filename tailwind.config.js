/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Noto Sans", "sans-serif"],
        serif: ["Noto Serif", "serif"],
        mono: ["Noto Mono", "monospace"]
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
}
