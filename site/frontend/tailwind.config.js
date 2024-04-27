/** @type {import('tailwindcss').Config} */

export default {
  content: ["./src/**/*.{html,js,jsx}"],
  theme: {
    extend: {
      backgroundImage: {
        '01': "url('./src/assets/images/01.png')"
      },
      from: {
        '01': "url('./src/assets/images/01.png')"
      }
    },
  },
  plugins: [],
}
