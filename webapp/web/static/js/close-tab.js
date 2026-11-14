document.addEventListener('sl-close', (event) => {
    const tab = event.target;
    if (tab.tagName !== 'SL-TAB') return;

    const tabGroup = tab.closest('sl-tab-group');
    if (!tabGroup) return;

    const panel = tabGroup.querySelector(`sl-tab-panel[name="${tab.panel}"]`);

    // Переключаемся на соседнюю вкладку
    if (tab.active) {
        const allTabs = Array.from(tabGroup.querySelectorAll('sl-tab[slot="nav"]'));
        const currentIndex = allTabs.indexOf(tab);
        const prevTab = allTabs[currentIndex - 1];
        const nextTab = allTabs[currentIndex + 1];

        if (prevTab) tabGroup.show(prevTab.panel);
        else if (nextTab) tabGroup.show(nextTab.panel);
    }

    // Уведомляем сервер о закрытии вкладки
    fetch('/app/close_tab', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tab_name: tab.panel })
    });

    tab.remove();
    if (panel) panel.remove();
});
