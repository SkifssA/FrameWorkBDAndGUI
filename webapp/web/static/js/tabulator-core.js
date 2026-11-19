(function () {
    "use strict";

    const registry = new Map();

    function initTable(el) {
        console.log('[Tabulator] initTable вызван для:', el.id, 'Классы:', el.className);

        if (registry.has(el.id)) {
            console.log('[Tabulator] Таблица уже в реестре, пропускаем:', el.id);
            return;
        }

        if (!el.dataset.tabulator) {
            console.warn('[Tabulator] Нет data-tabulator атрибута:', el.id);
            return;
        }

        console.log('[Tabulator] Парсим конфиг для:', el.id);
        let cfg;
        try {
            cfg = JSON.parse(el.dataset.tabulator);
        } catch (e) {
            console.error('[Tabulator] Ошибка парсинга JSON для:', el.id, e);
            return;
        }

        const opts = {
            index: "id",
            columns: cfg.columns,
            layout: "fitColumns",
            height: "100%",
            placeholder: "Нет данных",
            movableColumns: cfg.options?.movableColumns ?? true,
            resizableColumns: cfg.options?.resizableColumns ?? true,
        };

        if (cfg.url) {
            opts.ajaxURL = cfg.url;
            opts.ajaxConfig = { method: "GET" };
        } else {
            opts.data = cfg.data || [];
        }

        console.log('[Tabulator] Создаём таблицу:', el.id, 'URL:', cfg.url || 'локально');
        const table = new Tabulator(el, opts);
        registry.set(el.id, table);
        console.log('[Tabulator] ✅ Таблица создана:', el.id);
    }

    function destroyTable(el) {
        console.log('[Tabulator] destroyTable вызван для:', el.id);
        const t = registry.get(el.id);
        if (t) {
            console.log('[Tabulator] Уничтожаем таблицу:', el.id);
            t.destroy();
            registry.delete(el.id);
            console.log('[Tabulator] ✅ Таблица уничтожена и удалена из реестра:', el.id);
        } else {
            console.warn('[Tabulator] Таблица не найдена в реестре:', el.id);
        }
    }

    function redrawTable(el) {
        const t = registry.get(el.id);
        if (t) {
            t.redraw(true);
            console.log('[Tabulator] Redraw:', el.id);
        }
    }

    function setupEventListeners() {
        if (!document.body) return false;

        // 1. Инициализация при первой загрузке
        console.log('[Tabulator] Сканируем DOM при загрузке...');
        document.querySelectorAll(".app-table").forEach(el => {
            console.log('[Tabulator] Найдена таблица при загрузке:', el.id);
            initTable(el);
        });

        // 2. HTMX подгрузил новый фрагмент
        document.body.addEventListener("htmx:load", (e) => {
            console.log('[Tabulator] htmx:load сработал. Элемент:', e.detail.elt);
            const tables = e.detail.elt.querySelectorAll(".app-table");
            console.log('[Tabulator] Найдено таблиц в фрагменте:', tables.length);
            tables.forEach(el => {
                console.log('[Tabulator] Инициализируем из htmx:load:', el.id);
                initTable(el);
            });
        });

        // 3. Shoelace: вкладка стала активной
        document.body.addEventListener("sl-show", (e) => {
            const panel = e.detail?.target || e.target;
            if (!panel?.querySelectorAll) return;
            console.log('[Tabulator] sl-show для панели:', panel);
            panel.querySelectorAll(".app-table").forEach((el) => {
                console.log('[Tabulator] Инициализируем из sl-show:', el.id);
                initTable(el);
                setTimeout(() => redrawTable(el), 50);
            });
        });

        // 4. Очистка при удалении
        document.body.addEventListener("htmx:beforeCleanupElement", (e) => {
            console.log('[Tabulator] htmx:beforeCleanupElement:', e.detail.elt);
            const el = e.detail.elt;
            if (el.classList?.contains("app-table")) {
                destroyTable(el);
            } else {
                el.querySelectorAll(".app-table").forEach(destroyTable);
            }
        });

        console.log("[Tabulator Manager] Event listeners setup complete");
        return true;
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", () => {
            if (!setupEventListeners()) window.addEventListener("load", setupEventListeners);
        });
    } else {
        if (!setupEventListeners()) window.addEventListener("load", setupEventListeners);
    }

    // Публичный API для внешней очистки
    window.TabulatorManager = {
        destroy: destroyTable,
        destroyAll: function (container) {
            if (!container || !container.querySelectorAll) return;
            const tables = container.querySelectorAll('.app-table');
            console.log('[TabulatorManager] destroyAll: найдено таблиц:', tables.length);
            tables.forEach(destroyTable);
        },
        has: function (id) { return registry.has(id); },
        get: function (id) { return registry.get(id); },
        registry: registry  // для отладки
    };
})();