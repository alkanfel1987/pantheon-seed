# Pantheon Seed — mini-core

**Русский:** [README.md](README.md)

A mini-core for Claude Code: twelve skills for working with information and quality, a memory scaffold and session rules. You train it on your own tasks.

The skills are written in Russian.

## Why this exists

One person finds their own mistakes slowly: for a class of slip to become visible, it has to repeat several times. If many people train the mini-core, each on their own tasks, the shared core grows from everyone's experience at once.

The goal of the project is **a core that learns faster from the experience of many people and gives that experience back to each of them**. You train your mini-core. Skills that have worked for you go through review and enter the shared core. From there they reach all users, together with our own improvements, in the next release.

```
  main core ──── release ────▶ mini-core of every user
        ▲                                   │
        │                        training on their own tasks
   7+1 quarantine                           │
   blind check                              ▼
   human decision ◀── form or fork ── skill that worked
```

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

`docs/` holds the foundations: the map of methods, the Pramana five, the 7+1 quarantine filter. `memory/` is the memory scaffold: an index, a sample session trace, the tag convention. `scripts/` holds the blind check, the repeat counter and the bridge.

## How the mini-core learns

1. Each session keeps a session trace: mistakes and techniques that worked are recorded with tags (`memory/pattern-promotion.md`).
2. A class that has repeated three times is surfaced by `scripts/pattern_counter.py`.
3. The `promote-pattern` skill turns it into a fix: correct a skill, add a rule to `CLAUDE.md`, or create a new skill in `.claude/skills/`.

## What goes out and what does not

**Memory and session traces stay with you** — they are in `.gitignore` and do not reach a public fork. Only the skills from `.claude/skills/` are shared, and only if you committed them to your fork yourself.

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
| a work report, a skill for the core | forms in [pantheon-seed-data](https://github.com/alkanfel1987/pantheon-seed-data) |
| a vulnerability | **private**: [Security → Report a vulnerability](https://github.com/alkanfel1987/pantheon-seed/security/advisories/new), see [SECURITY.md](SECURITY.md) |

We review submissions once a week and **reply within 14 days**. GitHub itself will notify you about labels and comments on your submission.

## License

MIT — see [LICENSE](LICENSE).
