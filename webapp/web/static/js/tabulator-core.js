(function () {
    "use strict";

    const registry = new Map();

    function initTable(el) {
        if (registry.has(el.id)) return;
        if (!el.dataset.tabulator) return;

        const cfg = JSON.parse(el.dataset.tabulator);

        const opts = {
            index: "id",
            columns: cfg.columns,
            layout: "fitColumns",
            height: "100%",
            placeholder: "Нет данных",
            movableColumns: cfg.options?.movableColumns ?? true,
            resizableColumns: cfg.options?.resizableColumns ?? true,
        };

        // Remote или локально?
        if (cfg.url) {
            opts.ajaxURL = cfg.url;
            opts.ajaxConfig = { method: "GET" };
        } else {
            opts.data = cfg.data || [];
        }

        const table = new Tabulator(el, opts);
        registry.set(el.id, table);
        console.log("Tabulator:", el.id, cfg.url ? "remote" : "local");
    }

    function destroyTable(el) {
        const t = registry.get(el.id);
        if (t) { t.destroy(); registry.delete(el.id); }
    }

    function redrawTable(el) {
        const t = registry.get(el.id);
        if (t) t.redraw(true);
    }

    function setupEventListeners() {
        // Проверяем, что body существует
        if (!document.body) {
            console.warn("document.body ещё не готов, ждём...");
            return false;
        }

        // 1. Инициализация при загрузке
        document.querySelectorAll(".app-table").forEach(initTable);

        // 2. HTMX подгрузил фрагмент
        document.body.addEventListener("htmx:load", (e) => {
            e.detail.elt.querySelectorAll(".app-table").forEach(initTable);
        });

        // 3. Shoelace: вкладка стала активной
        document.body.addEventListener("sl-show", (e) => {
            const panel = e.detail?.target || e.target;
            if (!panel?.querySelectorAll) return;
            panel.querySelectorAll(".app-table").forEach((el) => {
                initTable(el);
                redrawTable(el);
            });
        });

        // 4. Очистка при удалении
        document.body.addEventListener("htmx:beforeCleanupElement", (e) => {
            const el = e.detail.elt;
            if (el.classList?.contains("app-table")) destroyTable(el);
            else el.querySelectorAll(".app-table").forEach(destroyTable);
        });

        console.log("Event listeners setup complete");
        return true;
    }

    // Пробуем инициализировать
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", () => {
            if (!setupEventListeners()) {
                // Если body всё ещё null, ждём полной загрузки
                window.addEventListener("load", setupEventListeners);
            }
        });
    } else {
        // DOM уже готов
        if (!setupEventListeners()) {
            window.addEventListener("load", setupEventListeners);
        }
    }
})();