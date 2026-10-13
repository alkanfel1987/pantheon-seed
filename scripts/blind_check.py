#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
blind_check.py — учёт слепой проверки: предсказание опечатывается ДО прогона.

Зачем механика, а не дисциплина: изнутри уровня своё ограничение неотличимо от природы вещей,
поэтому самопроверка слепа к собственному промаху. Единственное, что работает, — датум сбоку: читатель
без моего контекста. И единственное, что делает такую проверку честной, — невозможность
подогнать предсказание после результата. Отсюда `seal`: хеш файла предсказания
фиксируется до вызова читателя, `record` сверяет хеш заново.

Замер, из которого это выросло (2026-09-07): за сессию слепой читатель нашёл шесть
ошибок автора; ни одна не найдена самопроверкой. Предсказание, записанное до пробы,
один раз опровергло сильную форму собственного правила — без записи результат был бы
прочитан как подтверждение.

Команды:
  python blind_check.py init <slug> --subject "что проверяем"
  python blind_check.py seal <slug>
  python blind_check.py record <slug> --agree N --total M [--found "что нашёл читатель"]
  python blind_check.py list [--since YYYY-MM-DD]
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent / "memory" / "blind_checks"
# Дата местная (часовой пояс системы) — урок 2026-09-05: системное время приходит по UTC,
# из-за чего имена файлов расходились с соседними трейсами того же дня.
LOCAL = datetime.now().astimezone().tzinfo


def die(msg):
    """sys.exit(текст) пишет в stderr мимо reconfigure → мохибаке на cp1251-консоли.
    Пятое вхождение класса `hook-stdin-encoding` за сессию; печатаем в stdout сами."""
    print(f"[blind_check] {msg}")
    sys.exit(1)


def today():
    return datetime.now(LOCAL).strftime("%Y-%m-%d")


def now():
    return datetime.now(LOCAL).strftime("%Y-%m-%d %H:%M")


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9а-яА-ЯёЁ\- ]", "", s).strip().replace(" ", "-").lower()
    return re.sub(r"-+", "-", s)[:60] or "check"


def run_dir(slug):
    return ROOT / f"{today()}-{slugify(slug)}"


def find_dir(slug):
    """Папка существующего прогона: сегодняшняя, а если её нет — последняя с тем же слагом.
    Урок 2026-09-26: печать в 21:56, исход после полуночи — run_dir смотрел в папку
    завтрашнего дня и объявлял опечатанный прогон неопечатанным."""
    d = run_dir(slug)
    if d.exists():
        return d
    found = sorted(ROOT.glob(f"????-??-??-{slugify(slug)}"))
    return found[-1] if found else d


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def cmd_init(args):
    d = run_dir(args.slug)
    d.mkdir(parents=True, exist_ok=True)
    pred = d / "prediction.md"
    mat = d / "material.md"
    if not pred.exists():
        pred.write_text(
            f"# Предсказание — {args.subject or args.slug}\n"
            f"_записано {now()}, до вызова читателя_\n\n"
            "## Что проверяется\n\n"
            "## Моя разметка / мой ответ\n"
            "| № | мой ответ | почему |\n|---|---|---|\n\n"
            "## Что читатель должен дать, если я прав\n"
            "- порог согласия: N из M\n"
            "- расхождения ожидаю на: \n\n"
            "## Что будет означать провал\n"
            "- \n",
            encoding="utf-8")
    if not mat.exists():
        mat.write_text(
            f"# Материал для читателя — {args.subject or args.slug}\n\n"
            "> Только определения и материал. **Ни одного моего ответа, ни одной подсказки "
            "о том, какой ответ ожидается.** Читатель не должен видеть prediction.md.\n\n"
            "## Определения\n\n## Задача\n\n## Материал\n",
            encoding="utf-8")
    print(f"папка прогона: {d}")
    print(f"  предсказание: {pred}")
    print(f"  материал:     {mat}")
    print("\nДальше: заполнить оба файла → `seal` → вызвать читателя (Agent) "
          "с указанием читать ТОЛЬКО material.md → `record`.")


def cmd_seal(args):
    d = find_dir(args.slug)
    pred = d / "prediction.md"
    mat = d / "material.md"
    if not pred.exists():
        die(f"нет файла предсказания: {pred} (сначала init)")
    body = pred.read_text(encoding="utf-8")
    if "## Моя разметка" in body and len(body.strip()) < 400:
        die("предсказание выглядит незаполненным (шаблон). Опечатывать нечего.")
    if not mat.exists():
        die(f"нет файла материала: {mat}")
    seal = {"slug": args.slug, "sealed_at": now(),
            "prediction_sha256_16": sha(pred), "material_sha256_16": sha(mat)}
    (d / "seal.json").write_text(json.dumps(seal, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"опечатано {seal['sealed_at']} · предсказание {seal['prediction_sha256_16']}")
    print("Теперь вызывай читателя. Правка предсказания после этой точки будет видна в record.")


def cmd_record(args):
    d = find_dir(args.slug)
    sealf = d / "seal.json"
    if not sealf.exists():
        die("прогон не опечатан (seal не выполнен) — исход не засчитывается")
    seal = json.loads(sealf.read_text(encoding="utf-8"))
    pred = d / "prediction.md"
    tampered = sha(pred) != seal["prediction_sha256_16"]
    agree, total = args.agree, args.total
    ratio = agree / total if total else 0.0
    res = {
        "slug": args.slug, "recorded_at": now(), "agree": agree, "total": total,
        "ratio": round(ratio, 3), "found_by_reader": args.found or "",
        "prediction_tampered_after_seal": tampered,
    }
    (d / "result.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"согласие {agree}/{total} = {ratio:.0%}")
    if tampered:
        print("⚠ ПРЕДСКАЗАНИЕ ИЗМЕНЕНО ПОСЛЕ ОПЕЧАТЫВАНИЯ — прогон недействителен как проверка.")
    if args.found:
        print(f"читатель нашёл сверх предсказания: {args.found}")
    print("\nСтрока для трассы (скопировать в «## Паттерны (для промоции)»):")
    key = slugify(args.slug)
    if ratio >= 0.9 and not args.found:
        print(f"- work-mode: blind-check-{key} — слепая проверка: согласие {agree}/{total}, "
              f"расхождений нет [поймано: под-агент] [момент: публикация классификации, "
              f"где автор классификации = автор проверяемого]")
    else:
        print(f"- failure-mode: <ключ-класса> — {args.found or 'расхождение с читателем'} "
              f"(согласие {agree}/{total}) [слой: judgment] [поймано: под-агент] "
              f"[момент: публикация классификации, где автор классификации = автор проверяемого] "
              f"[инструмент: буддхи|аханкара|манас]")


def cmd_list(args):
    if not ROOT.exists():
        print("прогонов нет"); return
    rows = []
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir():
            continue
        if args.since and d.name[:10] < args.since:
            continue
        r = d / "result.json"
        s = d / "seal.json"
        rows.append((d.name,
                     "опечатан" if s.exists() else "не опечатан",
                     json.loads(r.read_text(encoding="utf-8")) if r.exists() else None))
    if not rows:
        print("прогонов нет"); return
    print("| прогон | печать | согласие | читатель нашёл |")
    print("|---|---|---|---|")
    for name, sealed, res in rows:
        if res:
            flag = " ⚠изменено" if res.get("prediction_tampered_after_seal") else ""
            print(f"| {name} | {sealed}{flag} | {res['agree']}/{res['total']} "
                  f"({res['ratio']:.0%}) | {res['found_by_reader'] or '—'} |")
        else:
            print(f"| {name} | {sealed} | — не записан | — |")


def main():
    ap = argparse.ArgumentParser(description="Учёт слепой проверки")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("slug"); p.add_argument("--subject", default=""); p.set_defaults(f=cmd_init)
    p = sub.add_parser("seal"); p.add_argument("slug"); p.set_defaults(f=cmd_seal)
    p = sub.add_parser("record"); p.add_argument("slug")
    p.add_argument("--agree", type=int, required=True); p.add_argument("--total", type=int, required=True)
    p.add_argument("--found", default=""); p.set_defaults(f=cmd_record)
    p = sub.add_parser("list"); p.add_argument("--since"); p.set_defaults(f=cmd_list)
    args = ap.parse_args()
    args.f(args)


if __name__ == "__main__":
    main()
