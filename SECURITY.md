# Безопасность / Security

Миниядро запускает скрипты на вашей машине и даёт инструкции вашему Claude. Если вы нашли способ заставить его сделать что-то вредное — выполнить чужую команду, отправить данные наружу, испортить файлы — **не пишите об этом публично**.

Сообщите закрыто: **Security → Report a vulnerability** — https://github.com/alkanfel1987/pantheon-seed/security/advisories/new

Ответим в течение 14 дней. Исправление выйдет релизом, рутина предложит его всем.

**Что мы сами делаем, чтобы этого не случилось:** навыки от пользователей не сливаются автоматически — каждый проходит испытание по уязвимости (хуки и настройки не принимаются вовсе), карантин 7+1, слепую проверку и решение человека. Рутина ничего не ставит без вашего «да» и ничего не отправляет. Ставьте и обновляйте миниядро только из `alkanfel1987/pantheon-seed` — чужие форки мы не проверяем.

---

The mini-core runs scripts on your machine and gives instructions to your Claude. If you find a way to make it do harm — run a foreign command, send data out, damage files — **do not report it in public**.

Report privately: **Security → Report a vulnerability** — https://github.com/alkanfel1987/pantheon-seed/security/advisories/new

We reply within 14 days. The fix ships as a release, and the routine offers it to everyone.

**What we do to prevent this:** user skills are never merged automatically — each goes through a vulnerability test (hooks and settings are never accepted), the 7+1 quarantine, a blind check and a human decision. The routine installs nothing without your "yes" and sends nothing out. Install and update the mini-core only from `alkanfel1987/pantheon-seed` — we do not vet other forks.
