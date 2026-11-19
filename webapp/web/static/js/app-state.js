/* ============================================================
   APP-STATE.JS — глобальное состояние приложения на Alpine.js
   БЕЗ $nextTick, БЕЗ сложных зависимостей
   ============================================================ */

// Ждём, пока Alpine загрузится
document.addEventListener('alpine:init', () => {

    Alpine.data('appState', () => ({
        showSidebar: true,
        activeTabId: 'home',
        tabs: [
            { id: 'home', title: 'Главная', icon: 'house', url: '/api/home' }
        ],

        // Инициализация — просто, без $nextTick
        init() {
            console.log('appState initialized');
            // Контент загрузится через SSE openApp, здесь ничего не делаем
        },

        // Переключить вкладку
        switchTab(id) {
            this.activeTabId = id;
            this.loadTabContent(id);
        },

        // Открыть модуль
        openModule(moduleId, moduleName) {
            const id = `mod-${moduleId}`;

            // Если вкладка уже есть — просто переключаемся
            if (this.tabs.find(t => t.id === id)) {
                this.switchTab(id);
                return;
            }

            // Добавляем новую вкладку
            this.tabs.push({
                id: id,
                title: moduleName,
                icon: 'folder',
                url: `/api/module/${moduleId}/menu`
            });

            this.activeTabId = id;
            this.loadTabContent(id);
        },

        // Закрыть вкладку
        closeTab(id, event) {
            if (event) event.stopPropagation();

            const index = this.tabs.findIndex(t => t.id === id);
            if (index === -1) return;

            this.tabs.splice(index, 1);

            // Если закрыли активную — переключаемся на соседнюю
            if (this.activeTabId === id) {
                const newTab = this.tabs[Math.max(0, index - 1)] || this.tabs[0];
                if (newTab) {
                    this.activeTabId = newTab.id;
                    this.loadTabContent(newTab.id);
                }
            }
        },

        // Загрузить контент вкладки через HTMX
        loadTabContent(tabId) {
            const tab = this.tabs.find(t => t.id === tabId);
            if (!tab) return;

            const container = document.getElementById(`panel-${tabId}`);
            if (!container) return;

            // Если контент уже загружен — не грузим повторно
            if (container.dataset.loaded === tab.url) return;

            // Проверяем, что HTMX доступен
            if (typeof htmx !== 'undefined') {
                htmx.ajax('GET', tab.url, {
                    target: container,
                    swap: 'innerHTML'
                });
                container.dataset.loaded = tab.url;
            } else {
                console.warn('HTMX not loaded yet');
            }
        },

        // Действия меню
        toggleSidebar() {
            this.showSidebar = !this.showSidebar;
        },

        saveCurrent() {
            this.$dispatch('save-request', { tabId: this.activeTabId });
        },

        closeCurrent() {
            const tab = this.tabs.find(t => t.id === this.activeTabId);
            if (tab) this.closeTab(tab.id);
        },

        openHomeTab() {
            this.switchTab('home');
        },

        showAbout() {
            document.querySelector('#about-dialog')?.show();
        },

        toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        },

        exitApp() {
            if (confirm('Закрыть приложение?')) {
                window.close();
            }
        }
    }));

    console.log('appState registered with Alpine');
});

// Глобальная функция для вызова операций из меню
window.callOper = function (operId, formName, sel = 'Default') {
    const url = `/app/${formName}/${sel}/action/${operId}`;

    if (typeof htmx !== 'undefined') {
        htmx.ajax('GET', url);
    }

    // Закрываем все открытые меню
    document.querySelectorAll('sl-dropdown[open]').forEach(dd => {
        dd.open = false;
    });
};

// Горячие клавиши
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'b') {
        e.preventDefault();
        document.dispatchEvent(new CustomEvent('toggle-sidebar'));
    }
    if (e.ctrlKey && e.key === 'w') {
        e.preventDefault();
        document.dispatchEvent(new CustomEvent('close-current-tab'));
    }
});

document.addEventListener('htmx:afterSettle', function (event) {
    const target = event.detail.elt || document;

    const containers = [];
    if (target.classList && target.classList.contains('auto-split')) {
        containers.push(target);
    }
    if (target.querySelectorAll) {
        target.querySelectorAll('.auto-split').forEach(el => containers.push(el));
    }

    // Сортируем по глубине вложенности: сначала внешние (меньше ancestors), потом внутренние
    containers.sort((a, b) => {
        let depthA = 0, depthB = 0;
        let nodeA = a, nodeB = b;
        while (nodeA.parentElement) { depthA++; nodeA = nodeA.parentElement; }
        while (nodeB.parentElement) { depthB++; nodeB = nodeB.parentElement; }
        return depthA - depthB; // внешние первыми
    });

    containers.forEach(initSplit);

    function initSplit(el) {
        if (el.dataset.splitInit) return;

        const direction = el.dataset.splitDirection || 'horizontal';
        const sizes = el.dataset.splitSizes ? el.dataset.splitSizes.split(',').map(Number) : null;
        const minSize = Number(el.dataset.splitMinSize) || 100;
        const gutter = Number(el.dataset.splitGutter) || 8;

        const children = Array.from(el.children).filter(c => c.tagName === 'DIV');

        const options = {
            direction: direction,
            minSize: minSize,
            gutterSize: gutter,
            elementStyle: function (dimension, size, gutterSize) {
                return {
                    'flex-basis': 'calc(' + size + '% - ' + gutterSize + 'px)'
                };
            },
            gutterStyle: function (dimension, gutterSize) {
                return {
                    'flex-basis': gutterSize + 'px'
                };
            }
        };

        if (sizes) options.sizes = sizes;

        Split(children, options);

        el.dataset.splitInit = 'true';
    }
});