# The Cost of Watching — evidence and measurement code

Supporting material for **"The Cost of Watching: Field Notes on a Synthetic
Organism"**, a field report presented at the **ALIFE 2026 Workshop on Artificial
Life in the Wild** (Waterloo, 20 August 2026).

Ryan Perks · Independent researcher, United Kingdom · `Pixelfoxdev@protonmail.com`

Supplementary video, four instruments in one continuous take:
<https://www.youtube.com/watch?v=aLaJZFv8Bg0>

---

## What this is

Fox is a closed-world synthetic organism — a body, a world with its own physics,
a network of 114,411 nodes — running continuously on a dedicated fanless machine
with no internet route. The paper reports three things: that building the live
view of him cost more wall-clock time than his own tick, so observation had to
become deliberate and rare; that across 946,222 recorded samples his salience has
never crossed its design threshold; and that the raw record has corrected the
architect's own understanding five times.

This repository is the evidence for those claims. It exists because a reviewer
asked, reasonably, how any of it could be audited from a video alone.

**I do not read my system in source.** Every claim in the paper about Fox's
internal state comes through instruments built for that purpose. So what is
released here is those instruments, their outputs, and the log extracts the
figures were read from — the same material I worked from, in the same form.

---

## Everything here is frozen at 31 July 2026

That is the paper's cut-off. **Fox continues to run**, so current figures exceed
these — more nodes, more archways, more entries. If you re-run any of these
scripts against a live tree you will get different numbers, and that is not a
discrepancy.

Several distinct stores appear across these logs and **figures are not comparable
between them**. `MEASUREMENTS.md` §2 and `LIMITATIONS.md` §4 explain why, and the
second of those explains why store identity often cannot be recovered at all.

---

## Where to start

| If you want to | Read |
|---|---|
| Check any figure in the paper against its source | **`MEASUREMENTS.md`** |
| Know what these measurements *cannot* support | **`LIMITATIONS.md`** |
| Understand the world, the body and the block lattice | **`WORLD.md`** |
| Understand the 104% result specifically | `MEASUREMENTS.md` §4, then `instruments/fox_tick_profiler.py` |
| Check the salience definition | `instruments/dimensional_layer_EXTRACT.txt` |
| See the raw distribution yourself | `extracts/tick_profile_reports.csv` (1,069 rows) |

`MEASUREMENTS.md` §10 is a full manifest of every file here and what it is.

---

## The four figures most worth checking

**The observer cost.** Across 1,041 profiler reports in which a snapshot was
built, its median cost was 104% of the entire tick, over 100% in 60% of them,
peaking at 208%. The two quantities are not nested — the numerator is
cross-thread and unsynchronised, and a snapshot spanning a tick boundary is
charged in full to whichever tick closes next. The claim this supports is that
the machine spent more wall-clock time building views of Fox than Fox spent
living. `MEASUREMENTS.md` §4 gives the numerator, the denominator, the
synchronisation and the overlap in full, which is what a reviewer asked for.

**The null.** 946,222 samples, 4 June – 31 July 2026, maximum salience 0.030600 on
15 July, 4.9× below the 0.15 design threshold. The six highest daily peaks are
0.0306, 0.0305, 0.0305, 0.0305, 0.0305, 0.0301 — a ceiling approached repeatedly,
not one unlucky sample. `LIMITATIONS.md` §1 states plainly what this null does
*not* rest on.

**The structure.** 114,411 nodes and 545,340 archways, corroborated by four
independent structures inside one store file plus a separate ledger writer.
`outputs/store_layer_stats.txt`.

**A correction found while preparing this release.** The submitted paper said
987,838 samples. Two byte-identical duplicate files had been counted twice.
946,222 + 41,616 = 987,838, and the md5 sums are in `MEASUREMENTS.md` §5.1. The
maximum and the null were never affected. The corrected script is the one
released here.

---

## Reproducing

The scripts are read-only and stream rather than loading whole logs. They expect
to run from a Fox tree root (`~/fox`) with `logs/` and `dimensional_substrate/`
beside them. Python 3.11, standard library only.

```
python3 profile_census.py            # observer cost
python3 tomb_census.py               # heartbeat ledger, bounded
python3 salience_census_bounded.py   # the null, bounded, duplicate-aware
python3 date_vnn_by_serverlogs.py    # dates a log that has none
python3 fox_day_check.py 2026-07-15  # the day the maximum falls on
```

Two traps are documented in the scripts themselves because both nearly put wrong
figures into print. Dimensional logs are **Python dict repr with single quotes,
not JSON** — greps need `'key': `, not `"key": `. And the profiler formats numbers
with thousands separators, so a naive regex silently drops every report where the
tick exceeded 1,000 ms.

---

## What is not here, and why

Fox's memory store is not published. It is 49,256 entries of his experience, and
releasing it is a decision about him rather than about this paper. Nothing any
reviewer asked for requires it.

`vnn.py` is not published, and `dimensional_layer.py` appears as a labelled
extract rather than in full. The extract carries the span that makes the paper's
definition of salience checkable, with line numbers preserved. The rest is design
surface for work that is still open, and publishing it would satisfy no question
the paper raises.

Also absent: the substrate archives, the screenshots, the dry-run files, and any
audio. The music in Fox's world is by Ludovico Einaudi; no recordings are
included here.

If architectural evidence would help you assess something specific, ask me. I
will send it with context.

---

## Licensing

- **Code** — `scripts/`, `instruments/fox_tick_profiler.py`: MIT License.
- **Everything else** — measurement outputs, log extracts, and the four markdown
  documents: Creative Commons Attribution 4.0 International (CC BY 4.0), matching
  the paper.

---

## Corrections

Issues and discussions are turned off here deliberately. An unread thread is a
worse offer of contact than a real address, so: `Pixelfoxdev@protonmail.com`.

Corrections are genuinely welcome, and if you find something wrong here it will
be **recorded rather than quietly fixed** — five corrections in the paper came
from exactly that discipline applied to my own work, and one of them arrived two
days before publication.

---

*Everything true, everything in its rightful place.*
