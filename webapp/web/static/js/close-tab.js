document.addEventListener('sl-close', (event) => {
    const tab = event.target;
    if (tab.tagName !== 'SL-TAB') return;

    const tabGroup = tab.closest('sl-tab-group');
    if (!tabGroup) return;

    const panel = tabGroup.querySelector(`sl-tab-panel[name="${tab.panel}"]`);
    const panelId = tab.panel;

    // 1. Переключаемся на соседнюю вкладку, если закрываем активную
    if (tab.active) {
        const allTabs = Array.from(tabGroup.querySelectorAll('sl-tab[slot="nav"]'));
        const currentIndex = allTabs.indexOf(tab);
        const prevTab = allTabs[currentIndex - 1];
        const nextTab = allTabs[currentIndex + 1];

        if (prevTab) tabGroup.show(prevTab.panel);
        else if (nextTab) tabGroup.show(nextTab.panel);
    }

    // 2. Уведомляем сервер
    fetch('/app/close_tab', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tab_name: panelId })
    }).catch(err => console.error('Ошибка уведомления сервера:', err));

    // 3. ЯВНАЯ ОЧИСТКА РЕЕСТРА — не зависим от htmx:beforeCleanupElement
    if (window.TabulatorManager && panel) {
        console.log('[sl-close] Очистка таблиц в панели:', panelId);
        window.TabulatorManager.destroyAll(panel);
    }

    // 4. Удаляем DOM. Используем htmx.remove если доступен, иначе нативный remove
    const safeRemove = (el) => {
        if (!el) return;
        try {
            if (typeof htmx !== 'undefined' && typeof htmx.remove === 'function') {
                htmx.remove(el);
            } else {
                el.remove();
            }
        } catch (e) {
            console.warn('[sl-close] htmx.remove не сработал, fallback на .remove():', e);
            el.remove();
        }
    };

    safeRemove(panel);
    safeRemove(tab);
});