(function () {
    const instances = new WeakMap();

    function fitHeight(grid) {
        // Вычисляем доступную высоту: от верха грида до низа окна
        const top = grid.getBoundingClientRect().top;
        const available = window.innerHeight - top;
        if (available > 100) {
            grid.style.height = available + 'px';
        }
    }

    function initSplits() {
        document.querySelectorAll('[data-split-grid]').forEach(grid => {
            if (instances.has(grid)) return;

            const key = 'split:' + grid.dataset.splitGrid;
            const saved = localStorage.getItem(key);

            const columnGutters = [...grid.querySelectorAll(':scope > [data-split-col]')]
                .map(el => ({ element: el, track: Number(el.dataset.splitCol) }));
            const rowGutters = [...grid.querySelectorAll(':scope > [data-split-row]')]
                .map(el => ({ element: el, track: Number(el.dataset.splitRow) }));

            if (columnGutters.length === 0 && rowGutters.length === 0) {
                return;
            }

            // 1. Ставим реальную высоту в inline-стиль (обходит Shadow DOM)
            fitHeight(grid);

            // 2. Начальные треки, если их ещё нет
            if (rowGutters.length > 0 && !grid.style.gridTemplateRows) {
                grid.style.gridTemplateRows = '1fr 6px 1fr';
            }
            if (columnGutters.length > 0 && !grid.style.gridTemplateColumns) {
                grid.style.gridTemplateColumns = '1fr 6px 1fr';
            }

            // 3. Восстанавливаем сохранённые размеры
            if (saved) {
                try {
                    const s = JSON.parse(saved);
                    if (s.cols) grid.style.gridTemplateColumns = s.cols;
                    if (s.rows) grid.style.gridTemplateRows = s.rows;
                } catch (e) { /* ignore */ }
            }

            try {
                const instance = Split({
                    columnGutters,
                    rowGutters,
                    minSize: Number(grid.dataset.splitMin || 50),
                    onDragEnd() {
                        localStorage.setItem(key, JSON.stringify({
                            cols: grid.style.gridTemplateColumns,
                            rows: grid.style.gridTemplateRows,
                        }));
                    },
                });
                instances.set(grid, instance);
            } catch (e) {
                console.error('[SplitGrid] ❌', grid.dataset.splitGrid, e);
            }
        });
    }

    // Пересчёт высоты при ресайзе окна
    window.addEventListener('resize', () => {
        document.querySelectorAll('[data-split-grid]').forEach(fitHeight);
    });

    document.addEventListener('DOMContentLoaded', initSplits);
    document.addEventListener('htmx:afterSettle', initSplits);
})();