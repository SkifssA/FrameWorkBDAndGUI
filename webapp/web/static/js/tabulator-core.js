(function () {
    "use strict";

    const registry = new Map();

    function initTable(el) {

        if (registry.has(el.id)) {
            return;
        }

        if (!el.dataset.tabulator) {
            return;
        }

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

        const table = new Tabulator(el, opts);
        registry.set(el.id, table);
        console.log('[Tabulator] ✅ Таблица создана:', el.id);
    }

    function destroyTable(el) {
        const t = registry.get(el.id);
        if (t) {
            t.destroy();
            registry.delete(el.id);
        } else {
            console.warn('[Tabulator] Таблица не найдена в реестре:', el.id);
        }
    }

    function redrawTable(el) {
        const t = registry.get(el.id);
        if (t) {
            t.redraw(true);
        }
    }

    function setupEventListeners() {
        if (!document.body) return false;

        // 1. Инициализация при первой загрузке
        document.querySelectorAll(".app-table").forEach(el => {
            initTable(el);
        });

        // 2. HTMX подгрузил новый фрагмент
        document.body.addEventListener("htmx:load", (e) => {
            const tables = e.detail.elt.querySelectorAll(".app-table");
            tables.forEach(el => {
                initTable(el);
            });
        });

        // 3. Shoelace: вкладка стала активной
        document.body.addEventListener("sl-show", (e) => {
            const panel = e.detail?.target || e.target;
            if (!panel?.querySelectorAll) return;
            panel.querySelectorAll(".app-table").forEach((el) => {
                initTable(el);
                setTimeout(() => redrawTable(el), 50);
            });
        });

        // 4. Очистка при удалении
        document.body.addEventListener("htmx:beforeCleanupElement", (e) => {
            const el = e.detail.elt;
            if (el.classList?.contains("app-table")) {
                destroyTable(el);
            } else {
                el.querySelectorAll(".app-table").forEach(destroyTable);
            }
        });

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
            tables.forEach(destroyTable);
        },
        has: function (id) { return registry.has(id); },
        get: function (id) { return registry.get(id); },
        registry: registry  // для отладки
    };
})();