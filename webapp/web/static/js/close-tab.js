document.addEventListener('sl-close', (event) => {
    // 1. Безопасное получение таба (на случай, если клик был по иконке внутри)
    const tab = event.target.closest('sl-tab');
    if (!tab) return;

    const tabGroup = tab.closest('sl-tab-group');
    if (!tabGroup) return;

    // Используем getAttribute, это надёжнее, чем свойство .panel
    const panelId = tab.getAttribute('panel');
    const panel = tabGroup.querySelector(`sl-tab-panel[name="${panelId}"]`);

    // 2. Переключаемся на соседнюю вкладку, если закрываем активную
    // hasAttribute надёжнее, чем tab.active во время событий
    if (tab.hasAttribute('active')) {
        const allTabs = Array.from(tabGroup.querySelectorAll(':scope > sl-tab[slot="nav"]'));
        const currentIndex = allTabs.indexOf(tab);
        const prevTab = allTabs[currentIndex - 1];
        const nextTab = allTabs[currentIndex + 1];

        const targetTab = prevTab || nextTab;
        if (targetTab) {
            const targetPanelId = targetTab.getAttribute('panel');
            // Вызываем переключение
            tabGroup.show(targetPanelId);
        }
    }

    // 3. Уведомляем сервер (в фоне, не блокируем UI)
    fetch('/app/close_tab', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tab_name: panelId })
    }).catch(err => console.error('Ошибка уведомления сервера:', err));

    // 4. ЯВНАЯ ОЧИСТКА РЕЕСТРА Tabulator
    if (window.TabulatorManager && panel) {
        console.log('[sl-close] Очистка таблиц в панели:', panelId);
        window.TabulatorManager.destroyAll(panel);
    }

    // 5. БЕЗОПАСНОЕ УДАЛЕНИЕ DOM
    // requestAnimationFrame гарантирует, что удаление произойдёт ПОСЛЕ того, 
    // как браузер отрисует результат tabGroup.show(), избежая конфликтов анимаций Shoelace
    requestAnimationFrame(() => {
        const safeRemove = (el) => {
            if (!el) return;
            try {
                if (typeof htmx !== 'undefined' && typeof htmx.remove === 'function') {
                    htmx.remove(el);
                } else {
                    el.remove();
                }
            } catch (e) {
                console.warn('[sl-close] Ошибка удаления элемента:', e);
                el.remove(); // Fallback
            }
        };

        safeRemove(panel);
        safeRemove(tab);
    });
});