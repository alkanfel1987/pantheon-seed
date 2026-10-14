"""Обезличенная сводка ошибок для общего ядра. В сеть ничего не шлёт.

    python scripts/share_errors.py              # показать сводку, спросить согласие, напечатать ссылку на форму
    python scripts/share_errors.py --yes        # человек уже согласился в чате: сразу печатать ссылку
    python scripts/share_errors.py --self-test  # проверка на синтетических трейсах

Читает теги `failure-mode` в memory/session_traces. В сводку идут только: версия навыков (из CHANGELOG.md),
дата, имена классов из «Словаря базовых классов» (memory/pattern-promotion.md) со счётом и строка
«прочие: N» — число тегов вне словаря, без имён (имя чужого класса может нести личное).
Текст трейсов, описания, моменты, пути, имена проектов в сводку не попадают: из тега берётся только ключ.
Отправляет человек сам: скрипт печатает ссылку на форму pantheon-seed-data с предзаполненными полями.
"""
import argparse
import datetime
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
FORM = "https://github.com/alkanfel1987/pantheon-seed-data/issues/new?template=error-summary.yml"
MAX_URL = 6000  # ponytail: GitHub режет адрес примерно с 8 тыс. знаков; выше нашего потолка сводка вставляется руками
# Тот же разбор тега, что в pattern_counter.py: `failure-mode: ключ` и ``failure-mode `ключ` ``.
RE_FAILURE = re.compile(r"failure-mode(?::\s*`?|\s+`)([a-z0-9][a-z0-9\-]*)", re.IGNORECASE)
RE_KEY = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_dictionary(text):
    """Ключи из раздела «Словарь базовых классов»: первая колонка таблицы, в обратных кавычках."""
    if "## Словарь базовых классов" not in text:
        raise SystemExit("в memory/pattern-promotion.md нет раздела «Словарь базовых классов»")
    section = text.split("## Словарь базовых классов", 1)[1].split("\n## ", 1)[0]
    return {k for k in re.findall(r"^\|\s*`([^`]+)`\s*\|", section, re.M) if RE_KEY.match(k)}


def skills_version(changelog):
    m = re.search(r"^## (v\d+\.\d+\.\d+)", changelog, re.M)
    return m.group(1) if m else "неизвестна"


def count_tags(traces_dir):
    """{ключ: сколько раз встретился} по всем трейсам; шаблон `_*.md` пропускается."""
    counts = Counter()
    for f in sorted(Path(traces_dir).glob("*.md")):
        if not f.name.startswith("_"):
            counts.update(k.lower() for k in RE_FAILURE.findall(f.read_text(encoding="utf-8", errors="replace")))
    return counts


def summary(counts, dictionary, version, today):
    """Текст сводки. Единственные строки из данных пользователя — ключи, прошедшие через словарь."""
    known = sorted(((k, n) for k, n in counts.items() if k in dictionary), key=lambda kn: (-kn[1], kn[0]))
    other = sum(n for k, n in counts.items() if k not in dictionary)
    return "\n".join([f"версия навыков: {version}", f"дата: {today}", "классы:"]
                     + [f"  {k}: {n}" for k, n in known] + [f"прочие: {other}"])


def form_url(version, text):
    """Ссылка на форму с предзаполнением по id полей (version, summary). Слишком длинная — без сводки."""
    base = f"{FORM}&version={quote(version, safe='')}"
    url = f"{base}&summary={quote(text, safe='')}"
    return url if len(url) <= MAX_URL else base


def self_test():
    dictionary = {"claim-at-n1", "verification-skipped", "scope-exceeded"}
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "2026-10-01-ivan.md").write_text(
            "# Иван Петров, проект «Ромашка», пароль hunter2, C:\\Users\\Ivan\\secret.txt\n"
            "## Паттерны\n"
            "- failure-mode: claim-at-n1 — Иван назвал сумму 4200 руб. по одному звонку [момент: файл C:\\Users\\Ivan\\x]\n"
            "- failure-mode: ivan-romashka-billing — личный класс\n"
            "- failure-mode: Claim-At-N1-extra — похожее имя, но не из словаря\n"
            "- friction: verification-skipped — трение не считается ошибкой\n"
            "- failure-mode `verification-skipped` · слой judgment\n", encoding="utf-8")
        (Path(d) / "2026-10-02-x.md").write_text(
            "- failure-mode: CLAIM-AT-N1 — регистр не важен\n- failure-mode: scope-exceeded\n", encoding="utf-8")
        (Path(d) / "_template.md").write_text("- failure-mode: claim-at-n1\n", encoding="utf-8")
        counts = count_tags(d)
    assert counts["claim-at-n1"] == 2 and counts["verification-skipped"] == 1 and counts["scope-exceeded"] == 1, counts
    text = summary(counts, dictionary, "v0.5.1", "2026-10-14")
    assert text.splitlines() == ["версия навыков: v0.5.1", "дата: 2026-10-14", "классы:", "  claim-at-n1: 2",
                                 "  scope-exceeded: 1", "  verification-skipped: 1", "прочие: 2"], text
    url = form_url("v0.5.1", text)
    shown = (text + url).lower()  # всё, что увидит человек и форма (counts — внутреннее, наружу не идёт)
    for secret in ("Иван", "Ivan", "Ромашка", "hunter2", "4200", "secret", "billing", "extra", "Users", "звонок"):
        assert secret.lower() not in shown, secret
    assert "summary=" in url and len(url) < MAX_URL
    # Худший случай: весь словарь с большими счётами — должен помещаться в ссылку со сводкой.
    full = load_dictionary((ROOT / "memory" / "pattern-promotion.md").read_text(encoding="utf-8"))
    assert 10 <= len(full) <= 20, len(full)
    big = summary(Counter({k: 9999 for k in full}), full, "v10.10.10", "2026-10-14")
    assert "summary=" in form_url("v10.10.10", big), "сводка на весь словарь не помещается в ссылку"
    assert "summary=" not in form_url("v1", "x" * 7000)
    print(f"self-test: ok (классов в словаре: {len(full)}, длина ссылки на весь словарь: {len(form_url('v10.10.10', big))})")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Обезличенная сводка ошибок (в сеть ничего не шлёт)")
    ap.add_argument("--traces", default=str(ROOT / "memory" / "session_traces"), help="папка с трейсами")
    ap.add_argument("--yes", action="store_true", help="человек уже согласился в чате; не спрашивать")
    ap.add_argument("--self-test", action="store_true", help="проверка на синтетических трейсах")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not Path(a.traces).is_dir():
        raise SystemExit(f"папки трейсов нет: {a.traces}")
    dictionary = load_dictionary((ROOT / "memory" / "pattern-promotion.md").read_text(encoding="utf-8"))
    counts = count_tags(a.traces)
    if not counts:
        return print("Тегов failure-mode в трейсах нет — делиться пока нечем.")
    version = skills_version((ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))
    text = summary(counts, dictionary, version, datetime.date.today())
    print("Сводка (это всё, что уйдёт; после отправки её видят все):\n\n" + text + "\n")
    print("В ней нет: текстов трейсов, описаний, моментов, путей, имён, названий проектов и названий классов вне словаря.\n")
    if not a.yes:
        if not sys.stdin.isatty():
            return print("Согласия нет (запуск без терминала). Покажи сводку человеку; если он согласен, повтори с --yes.")
        try:
            answer = input("Готовить ссылку на форму? [да/нет] ").strip().lower()
        except EOFError:
            answer = ""
        if answer not in ("да", "д", "y", "yes"):
            return print("Согласия нет, ничего не готовлю.")
    url = form_url(version, text)
    if "&summary=" not in url:
        print("Сводка не влезает в ссылку: открой форму и вставь текст выше в поле «Сводка».")
    print("Открой ссылку, проверь поля, поставь галочку согласия и нажми Submit сам (скрипт ничего не отправил):\n\n" + url)


if __name__ == "__main__":
    main()
