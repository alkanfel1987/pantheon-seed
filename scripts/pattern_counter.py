#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pattern_counter.py — счётчик повторяющихся паттернов по session_traces.

Сканирует трейсы, извлекает теги контура промоции, считает повторы по ключу
и печатает показатели контура обучаемости (G, D).
Источник правды по тегам: memory/pattern-promotion.md

Виды тегов:
  failure-mode: <ключ> — повторяющаяся ошибка/баг
  friction:     <ключ> — трение (ресурс потрачен, ничего не сломано)
  work-mode:    <ключ> — повторяющийся режим работы по алгоритму
  r2:           [<ключ>] — старый тег типа улучшения, обратная совместимость

Грани тега (2026-09-07, слой 1 интеграции):
  [слой:] [поймано:] [момент:] — были; [инструмент:] [уровень:] — добавлены.
  Без извлечения [поймано:] показатели контура контура обучаемости не считались вовсе.

Примеры:
  python pattern_counter.py
  python pattern_counter.py --min 2 --kind failure-mode
  python pattern_counter.py --since 2026-09-01          # окно для замера сдвига D
  python pattern_counter.py --kind all --json
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# cp1251-консоль (урок 2026-06-14): кириллица/«×» падают на UnicodeEncodeError.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DEFAULT_TRACES = Path(__file__).resolve().parent.parent / "memory" / "session_traces"

# Дата из имени файла: 2026-06-14-...md
RE_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")

# failure-mode: ключ   /  work-mode: ключ   /  friction: ключ
RE_FAILURE = re.compile(r"failure-mode(?::\s*`?|\s+`)([a-z0-9][a-z0-9\-]*)", re.IGNORECASE)
RE_WORK = re.compile(r"work-mode(?::\s*`?|\s+`)([a-z0-9][a-z0-9\-]*)", re.IGNORECASE)
RE_FRICTION = re.compile(r"friction(?::\s*`?|\s+`)([a-z0-9][a-z0-9\-]*)", re.IGNORECASE)
# R2-класс: [methodology]  /  R2: [capability-gain, risk-reduction]
RE_R2 = re.compile(r"R2(?:-класс)?:\s*\[([^\]]+)\]", re.IGNORECASE)

# Строка тега целиком — из неё берутся грани, привязанные к ключу.
RE_TAG_LINE = re.compile(
    r"^\s*-\s*(failure-mode|work-mode|friction):\s*([a-z0-9][a-z0-9\-]*)(.*)$",
    re.IGNORECASE | re.MULTILINE,
)

# Грани. Момент решает средство (лестница), поймано даёт D, инструмент — корень
# отказа на слое judgment, уровень — глубину лестницы, на которой живёт класс.
FACETS = {
    "момент": re.compile(r"\[момент:\s*([^\]]+)\]", re.IGNORECASE),
    "поймано": re.compile(r"\[поймано:\s*([^\]]+)\]", re.IGNORECASE),
    "слой": re.compile(r"\[слой:\s*([^\]]+)\]", re.IGNORECASE),
    "инструмент": re.compile(r"\[инструмент:\s*([^\]]+)\]", re.IGNORECASE),
    "уровень": re.compile(r"\[уровень:\s*([^\]]+)\]", re.IGNORECASE),
}

# Значения «поймано», считающиеся механической проверкой (показатель G).
# Читатель — слепой под-агент: датум сбоку, равноценен механике.
MECHANICAL = {"механика", "читатель", "под-агент"}
# Одна сущность — одна категория. «сам, на живой выдаче» и «сам» — один детектор,
# иначе D дробится хвостами и замер сдвига невозможен (найдено первым прогоном 2026-09-07).
DETECTORS = ("механика", "читатель", "под-агент", "оператор", "сам")


def normalize_caught(value):
    """«сам, при первом полном прогоне» → «сам»; неизвестное → как есть."""
    low = value.lower()
    for d in DETECTORS:
        if low.startswith(d):
            return d
    return low.split(",")[0].strip()


def extract_facets(text):
    """Вернуть {'<вид>:<ключ>': {грань: значение}} по строкам тегов."""
    out = {}
    for kind, key, tail in RE_TAG_LINE.findall(text):
        rec = {}
        for name, rx in FACETS.items():
            m = rx.search(tail)
            if m:
                val = m.group(1).strip()
                rec[name] = normalize_caught(val) if name == "поймано" else val
        if rec:
            out[f"{kind.lower()}:{key.lower()}"] = rec
    return out


def extract(text):
    """Вернуть {'failure-mode': [...], 'work-mode': [...], 'friction': [...], 'r2': [...]}."""
    found = {"failure-mode": [], "work-mode": [], "friction": [], "r2": []}
    found["failure-mode"] = [m.lower() for m in RE_FAILURE.findall(text)]
    found["work-mode"] = [m.lower() for m in RE_WORK.findall(text)]
    found["friction"] = [m.lower() for m in RE_FRICTION.findall(text)]
    for grp in RE_R2.findall(text):
        for k in grp.split(","):
            k = k.strip().lower()
            if k:
                found["r2"].append(k)
    return found


def scan(traces_dir, kinds, since=None):
    agg = defaultdict(lambda: {"count": 0, "dates": set(), "files": set(), "kind": "",
                               "момент": set(), "поймано": set(), "слой": set(),
                               "инструмент": set(), "уровень": set()})
    files = sorted(f for f in traces_dir.glob("*.md") if not f.name.startswith("_"))
    scanned = 0
    for f in files:
        m = RE_DATE.search(f.name)
        date = m.group(1) if m else "?"
        if since and date != "?" and date < since:
            continue
        scanned += 1
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = f.read_text(encoding="cp1251", errors="replace")
        found = extract(text)
        facets = extract_facets(text)
        for kind in kinds:
            for key in found[kind]:
                tagkey = f"{kind}:{key}"
                rec = agg[tagkey]
                rec["count"] += 1
                rec["dates"].add(date)
                rec["files"].add(f.name)
                rec["kind"] = kind
                for name, value in facets.get(tagkey, {}).items():
                    rec[name].add(value)
    return agg, scanned


def metrics(agg):
    """Показатели контура обучаемости.

    G — доля уникальных классов, у которых хотя бы одно вхождение поймано механикой.
    D — распределение детекторов по вхождениям (механика / сам / оператор / не указан).
    Плюс: доля классов с названным моментом (без него промоция берёт слабейшее средство).
    """
    total = len(agg)
    with_mech = sum(1 for r in agg.values() if r["поймано"] & MECHANICAL)
    with_moment = sum(1 for r in agg.values() if r["момент"])
    d = Counter()
    for r in agg.values():
        if r["поймано"]:
            for v in r["поймано"]:
                d[v] += r["count"] / max(1, len(r["поймано"]))
        else:
            d["не указан"] += r["count"]
    instr = Counter()
    for r in agg.values():
        for v in r["инструмент"]:
            instr[v] += 1
    return {
        "классов": total,
        "G_покрытие_механикой": round(with_mech / total, 3) if total else 0.0,
        "классов_с_моментом": round(with_moment / total, 3) if total else 0.0,
        "D_детекторы": {k: round(v, 1) for k, v in d.most_common()},
        "инструмент": dict(instr.most_common()),
    }


def main():
    ap = argparse.ArgumentParser(description="Счётчик повторяющихся паттернов по session_traces")
    ap.add_argument("--traces", default=str(DEFAULT_TRACES), help="папка с трейсами")
    ap.add_argument("--min", type=int, default=3, help="порог повторов (дефолт 3)")
    ap.add_argument("--since", help="считать только трейсы с датой >= YYYY-MM-DD (окно замера)")
    ap.add_argument("--kind", default="promotion",
                    choices=["promotion", "failure-mode", "work-mode", "friction", "r2", "all"],
                    help="какие теги считать; promotion=failure-mode+work-mode+friction (дефолт)")
    ap.add_argument("--json", action="store_true", help="вывод JSON")
    args = ap.parse_args()

    traces_dir = Path(args.traces)
    if not traces_dir.is_dir():
        print(f"[pattern_counter] папка трейсов не найдена: {traces_dir}", file=sys.stderr)
        sys.exit(2)

    if args.kind == "promotion":
        kinds = ["failure-mode", "work-mode", "friction"]
    elif args.kind == "all":
        kinds = ["failure-mode", "work-mode", "friction", "r2"]
    else:
        kinds = [args.kind]

    agg, n_files = scan(traces_dir, kinds, args.since)
    met = metrics(agg)

    rows = []
    for tagkey, rec in agg.items():
        if rec["count"] >= args.min:
            rows.append({
                "tag": tagkey,
                "kind": rec["kind"],
                "count": rec["count"],
                "first": min(rec["dates"]) if rec["dates"] else "?",
                "last": max(rec["dates"]) if rec["dates"] else "?",
                "files": sorted(rec["files"]),
                "moments": sorted(rec["момент"]),
                "поймано": sorted(rec["поймано"]),
                "инструмент": sorted(rec["инструмент"]),
                "уровень": sorted(rec["уровень"]),
            })
    rows.sort(key=lambda r: (-r["count"], r["tag"]))

    if args.json:
        print(json.dumps({
            "traces_dir": str(traces_dir),
            "files_scanned": n_files,
            "since": args.since,
            "min": args.min,
            "kinds": kinds,
            "метрики": met,
            "candidates": rows,
        }, ensure_ascii=False, indent=2))
        return

    print(f"# Кандидаты на промоцию (повторов >= {args.min})")
    win = f" · окно с {args.since}" if args.since else ""
    print(f"Трейсов просканировано: {n_files}{win} · виды тегов: {', '.join(kinds)}\n")

    # Показатели контура — печатаются всегда, считаются по ВСЕМ классам, не только выше порога.
    print("## Показатели контура обучаемости")
    print(f"- классов всего: **{met['классов']}**")
    print(f"- **G** (покрытие механической проверкой): **{met['G_покрытие_механикой']:.0%}**")
    print(f"- классов с названным моментом: {met['классов_с_моментом']:.0%}")
    d = met["D_детекторы"]
    if d:
        print("- **D** (чем поймано, по вхождениям): " +
              " · ".join(f"{k} {v}" for k, v in d.items()))
    if met["инструмент"]:
        print("- инструмент (корень отказа): " +
              " · ".join(f"{k} {v}" for k, v in met["инструмент"].items()))
    print()

    if not rows:
        print("Кандидатов нет — пустой результат валиден (порог, не квота).")
        below = sum(1 for r in agg.values() if r["count"] < args.min)
        if below:
            print(f"({below} уникальных тегов встречались < {args.min} раз — пока не созрели.)")
        return

    print("| тег | вид | повторов | первый | последний | поймано | инструмент | момент |")
    print("|---|---|---|---|---|---|---|---|")
    for r in rows:
        moment = "; ".join(r["moments"]) if r["moments"] else "— НЕ НАЗВАН"
        caught = "; ".join(r["поймано"]) if r["поймано"] else "—"
        instr = "; ".join(r["инструмент"]) if r["инструмент"] else "—"
        print(f"| `{r['tag']}` | {r['kind']} | {r['count']} | {r['first']} | "
              f"{r['last']} | {caught} | {instr} | {moment} |")
    print("\nДетали (файлы):")
    for r in rows:
        print(f"- `{r['tag']}` ({r['count']}×): {', '.join(r['files'])}")

    # Момент решает, каким средством чинить (лестница в memory/pattern-promotion.md).
    blind = [r["tag"] for r in rows if not r["moments"]]
    if blind:
        print(f"\n⚠ Без названного момента: {len(blind)} из {len(rows)} — "
              f"{', '.join('`%s`' % t for t in blind)}")
        print("  Для них сначала найти наблюдаемое событие, потом промотировать. "
              "Правило без момента не пишется (лестница средств, ступень 4).")

    # Классы, пойманные только оператором, — там, где внутренние детекторы слепы.
    only_op = [r["tag"] for r in rows if r["поймано"] and set(r["поймано"]) == {"оператор"}]
    if only_op:
        print(f"\n⚠ Пойманы только оператором: {', '.join('`%s`' % t for t in only_op)}")
        print("  Это места, где свой детектор отсутствует. Первый кандидат на слепую проверку "
              "(/blind-check) или датчик.")


if __name__ == "__main__":
    main()
