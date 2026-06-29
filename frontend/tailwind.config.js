/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}", "!./node_modules/**"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "background": "var(--color-background)",
        "surface": "var(--color-surface)",
        "midnight-blue": "var(--color-midnight-blue)",
        "primary": "var(--color-primary)",
        "primary-container": "var(--color-primary-container)",
        "on-primary": "var(--color-on-primary)",
        "starlight-gold": "var(--color-starlight-gold)",
        "secondary": "var(--color-secondary)",
        "tertiary": "var(--color-tertiary)",
        "impasto-white": "var(--color-impasto-white)",
        "on-surface": "var(--color-on-surface)",
        "on-surface-variant": "var(--color-on-surface-variant)",
        "outline": "var(--color-outline)",
        "error": "var(--color-error)",
        "cobblestone-gray": "var(--color-cobblestone-gray)",
        "surface-bright": "var(--color-surface-bright)",
      },
      borderRadius: {
        "sm": "var(--radius-sm)",
        "DEFAULT": "var(--radius-default)",
        "md": "var(--radius-md)",
        "lg": "var(--radius-lg)",
        "xl": "var(--radius-xl)",
        "full": "9999px",
      },
      spacing: {
        "unit": "var(--space-unit)",
        "gutter": "var(--space-gutter)",
        "margin-mobile": "var(--space-margin-mobile)",
        "margin-desktop": "var(--space-margin-desktop)",
        "reading-width": "var(--space-reading-width)",
      },
      fontFamily: {
        "display": ["Playfair Display", "serif"],
        "body": ["Manrope", "sans-serif"],
      },
      boxShadow: {
        "lamplight": "0 0 32px var(--shadow-lamplight)",
        "lamplight-lg": "0 0 48px var(--shadow-lamplight)",
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
}
