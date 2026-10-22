// mainmenu.js

// 1. Функция для безопасного получения элемента
function getActiveFormContainer() {
    return document.getElementById('main_menu_form_bar') || document.getElementById('openApp');
}

document.body.addEventListener('htmx:sseMessage', function (event) {
    setTimeout(() => {
        const openFormDiv = getActiveFormContainer();
        if (openFormDiv) {
            const urlElement = openFormDiv.querySelector('[data-push-url]');
            if (urlElement) {
                history.pushState(null, '', urlElement.dataset.pushUrl);
            }
        }
    }, 100);
});

// Защита от «залипания» курсора загрузки: если SSE-соединение оборвалось,
// а класс .htmx-request остался на узле — снимаем его принудительно.
document.body.addEventListener('htmx:sseError', function () {
    document.querySelectorAll('.htmx-request').forEach(function (el) {
        el.classList.remove('htmx-request');
    });
});