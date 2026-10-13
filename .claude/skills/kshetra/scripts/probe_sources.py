"""Живой пробник источников данных для навыка kshetra.

Отвечает на один вопрос: отдаёт ли источник данные ПРЯМО СЕЙЧАС и на каких условиях.
Никаких предположений — только код ответа, редиректы и первые байты тела.

Использование:
    python probe_sources.py <url> [<url> ...]
    python probe_sources.py --file endpoints.txt
    python probe_sources.py --mode name <url> [<url> ...]

Режимы:
    source (по умолчанию) — ось «источник данных»: 200 хорошо, 404/410/403 стена.
    name                  — ось «свобода имени»: смысл обратный, 404 значит имя СВОБОДНО,
                            а 200 — занято. Без этого режима проверка имени даёт ложный вердикт.

Вывод: строка на источник + итоговый вердикт. Код возврата 1, если хоть один источник закрыт.
"""

import json
import sys
import time
import urllib.error
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TIMEOUT = 20
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) kshetra-probe/1.0"

# Как читать код ответа. Ключ — код, значение — (состояние, что это значит).
MEANING = {
    200: ("ОТКРЫТ", "отдаёт данные без ключа"),
    401: ("ЗАКРЫТ-КЛЮЧ", "нужна авторизация — заложи получение доступа в срок"),
    403: ("ЗАКРЫТ-ПОЛИТИКА", "доступ запрещён: закрытый метод, блок по стране или по агенту"),
    404: ("НЕТ", "адреса не существует — проверь, не переехал ли источник"),
    410: ("МЁРТВ", "источник закрыт навсегда — замена обязательна"),
    429: ("ОГРАНИЧЕН", "лимит запросов — считай квоту до сборки"),
    451: ("ЗАКРЫТ-ПРАВО", "недоступен по юридическим причинам"),
}


def probe(url):
    started = time.time()
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            body = response.read(400)
            return {
                "url": url,
                "code": response.status,
                "final_url": response.url,
                "redirected": response.url.rstrip("/") != url.rstrip("/"),
                "ms": int((time.time() - started) * 1000),
                "head": body[:200].decode("utf-8", "replace").replace("\n", " "),
            }
    except urllib.error.HTTPError as error:
        return {
            "url": url,
            "code": error.code,
            "final_url": error.url,
            "redirected": False,
            "ms": int((time.time() - started) * 1000),
            "head": "",
        }
    except Exception as error:  # сеть, DNS, TLS, таймаут
        return {
            "url": url,
            "code": None,
            "final_url": None,
            "redirected": False,
            "ms": int((time.time() - started) * 1000),
            "head": "{}: {}".format(type(error).__name__, error),
        }


NAME_MEANING = {
    200: ("ЗАНЯТО", "имя уже существует — бери другое или согласуй с владельцем"),
    404: ("СВОБОДНО", "имени нет в реестре — можно занимать"),
    403: ("НЕЯСНО", "реестр не отвечает по существу, проверь вручную"),
}


def verdict(result, mode="source"):
    code = result["code"]
    if code is None:
        return "НЕДОСТУПЕН", "сеть или имя не разрешается: " + result["head"][:120]
    if mode == "name":
        if code in NAME_MEANING:
            return NAME_MEANING[code]
        return "НЕЯСНО", "код {} — разбирай вручную".format(code)
    if code in MEANING:
        return MEANING[code]
    if 200 <= code < 300:
        return "ОТКРЫТ", "отвечает кодом {}".format(code)
    if 300 <= code < 400:
        return "ПЕРЕЕЗД", "перенаправление на {}".format(result["final_url"])
    if 500 <= code:
        return "СБОЙ-СЕРВЕР", "код {} — повтори позже, вывод не делай".format(code)
    return "НЕЯСЕН", "код {} — разбирай вручную".format(code)


BLOCKING = {
    "source": ("МЁРТВ", "ЗАКРЫТ-ПОЛИТИКА", "ЗАКРЫТ-ПРАВО", "НЕТ", "НЕДОСТУПЕН"),
    "name": ("ЗАНЯТО", "НЕДОСТУПЕН"),
}


def main(urls, mode="source"):
    rows = []
    blocked = False
    for url in urls:
        result = probe(url)
        state, meaning = verdict(result, mode)
        if state in BLOCKING[mode]:
            blocked = True
        rows.append({**result, "state": state, "meaning": meaning})
        print("{:<16} {:<5} {:>6}мс  {}".format(
            state, result["code"] if result["code"] else "—", result["ms"], url))
        print("{:<16} {}".format("", meaning))
        if result["redirected"]:
            print("{:<16} переезд → {}".format("", result["final_url"]))
        print()

    print("=" * 70)
    if mode == "name":
        print("ВЕРДИКТ: часть имён занята — выбери другое." if blocked
              else "ВЕРДИКТ: проверенные имена свободны.")
    elif blocked:
        print("ВЕРДИКТ: поле имеет закрытые источники — замена обязательна до сборки.")
    else:
        print("ВЕРДИКТ: проверенные источники отвечают.")
    print("Сырые данные ниже — приложи их к решению, не пересказывай по памяти.")
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 1 if blocked else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        raise SystemExit(2)
    run_mode = "source"
    if args[0] == "--mode":
        run_mode = args[1]
        args = args[2:]
        if run_mode not in BLOCKING:
            print("Неизвестный режим: {}. Доступны: {}".format(run_mode, ", ".join(BLOCKING)))
            raise SystemExit(2)
    if args and args[0] == "--file":
        with open(args[1], encoding="utf-8") as handle:
            targets = [line.strip() for line in handle if line.strip() and not line.startswith("#")]
    else:
        targets = args
    if not targets:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(targets, run_mode))
