// mainmenu.js

// 1. Функция для безопасного получения элемента
function getActiveFormContainer() {
    return document.getElementById('openForm') || document.getElementById('openApp');
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

// Вызываем функцию, когда она нужна
// doSomethingWithForm(); 