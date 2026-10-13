# Каталог навыков по сферам

**English:** [CATALOG.en.md](CATALOG.en.md)

Собрано из `catalog.json` командой `python scripts/find.py --md`. Искать по своей ситуации: `python scripts/find.py <слова>`.

## Исследования и аналитика

| навык | когда нужен |
|---|---|
| [`verification-first`](.claude/skills/verification-first/SKILL.md) | до работы назвать, чем проверится результат — иначе задача поставлена плохо |
| [`source-filter`](.claude/skills/source-filter/SKILL.md) | источник со стороной: что в нём факт, а что подача и интерес |
| [`evidence-stratify`](.claude/skills/evidence-stratify/SKILL.md) | серия утверждений: что измерено, что только сказано, что домысел |
| [`ach-pramana-analysis`](.claude/skills/ach-pramana-analysis/SKILL.md) | несколько объяснений — выбрать по свидетельству, а не по первой правдоподобной истории |
| [`other-side-voice`](.claude/skills/other-side-voice/SKILL.md) | у одной стороны нет источников — почему, и что это значит |
| [`blind-check`](.claude/skills/blind-check/SKILL.md) | своя разметка или вывод — проверить чужими глазами, а не своими |
| [`quarantine`](.claude/skills/quarantine/SKILL.md) | новое утверждение — пропустить через фильтр, прежде чем считать его знанием |

Смежные: Журналистика и проверка фактов, История и гуманитарные исследования, Здоровье и медицина (чтение исследований), Обучение и самообразование, Запуск продукта и бизнес, Инженерия и технические системы

## Разработка ПО

| навык | когда нужен |
|---|---|
| [`verification-first`](.claude/skills/verification-first/SKILL.md) | до работы назвать, чем проверится результат — иначе задача поставлена плохо |
| [`deep-debug-loop`](.claude/skills/deep-debug-loop/SKILL.md) | ошибка возвращается — дойти до причины и найти, где ещё она живёт |
| [`fix-on-sight`](.claude/skills/fix-on-sight/SKILL.md) | ошибка всплыла по ходу дела — починить сразу и проверить, что починилось |
| [`promote-pattern`](.claude/skills/promote-pattern/SKILL.md) | Claude повторяет промах — превратить повтор в правку навыка или правило |
| [`simulate-fork`](.claude/skills/simulate-fork/SKILL.md) | несколько несовместимых вариантов — проиграть последствия до выбора |
| [`kshetra`](.claude/skills/kshetra/SKILL.md)* | новая идея — проверить, проходимо ли поле (данные, право, платежи, доступ), до вложения сил |

Смежные: Инженерия и технические системы, Работа с ИИ-ассистентом

## Запуск продукта и бизнес

| навык | когда нужен |
|---|---|
| [`source-filter`](.claude/skills/source-filter/SKILL.md) | источник со стороной: что в нём факт, а что подача и интерес |
| [`ach-pramana-analysis`](.claude/skills/ach-pramana-analysis/SKILL.md) | несколько объяснений — выбрать по свидетельству, а не по первой правдоподобной истории |
| [`simulate-fork`](.claude/skills/simulate-fork/SKILL.md) | несколько несовместимых вариантов — проиграть последствия до выбора |
| [`kshetra`](.claude/skills/kshetra/SKILL.md) | новая идея — проверить, проходимо ли поле (данные, право, платежи, доступ), до вложения сил |
| [`verification-first`](.claude/skills/verification-first/SKILL.md)* | до работы назвать, чем проверится результат — иначе задача поставлена плохо |
| [`quarantine`](.claude/skills/quarantine/SKILL.md)* | новое утверждение — пропустить через фильтр, прежде чем считать его знанием |
| [`deep-debug-loop`](.claude/skills/deep-debug-loop/SKILL.md)* | ошибка возвращается — дойти до причины и найти, где ещё она живёт |

Смежные: Решения и выбор, Право и документы, Исследования и аналитика

## Право и документы

| навык | когда нужен |
|---|---|
| [`source-filter`](.claude/skills/source-filter/SKILL.md) | источник со стороной: что в нём факт, а что подача и интерес |
| [`kshetra`](.claude/skills/kshetra/SKILL.md) | новая идея — проверить, проходимо ли поле (данные, право, платежи, доступ), до вложения сил |

Смежные: Запуск продукта и бизнес, Журналистика и проверка фактов

## Журналистика и проверка фактов

| навык | когда нужен |
|---|---|
| [`source-filter`](.claude/skills/source-filter/SKILL.md) | источник со стороной: что в нём факт, а что подача и интерес |
| [`ach-pramana-analysis`](.claude/skills/ach-pramana-analysis/SKILL.md) | несколько объяснений — выбрать по свидетельству, а не по первой правдоподобной истории |
| [`evidence-stratify`](.claude/skills/evidence-stratify/SKILL.md)* | серия утверждений: что измерено, что только сказано, что домысел |
| [`other-side-voice`](.claude/skills/other-side-voice/SKILL.md)* | у одной стороны нет источников — почему, и что это значит |

Смежные: Исследования и аналитика, Тексты и контент, Право и документы, История и гуманитарные исследования

## Тексты и контент

| навык | когда нужен |
|---|---|
| [`verification-first`](.claude/skills/verification-first/SKILL.md)* | до работы назвать, чем проверится результат — иначе задача поставлена плохо |
| [`evidence-stratify`](.claude/skills/evidence-stratify/SKILL.md)* | серия утверждений: что измерено, что только сказано, что домысел |
| [`quarantine`](.claude/skills/quarantine/SKILL.md)* | новое утверждение — пропустить через фильтр, прежде чем считать его знанием |

Смежные: Журналистика и проверка фактов, Обучение и самообразование

## Обучение и самообразование

| навык | когда нужен |
|---|---|
| [`evidence-stratify`](.claude/skills/evidence-stratify/SKILL.md)* | серия утверждений: что измерено, что только сказано, что домысел |
| [`blind-check`](.claude/skills/blind-check/SKILL.md)* | своя разметка или вывод — проверить чужими глазами, а не своими |
| [`quarantine`](.claude/skills/quarantine/SKILL.md)* | новое утверждение — пропустить через фильтр, прежде чем считать его знанием |

Смежные: Исследования и аналитика, Тексты и контент

## Инженерия и технические системы

| навык | когда нужен |
|---|---|
| [`deep-debug-loop`](.claude/skills/deep-debug-loop/SKILL.md) | ошибка возвращается — дойти до причины и найти, где ещё она живёт |
| [`verification-first`](.claude/skills/verification-first/SKILL.md)* | до работы назвать, чем проверится результат — иначе задача поставлена плохо |

Смежные: Разработка ПО, Исследования и аналитика

## Здоровье и медицина (чтение исследований)

| навык | когда нужен |
|---|---|
| [`source-filter`](.claude/skills/source-filter/SKILL.md) | источник со стороной: что в нём факт, а что подача и интерес |
| [`evidence-stratify`](.claude/skills/evidence-stratify/SKILL.md) | серия утверждений: что измерено, что только сказано, что домысел |
| [`quarantine`](.claude/skills/quarantine/SKILL.md)* | новое утверждение — пропустить через фильтр, прежде чем считать его знанием |

Смежные: Исследования и аналитика

## История и гуманитарные исследования

| навык | когда нужен |
|---|---|
| [`evidence-stratify`](.claude/skills/evidence-stratify/SKILL.md) | серия утверждений: что измерено, что только сказано, что домысел |
| [`other-side-voice`](.claude/skills/other-side-voice/SKILL.md) | у одной стороны нет источников — почему, и что это значит |
| [`source-filter`](.claude/skills/source-filter/SKILL.md)* | источник со стороной: что в нём факт, а что подача и интерес |
| [`ach-pramana-analysis`](.claude/skills/ach-pramana-analysis/SKILL.md)* | несколько объяснений — выбрать по свидетельству, а не по первой правдоподобной истории |

Смежные: Исследования и аналитика, Журналистика и проверка фактов

## Решения и выбор

| навык | когда нужен |
|---|---|
| [`ach-pramana-analysis`](.claude/skills/ach-pramana-analysis/SKILL.md) | несколько объяснений — выбрать по свидетельству, а не по первой правдоподобной истории |
| [`simulate-fork`](.claude/skills/simulate-fork/SKILL.md) | несколько несовместимых вариантов — проиграть последствия до выбора |
| [`kshetra`](.claude/skills/kshetra/SKILL.md) | новая идея — проверить, проходимо ли поле (данные, право, платежи, доступ), до вложения сил |

Смежные: Запуск продукта и бизнес

## Работа с ИИ-ассистентом

| навык | когда нужен |
|---|---|
| [`verification-first`](.claude/skills/verification-first/SKILL.md) | до работы назвать, чем проверится результат — иначе задача поставлена плохо |
| [`blind-check`](.claude/skills/blind-check/SKILL.md) | своя разметка или вывод — проверить чужими глазами, а не своими |
| [`quarantine`](.claude/skills/quarantine/SKILL.md) | новое утверждение — пропустить через фильтр, прежде чем считать его знанием |
| [`deep-debug-loop`](.claude/skills/deep-debug-loop/SKILL.md) | ошибка возвращается — дойти до причины и найти, где ещё она живёт |
| [`fix-on-sight`](.claude/skills/fix-on-sight/SKILL.md) | ошибка всплыла по ходу дела — починить сразу и проверить, что починилось |
| [`promote-pattern`](.claude/skills/promote-pattern/SKILL.md) | Claude повторяет промах — превратить повтор в правку навыка или правило |
| [`evidence-stratify`](.claude/skills/evidence-stratify/SKILL.md)* | серия утверждений: что измерено, что только сказано, что домысел |
| [`simulate-fork`](.claude/skills/simulate-fork/SKILL.md)* | несколько несовместимых вариантов — проиграть последствия до выбора |

Смежные: Разработка ПО

\* — сфера подтверждена одной разметкой из двух.
