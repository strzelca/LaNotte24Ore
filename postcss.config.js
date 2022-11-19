module.exports = {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
        'postcss-import': {},
        'tailwindcss/nesting': 'postcss-nesting',
        ...(process.env.NODE_ENV === 'production' ? { cssnano: {} } : {}),
    }
}