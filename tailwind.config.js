/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: [
    './web/templates/**/*.html',
    './web/routes/templates/**/*.html'
  ],
  theme: {
    fontFamily: {
      sans: ["Noto Sans", "sans-serif"],
      serif: ["Noto Serif", "serif"],
      mono: ["Noto Mono", "monospace"]
    },
    extend: {
    },
  },
  plugins: [],
}
