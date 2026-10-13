"""Рутина миниядра: проверка, отчёт, подготовка обновления. Работает локально, без модели и без сети, кроме git fetch.

    python scripts/routine.py run        # проверить всё и записать memory/routine-status.md
    python scripts/routine.py apply      # поставить подготовленный релиз (только по слову человека)
    python scripts/routine.py rollback   # вернуть состояние до последнего apply
    python scripts/routine.py report     # сводные числа для формы в pantheon-seed-data (отправляет человек)
    python scripts/routine.py install    # раз в день по расписанию ОС (Windows — планировщик задач)
    python scripts/routine.py uninstall

Рутина ничего не отправляет наружу и сама ничего не ставит: обновление готовится,
решение — за человеком (в начале сессии Claude показывает изменения и спрашивает).
"""
import datetime
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUS = ROOT / "memory" / "routine-status.md"
PREV = ROOT / "memory" / "routine-prev.txt"
SKILLS = ROOT / ".claude" / "skills"
TASK = "PantheonSeedRoutine"


def run_(*args, **kw):
    """subprocess.run без консольного окна: из рутины под pythonw каждый git иначе мигал бы окном."""
    if sys.platform == "win32":
        kw.setdefault("creationflags", subprocess.CREATE_NO_WINDOW)
    return subprocess.run(*args, **kw)


def git(*args):
    r = run_(["git", "-C", str(ROOT), *args], capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout.rstrip(), r.stderr.strip()


def check():
    """Целостность: frontmatter навыков, ссылки в .md, скрипты отвечают на --help."""
    problems = []
    for skill in sorted(SKILLS.iterdir()):
        md = skill / "SKILL.md"
        text = md.read_text(encoding="utf-8") if md.is_file() else ""
        if not re.search(r"^name:", text, re.M) or not re.search(r"^description:", text, re.M):
            problems.append(f"{skill.name}: нет SKILL.md или в нём нет name/description")
    try:
        listed = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))["skills"]
        problems += [f"catalog.json: навыка {k} нет в .claude/skills" for k in listed if not (SKILLS / k / "SKILL.md").is_file()]
    except (OSError, ValueError, KeyError) as e:
        problems.append(f"catalog.json не читается: {e}")
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts or md.parent.name == "session_traces":
            continue
        text = re.sub(r"<!--.*?-->", "", md.read_text(encoding="utf-8"), flags=re.S)
        for target in re.findall(r"\]\(([^)#\s<]+)\)", text):
            if not target.startswith(("http", "mailto")) and not (md.parent / target).exists():
                problems.append(f"{md.relative_to(ROOT)}: битая ссылка {target}")
    scripts = [p for p in ROOT.rglob("*.py") if ".git" not in p.parts and p.name != "routine.py"]
    for py in scripts:
        try:
            r = run_([sys.executable, "-I", str(py), "--help"], capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=30)
            if "Traceback" in r.stderr:
                problems.append(f"{py.relative_to(ROOT)}: падает на --help — {r.stderr.strip().splitlines()[-1]}")
        except subprocess.TimeoutExpired:
            problems.append(f"{py.relative_to(ROOT)}: --help не ответил за 30 с")
    return len(list(SKILLS.iterdir())), len(scripts), problems


def journal_dir(root=ROOT):
    """Где Claude Code хранит журналы сессий этой папки."""
    return Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(root))


def usage():
    """Сколько раз вызван каждый навык — по локальным журналам сессий, только имена навыков."""
    calls = Counter()
    for f in journal_dir().glob("*.jsonl"):
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if '"Skill"' not in line:
                continue
            try:
                content = json.loads(line).get("message", {}).get("content", [])
            except (json.JSONDecodeError, AttributeError):
                continue
            for item in content if isinstance(content, list) else []:
                if isinstance(item, dict) and item.get("type") == "tool_use" and item.get("name") == "Skill":
                    calls[item.get("input", {}).get("skill", "?")] += 1
    return calls


def patterns():
    r = run_([sys.executable, "-I", str(ROOT / "scripts" / "pattern_counter.py")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    keep = [l for l in r.stdout.splitlines() if l.startswith(("Трейсов", "- классов", "- **G**", "- **D**", "Кандидатов"))]
    return keep or ["счётчик ничего не вывел"]


def update():
    """Найти релиз новее текущего. Ничего не ставит."""
    remote = "upstream" if git("remote", "get-url", "upstream")[0] == 0 else "origin"
    rc, _, err = git("fetch", "--quiet", "--tags", remote)
    if rc:
        return {"state": "error", "text": f"git fetch {remote}: {err}"}
    latest = git("tag", "-l", "v*", "--sort=-v:refname")[1].splitlines()
    if not latest:
        return {"state": "none", "text": "релизов нет"}
    latest = latest[0]
    current = git("describe", "--tags", "--abbrev=0", "--match", "v*")[1] or "нет"
    if git("merge-base", "--is-ancestor", latest, "HEAD")[0] == 0:
        return {"state": "current", "text": f"установлена последняя версия ({current})"}
    changed = git("diff", "--name-only", f"HEAD...{latest}")[1].splitlines()
    local = {l[3:] for l in git("status", "--porcelain")[1].splitlines()}
    mine = set(git("diff", "--name-only", f"{latest}...HEAD")[1].splitlines()) | local
    clash = sorted(set(changed) & mine)
    log = git("log", "--oneline", f"HEAD..{latest}")[1]
    return {"state": "conflict" if clash else "ready", "tag": latest, "current": current,
            "text": log, "clash": clash}


def run():
    skills, scripts, problems = check()
    calls = usage()
    up = update()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    out = [f"# Рутина миниядра · {now}", "", "## Обновление"]
    if up["state"] == "ready":
        out += [f"**Готов релиз {up['tag']}** (сейчас {up['current']}). Поставить: `python scripts/routine.py apply`.",
                "", "```", up["text"], "```"]
    elif up["state"] == "conflict":
        out += [f"**Есть релиз {up['tag']}, но ставить нельзя без разбора:** ты менял файлы, которые меняет и релиз:"]
        out += [f"- `{p}`" for p in up["clash"]]
        out += ["Свои навыки держи под своим именем; правку нашего навыка — сохранить отдельно и вернуть через CONTRIBUTING."]
    else:
        out += [up["text"]]
    out += ["", f"## Целостность — навыков {skills}, скриптов {scripts}"]
    out += [f"- {p}" for p in problems] or ["Всё цело."]
    out += ["", "## Вызовы навыков (по журналам сессий в этой папке)"]
    out += [f"- {k}: {v}" for k, v in calls.most_common()] or [f"Журналов нет ({journal_dir()})."]
    out += ["", "## Цикл обучения (scripts/pattern_counter.py)"] + [f"{l}" for l in patterns()]
    out += ["", "_Отчёт локальный. Ничего не отправлено. Поделиться — только сводными числами, по своему решению._"]
    STATUS.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"готово → {STATUS} · обновление: {up['state']} · проблем: {len(problems)}")


def scrub(text):
    """Убрать из текста пути, по которым видно имя пользователя и устройство машины."""
    for p in (str(ROOT), str(Path.home())):
        text = text.replace(p, "~").replace(p.replace("\\", "/"), "~")
    return re.sub(r"[A-Za-z]:[\\/][^\s'\"]*|/(?:home|Users)/[^\s'\"]*", "<путь>", text)


def report():
    """Текст для формы «Отчёт о работе» в pantheon-seed-data: только сводные числа и имена навыков."""
    import platform
    skills, scripts, problems = check()
    calls = usage()
    version = git("describe", "--tags", "--match", "v*")[1] or "без релиза"
    sessions = len(list(journal_dir().glob("*.jsonl")))
    out = [f"версия: {version}", f"ОС: {platform.system()}", f"навыков: {skills} · скриптов: {scripts}",
           f"сессий в журнале: {sessions}", f"проблем целостности: {len(problems)}"]
    out += [f"  - {scrub(p)}" for p in problems]
    out += ["вызовы навыков:"] + ([f"  - {k}: {v}" for k, v in calls.most_common()] or ["  нет"])
    out += ["цикл обучения:"] + [f"  {scrub(l)}" for l in patterns()]
    print("\n".join(out))
    print("\nВставить в форму: https://github.com/alkanfel1987/pantheon-seed-data/issues/new?template=report.yml")


def apply():
    up = update()
    if up["state"] != "ready":
        raise SystemExit(f"ставить нечего или нельзя: {up['state']} — {up.get('clash') or up['text']}")
    before = git("rev-parse", "HEAD")[1]
    rc, out, err = git("merge", "--no-edit", up["tag"])
    if rc:
        git("merge", "--abort")
        raise SystemExit(f"слияние не прошло, всё откатано: {err or out}")
    after = git("rev-parse", "HEAD")[1]
    PREV.write_text(f"{before} {after} {up['current']} {up['tag']}\n", encoding="utf-8")
    print(f"поставлен {up['tag']}; вернуть прежнее: python scripts/routine.py rollback")
    run()


def rollback():
    """Вернуть состояние до последнего apply — если с тех пор ничего своего не коммитили и не правили."""
    if not PREV.exists():
        raise SystemExit("откатывать нечего: apply ещё не запускался")
    before, after, old, new = PREV.read_text(encoding="utf-8").split()
    if git("status", "--porcelain")[1]:
        raise SystemExit("есть незакоммиченные правки — сохрани их, потом откат")
    if git("rev-parse", "HEAD")[1] != after:
        raise SystemExit(f"после установки {new} появились свои коммиты — откат сотрёт их; откатывай вручную")
    git("reset", "--hard", before)
    PREV.unlink()
    print(f"возвращено состояние до {new} (было {old})")
    run()


def install(dry=False):
    exe = Path(sys.executable)
    if sys.platform == "win32" and exe.with_name("pythonw.exe").exists():
        exe = exe.with_name("pythonw.exe")  # без консольного окна, которое иначе мигало бы каждый день
    cmd = f'"{exe}" -I "{Path(__file__).resolve()}" run'
    if sys.platform == "win32":
        args = ["schtasks", "/Create", "/SC", "DAILY", "/ST", "09:00", "/TN", TASK, "/TR", cmd, "/F"]
        if dry:
            print(" ".join(args))
            return
        r = run_(args, capture_output=True, text=True)
        print(r.stdout.strip() or r.stderr.strip())
    else:
        print("Добавь строку в crontab (crontab -e):\n0 9 * * * " + cmd.replace('"', ""))


def uninstall():
    if sys.platform == "win32":
        run_(["schtasks", "/Delete", "/TN", TASK, "/F"])
    else:
        print("Удали строку с routine.py из crontab (crontab -e).")


def main():
    if sys.stdout is None:  # pythonw из планировщика: окна нет, вывода нет — пишем в журнал
        sys.stdout = sys.stderr = open(ROOT / "memory" / "routine.log", "a", encoding="utf-8")
        print(f"--- {datetime.datetime.now():%Y-%m-%d %H:%M} {' '.join(sys.argv[1:])}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    cmd = sys.argv[1] if len(sys.argv) > 1 else "--help"
    actions = {"run": run, "apply": apply, "rollback": rollback, "report": report, "install": install, "uninstall": uninstall,
               "install-dry": lambda: install(dry=True)}
    if cmd not in actions:
        print(__doc__)
        raise SystemExit(0 if cmd in ("-h", "--help") else 2)
    try:
        actions[cmd]()
    except Exception:
        import traceback
        traceback.print_exc()  # в журнал, если запущены планировщиком
        raise


if __name__ == "__main__":
    assert journal_dir(Path(r"C:\ProjectS\pantheon-seed")).name == "C--ProjectS-pantheon-seed"
    assert "Ivan" not in scrub(r"FileNotFoundError: 'C:\Users\Ivan\x.md' и /home/Ivan/y")
    main()
