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
        if (link.pathname.replace(/\/$/, '') === location.pathname.replace(/\/$/, '')) {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        }
    });
})();
