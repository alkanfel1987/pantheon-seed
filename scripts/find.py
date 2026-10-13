"""Найти навыки по своей сфере и смежным — или собрать каталог для ручного выбора.

    python scripts/find.py медицина               # навыки сферы, затем смежных
    python scripts/find.py запускаю стартап, нужен договор
    python scripts/find.py --list                 # все сферы
    python scripts/find.py --en law               # вывод по-английски
    python scripts/find.py --md                   # пересобрать CATALOG.md и CATALOG.en.md

Каталог — catalog.json: сферы (синонимы для поиска, смежные сферы) и навыки
(основные сферы — в них навык подтверждён двумя независимыми разметками; «также» — одной).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAT = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
SPHERES, SKILLS = CAT["spheres"], CAT["skills"]
T = {
    "ru": {"found": "Сферы", "main": "Основные навыки", "also": "Также пригодятся", "near": "Из смежных сфер",
           "empty": "пока нет навыков — твой может стать первым (CONTRIBUTING.md)", "none": "Сфера не узнана. Все сферы:",
           "title": "Каталог навыков по сферам", "skill": "навык", "when": "когда нужен"},
    "en": {"found": "Spheres", "main": "Main skills", "also": "Also useful", "near": "From adjacent spheres",
           "empty": "no skills yet — yours can be the first (CONTRIBUTING.en.md)", "none": "Sphere not recognised. All spheres:",
           "title": "Skill catalogue by sphere", "skill": "skill", "when": "when you need it"},
}


def match(text):
    words = re.findall(r"\w+", text.lower())
    found = []
    for sid, s in SPHERES.items():
        for stem in s["find"] + [sid]:
            if any(w == stem if len(stem) <= 3 else stem in w for w in words):
                found.append(sid)
                break
    return found


def skills_in(sid, kind):
    return [k for k, v in SKILLS.items() if sid in v[kind]]


def answer(text, lang="ru"):
    t, out = T[lang], []
    found = match(text)
    if not found:
        return "\n".join([t["none"]] + [f"  {sid}: {s[lang]}" for sid, s in SPHERES.items()])
    shown = set()
    out.append(f"{t['found']}: " + ", ".join(SPHERES[s][lang] for s in found))
    for kind in ("main", "also"):
        names = [k for s in found for k in skills_in(s, kind) if k not in shown]
        names = list(dict.fromkeys(names))
        if names:
            out.append(f"\n{t[kind]}:")
            out += [f"  {k} — {SKILLS[k][lang]}" for k in names]
            shown.update(names)
    if not shown:
        out.append(f"\n{t['empty']}")
    near = [n for s in found for n in SPHERES[s]["near"] if n not in found]
    for n in dict.fromkeys(near):
        names = [k for k in skills_in(n, "main") if k not in shown]
        if names:
            out.append(f"\n{t['near']} — {SPHERES[n][lang]}:")
            out += [f"  {k} — {SKILLS[k][lang]}" for k in names]
            shown.update(names)
    return "\n".join(out)


def markdown(lang):
    t = T[lang]
    other = "CATALOG.en.md" if lang == "ru" else "CATALOG.md"
    label = "**English:**" if lang == "ru" else "**Русский:**"
    out = [f"# {t['title']}", "", f"{label} [{other}]({other})", ""]
    out.append("Собрано из `catalog.json` командой `python scripts/find.py --md`. Искать по своей ситуации: `python scripts/find.py <слова>`."
               if lang == "ru" else
               "Built from `catalog.json` by `python scripts/find.py --md`. Search by your situation: `python scripts/find.py <words>`.")
    for sid, s in SPHERES.items():
        out += ["", f"## {s[lang]}", ""]
        rows = [(k, "") for k in skills_in(sid, "main")] + [(k, "*") for k in skills_in(sid, "also")]
        if not rows:
            out.append(f"_{t['empty']}_")
        else:
            out += [f"| {t['skill']} | {t['when']} |", "|---|---|"]
            out += [f"| [`{k}`](.claude/skills/{k}/SKILL.md){m} | {SKILLS[k][lang]} |" for k, m in rows]
        near = ", ".join(SPHERES[n][lang] for n in s["near"])
        out += ["", ("Смежные: " if lang == "ru" else "Adjacent: ") + near]
    out += ["", ("\\* — сфера подтверждена одной разметкой из двух." if lang == "ru"
                 else "\\* — sphere confirmed by one of two independent labellings.")]
    return "\n".join(out) + "\n"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    lang = "en" if "--en" in args else "ru"
    args = [a for a in args if a != "--en"]
    if args[:1] == ["--md"]:
        (ROOT / "CATALOG.md").write_text(markdown("ru"), encoding="utf-8")
        (ROOT / "CATALOG.en.md").write_text(markdown("en"), encoding="utf-8")
        print("CATALOG.md, CATALOG.en.md")
    elif not args or args[0] in ("--list", "-h", "--help"):
        print(__doc__ if args[:1] in (["-h"], ["--help"]) else answer("", lang))
    else:
        print(answer(" ".join(args), lang))


if __name__ == "__main__":
    assert match("истории религий") == ["history"], match("истории религий")
    assert match("медицина") == ["health"]
    assert "product" in match("запускаю стартап") and "law" in match("нужен договор")
    assert match("ии агент") == ["ai-work"]
    main()
