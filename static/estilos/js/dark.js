
      document.addEventListener('DOMContentLoaded', () => {
            const toggleBtn = document.getElementById('themeToggle');
            const themeIcon = document.getElementById('themeIcon');
            const body = document.body;

            // Verificar preferencia guardada
            const savedTheme = localStorage.getItem('theme');
            if (savedTheme === 'dark') {
                body.classList.add('dark-mode');
                themeIcon.className = 'fas fa-sun';
            }

            // Manejar clic del botón
            toggleBtn.addEventListener('click', () => {
                body.classList.toggle('dark-mode');
                
                if (body.classList.contains('dark-mode')) {
                    themeIcon.className = 'fas fa-sun';
                    localStorage.setItem('theme', 'dark');
                } else {
                    themeIcon.className = 'fas fa-moon';
                    localStorage.setItem('theme', 'light');
                }
            });
        });