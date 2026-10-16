const menuItems = document.querySelectorAll('.menu-item');

// Глобальный обработчик клика
document.addEventListener('click', (e) => {

    const menuItem = e.target.closest('.menu-item');

    if (menuItem) {

        // Проверяем, не кликнули ли по ссылке
        const link = e.target.closest('a');

        if (link) {
            document.querySelectorAll('.menu-item.active').forEach(i => {
                i.classList.remove('active');
            });
            return;
        }

        e.stopPropagation();

        const isActive = menuItem.classList.contains('active');

        // Закрываем ВСЕ меню
        document.querySelectorAll('.menu-item.active').forEach(i => {
            i.classList.remove('active');
        });

        // Открываем текущее, если было закрыто
        if (!isActive) {
            menuItem.classList.add('active');
        }
    } else {
        document.querySelectorAll('.menu-item.active').forEach(i => i.classList.remove('active'));
    }
});

// Обработчик наведения
document.addEventListener('mouseover', (e) => {
    const menuItem = e.target.closest('.menu-item');
    if (!menuItem) return;

    const activeItem = document.querySelector('.menu-item.active');
    if (activeItem && activeItem !== menuItem) {
        activeItem.classList.remove('active');
        menuItem.classList.add('active');
    }
});