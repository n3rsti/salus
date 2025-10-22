import colors from 'tailwindcss/colors'

export default {
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primary_light: colors.emerald[200],
                primary: colors.emerald[300],
                primary_dark: colors.emerald[400],
            }
        }
    }
}
