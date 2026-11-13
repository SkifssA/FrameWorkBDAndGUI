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
window.callOper = function (operId, formName) {
    const url = `/${formName}/Default/action/${operId}`;

    if (typeof htmx !== 'undefined') {
        htmx.ajax('GET', url, {
            target: '#app-content',
            swap: 'innerHTML'
        });
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