module.exports = {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
        'postcss-import': {},
        'postcss-icon.material-design': {},
        'tailwindcss/nesting': 'postcss-nesting',
        ...(process.env.NODE_ENV === 'production' ? { cssnano: {} } : {}),
    }
}