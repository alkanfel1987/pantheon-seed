---
name: quarantine
description: Запустить 7-фильтр для входящего claim'а (paper / methodology / idea / bridge-claim / source) перед встраиванием в память миниядра. Реализует конвейер карантина (docs/quarantine.md). Используй ВСЕГДА когда новый external claim претендует на встраивание в память миниядра (`memory/`, scope-документ проекта, продукт, коммерческое предложение, outreach), либо когда пользователь говорит «через карантин», «прогнать фильтр», «проверить claim», «карантин», «quarantine». НЕ используй для личных наблюдений пользователя или internal technical decisions без external evidence.
argument-hint: [claim title or path to existing inbox entry]
---

# quarantine — 7-фильтр для входящих claims

> Навык оценивает не ценность материала, а его проходимость; яркость не довод за пропуск.
> **Держать на этом прогоне:** *сатья* — осадок называется своим именем («не прошло F2», не «слабовато»); *индрия-ниграха* — яркость, срочность и красота формулировки не влияют на проход; *шауча* — один claim, один проход, не сшивать несколько утверждений в один вердикт.

Реализует конвейер карантина: спецификация — `<корень миниядра>/docs/quarantine.md`; входящие утверждения, журналы и сводка живут в `<корень миниядра>/memory/quarantine/` (ниже пути `inbox/`, `under-review/`, `integrated/`, `archived-with-triggers/`, `purged-log.md`, `_Index.md` — относительно этой папки).

**Первый запуск:** если `memory/quarantine/` неполна — создать папки `inbox/`, `under-review/`, `integrated/`, `archived-with-triggers/` и файлы `integrated/_log.md`, `purged-log.md`, `_Index.md`. Образец `_Index.md`:

```markdown
# Карантин — сводка

## Метрика здоровья фильтра
<!-- снимок за скользящие 30 дней: дата · integration N · archive N · purge N · purge-rate % -->

## Archived (active triggers)
<!-- - [[файл]] — new_evidence_trigger / time_trigger / context_trigger -->
```

**F8 и pre-mortem:** кроме семи фильтров, `docs/quarantine.md` описывает F8 (ACH, включается по условию — §3, «F8 · ACH») и обязательный pre-mortem перед исходом A (§4). Перед Outcome A пройти оба по документу.

## Когда срабатывает

Скилл активируется когда:
- Пользователь явно вызвал `/quarantine` (с аргументом или без)
- Пользователь сказал «через карантин», «прогнать через фильтр», «проверить claim», «карантин этому»
- В сессии появляется external claim претендующий на встраивание в память миниядра (paper extract, methodology, bridge-claim, новый источник)
- При формировании academic/outreach deliverable если в нём ещё неотфильтрованные claims

**НЕ срабатывает:**
- Личные заметки пользователя (вне карантина)
- Internal technical decisions без external evidence
- Routine операционные действия
- Артефакты внутри проекта, не уходящие во внешний мир

## Workflow

### Шаг 0 · Determine mode

Аргумент `[claim title or path]`:
- **Без аргумента или новый claim:** mode=NEW — создать entry в `memory/quarantine/inbox/`
- **С путём к существующему файлу в inbox/under-review:** mode=REVIEW — продолжить с конкретным файлом
- **Без аргумента, но есть entries в under-review/:** mode=RESUME — показать список pending review

### Шаг 1 · Capture entry (mode=NEW)

Создать файл `memory/quarantine/inbox/YYYY-MM-DD-short-slug.md` (папку создать, если её нет) со структурой:

```markdown
---
tags: [quarantine, inbox, pending-review]
source: "URL or citation"
type: paper / methodology / idea / bridge-claim / source / hypothesis
submitter: claude / user
submitted_date: 2026-MM-DD
status: pending
filters_passed: []
filters_failed: []
---

# Claim title

**Claim (1-2 предл.):** что утверждается

**Why submitted:** контекст откуда пришло

**Initial relevance:** к какому проекту / документу ядра / продукту applicable

**Verification needed:** что проверить в фильтрах
```

### Шаг 2 · Запустить 7-фильтр

Пройти **все 7 фильтров** в порядке. Output каждого:
- 🟢 passed (evidence ≥ claim)
- 🟡 partially passed (marginal но не failure)
- 🟠 weak (concerning but not blocking)
- 🔴 failed (decisive)

**Filter 1 — Pramāṇa-pañcaka** (`docs/pramana-panchaka.md`):
- Кто говорит? (author/venue/credibility)
- Когда? (date/recency)
- На основании чего? (methodology/data)
- С какой целью? (motivation/conflict of interest)
- Что говорят другие? (peer position/contradictions)

**Filter 2 — воспроизводимость (replication-as-reality):**
- ≥2 независимых peer-reviewed источника подтверждающих? (🟢)
- 1 peer-reviewed + supporting refs? (🟡)
- 1 peer-reviewed без replication? (🟠)
- 0 peer-reviewed? (🔴)

**Filter 3 — анти-инфляция:**
- evidence ≥ декларация? (🟢)
- approximate parity? (🟡)
- декларация > evidence на ступень? (🟠)
- декларация >> evidence? (🔴)

**Filter 4 — позиционирование слоя:**
- Является ли это substrate / applied projection / product feature / narrative frame?
- Правильно ли стратифицируем layer? Misposition (heuristic трактуемый как substrate) = failure

**Filter 5 — mahā-vrata scan:**
- Satya (правда) — verifiable?
- Asteya (не присваивать) — attribution proper?
- Ahimsa (не вредить) — нет harm для пользователей/клиентов?
- Shaucha (чистота) — нет ли скрытого hype-driver'а?
- Indriya-nigraha (не импульс) — calibrated, не reactive?

**Filter 6 — Bridge-check:**
- В каком регистре делается claim о connectivity?
- Peer-reviewed bridge или heuristic параллель?
- Если heuristic — нужен explicit dis-claim или relegation к narrative-only

**Filter 7 — Sunk-cost neutrality:**
- «Если бы я узнал claim сейчас впервые, не зная сколько уже потрачено — принял бы я его?»
- Если ответ зависит от accumulated investment — red flag

### Шаг 3 · Move entry to under-review

При начале применения фильтров:
- Переместить файл inbox/ → under-review/
- Обновить frontmatter: `status: under-review`, обновлять `filters_passed` / `filters_failed` по мере прохождения

### Шаг 4 · Decision

После завершения 7-фильтра:

**Outcome A · Integration** (all 🟢/🟡, no 🔴):
1. Перенести содержание в память миниядра: отдельный файл `memory/<тип>_<имя>.md` + строка-указатель в `memory/MEMORY.md` (как в образце `memory/MEMORY.md`), с явной attribution (author + venue + date + filter scores)
2. Создать entry в `memory/quarantine/integrated/_log.md`:
   ```
   ### 2026-MM-DD · Claim-title
   - **Source:** ...
   - **Integrated location:** [[link]]
   - **Filter scores:** F1🟢 F2🟢 F3🟡 F4🟢 F5🟢 F6🟢 F7🟢
   ```
3. Удалить файл из `under-review/`

**Outcome B · Archive-with-triggers** (claim valuable но не подтверждён сейчас):
1. Переместить в `memory/quarantine/archived-with-triggers/`
2. Обязательные frontmatter поля:
   - `status: archived`
   - `archived_date: YYYY-MM-DD`
   - `filters_at_archive: [F1🟡, F2🟠, ...]`
   - `new_evidence_trigger:` (что должно появиться)
   - `time_trigger: YYYY-MM-DD` (default +6 мес)
   - `context_trigger:` (смена проекта или контекста)
3. Triggers должны быть **falsifiable** — конкретные events, не «когда будет ясно»

**Outcome C · Purge** (грубый провал F2–F5, fabrication, no epistemic foundation):
1. Добавить запись в `memory/quarantine/purged-log.md`:
   ```
   ### 2026-MM-DD · Claim-title
   - **Source:** ...
   - **Type:** ...
   - **Claim:** ...
   - **Filters failed:** F2🔴 — нет peer-review replication; F3🔴 — inflation
   - **Reason for purge:** ...
   - **Triggers that would reopen:** none / specific condition
   ```
2. Удалить файл из `under-review/`
3. **НЕ удалять source-указатель** в purged-log — claim может прийти повторно

### Шаг 5 · Update _Index.md

Если изменился покупательский счёт (purge/integration/archive metrics) — обновить snapshot в `_Index.md` под секцией «Метрика здоровья фильтра».

## Quick checklist format

Для interactive use в session — вывести таблицу:

```
## 7-фильтр для: <claim title>

| # | Filter | Score | Notes |
|---|---|---|---|
| F1 | Pramāṇa-pañcaka | 🟢/🟡/🟠/🔴 | ... |
| F2 | воспроизводимость | ... | ... |
| F3 | анти-инфляция | ... | ... |
| F4 | позиционирование слоя | ... | ... |
| F5 | mahā-vrata | ... | ... |
| F6 | Bridge-check | ... | ... |
| F7 | Sunk-cost neutrality | ... | ... |

**Decision:** Integration / Archive-with-triggers / Purge
**Action:** <конкретные file moves + updates>
```

## Антипаттерны

- ❌ Skip фильтров «для скорости» — defeats purpose; либо whitelist, либо все 7
- ❌ Pre-decide outcome и потом «проверить» — confirmation theatre
- ❌ Vague triggers в archive — «потом», «когда будет ясно» = camouflaged purge
- ❌ Quarantine для личных заметок — они вне карантина
- ❌ Понижать threshold под claim — если 5/7 не проходят, не подстраивать фильтры
- ❌ Применение retrospectively к уже существующей памяти — quarantine только для **новых** claims с момента внедрения карантина, кроме ad-hoc при сомнении

## Метрика здоровья

После закрытия decision проверить purge-rate на rolling 30 дней:
- Если <5% или >70% — повод запросить у пользователя пересмотр фильтров или sources
- Целевой диапазон: purge 20-50%, integration 30-60%, archive 10-30%

Метрика логируется в `_Index.md`.

## Связь с другими skills

- **simulate-fork** — если quarantine decision involves mutually-exclusive options (e.g., integration vs archive), запустить simulate-fork
- **verification-first** — Filter 2 (replication) ↔ verification-first plan
- **graphify** (если установлен) — после integration в память миниядра можно обновить граф знаний

## Справочные документы

Полная спецификация: `<корень миниядра>/docs/quarantine.md`
Сводка (dashboard): `<корень миниядра>/memory/quarantine/_Index.md`
