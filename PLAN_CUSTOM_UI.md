# PLAN: Custom UI — произвольные HTML-страницы модулей внутри frame системы

## 0. Проверка тезиса «schema-driven UI тянет не-CRUD»

**Вердикт: сам по себе — нет, но каркас вокруг него — почти да.**

Что уже есть и работает на не-CRUD (проверено по коду):
- Транспорт событий **не завязан на CRUD**: `emit_event(formEvent)` → SSE-очередь сессии →
  клиентские свопы. Тип события — свободная строка (`personType`), шаблон ответа собирается
  из `dataForEvent[event.type]`.
- `putEvent.w(PutData)` умеет отрендерить **любой Jinja-шаблон с любым context** — это и есть
  готовая точка входа для кастомного UI.
- `metaSchema.typeForm` — простая строка, ничем не ограничена; генератор создаёт только
  `list`/`card`, но система их не проверяет жёстко.

Что блокирует сегодня:
1. `dictEvent.dataForEvent` — закрытый dict на 6 типов. Новый `typeEvent` без записи сюда →
   KeyError при первом же событии.
2. `webapp/web/templates/form/baseForm.html` — `{% if typeForm == 'list' %}...{% elif 'card' %}
   {% else %}ТАКОГО ТИПА ФОРМЫ НЕТ{% endif %}`. Т.е. UI — это switch по типу формы, а не
   реестр renderer'ов.
3. События могут порождать только core-классы (`EmptyPub`/`Form`) — у модуля нет легального
   способа сказать «открой мою страницу».
4. Нет механизма регистрации шаблонов модуля: `templates = Jinja2Templates(directory="webapp/web/templates")`
   — одна глобальная директория.

Вывод: идея пользователя («вкидывать свои html в frame») — правильный architectural escape hatch.
Это превращает «schema-driven или никак» в «schema-driven by default, custom when needed».

---

## 1. Концепция

Каждый модуль получает директорию `module/<code>/web/`:

```
module/dgn/
├── web/
│   ├── templates/          # Jinja2-шаблоны модуля (namespace: dgn/)
│   │   └── battle.html     # extends "main.html" OR partial-фрагмент для свопов
│   └── static/             # CSS/JS модуля (раздаётся с /static/dgn/...)
```

Форма в Dmeta объявляется как кастомная:

```json
// Bc_...Dmeta.json / Dgn_...Dmeta.json
{ "name": "Battle", "typeForm": "custom", "template": "dgn/battle.html" }
```

Правила:
- Рендерер выбирается по `typeForm`: `list`/`card` → встроенные, `custom` → шаблон из
  манифеста формы. Никаких new-типов enum не нужно — строка уже свободна.
- Кастомная страница живёт внутри общего frame (`main.html`): получает те же SSE-свопы,
  form_bar, title — т.е. остаётся частью системы, а не дикой iframe-вставкой.
- Опциональный режим `<iframe>` — только для внешнего контента (например, встроенный
  dashboards/grafana); для своих страниц iframe не нужен и вредит (стиль, SSE, auth).

## 2. Механика (по существующим точкам расширения)

### 2.1 Реестр renderer'ов вместо switch
`webapp/logic/dictEvent.py`:
```python
RENDERERS: dict[str, Callable[[formEvent], PutData]] = {
    "list": open_form, "card": open_form, ...  # текущее поведение
}
def register_renderer(typeForm: str, fn): RENDERERS[typeForm] = fn
```
Ключевые слова `typeForm` больше не замкнуты; `dataForEvent` тоже расширяется через
`register_event(typeEvent.openCustom, {...})`. Модули регистрируют в своём `config/hooks.json`
или явным импортом при загрузке модуля.

### 2.2 TemplateLoader модулей
`webapp/logic/var.py`: заменить одну директорию на `ChoiceLoader([FileSystemLoader(webapp),
*[FileSystemLoader(f"module/{m}/web/templates") for m in loaded_modules]])`.
Шаблон адресуется `dgn/battle.html` — namespace = код модуля, коллизий нет.

### 2.3 Раздача статики
При загрузке модуля: `app.mount(f"/static/{code}", StaticFiles(...))` — JS/CSS модуля
без пересборки фронтенда.

### 2.4 Двусторонняя связь кастомной страницы с @Oper
Не изобретаем ничего: у кастомной страницы тот же контракт, что у list/card —
`POST /api/action_oper` с `form=Dgn_Run/Battle` + payload. Для боя:
`htmx.post('/api/action_oper', {form:'Dgn_Run/Battle', oper:'useSkill', heroId, skillId, targetPos})`
→ сервер считает ход → `emit_event(refresh)` → страница получает новый HTML-фрагмент
(или отдельный event `battle:turn` со своим шаблоном — см. 2.1).

### 2.5 Безопасность (обязательно, иначе фича = XSS-конвейер)
- В `validateOpenClass`/`open_form` добавить whitelist: форма доступна как custom, только если
  её `template` лежит в `module/<код>/web/templates` того же модуля (проверка пути после
  normpath, запрет `..`).
- Шаблоны модулей рендерятся тем же Jinja2-движком — документировать: `|e` по умолчанию,
  raw-HTML только из доверенных источников.
- Если оставляем iframe-режим: `sandbox="allow-scripts"` без `allow-same-origin`, CSP
  `frame-src 'self'`.

## 3. Этапы

| # | Задача | Объём |
|---|--------|-------|
| 1 | ChoiceLoader + mount статики модулей | S |
| 2 | Вынести выбор шаблона из baseForm.html в `PutData.name_template`; ветка `typeForm=='custom'` в `open_form` | S |
| 3 | `register_renderer` / расширяемый `dataForEvent` (убрать закрытые dict'ы) | M |
| 4 | Whitelist проверка путей шаблонов + тесты на path traversal | S |
| 5 | Демо: `module/dgn/web/templates/battle.html` (боевой экран DGN из PLAN_DGN) | M |
| 6 | Документация контракта в README/CONVENTION (что может кастомный шаблон: SSE-события, action_oper, form_bar) | S |

Этап 5 — одновременно и есть **проверка тезиса**: если боевой экран DD-like собирается на
этём каркасе без правок ядра (кроме регистрации renderer'а) — тезис подтверждён.

## 4. Риски
- Регистрируя кастомщину, теряем гарантию «весь UI консистентен» — лечится базовым
  CSS-каркасом (`main.css` переменные + класс `.frame-content`), который шаблоны модулей
  должны использовать.
- Синхронизация состояния: кастомная страница не знает про active_row/фильтры Form —
  контракт: сервер всегда кладёт данные в context, страница ничего сама не грузит.
- Баг с session_id (все в "default") станет критичнее: два браузера будут драться за один
  активный custom-форм. Чинить в первую очередь (см. PLAN_DGN этап 0).
