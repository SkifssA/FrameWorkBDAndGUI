console.log('✅ Встроенный mainmenu.js загружен');

// Проверяем, есть ли меню на странице
const menuItems = document.querySelectorAll('.menu-item');
console.log('📋 Найдено .menu-item:', menuItems.length);

// Глобальный обработчик клика
document.addEventListener('click', (e) => {
    console.log('🖱️ КЛИК!', {
        target: e.target,
        tagName: e.target.tagName,
        className: e.target.className,
        path: e.composedPath()
    });

    const menuItem = e.target.closest('.menu-item');
    console.log('🔍 closest(.menu-item):', menuItem);

    if (menuItem) {
        console.log('✅ Клик внутри .menu-item');

        // Проверяем, не кликнули ли по ссылке
        const link = e.target.closest('a');
        console.log(' Клик по ссылке:', link);

        if (link) {
            console.log('️ Клик по ссылке, закрываем меню');
            document.querySelectorAll('.menu-item.active').forEach(i => {
                console.log(' Убираем active у:', i);
                i.classList.remove('active');
            });
            return;
        }

        e.stopPropagation();

        const isActive = menuItem.classList.contains('active');
        console.log('🔄 Было активно:', isActive);

        // Закрываем ВСЕ меню
        document.querySelectorAll('.menu-item.active').forEach(i => {
            console.log('❌ Закрываем:', i);
            i.classList.remove('active');
        });

        // Открываем текущее, если было закрыто
        if (!isActive) {
            console.log(' Добавляем active к:', menuItem);
            menuItem.classList.add('active');
            console.log('✅ Классы после:', menuItem.classList);
        }
    } else {
        console.log('❌ Клик вне меню, закрываем всё');
        document.querySelectorAll('.menu-item.active').forEach(i => i.classList.remove('active'));
    }
});

// Обработчик наведения
document.addEventListener('mouseover', (e) => {
    const menuItem = e.target.closest('.menu-item');
    if (!menuItem) return;

    const activeItem = document.querySelector('.menu-item.active');
    if (activeItem && activeItem !== menuItem) {
        console.log('🔄 Переключение при наведении');
        activeItem.classList.remove('active');
        menuItem.classList.add('active');
    }
});