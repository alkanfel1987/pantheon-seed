# Pantheon Seed — mini-core

**Русский:** [README.md](README.md)

The mini-core gives Claude Code skills, memory and rules. They learn from your work and receive what others have learned. It starts with twelve skills. After that there will be as many as grow out of the work of everyone who uses it.

The skills are written in Russian.

## Sound familiar?

If you work with Claude every day, you've seen this.

- **Confident, and wrong.** Claude cites an article it never opened, retells a retelling, names a number nobody measured. It sounds convincing, and checking it falls to you.
  → `verification-first`, `source-filter` and `evidence-stratify` make it open the source first, separate what was measured from what was merely said, and mark what each conclusion rests on.
- **The same mistake for the fifth time.** You corrected it, and in the next session it does the same thing. An agreement lives until the end of the conversation.
  → The mini-core writes slips into the session trace. A class of slip that repeats three times becomes a fix to a skill or a rule in `memory/rules.md` — and the fix stays.
- **"I checked — all correct."** Claude checks its own work and, of course, approves it.
  → `blind-check`: a separate executor does the checking, and it sees only the material, not the author's reasoning. The expectation is written down before the check, so it can't be fitted afterwards.
- **Fixed the symptom — the bug came back.**
  → `deep-debug-loop` goes down layer by layer to the cause and checks where else in the system the same error lives.
- **Memory lies.** What Claude "remembers" about your project went stale a month ago, but it is presented as fact.
  → Memory here is a snapshot: before advising from memory, Claude re-checks the file or the fact. An unverified claim doesn't get into memory at all — that is what `quarantine` is for.
- **Skills from the internet are a lottery.** Huge prompt bundles: half of them don't work, some install hooks and scripts that do who knows what on your machine.
  → A skill gets in here only if it has already worked for someone on a real task, passed quarantine, a blind check and a human decision. Hooks are not accepted at all.
- **You are alone.** Everything you worked out yourself — how to stop Claude inventing sources, how to run debugging — lives in your head and is lost if you don't write it down.
  → What worked for you can be given to the shared core. What worked for others comes to you.

## Why your mini-core needs to grow

At the start the mini-core is the same for everyone. It becomes valuable when it starts to reflect your work: your frequent slips are closed by rules, your techniques have become skills, memory knows your projects. Each week with it makes the next one cheaper: less correcting, less re-checking.

The second source of growth is other people. You close your own ten typical mistakes. A hundred people each close theirs, and you will run into many of those tomorrow without knowing about them yet. The core collects these solutions, and they reach you before you step on the same rake.

```
  main core ──── release ────▶ mini-core of every user
        ▲                                   │
        │                        training on their own tasks
   7+1 quarantine                           │
   blind check                              ▼
   human decision ◀── form or fork ── skill that worked
```

## Why skills come from people, not from machine self-learning

We could have let the system learn on its own: collect logs, compute metrics, rewrite instructions automatically. We chose otherwise.

- **A machine learns from what can be measured, not from what matters.** A metric sees "answer received" and doesn't see "the answer is wrong, and it will surface in a week". A skill that a person shared has been through their real task — one where a mistake cost time or money.
- **Whoever grades themselves piles up their own error.** If the same Claude invents a fix and itself decides that it helped, its blind spots aren't caught, they are reinforced. An independent view is needed. Another person, for whom the skill worked on a different task, is exactly that check.
- **A machine invents protection against troubles that never happened.** Rewriting itself from logs, a system grows rules against failures that never occurred. No metric will show this until the context gets clogged with extras. A skill from a person names the pain it closes and the condition under which it is removed.
- **A skill can be read.** It is plain text: you can see what it does and adjust it to yourself. Automatically rewritten instructions turn into something nobody wrote and nobody understands.
- **A machine needs mountains of data; a skill needs one working case and a check.** The mini-core is useful from day one, not after thousands of sessions.

There is self-learning inside the mini-core too, but the decision is yours: the counter shows what repeats, and you accept the fix.

## How to find your own in the shared stream

There will be many skills. You won't have to go through them.

- **Pick by your sphere.** [CATALOG.en.md](CATALOG.en.md) lists the skills across twelve spheres of use — law, medicine, product launch, software, history and more — each with its adjacent spheres. Search by your situation: `python scripts/find.py --en medicine` or `python scripts/find.py --en startup contract` — skills of your sphere first, then of the adjacent ones. Or just ask Claude: "which skills fit my task?" — it will work out which spheres you mean.

- **Claude chooses on its own.** Each skill describes the task it is needed for, and Claude Code attaches it when the task matches the description. You write what needs to be done — the right skill fires.
- **The routine shows what you actually use.** A skill that hasn't been called once in a month can be removed from your setup.
- **Every accepted skill has its pain named.** `data/skills/` records what it closes and which checks it passed. You search by your pain, not by name.
- **Users' reports show what works for many.** Which skills are called more often and where they break is visible in the shared numbers.
- **Not everything reaches you.** A filter at the entrance cuts off the noise: only what passed the check gets into a release.

## Project goals and what they give you

The project has three goals. Each has functions built in for it, and what a person gets comes from them.

### 1. Claude works with information by verifiable rules

**Built in:** skills for checking sources, for separating what was measured from what was merely said, for a blind check of your own markup, and for quarantine before anything is written to memory; a map of methods that tells you which skill to use for which task.

**What this gives you:** answers and conclusions whose basis is visible. Claude tells a primary source from a retelling, a number from an opinion, the verified from the assumed, and the unverified does not settle into memory as fact.

### 2. Claude learns from its own mistakes — yours and everyone's

**Built in:** a session trace for each session, with tags for mistakes and for techniques that worked; a counter that surfaces any class that has repeated three times; the `promote-pattern` skill, which turns it into a skill fix, a rule or a new skill.

**What this gives you:** a slip that has repeated three times stops being a habit and becomes a fix. Each week of work, your mini-core is tuned more precisely to your tasks.

### 3. Everyone's experience returns to everyone

**Built in:** a bridge to the main core — submission forms and a review of forks; 7+1 quarantine, a blind check and a human decision for each skill; releases; a routine that prepares an update once a day.

**What this gives you:** a skill that worked for one person comes to you in the next release, after review. Your own skill can spread to all mini-cores, and authorship stays in the git history.

### What holds through all three

- **What is yours stays yours.** Memory and session traces live on your disk and do not go to a public fork. Only what you committed yourself or sent through a form goes out.
- **Nothing is installed without you.** The routine prepares an update, and you install it, with one "yes".
- **No server, no telemetry, no payment to us.** MIT license.

## Project status

- **Version 0.4, 14.10.2026.** Twelve skills, a routine with rollback, a bridge, data intake and three feedback channels are built and checked against scenarios. The first users are the next stage.
- **Platform:** tested on Windows; Linux and macOS are supported by the design of the routine (cron instead of the task scheduler) and are waiting for their first runs.
- **Claude Code is required** (a subscription or an Anthropic key).
- **Next:** user reports will show which skills work best and where to improve them; `routine.py report` and the intake form are built for this. Each accepted skill extends the core for everyone.

## Getting started

You need [Claude Code](https://claude.com/claude-code), git and Python 3 (for the blind-check scripts and the repeat counter).

1. Click **Fork** on this page (or `gh repo fork alkanfel1987/pantheon-seed --clone`, if you have the GitHub CLI).
2. Clone your fork and add our repository as the source of updates:

```bash
git clone https://github.com/<your-login>/pantheon-seed.git
cd pantheon-seed
git remote add upstream https://github.com/alkanfel1987/pantheon-seed.git
claude
```

Install and update the mini-core **only from `alkanfel1987/pantheon-seed`**: we do not review other people's forks.

Sessions are started from this folder: Claude Code picks up the skills from `.claude/skills/`, the rules from `CLAUDE.md` and the memory from `memory/` by itself. There is nothing to install. On first launch Claude Code will ask whether to trust the folder — after "yes" the permissions from `.claude/settings.json` take effect too: only the check (`routine.py run`) and the report (`routine.py report`) run without a prompt, and Claude asks about everything else.

### Skills only, in one command

If you only want the standalone skills, without memory and rules, install them as a plugin from any folder:

```
/plugin marketplace add alkanfel1987/pantheon-seed
/plugin install pantheon-seed-skills@pantheon-seed
```

You get 8 skills: `ach-pramana-analysis`, `deep-debug-loop`, `evidence-stratify`, `kshetra`, `other-side-voice`, `simulate-fork`, `source-filter`, `verification-first` (the skill texts are in Russian). Blind check, quarantine, fix-on-sight and pattern promotion work only from the mini-core folder — they need `memory/` and `scripts/`, so they are not in the plugin. Learning from your own mistakes comes only with the full mini-core.

### Working with your own projects

The mini-core works where Claude Code is open. So **open Claude Code in the mini-core folder and attach your project as a second directory**:

```bash
cd pantheon-seed
claude --add-dir ../my-project
```

In the Claude app, use "add folder" for the session. This way the mini-core's skills, memory and rules work on your code.

### Your own rules and skills

- **Rules** go in `memory/rules.md` (Claude will create it in the first session). Do not edit `CLAUDE.md`: releases update it, and your edit would block the update.
- **Skills** go under your own name: `.claude/skills/my-…/`. It is better not to edit our skills: if you did, the routine will not update that file and will tell you so.

## Routine: checks and updates

```bash
python scripts/routine.py install
```

Once a day (Windows — the task scheduler; Linux/macOS — a cron line) the routine:

- checks integrity: the skills are in place, the scripts respond, the links are intact;
- counts, from Claude Code's local logs, which skills you actually call, and summarizes the learning cycle;
- looks at whether a new **release** has come out (not just a fresh `main`) and prepares it.

Everything is written to `memory/routine-status.md`. At the start of the next session Claude will tell you what it found and ask whether to install the update. **The routine itself installs nothing and sends nothing.** It does not call the model and spends no tokens.

**Create your own skills under your own name** (`.claude/skills/my-…`). If you edited one of our skills and a release changes the same file, the routine will not update it and will name the file. It is better to return your edit to the core through [CONTRIBUTING.en.md](CONTRIBUTING.en.md).

Without the routine: `python scripts/routine.py run`, then `python scripts/routine.py apply`. If something breaks after an update, `python scripts/routine.py rollback` returns the previous state (provided you have not committed anything of your own since the update).

To follow releases: on the repository page, Watch → Custom → Releases.

**Share how the mini-core works:** `python scripts/routine.py report` prints summary numbers (no paths and no texts). You can paste them into the "Work report" form in [pantheon-seed-data](https://github.com/alkanfel1987/pantheon-seed-data). You send it yourself; the routine sends nothing.

## What is inside

| Family | Skills |
|---|---|
| knowledge and filters | `verification-first` · `source-filter` · `evidence-stratify` · `ach-pramana-analysis` · `other-side-voice` · `blind-check` · `quarantine` |
| quality | `deep-debug-loop` · `fix-on-sight` · `promote-pattern` |
| decisions | `simulate-fork` · `kshetra` |

`docs/` holds the foundations: the map of methods, a [practice map by reader pain](docs/methods-practice.md) (in Russian: methods that were actually run, grouped by the problem they address), the Pramana five, the 7+1 quarantine filter. `memory/` is the memory scaffold: an index, a sample session trace, the tag convention. `scripts/` holds the blind check, the repeat counter and the bridge.

## How the mini-core learns

1. Each session keeps a session trace: mistakes and techniques that worked are recorded with tags (`memory/pattern-promotion.md`).
2. A class that has repeated three times is surfaced by `scripts/pattern_counter.py`.
3. The `promote-pattern` skill turns it into a fix: correct a skill, add a rule to `CLAUDE.md`, or create a new skill in `.claude/skills/`.

## What goes out and what does not

**Memory and session traces stay with you** — they are in `.gitignore` and do not reach a public fork. Only the skills from `.claude/skills/` are shared, and only if you committed them to your fork yourself.

### Share a summary of your mistakes

If you want to help the core see which mistakes many people make, run `python scripts/share_errors.py`. The script reads the `failure-mode` tags in your session traces and shows the whole summary. You answer yes or no; it **sends nothing itself**: it prints a link to the "Error summary" form in [pantheon-seed-data](https://github.com/alkanfel1987/pantheon-seed-data) with the text already filled in, and only you can check the fields, tick the box and press Submit.

- **The summary has:** the skills version, the date, names of classes from the shared dictionary (`memory/pattern-promotion.md`, "Словарь базовых классов") with how many times each occurred, and a line "прочие: N" — how many tags are not from the dictionary.
- **The summary does not have:** trace texts or descriptions of mistakes, moments, paths, names, project names, or names of classes outside the dictionary (even the name of your own class can carry something personal, so it is visible only as a number).
- **Your GitHub login is visible:** the issue is opened from your account, and it is public like any submission. The login is needed to count different people: a class goes to review only if at least three people submitted it. One person counts once, however many times they submit.

To check the script: `python scripts/share_errors.py --self-test`.

## How a contribution reaches the core

From time to time the main core reviews forks (`scripts/bridge.py harvest`). Changed and new skills are **never merged automatically**. Each one goes into quarantine:

- a vulnerability test — what the contribution can do on someone else's machine: text, code or hooks;
- the 7+1 filter (`docs/quarantine.md`) and a blind check;
- a human decision on each skill.

Hooks and settings are not accepted at all. More in [CONTRIBUTING.en.md](CONTRIBUTING.en.md).

## Where to write

| What | Where |
|---|---|
| a bug | Issues of this repository — the "Bug" form |
| a question, an idea, "here is what I got working" | [Discussions](https://github.com/alkanfel1987/pantheon-seed/discussions) |
| a work report, an error summary, a skill for the core | forms in [pantheon-seed-data](https://github.com/alkanfel1987/pantheon-seed-data) |
| a vulnerability | **private**: [Security → Report a vulnerability](https://github.com/alkanfel1987/pantheon-seed/security/advisories/new), see [SECURITY.md](SECURITY.md) |

We review submissions once a week and **reply within 14 days**. GitHub itself will notify you about labels and comments on your submission.

## License

MIT — see [LICENSE](LICENSE).
