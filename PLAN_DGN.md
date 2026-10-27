# План модуля Dgn — Darkest Dungeon-кролик на базе Sourcerer Generator

> Идея: пошаговый roguelike-бой (отряд 4 героя × позиции 1–4, генсдизайн через броски точности/урона,
> стресс и аффликции) как прикладной модуль платформы. Модуль специально спроектирован так,
> чтобы стресс-тестировать слабые места ядра (см. раздел «Бенчмарк для платформы»).

---

## 0. Предварительные условия (блокеры — чиним до начала)

| # | Блокер | Где | Зачем Dgn |
|---|--------|-----|-----------|
| B1 | `_getFormByName` падает на AttributeError | `core/empty/pub.py` | Реестр @Oper не переживёт динамическое разрешение форм |
| B2 | Сессии без `session_id` cookie | webapp middleware | Бои живут в сессии; сейчас все игроки делят один `"default"` session |
| B3 | Утечка `user_sessions` | SSE queue | Забег генерирует много событий — dict разрастётся |
| B4 | Синхронный libsql в async-пути | Turso client | Каждый ход = несколько записей в RunLog; нужен threadpool или батчинг |
| B5 | Дубли operation id в эндпоинтах | `projectEndPoint.py` | Dgn добавит свои роуты — конфликт усугубится |
| B6 | Golden-тесты builders рассинхронизированы | `tests/core/test_bilders.py` | Генерация слоёв Dgn должна быть воспроизводима |

**Критерий выхода:** pytest зелёный (91+ тестов), два браузера имеют разные сессии.

---

## 1. Структура модуля

```
module/dgn/
├── module.yaml          # манифест: имя, версии слоёв, hooks (пустой — см. баг runHook)
├── odb/                 # схема данных (source of truth)
│   ├── hero_class.py    # Metaclass HeroClass
│   ├── hero.py          # Metaclass Hero, RosterSlot
│   ├── skill.py         # Metaclass Skill
│   ├── trait.py         # Metaclass Trait, Affliction
│   ├── enemy.py         # Metaclass EnemyType
│   ├── dungeon.py       # Metaclass DungeonZone, Run, RunLog, Protagonist
│   └── *_dpi.py         # сгенерированные классы (не трогать руками — createFileA/D)
├── dmeta/               # метаданные форм (schema-driven UI)
│   ├── hero_form.py     # карточка героя: HP/STRESS бары, инвентарь
│   ├── battle_form.py   # боевой экран: отряд × враги, кнопки @Oper
│   └── ...
├── ameta/               # ручные дополнения к метаданным
├── logic/               # НЕ генерируется — чистая игровая логика
│   ├── rng.py           # seed-based RNG (детерминизм забега)
│   ├── combat.py        # разрешалка хода: accuracy roll → damage → stress
│   ├── affliction.py    # checkAfflictionRoll, флаги (irrational, death's aid...)
│   └── loot.py          # награды после боя
├── hooks/               # on_startup: регистрация справочников (после починки B-runHook)
└── tests/
    ├── test_combat_math.py
    ├── test_affliction.py
    └── test_run_determinism.py
```

Правила именования — по `CONVENTION_MODULE_NAMING.md`: `Dgn_HeroPub`, `Dgn_BattleOper` и т.д.

---

## 2. Модель данных (odb)

### Справочники (претсеты, редактируются в UI)
- **HeroClass**: name, positions(1-4 allowed), stats_json `{hp, spd, acc, dodge, crit, phys_dmg, stress_dmg, prot}`, skills_m2m → Skill
- **Skill**: name, target_rule (`enemy_single|enemy_row|ally_single|self|all`), base_acc, dmg_min/max, stress_min/max, heal, move_forward/back, buff_json, cooldown
- **Trait**: name, effect_json (триггер: `on_crit`, `on_stress_above_50`, ...)
- **Affliction**: name, chance_modifier, effects_json (−acc, +dmg vs afflicted, refusal to act...)
- **EnemyType**: stats_json, moves_m2m → Skill, loot_table_json
- **DungeonZone**: name, depth_max, rooms_count, enemy_pool_m2m → EnemyType, light_start

### Инстансы (игровые данные)
- **Protagonist**: hamlet-уровень, gold, supplies, unlock-флаги (json)
- **Hero**: class_FK, level, xp, hp_cur, stress, traits_m2m, quirks_json, gear_json, roster_slot_FK?
- **RosterSlot**: position(1-4), hero_FK nullable — состав отряда вне боя
- **Run**: protagonist_FK, zone_FK, seed, state_json (комната, свет, припасы), started_at
- **RunLog**: run_FK, seq_no, event_json — журнал всех бросков (для реплея и отладки)

Ключевое решение: **состояние боя держится в `Run.state_json`**, а не в памяти сервера —
переживает перезапуск dev-сервера и резолвит зависимость от бага B2/B3.

---

## 3. Игровой цикл как @Oper-ы

Все действия — методы с `@Oper` в `Dgn_RunPub` / `Dgn_BattleOper`, вызываются через ActionDispatcher (штатный путь платформы):

| Oper | Что делает | HTMX-ответ |
|------|-----------|------------|
| `startRun` | создаёт Run (seed), заполняет state | редирект на battle_form |
| `makeMove` | ход героя: accuracy roll → результат | fragment перерисовки поля боя + SSE-событие |
| `enemyTurn` | ИИ: выбор цели/умения, тот же разрешалкой | fragment |
| `checkStress` | после урона стресс: save-roll → affliction/flag | SSE-уведомление |
| `endBattle` | XP, лут, потери, смерть героя | screen результатов |
| `retreat` | probability by light level | fragment/SSE |

Математика — копия DD1 (проверена по открытым формулам):
```
hit_chance = base_acc * (100 - dodge)/100 * skill_mods, clamp [0..100]
crit: (100 - prot... ) — упрощённо: crit_roll < crit% → x2 dmg
stress_damage = base ± variance, модификаторы: fear-flag +25%, vs-afflicted +50%
affliction_roll: stress > threshold → roll < (stress/100 * mod) → аффликция
```

Детерминизм: все рандомы из `random.Random(run.seed + seq)` — забег воспроизводим по RunLog (тестируется!).

---

## 4. UI (dmeta + HTMX)

- **battle_form**: таблица 2×4 (отряд vs враги), у каждого слота — HP/STRESS прогресс-бары
  (`<progress>` + CSS), подсветка активной позиции, оверлей аффликции.
- Кнопки умения → `hx-post /api/action/{oper}` с payload (skill_id, target_pos).
- Анимации ударов — минимальные CSS-переходы; текст боя летит через **SSE-очередь сессии**
  (это обкатывает очереди на реальной нагрузке).
- **roster_form** — drag&drop позиций (потом; MVP — select'ы).
- Бары стресса/HP рисуются паттерном из Dmeta (проверка тезиса «schema-driven UI работает для не-CRUD» ).

---

## 5. Этапы

### MVP (1 вечер) — «бой в консоли через один oper»
- [ ] Починить B1 (getattr default=None) — 15 минут
- [ ] odb: HeroClass, Hero, Skill, EnemyType (только stats_json)
- [ ] Прогнать генератор → Dpi/Ameta, smoke-тест импорта
- [ ] `Dgn_RunPub.makeMove`: одна формула `(ATK*ACC)/(DEF)`, результат в RunLog
- [ ] Тест детерминизма: seed → предсказуемая последовательность
- Дефиниция готовности: два разных seed дают разные бои, одинаковый — идентичный лог.

### v0.2 — полный бой
- [ ] Позиции 1–4, move-skills (push/pull), AoE-правило (позиция влияет на цель)
- [ ] Очередь ходов по SPD, вражеский ИИ (взвешенный выбор из move-pool)
- [ ] Стресс → аффликции → флаги (irrational, fatalistic, death's aid, bloodlust)
- [ ] Смерть героя (death's save), ранения после боя
- [ ] Light-уровень и retreat

### v0.3 — забег и мета
- [ ] Комнатная цепочка DungeonZone, комнаты-события (json-диалоги)
- [ ] XP/level-up, лут (gear_json), возврат в Hamlet (Protagonist)
- [ ] Quirks (положительные/отрицательные)
- [ ] Экран результатов забега из RunLog (реплей!)

### v0.4 — полировка платформы
- [ ] JSON-редактор полей (type=json в Dmeta) — нужен для stats_json/effect_json
- [ ] Перенос состояния в Turso через threadpool (обкатка B4 под нагрузкой)
- [ ] SSE-стрим боя (обкатка B2/B3)

---

## 6. Бенчмарк для платформы (зачем это нужно ядру)

| Фича Dgn | Что проверяет в ядре |
|----------|---------------------|
| stats_json в справочниках | типизированный редактор JSON-полей (сейчас нет) |
| makeMove per turn | SSE-очереди + изоляция сессий (B2/B3) |
| RunLog записи | синхронный libsql в async (B4) |
| dynamic target_form у кнопок | Form._get_children crash (KeyError на мусорном form_id) |
| hooks/on_startup | мёртвый runHook + отсутствующий класс в hooks.json |
| генерация 6 odb-классов | golden-тесты builders (B6), builderDpi битый при пустом attr |

Каждый найденный при игре баг = фикс в ядро. Dgn выступает «котлом», в котором варятся контракты README.

---

## 7. Риски

1. **Объём игровой логики vs время** — mitigation: MVP строго один oper, остальное итерациями.
2. **Генератор может не покрыть не-CRUD формы** (боевой экран) — mitigation: dmeta/ameta разделение уже есть; при провале — писать battle_form вручную в ameta, это легальный путь.
3. **Рассинхрон тестов (B6)** может съесть время — mitigation: начать с этапа 0, не трогать генерацию пока pytest красный.
