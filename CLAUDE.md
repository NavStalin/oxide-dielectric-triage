# Oxide dielectric triage assistant (Lila Sciences take-home)

Due to the recruiting coordinator **Sunday 2026-11-22**. Team talk Monday 2026-11-23.
The panel is senior: judgment and scientific reasoning first, engineering second.

## Read these first, in order

1. `docs/BRIEF.md`: the original brief. The pitch and non-negotiables are binding.
2. `docs/VERIFIED_FACTS.md`: real field names, coverage numbers and URLs, checked live. Trust this over the brief's guesses.
3. `DECISIONS.md`: the decision log. D-013 to D-021 were made during planning and amend the brief.
4. `docs/PLAN.md`: architecture, module specs, and milestone tasks with acceptance checks.
5. `docs/TALK_NOTES.md` (local only, git-ignored): material for the Monday talk. Add to it whenever the data surprises us or a decision is worth defending out loud. The sanity checks and learning roadmap (D-022, D-023) must stay in it.

Where the brief and `DECISIONS.md` disagree, `DECISIONS.md` wins (most importantly D-013: recompute the hull, never score the JARVIS `ehull` field).

## Rules that never bend

- **Never invent data.** No property value, citation, URL or record ID appears unless it came from a fetched public record. If you're about to type a number or URL from memory, stop and fetch it.
- **Missing stays missing.** `None`, never 0, never imputed. It becomes a caveat and lowers confidence.
- **Synthetic data lives only in `tests/fixtures/synthetic_*`** and is never read by the app.
- **Verify before assuming.** New field, endpoint or URL: print or fetch it, then add it to `docs/VERIFIED_FACTS.md`.
- **Log every choice in `DECISIONS.md`** as you make it: decision, alternatives, one-line why.
- **The app runs with no API key and no network** once a snapshot exists. OQMD being down must never break a run.
- **Citations and the caveats block can't be turned off** by any user input or setting.
- **Code decides, the model only handles language.** No LLM call may filter, score, rank or produce a number.

## How to work

- Work through `docs/PLAN.md` one milestone at a time. **Stop and show Nav at the end of each milestone**: what was built, the test output, anything surprising in the data.
- Tick the task checkboxes in `docs/PLAN.md` as you go so a fresh session can pick up.
- Ask Nav which LLM key they have before building any provider (Milestone 2).
- If the data contradicts the plan, say so and propose a change. Don't tune weights to make a result look good.
- Keep modules small and typed. Every scoring function is pure and unit-tested.
- Commit at the end of each milestone, and only when Nav says to.

## Commands

```
make setup      # uv sync
make snapshot   # fetch JARVIS, recompute hull, write data/snapshot/
make test       # pytest (network tests deselected)
make lint       # ruff
make app        # streamlit
make evals      # run the eval cases and write evals/results/
```

Run Python with `uv run ...`. The raw JARVIS zip is already cached in `data/raw/`.
