/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}", "!./node_modules/**"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "background": "rgb(var(--color-background) / <alpha-value>)",
        "surface": "rgb(var(--color-surface) / <alpha-value>)",
        "midnight-blue": "rgb(var(--color-midnight-blue) / <alpha-value>)",
        "primary": "rgb(var(--color-primary) / <alpha-value>)",
        "primary-container": "rgb(var(--color-primary-container) / <alpha-value>)",
        "on-primary": "rgb(var(--color-on-primary) / <alpha-value>)",
        "starlight-gold": "rgb(var(--color-starlight-gold) / <alpha-value>)",
        "secondary": "rgb(var(--color-secondary) / <alpha-value>)",
        "tertiary": "rgb(var(--color-tertiary) / <alpha-value>)",
        "impasto-white": "rgb(var(--color-impasto-white) / <alpha-value>)",
        "on-surface": "rgb(var(--color-on-surface) / <alpha-value>)",
        "on-surface-variant": "rgb(var(--color-on-surface-variant) / <alpha-value>)",
        "outline": "rgb(var(--color-outline) / <alpha-value>)",
        "error": "rgb(var(--color-error) / <alpha-value>)",
        "cobblestone-gray": "rgb(var(--color-cobblestone-gray) / <alpha-value>)",
        "surface-bright": "rgb(var(--color-surface-bright) / <alpha-value>)",
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
        "lamplight": "0 0 32px rgba(235, 180, 43, 0.15)",
        "lamplight-lg": "0 0 48px rgba(235, 180, 43, 0.15)",
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
}
