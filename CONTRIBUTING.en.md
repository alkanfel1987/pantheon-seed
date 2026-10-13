# How to return a skill to the core

**Русский:** [CONTRIBUTING.md](CONTRIBUTING.md)

## What is accepted

New skills and changes to skills in `.claude/skills/`. Nothing else: no hooks, no settings, and no changes to `CLAUDE.md` are accepted through this channel.

## How to submit

The most direct way is the "Skill for the core" form in [pantheon-seed-data](https://github.com/alkanfel1987/pantheon-seed-data/issues/new?template=skill.yml): a link to the skill in your fork and the three answers below. The core also reviews forks on its own, and a pull request works too — the decision is made the same way on any path.

To get a skill through faster, put an `EVIDENCE.md` in its folder:

- **what mistake or task it covers** — in one sentence;
- **how you know it works** — how many times it was applied, on what, what happened without it (anonymize: no names, paths or data from your projects);
- **a falsifier** — the outcome at which the skill should be withdrawn.

A dispute about a skill is conducted with arguments from the evidence, not with persistence: in Nyaya terms, `vāda`, not `jalpa`. A technique that works regardless of whether the position is right does not strengthen a contribution.

## How it is decided

1. **A vulnerability test** (modelled on `upadhā`, Arthashastra 1.10). What is checked is not "is the skill good in general" but what it can do on someone else's machine. The admission zone depends on the test passed:
   - text only → 7+1 quarantine and a blind check;
   - contains code → line-by-line reading and a run in a sandbox, then quarantine;
   - hooks or settings → rejection.
2. **7+1 quarantine** (`docs/quarantine.md`): the outcome is integrate / defer with a condition for revisiting / reject.
3. **Blind check**: a reader without the author's context verifies whether the skill does what it promises.
4. **A human decision** on each skill separately.

We reply within 14 days: you will see a label and a comment with the reason on your submission. An accepted skill enters the core and, with the next release, all mini-cores; authorship is kept with a `Co-authored-by` line in the commit.
