/** @type {import('tailwindcss').Config} */

export default {
  content: ["./src/**/*.{html,js,jsx}"],
  theme: {
    extend: {
      backgroundImage: {
        '01': "url('./src/assets/images/01.png')",
        '03': "url('./src/assets/images/03.jpg')"
      },
      from: {
        '01': "url('./src/assets/images/01.png')",
        '03': "url('./src/assets/images/03.jpg')"
      },
      padding: {
        '2.5': "10.5px"
      }
    },
  },
  plugins: [],
}
