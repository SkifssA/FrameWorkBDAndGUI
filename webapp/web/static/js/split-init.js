/**
 * Инициализация Split.js для элементов с классом .auto-split
 */
function initSplitContainers(target) {
    // 1. Проверка: подключена ли библиотека Split.js
    if (typeof Split === 'undefined') {
        console.warn('Split.js не найден. Убедитесь, что <script src="..."> подключен в HTML.');
        return;
    }

    const containers = [];

    // 2. Собираем все целевые элементы в области обновления
    if (target.classList && target.classList.contains('auto-split')) {
        containers.push(target);
    }
    if (target.querySelectorAll) {
        target.querySelectorAll('.auto-split').forEach(el => containers.push(el));
    }

    if (containers.length === 0) return;

    // 3. Сортируем по глубине вложенности: сначала внешние, потом внутренние.
    // Это критически важно для корректной работы вложенных сплитов.
    containers.sort((a, b) => {
        let depthA = 0, depthB = 0;
        let nodeA = a, nodeB = b;
        while (nodeA.parentElement) { depthA++; nodeA = nodeA.parentElement; }
        while (nodeB.parentElement) { depthB++; nodeB = nodeB.parentElement; }
        return depthA - depthB;
    });

    // 4. Инициализируем каждый контейнер
    containers.forEach(el => {
        // Пропускаем, если уже инициализирован (защита от дублирования при HTMX)
        if (el.dataset.splitInit === 'true') return;

        // Split.js работает только с прямыми дочерними элементами
        const children = Array.from(el.children).filter(c => c.tagName === 'DIV');

        // Для разделения нужно минимум 2 элемента
        if (children.length < 2) {
            return;
        }

        const direction = el.dataset.splitDirection || 'horizontal';
        const sizes = el.dataset.splitSizes ? el.dataset.splitSizes.split(',').map(Number) : null;
        const minSize = Number(el.dataset.splitMinSize) || 100;
        const gutter = Number(el.dataset.splitGutter) || 8;

        const options = {
            direction: direction,
            minSize: minSize,
            gutterSize: gutter,
            elementStyle: function (dimension, size, gutterSize) {
                return {
                    'flex-basis': 'calc(' + size + '% - ' + gutterSize + 'px)',
                    'flex-grow': '0',  // <-- ВАЖНО: запрещаем автоматическое растягивание
                    'flex-shrink': '0' // <-- ВАЖНО: запрещаем автоматическое сжатие
                };
            },
            gutterStyle: function (dimension, gutterSize) {
                return {
                    'flex-basis': gutterSize + 'px',
                    'flex-grow': '0',
                    'flex-shrink': '0'
                };
            }
        };

        if (sizes) {
            options.sizes = sizes;
        }

        // Запускаем Split.js
        Split(children, options);

        // Помечаем как инициализированный
        el.dataset.splitInit = 'true';
    });
}

// 5. Привязываем к начальной загрузке страницы (на случай, если первый рендер не через HTMX)
document.addEventListener('DOMContentLoaded', function () {
    initSplitContainers(document);
});

// 6. Привязываем к событию HTMX после обновления DOM
document.addEventListener('htmx:afterSettle', function (event) {
    const target = event.detail.elt || document;
    initSplitContainers(target);
});