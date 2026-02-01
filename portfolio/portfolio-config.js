// Shared Tailwind Configuration
// Links CSS variables to Tailwind utility classes
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'bg-main': 'var(--color-bg-main)',
                'bg-card': 'var(--color-bg-card)',
                'bg-sub': 'var(--color-bg-sub)',
                'text-title': 'var(--color-text-title)',
                'text-body': 'var(--color-text-body)',
                'text-secondary': 'var(--color-text-secondary)',
                accent: 'var(--color-accent)',
                'border-default': 'var(--color-border)',
            },
        },
    },
};
