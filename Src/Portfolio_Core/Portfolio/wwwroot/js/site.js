(() => {
    const toggle = document.getElementById('themeToggle');
    if (toggle) {
        toggle.checked = document.documentElement.getAttribute('data-bs-theme') === 'dark';
        toggle.addEventListener('change', () => {
            const theme = toggle.checked ? 'dark' : 'light';
            document.documentElement.setAttribute('data-bs-theme', theme);
            try { localStorage.setItem('theme', theme); } catch { /* Theme still works without storage. */ }
        });
    }
    document.querySelectorAll('.navbar .nav-link').forEach(link => {
        const target = link.pathname.replace(/\/$/, '').toLowerCase();
        const current = location.pathname.replace(/\/$/, '').toLowerCase();
        if (target === current) {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        } else if ((target === '/skills/technologies' && current.startsWith('/skills/') && current !== '/skills/ai') ||
                   (target === '/experience' && current.startsWith('/experience/')) ||
                   (target === '/experience/index' && current.startsWith('/experience/'))) {
            link.classList.add('active');
        }
    });
})();
