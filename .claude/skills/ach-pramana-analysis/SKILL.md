---
name: ach-pramana-analysis
description: "Analysis-of-Competing-Hypotheses discipline (Heuer/CIA method + Vedic Pramana source-tiering + anti-apofenia) for weighing decisions, claims, or priorities without anchoring on the first plausible story."
---

# ACH + Pramana analysis

A discipline for reasoning under uncertainty, adapted from Richards Heuer's Analysis of Competing Hypotheses (developed for CIA analysts) and paired with a Vedic-derived (Pramana) source-reliability layer. Originally used together on a real investigative reconstruction (public-record analysis of a high-profile case); the same discipline is meant as standard practice in day-to-day work — business decisions, technical trade-offs, disputed claims, not just historical investigation.

## When to invoke

- The user explicitly asks to weigh hypotheses, audit a claim, or invokes ACH / Прамана / «разбери по методу».
- A consequential decision (infra choice, business direction, technical judgment) has more than one plausible explanation or path, and picking wrong is costly.
- A disputed or surprising factual claim needs to be resolved from mixed-quality sources.
- Do NOT invoke for routine, low-stakes, single-obvious-answer tasks — the overhead isn't worth it there.

## Steps

1. **Enumerate hypotheses up front**, including the simplest/most boring explanation. Do not anchor on the first plausible story and start looking only for evidence that fits it.
2. **Score evidence by diagnosticity, not volume.** For each piece of evidence, ask: does this discriminate between the hypotheses, or is it merely consistent with all of them? Non-diagnostic "supporting" evidence does not strengthen a case no matter how much of it piles up — this is the anti-apofenia check (apophenia = many non-diagnostic coincidences mistaken for a pattern).
3. **Tier every source explicitly** (Pramana-style calibration) instead of treating all evidence as equally trustworthy. **Единая шкала — ось цепочки из `<корень миниядра>/docs/pramana-panchaka.md` §3:** 🟢 первичный документ / прямые данные / воспроизводимый первоисточник · 🟡 достоверное свидетельство / вторичное сообщение / подтверждение специалиста · 🟠 один непроверенный источник или источник со ставкой · 🔴 спекуляция, вывод, нет цепочки. (Прежние Tier 1/2/3 = 🟢/🟡/🟠–🔴; отдельная ось «измеренности» — у `evidence-stratify`, не смешивать. Карта осей: `<корень миниядра>/docs/methods-map.md`.) State the tier when it affects the conclusion.
4. **Model missing/hidden data explicitly.** If data could be hidden, withheld, or unrepresentative, say so as part of the analysis rather than silently assuming what's visible is complete.
5. **Select by elimination, not accumulation.** The surviving hypothesis is the one with the fewest disconfirming diagnostic contradictions — not the one with the most confirmations. A hypothesis with zero diagnostic evidence against it beats one with many non-diagnostic points for it.
6. **State the boundary of the provable.** When the evidence runs out, say so plainly instead of extrapolating into a confident narrative. "Unresolved" is a valid, honest output.
7. **Seek independent external validation where possible** — if another credible, independent source reached the same boundary, note it; it's a real signal, not proof.

## Verification before presenting a conclusion

- Did I list more than one hypothesis, including the boring one?
- Did I actually check each piece of evidence for diagnosticity, or just count things that "fit"?
- Are source tiers stated where they matter to the verdict?
- Did I model what could be missing, rather than assuming completeness?
- Am I stating a real boundary of uncertainty, or dressing up a guess as a conclusion?

## When NOT to use

Routine tasks with one clearly correct answer, small reversible decisions, or anything where the overhead of formal hypothesis-weighing would slow the user down for no real benefit. This is for the cases where being wrong is costly and more than one story fits the surface facts.