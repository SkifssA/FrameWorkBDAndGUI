document.addEventListener('htmx:sseBeforeMessage', function (event) {

    if (event.detail.type === 'switchTab') {
        try {
            const data = JSON.parse(event.detail.data);

            let tabGroup = null;
            for (const g of document.querySelectorAll('sl-tab-group')) {
                const found = g.querySelector(`sl-tab[panel="${data.panel}"]`);
                if (found) {
                    tabGroup = g;
                    break;
                }
            }

            if (tabGroup) {
                tabGroup.show(data.panel);
                event.preventDefault();
            } else {
                console.warn('[DIAG switchTab] ❌ Группа с таким табом не найдена');
            }
        } catch (e) {
            console.error('[DIAG switchTab] ❌ Ошибка:', e);
        }
    }

});