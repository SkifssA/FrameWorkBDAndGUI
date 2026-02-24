# 🍺 Tavern Hero: DPG-Driven Idle RPG

[![Status](https://img.shields.io/badge/status-experimental-orange)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)]()
[![GUI](https://img.shields.io/badge/GUI-DearPyGui-purple)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

Tavern Hero — это текстовая Idle RPG, построенная на базе кастомной системы управления данными с интерфейсом на **Dear PyGui**.

Проект демонстрирует возможность создания полноценного игрового цикла (Game Loop) внутри десктопного приложения, где состояние игры хранится в БД, логика выполняется фоновыми скриптами, а интерфейс отрисовывается через DPG.

## 🗺️ Дорожная карта (Roadmap)

### Phase 0: Foundation (MVP) 🚧
- [ ] Настройка схемы БД.
- [ ] Загрузка списка героев.
- [ ] Отрисовка таблицы героев и карточки свойств.
- [ ] Базовый скрипт регенерации энергии (фон).

### Phase 1: Core Loop
- [ ] Реализация боевого скрипта (расчет урона, лут).
- [ ] Вывод лога боя в интерфейс в реальном времени.
- [ ] Система предметов и инвентаря.

### Phase 2: Visuals & UX
- [ ] Темы оформления (Dark mode, цветовое кодирование редкости).
- [ ] Всплывающие уведомления (Toasts) через `dpg.add_window`.
- [ ] Графики статистики (золото, опыт) через `dpg.add_plot`.

### Phase 3: Endgame
- [ ] Боссы и рейды на несколько героев.
- [ ] Система достижений.
- [ ] Упаковка в .exe (PyInstaller).

## 🚀 Запуск (Local Development)

### Требования
- Python 3.8+
- Dear PyGui


🤝 Contributing
Это личный pet-проект, но идеи по балансу, баг-репорты или предложения по UI приветствуются (Issues).
📄 License
MIT © Skifss