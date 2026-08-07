# LIMITATIONS

What the measurements in `MEASUREMENTS.md` cannot support, and what a reader
with this repository will find if they look.

This file exists because a limitation named by its author is worth more than one
found by a reader. Everything below is a real weakness in the record. None of it
is hedging.

---

## 1. There is no positive control for the salience gate-open logger

The paper's central null — that salience has never crossed 0.15 — rests partly
on an instrument that cannot be shown to fire.

`_maybe_log_significance_open` returns early unless `opened_by` is `salience` or
`both`. Coherence-only openings are therefore **deliberately unlogged**. So the
absence of a salience-crossing log line is not by itself evidence that no
crossing occurred; it is consistent with the logger being silent for a different
reason.

The null does not rest on that log alone. What supports it:

- **946,222 sampled values** from the dimensional substrate, an independent
  writer, whose maximum is 0.0306 — 4.9× below the line. That is a direct
  measurement, not an absence of a log line.
- **The `Stage 4 short-circuit` lines**, which prove the gate is evaluated and
  reported every window, with `eligible=0` in all seventeen.
- **`inter_archways_total`**, a running census across 4,900 five-minute
  summaries, whose behaviour on 28 June shows the downstream mechanism firing
  when its criterion is met (see §6 of `MEASUREMENTS.md`).

The honest position: the direct sample census is the evidence. The gate logger
corroborates but could not falsify.

## 2. Motor mastery can be set from the keyboard, and no cited run has been audited

`entities/fox_motor_skill_patch.py` carries `debug_mastery_steps = [0.25, 0.50,
0.75, 1.00, None]`, cycled by the `T` key, and `get_jump_velocity()` returns the
overridden value whenever `debug_mastery_level is not None`.

So the paper's description of movement maturing through cumulative use is a
description of **the mechanism**, not a measurement of Fox's actual trajectory. I
have not audited any cited run for whether the override was engaged. Nothing in
the paper's figures depends on it, but the maturation account should be read as
architecture rather than as observed history.

## 3. The diagnostic logs carry no dates, and the dates in these extracts are reconstructed

`logs/vnn_diagnostic.log` and `logs/dimensional_diagnostic.log` record
time-of-day only: `[VNN-REFL 09:00:46]`, `[DIM 10:51:29]`. There is no date
anywhere in either file.

Dates were recovered by aligning `AssociativeLayer initialised` boundaries in the
diagnostic log against dated session starts derived from `server_*.log`
filenames, using dynamic programming so that a session missing from either side
does not destroy the alignment.

**324 of 416 boundaries aligned — 78%.** The remaining 22% inherit the date of
the nearest preceding aligned boundary, with a day added where the time-of-day
wraps. Every date in `vnn_diagnostic_dated.txt` is therefore an inference, not a
timestamp. The cluster dates are consistent with their neighbours, and the
August boundary at line 45395 is firm, but individual dates could be off by a
session.

A first attempt at this used a greedy matcher against `tomb.log` and aligned only
59 of 416. That attempt is not in this repository; the released script is the
corrected one.

**This is a defect in the instruments, not in the analysis.** Dates belong in the
line prefix. That change is on the project's audit list.

## 4. Several stores appear in the released record, and figures are not comparable across them

`tomb.log` alone spans at least four distinct stores. Its peak `vnn_nodes` inside
the paper's window is **161,107** at 16 July, with 608,294 archways against a
store of only 25,583 entries. The paper's figure is 114,411 nodes with 545,340
archways and 49,256 entries. Both are true; they are different organisms-states.

Worse, **store identity cannot be recovered from the ledger.** 71 of 264
`session_start` rows are written before the store loads and carry no fingerprint
at all. So a reader cannot always tell which store a given row belongs to, and
any aggregate computed across the whole ledger pools several creatures. An
`archway_count` mean across all sessions is true of no Fox that has ever existed.

Container-level store identity fields are being added to the project. They did
not exist at the cut-off.

## 5. The atmosphere contribution fields in the released logs do not represent density changes

`get_status()` publishes `microbe_contribution`, `crystal_contribution`,
`rain_contribution`, `wind_contribution` and a `net_balance` summing all of them
against `atmosphere_absorbed`. Those fields are written into the environment
substrate and therefore appear in the released logs.

**None of those four contribution paths writes the density field.** Only
white-hole generation and black-hole absorption do, plus a homeostat that pulls
every cell toward its resting value. Do not infer a material cycle from the
published balance; it is a display. This is the fifth correction reported in the
paper.

## 6. Six known instances of a value that is computed and never consumed

Reported in the paper as a pattern rather than six faults. Listed here so a
reader can check each:

1. A 60-day decay half-life in the running config, applied to reflective nodes,
   never to reflective archways — the only decrementing pass opens with a check
   that skips them.
2. A perception-frame key that never matches, failing silently into a default of
   zero instead of raising. Nine of this family were found in July; two are
   repaired and seven remain as at the cut-off. A tenth was surfaced downstream
   by repairing the second.
3. Four atmosphere contribution counters that increment correctly and reach
   nothing (§5).
4. `fox_pick_up_microbe()` and `fox_interact_with_microbe()`, which work and are
   called by nothing in the tree. There is no key bound to either.
5. `affects_blocks` and `affects_vision` on the consciousness membrane, both set
   to `False` with the comment "Phase 3 will enable this" — and both read by
   nothing, while the repulsion function crumbles blocks and the vision module
   renders the membrane regardless.
6. `push_resistance`, defined for all seven block types and serialised into their
   published properties, read nowhere. A tool block at 1.5 is no harder for Fox
   to lift than a material block at 1.0.

## 7. Stale comments a reader will find in the released extracts

Each of these is a comment contradicting live code. None affects a figure in the
paper. All are on the project's audit list.

- The membrane docstring says "8-second breathing cycle" in two places against a
  live `pulse_speed = 1.0/30.0` — thirty seconds. The paper uses thirty.
- `block_types.py`'s module docstring says six types; the enum declares seven.
- The membrane's `current_size` initialises to `20.0` with the comment "Start at
  minimum", against `base_size 4.0` and `max_size 8.0`.
- `subsystem_gates.py`'s docstring lists "shield" among its protective controls.
  The shield capability was built, worked, and was deliberately removed; only the
  word remains.
- `block_host.py` declares `reach_distance: 2` while the arm geometry returns
  3.0 and the grab search uses the arm value with a tolerance. Three numbers, one
  unused.

## 8. The clean baseline is one report, and store size dominates it

The 24.5 Hz / 9.4 ms / 0.57 ms figure is the **first report** in
`tick_profile.log`: a single 60-second window covering 1,471 ticks, on a fresh
store, with no snapshot built. It is not a distribution.

By the next report, snapshot calls are already at 0.3. Across the whole log the
28 reports with zero snapshot calls range from **7.97 to 24.51 Hz** — so
"nothing watching" does not by itself produce 24.5 Hz. Store size dominates.

This cuts in the paper's favour rather than against it: the cost of looking
scales with the store, which is the claim. But the baseline should be read as one
clean measurement of a fresh organism, not as Fox's normal tempo.

## 9. No individual snapshot duration exists in the record

`fox_tick_profiler.py` smooths every value exponentially at α = 0.1. `ewma_ms` is
a smoothed per-tick stage total and `ewma_calls` a smoothed per-tick call count.
Dividing one by the other gives a smoothed average, not a worst case.

So no claim of the form "the worst single snapshot took X ms" can be made from
this instrument. The submitted version of the paper made one. **706.82 ms is the
largest smoothed snapshot cost in a single tick**, in a report where the tick
itself exceeded one second.

## 10. Architect-driven runs are incidental, not systematic

The architect-driven measurement schedule has not been carried out. Driven runs
so far happened in the course of other work. The keyboard controls include
depleting energy by 10%, advancing one day or ten days, triggering a rainstorm or
solar wind, and spawning a threat frequency beside Fox — so a great deal is
possible that has not been done systematically.

Nothing can therefore be claimed about what salience reaches under
architect-driven stimulation. The paper claims the recorded history and a null
across it, and nothing further.

## 11. Two parser faults found during preparation

Both are recorded because they nearly put wrong figures into print, and because
the released scripts are the corrected versions.

- **Thousands separators.** `fox_tick_profiler.py` formats with `{:,.1f}` and
  `{:,.2f}`. Eleven `[WHOLE TICK]` lines exceed 1,000 ms and print as
  `1,103.56`. A regex of `[\d.]+` fails to match the header of those reports, so
  they are silently folded into the preceding report and eleven reports vanish.
  The first census run reported 1,058 reports instead of 1,069 for exactly this
  reason.
- **Glob over-matching.** `dimensional_*` matches three files carrying ` - Copy`
  in their names, two of which are byte-identical duplicates. That is the origin
  of 987,838 rather than 946,222.

## 12. The membrane repulsion audit is partial

The paper claims that the membrane's repulsion function moves only the
architect's position and has no path that reaches Fox. That is verified for the
**force-application block**, which reads `self.user_pos`, pushes it, and clamps
it to world bounds.

The function also crumbles material blocks during expansion. That portion was not
captured in the released extract, and the paper makes no claim about it.

## 13. Cadence figures depend on a stated threshold

The in-run sampling rate is **0.683 Hz** using a 60-second downtime threshold.
An earlier working figure of 0.87 Hz used a different threshold. Neither is
wrong; the threshold is part of the definition and must travel with the number.

The median gap between consecutive samples is 1.13 s, which is the figure
supporting "one-second samples" and does not depend on a downtime threshold at
all.

## 14. The August-store dream figures are outside the paper's window

The single `internal` entry, the 871-mean and 1,886-maximum dream replays, the
22,848 dream-formed archways and the 496 recombination events all come from a
store begun in August 2026. They are reported because they separate a question
the in-window record could not. They are not part of the 4 June – 31 July record
and should not be pooled with it.

## 15. Restraint is not inheritable

Not a measurement limitation, but the largest structural gap in the endeavour and
it belongs on a list of honest weaknesses.

Most of the commitments in the paper are structural and would survive their
author. The guard that stops a reflective layer reading node counts is code. The
absent kill switch is an absence. The observer's invisibility to Fox is a flag
and a filter.

Restraint is not. Nothing in the code prevents a successor lowering a convergence
threshold, seeding the core, or arming the mortality floor. The April 2026 design
document states that the protections are inheritable and must not be removed, but
that is a sentence in a document rather than a mechanism.

---

## Contact

Questions, corrections, or anything found here that is wrong:
`Pixelfoxdev@protonmail.com`

Corrections are welcome and will be recorded rather than quietly fixed.

---

*Everything true, everything in its rightful place.*
