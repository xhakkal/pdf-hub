module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // PDFhub brand colors (matching CSS custom properties in style.css)
        primary: '#0f766e',           // --color-primary
        'primary-hover': '#0b5f59',   // --color-primary-hover
        'primary-light': '#ccfbf1',   // --color-primary-light
        'primary-glow': 'rgba(15, 118, 110, 0.18)', // --color-primary-glow
        surface: '#e9eee8',           // --color-surface
        'surface-hover': '#dfe8df',   // --color-surface-hover
        border: '#c7d3c7',             // --color-border
        'border-hover': '#9eafa1',    // --color-border-hover
        bg: '#f6f7f2',                // --color-bg
        'bg-elevated': '#ffffff',     // --color-bg-elevated
        text: '#17332f',              // --color-text
        muted: '#58706a',             // --color-text-muted
        dim: '#83958f',               // --color-text-dim
        success: '#2f855a',           // --color-success
        error: '#c2413b',             // --color-error
        warning: '#b7791f',           // --color-warning
        // Semantic aliases for convenience
        orange: '#c2413b',
        'orange-hover': '#a93631',
        brand: '#f6f7f2',
        elevated: '#ffffff',
        surface: '#e9eee8',
      },
      fontFamily: {
        'manrope': ['Manrope', 'Inter', 'sans-serif'],
        'inter': ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}