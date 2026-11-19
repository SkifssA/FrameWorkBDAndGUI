window.activateNewTab = function (element) {
    const tabGroup = element.closest ? element.closest('sl-tab-group') : element;
    if (!tabGroup || tabGroup.tagName !== 'SL-TAB-GROUP') return;

    // Отсекаем вложенные tab-group
    if (tabGroup.parentElement.closest('sl-tab-group')) return;

    if (tabGroup.id !== 'main_menu') return;

    requestAnimationFrame(() => {
        // 🔑 КЛЮЧЕВОЕ ИЗМЕНЕНИЕ: ищем только прямых дочерних табов
        const tabs = tabGroup.querySelectorAll(':scope > sl-tab[slot="nav"]');

        if (tabs.length > 0) {
            const lastTab = tabs[tabs.length - 1];
            const panelName = lastTab.getAttribute('panel');

            if (panelName) {
                console.log('[activateNewTab] ✅ Верхний уровень! Панель:', panelName);
                tabGroup.show(panelName);
            }
        }
    });
};