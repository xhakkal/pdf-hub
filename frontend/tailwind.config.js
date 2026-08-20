module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // PDFhub brand colors (matching CSS custom properties in style.css)
        primary: '#ff9f1c',           // --color-primary
        'primary-hover': '#ffb13d',   // --color-primary-hover
        'primary-light': '#ffe0a6',   // --color-primary-light
        'primary-glow': 'rgba(255, 159, 28, 0.34)', // --color-primary-glow
        surface: '#1d1d1d',           // --color-surface
        'surface-hover': '#292929',   // --color-surface-hover
        border: '#373737',            // --color-border
        'border-hover': '#555555',    // --color-border-hover
        bg: '#080808',                // --color-bg
        'bg-elevated': '#121212',     // --color-bg-elevated
        text: '#f5f5f5',              // --color-text
        muted: '#b0b0b0',             // --color-text-muted
        dim: '#777777',               // --color-text-dim
        success: '#22c55e',           // --color-success
        error: '#ef4444',             // --color-error
        warning: '#f59e0b',           // --color-warning
        // Semantic aliases for convenience
        orange: '#ff9f1c',
        'orange-hover': '#ffb13d',
        brand: '#080808',
        elevated: '#121212',
        surface: '#1d1d1d',
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