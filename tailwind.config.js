module.exports = {
  darkMode: 'media', // or 'media' or 'selector'
  theme: {
    extend: {
      screen: {
      }
    },
  },
  content: [
    // Important: keep the files that uses tailwind classes in a sub-folder and add them here
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/static/js/**/*.js'
  ],
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/container-queries'),
  ],
}
