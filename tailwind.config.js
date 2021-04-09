module.exports = {
  mode: 'jit',
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: false,
  },
  purge: {
    enabled: true,
    mode: 'all',
    preserveHtmlElements: false,
    // it's important to keep the "*.html" or "*.js" files that uses tailwind classes in a sub folder so that postcss can properly purge the classes 
    content: [
      // Important: keep the files that uses tailwind classes in a sub-folder and add them here
      './templates/**/*.html',
      './**/templates/**/*.html'
    ]
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}