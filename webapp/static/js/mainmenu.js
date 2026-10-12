// Логика открытия верхнего меню по клику
document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', (e) => {
        e.stopPropagation();
        document.querySelectorAll('.menu-item.active').forEach(i => i.classList.remove('active'));
        item.classList.toggle('active');
    });
});

// Переключение меню при наведении (если одно уже открыто)
let activeMenu = null;
document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('mouseenter', () => {
        if (activeMenu && activeMenu !== item) {
            activeMenu.classList.remove('active');
            item.classList.add('active');
            activeMenu = item;
        }
    });
    item.addEventListener('click', () => { activeMenu = item; });
});

document.addEventListener('click', () => {
    document.querySelectorAll('.menu-item.active').forEach(i => i.classList.remove('active'));
    activeMenu = null;
});