window.activateNewTab = function (group) {
    // group — это гарантированно тот <sl-tab-group>, на котором висит hx-on
    if (!group) {
        console.error('[activateNewTab] group не передан');
        return;
    }

    setTimeout(() => {
        const tabs = group.querySelectorAll('sl-tab[slot="nav"]');

        if (tabs.length > 0) {
            const lastTab = tabs[tabs.length - 1];
            if (lastTab && lastTab.panel) {
                group.show(lastTab.panel);
            } else {
                console.warn('[activateNewTab] У последнего таба нет panel');
            }
        }
    }, 50);
};