/**
 * Рекурсивно ищет первый элемент (начиная с panel), 
 * у которого в инлайн-стилях задан нужный лимит.
 */
function findElementWithLimit(element, cssProp) {
    // Проверяем сам элемент
    if (element.style && element.style.getPropertyValue(cssProp)) {
        return element;
    }

    // Рекурсивно ищем в детях
    if (element.children) {
        for (let child of element.children) {
            const found = findElementWithLimit(child, cssProp);
            if (found) return found;
        }
    }

    return null;
}

function getLimit(panel, isVertical, type, container) {
    const inlineProp = `${type}${isVertical ? 'Height' : 'Width'}`; // maxHeight
    const cssProp = inlineProp.replace(/([A-Z])/g, '-$1').toLowerCase(); // max-height

    // Ищем элемент с нужным стилем (рекурсивно по всем потомкам)
    const targetElement = findElementWithLimit(panel, cssProp);

    if (targetElement) {
        // getComputedStyle переведёт значения в пиксели
        const computedVal = window.getComputedStyle(targetElement)[inlineProp];
        const parsed = parseFloat(computedVal);
        if (!isNaN(parsed)) return parsed;
    }

    // Дефолтная логика, если стилей нет вообще нигде
    if (type === 'min') {
        return isVertical ? 100 : 160;
    } else {
        return isVertical ? container.clientHeight * 0.5 : container.clientWidth * 0.5;
    }
}

function initResizer(container) {
    const handles = container.querySelectorAll('.resize-handle');
    if (handles.length === 0) return;

    handles.forEach(handle => {
        handle.addEventListener('mousedown', onMouseDown);
        handle.addEventListener('dblclick', onDblClick);
    });

    function onMouseDown(e) {
        e.preventDefault();
        const handle = e.currentTarget;
        const targetName = handle.dataset.target;

        let panel;
        if (targetName === 'left') {
            panel = handle.previousElementSibling;
        } else {
            panel = handle.nextElementSibling;
        }

        if (!panel) return;

        const isVertical = targetName === 'bottom';
        const startPos = isVertical ? e.clientY : e.clientX;
        const startSize = isVertical
            ? panel.getBoundingClientRect().height
            : panel.getBoundingClientRect().width;

        handle.classList.add('is-dragging');
        document.body.classList.add('is-resizing');

        function onMouseMove(moveEvent) {
            const currentPos = isVertical ? moveEvent.clientY : moveEvent.clientX;
            const delta = currentPos - startPos;

            const isShrinking = (targetName === 'right' || targetName === 'bottom');
            const newSize = isShrinking ? startSize - delta : startSize + delta;

            // 🔥 Передаём container в getLimit
            const min = getLimit(panel, isVertical, 'min', container);
            const max = getLimit(panel, isVertical, 'max', container);

            console.log(min, max, panel)

            const clamped = Math.max(min, Math.min(max, newSize));
            panel.style.flexBasis = clamped + 'px';
        }

        function onMouseUp() {
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
            handle.classList.remove('is-dragging');
            document.body.classList.remove('is-resizing');
        }

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
    }

    function onDblClick(e) {
        const targetName = e.currentTarget.dataset.target;
        let panel;
        if (targetName === 'left') {
            panel = e.currentTarget.previousElementSibling;
        } else {
            panel = e.currentTarget.nextElementSibling;
        }
        if (panel) panel.style.flexBasis = '';
    }
}

// Наблюдаем за появлением #closeForm
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
            if (node.nodeType === 1) {
                if (node.id === 'closeForm') {
                    initResizer(node);
                } else {
                    const form = node.querySelector('#closeForm');
                    if (form) initResizer(form);
                }
            }
        });
    });
});
observer.observe(document.body, { childList: true, subtree: true });

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('closeForm');
    if (form) initResizer(form);
});

document.addEventListener('htmx:afterSwap', (e) => {
    const target = e.detail.target;
    if (!target) return;

    if (target.id === 'closeForm') {
        initResizer(target);
    } else {
        const form = target.querySelector('#closeForm');
        if (form) initResizer(form);
    }
});