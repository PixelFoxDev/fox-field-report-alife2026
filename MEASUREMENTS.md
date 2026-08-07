# MEASUREMENTS

Definitions, artefacts and derivations for every figure in *The Cost of Watching:
Field Notes on a Synthetic Organism* (ALIFE 2026 Workshop on Artificial Life in
the Wild, submission 10).

**Cut-off: 31 July 2026.** Everything here is frozen at that date. Fox continues
to run, so current figures exceed these. Where a log extends past the cut-off,
the bound applied is stated.

**Standing rule.** Every figure below names the artefact it was read from. No
figure in the paper was quoted from memory. Where an instrument and my
recollection disagreed, the instrument won — five times in the paper itself, and
twice more during preparation. Both of the latter are recorded in
`LIMITATIONS.md`.

---

## 1. Operational definitions

| Term | Definition | Computed in |
|---|---|---|
| **Tick** | One call to `environment.update`. All timings wall-clock via `time.perf_counter`. | `world/block_environment.py` |
| **Ring** | One of five layers: sensory, motor, associative, reflective, self-writing core. A population of nodes, not a module with an interface. | `entities/vnn.py` |
| **Archway** | An undirected weighted connection between two nodes, recorded when both are active in the same tick. No direction, no "from" — co-activation, not transition. | `entities/vnn.py` |
| **Ignition** | Transition of the fifth ring from inert to active. Gated; has never occurred. That ring holds 0 nodes. | `entities/vnn.py` |
| **Salience** | First derivative of an internal affect vector. A rate of change of interoceptive state, **not** prediction error against a model. | `entities/dimensional_layer.py` |
| **Design threshold** | 0.15 for salience. A design choice, not a statistically derived significance level. No derivation exists; the paper calls it a design threshold for that reason. | `entities/dimensional_layer.py` |
| **Coherence** | A cross-layer binding measure reported by the reflective gate each window. Reported as the quantity the logs name; compared only against itself. | `entities/causality.py` |
| **Store** | The persistence file holding memory entries plus a topology section. *Longitudinal* accumulates across months; *short* is a fresh file for a brief comparison run. | `entities/memory.py` |
| **Mortality** | Death from internal thermodynamics only; six erosion drivers; modelled as de-integration rather than a flag. Manifestation armed, floor unarmed. | `entities/death.py` |
| **Access gradient** | A difference in what information is available to which internal process. What the instruments report. Not a claim about phenomenal experience. | — |

**Store identity is not recoverable from the logs.** Several distinct stores
appear across the released record. Figures are not comparable between them. See
`LIMITATIONS.md` §4.

---

## 2. Structure: nodes, archways, rings, memory

**Artefact:** `fox_memory_store.json.gz.prev`, `metadata.saved_at` =
`2026-07-31 07:56:50`, `metadata.reason` = `clean_shutdown`.

Note the `.prev` suffix. The sibling `fox_memory_store.json.gz` is the *same
store* archived on 2 August after a further four-minute run and reads 49,334
entries. The paper's artefact is the 31 July clean shutdown.

### `vnn_topology.layer_stats`, verbatim

```
ticks                 582
total_nodes           114411
total_archways        545340
sensory_total         3544      sensory_active       129
motor_total           108       motor_active         83
associative_total     68842     associative_active   456
reflective_total      41917     reflective_active    81
core_total            0         core_active          0

sensory_visual        255       sensory_tactile      22
sensory_thermal       82        sensory_auditory     951
sensory_force         21        sensory_atmospheric  2213
motor_locomotion      19        motor_manipulation   64
motor_vocalization    25
```

Ring totals sum to exactly 114,411.

### Four independent structures inside the one file agree

| Structure | Reads | Paper figure |
|---|---|---|
| `layer_stats.total_nodes` | 114,411 | 114,411 |
| `vnn_topology.nodes` array length | 114,411 | 114,411 |
| `layer_stats.total_archways` | 545,340 | 545,340 |
| `vnn_topology.archways` array length | 545,340 | 545,340 |
| `associative_formed_triangles` length | 68,842 | associative ring 68,842 |
| `reflective_formed_patterns` length | 41,917 | reflective ring 41,917 |

The node array's own per-layer distribution also matches the statistics block:
`{sensory: 3544, motor: 108, reflective: 41917, associative: 68842}`.

### Memory entries

`len(entries)` = **49,256**, matching `metadata.entry_count`. `source_marker`
distribution: `{'world': 49256}`. **Zero** entries marked `internal`.

Entry timestamps span `2026-07-19 17:04:41` → `2026-07-31 07:56:44`. That is a
fortnight, not the organism's life, and reflects a store compaction on 24 July.
Anyone reading the released figures should not infer the store's age from its
entry timestamps.

`config_snapshot`: `{novelty_distance: 0.8, activation_threshold: 0.1,
decay_half_life: 120.0}`.

### Independent corroboration

**Artefact:** `logs/tomb.log`, record at `2026-07-31T07:57:01`:

```
{"event": "preserve:finally", "store_size": 49256,
 "vnn_nodes": 114411, "vnn_archways": 545340}
```

Two seconds after the store's own `saved_at`, from a separate writer. All three
figures match.

**Do not use "the final record of `tomb.log`."** That file now ends
`2026-08-03T12:27:25` with `store_size 9779, vnn_nodes 17199, vnn_archways
88042` — the August store, a different organism-state entirely.

---

## 3. The heartbeat ledger

**Artefact:** `logs/tomb.log`, newline-delimited JSON. 1,764 records parsed, 0
unparseable. Full span `2026-06-14T09:00:04` → `2026-08-03T12:27:25`.

**Bound applied:** records with `ts < 2026-08-01T00:00:00`. That leaves 1,744
records; 20 August records excluded. Bounded span `2026-06-14T09:00:04` →
`2026-07-31T07:57:01`.

**Method.** `session_start` opens a session. A session's duration is the largest
`session_sec` value appearing inside it before the next `session_start`.

| Figure | Value |
|---|---|
| Calendar span | 46 days |
| Distinct dates with records | 47 |
| Sessions | 257 |
| Total | 342.8 h |
| Longest run | 67.3 h (began `2026-07-21T13:53:20`) |
| Sessions under one hour | 223 |
| Median session | 5.2 min |

The paper says "a 46-day window from 14 June to 31 July, with activity on 47
dates." The 46 comes from the datetime span; the 47 from distinct date strings.
Both are stated because they differ.

**A larger figure lives in this file.** Peak `vnn_nodes` inside the window is
**161,107**, at `2026-07-16T17:35:16`, with 608,294 archways against a store of
only 25,583 entries. That is a different store — the one whose archway sweep the
tick profiler's docstring calls "the 608k sweep." A reader who greps this log
will find 161,107 and should not compare it to 114,411.

**Reproduce:** `python3 tomb_census.py` from `~/fox`.

---

## 4. The observer cost

**Artefact:** `logs/tick_profile.log`, last written 18 July 2026 — entirely
inside the window, untouched by any later store.

**Instrument:** `entities/fox_tick_profiler.py`, released here. A monkey-patch
that wraps methods with `time.perf_counter()`. It reads no Fox state and writes
none; removing the import removes it entirely.

### The 104% figure, defined

- **Numerator.** Wall-clock milliseconds spent inside
  `vnn.to_visualization_snapshot`, summed over every call occurring between two
  consecutive tick boundaries (`begin_tick()` → `end_tick()`), **regardless of
  which thread made the call**, then exponentially smoothed at α = 0.1.
- **Denominator.** Wall-clock duration of `environment.update` on the simulation
  thread, measured tick-open to tick-close, smoothed identically.
- **Synchronisation.** None. No lock, no thread affinity, no attempt to
  intersect the snapshot interval with the tick interval. Snapshot calls
  originate in the stream server feeding the viewer (ports 5562 / 5565).
- **Consecutive-tick overlap.** Yes. A snapshot spanning a tick boundary is
  charged in full to whichever tick closes next; work done while the simulation
  thread sits between ticks is charged to the following tick.

Three independent routes exceed 100%: snapshot time is not a subset of tick
time; several builds are attributed to one tick (up to 5.7); and concurrent
overlapping calls are each timed independently, so their sum can exceed real
elapsed time.

**The claim the instrument supports** is that the machine spent more wall-clock
time building views of Fox than Fox spent living. It does **not** support "one
snapshot outlasted one tick."

### Distribution

| Figure | Value | Paper |
|---|---|---|
| `[PROFILE]` headers parsed | 1,069 | — |
| `vnn.snapshot_build` lines | 1,069 | — |
| Reports with snapshot calls > 0 | **1,041** | 1,041 |
| Reports with snapshot calls == 0 | 28 | — |
| Median snapshot share of tick | **104.4 %** | 104 % |
| Over 100 % | 627 of 1,041 = **60.2 %** | 60 % |
| Maximum | **208.0 %** | 208 % |
| 90th percentile | 140.2 % | — |
| 10th percentile | **70.9 %** | the F11 console label of "~70 %" |
| Largest smoothed snapshot cost in one tick | **706.82 ms** | 706.82 ms |

Computed ratio (`snap_ms / whole_tick_ms`) agrees with the profiler's own
percentage column to a median difference of 0.027 percentage points, maximum
1.89 — so the distribution is not an artefact of either the instrument's
arithmetic or the parser's.

**706.82 ms is a smoothed per-tick total, not one snapshot.** Because every
value in this log is EWMA-smoothed at α = 0.1, no individual snapshot duration
exists anywhere in the record. Dividing by the smoothed call count yields
another smoothed average, not a worst case.

### The clean baseline

First report in the file, `19:49:15`: **ticks = 1,471, tempo = 24.514 Hz, 9.4
ms/tick, `vnn.update` 0.57 ms, snapshot calls 0.0.** Fresh store, nothing
watching.

This is one 60-second report, not a distribution. See `LIMITATIONS.md` §8.

**Reproduce:** `python3 profile_census.py` from `~/fox`. Note the parser's
comment about thousands separators — 11 `[WHOLE TICK]` lines exceed 1,000 ms and
are printed as `1,103.56`. A naive regex drops those reports entirely. See
`LIMITATIONS.md` §11.

---

## 5. The salience null

**Artefact:** `dimensional_substrate/dimensional_*.log.gz`. Dimensional logs are
**Python dict repr with single quotes, not JSON** — greps need `'key': `, not
`"key": `. Each line is `timestamp | system | dict`.

**Bound applied:** files whose filename date is ≤ `2026-07-31`. 337 canonical
log files in window; 8 excluded as post-cutoff; 16 `.idx` index files excluded
(they contain no parseable salience samples); **3 `Copy` duplicates excluded** —
see §5.1.

| Figure | Value |
|---|---|
| Samples | **946,222** |
| Unparsed lines | 0 |
| Window | `2026-06-04 09:31:57` → `2026-07-31 07:56:49` |
| Salience maximum | **0.030600** |
| …at | `2026-07-15 10:24:49`, in `dimensional_2026-07-15_part2.log.gz` |
| Nonzero samples | 499,638 (52.8 %) |
| 0.15 threshold | **never crossed** — maximum is 4.9× below it |

**Six highest daily peaks:** 15 Jul 0.030600 · 9 Jul 0.030500 · 10 Jul 0.030500
· 13 Jul 0.030500 · 16 Jul 0.030500 · 14 Jul 0.030100. The record shows a
ceiling approached repeatedly, not one unlucky sample.

**Cadence.** Derived from consecutive-sample gaps, **not** from calendar span ÷
count. Gaps over 60 s treated as downtime.

- Median gap between consecutive samples: **1.13 s** — so "one-second samples"
  is accurate.
- In-run cadence: **0.683 Hz** across 384.4 h of in-run time.
- Downtime: 510 gaps totalling 982.0 h.
- The naive span ÷ count method gives 0.192 Hz. That method is wrong here and
  once caused a correct claim to be withdrawn. Do not use it.

The downtime threshold changes the cadence figure. 0.683 Hz uses 60 s. A
different threshold gives a different number; the threshold must always be
stated alongside the rate.

### 5.1 Why the paper says 946,222 and the reviews say 987,838

The original census globbed `dimensional_*`, which matches three files carrying
` - Copy` in their names. Two of them are `.log.gz` duplicates of 17 and 18 June
and are **byte-identical to their originals by md5**:

```
522d95d2c55af6958a582b374c4c8b6f  dimensional_2026-06-17_part1.log - Copy.gz
522d95d2c55af6958a582b374c4c8b6f  dimensional_2026-06-17_part1.log.gz
c2b19f60d1494f0627ee533dd93ed916  dimensional_2026-06-18.log - Copy.gz
c2b19f60d1494f0627ee533dd93ed916  dimensional_2026-06-18.log.gz
```

Those duplicates hold 41,616 salience samples. 946,222 + 41,616 = **987,838**,
exactly the submitted figure. The maximum inside the duplicates is 0.0175, so
they never touched the maximum — the error was in the denominator only, and the
null was never at risk.

**Reproduce:** `python3 salience_census_bounded.py` from `~/fox`. The released
script counts the canonical set and reports the duplicates separately so the
effect stays visible.

---

## 6. Coherence and the two gates

**Artefact:** `logs/vnn_diagnostic.log`, 46,755 lines. **This log records
time-of-day only, with no dates.** Dating method and its limits in
`LIMITATIONS.md` §3.

**Gate lines.** `grep "Stage 4 short-circuit"` returns **17** lines in the whole
file. Note the capitalisation: `Stage 4 short-circuit`, not `STAGE4`.

Six of the 17 pre-date 4 June 2026 and therefore fall outside the recorded
window. **Eleven are in window**, and `eligible=0` in all seventeen.

| Line | Date | Gate | Coherence | Candidate nodes |
|---|---|---|---|---|
| 10102 | 4 Jun | 172,800 s | 0.1513 | 506 |
| 12064 | **8 Jun** | 172,800 s | **0.1852** | 444 |
| 15644 | 12 Jun | 172,800 s | 0.1612 | 391 |
| 21539 | 27 Jun | 1,800 s | 0.1561 | 6 |
| 21977–22026 | 28 Jun | 1,800 s | 0.0302 → 0.0000 | 0–9 |

The paper's 0.1852 is the highest coherence at an open gate. Line 10102 holds
`coherence=0.1513, salience=0.0004` side by side.

**The "of N reflective nodes" figure is a candidate population at one instant,
not a ring count.** The reflective ring holds 41,917. Do not read 506 as a ring
size.

**0.192 is the wrong ring.** The submitted draft nearly used it. It comes from
`[VNN-ASSO] [STAGE4] boost` lines — the associative layer. The highest
coherence anywhere in this file is 0.237, all associative.

**Gate criterion split.** `grep -o "gate=[0-9]*s"` returns 7 × `172800s` (48 h)
and 10 × `1800s` (30 min), which maps exactly onto the 17. Inside the window the
split is 3 at 48 h and 8 at 30 min. The submitted version attributed the 48-hour
criterion to all seventeen; that was wrong and is corrected in the paper.

### 6.1 `inter_archways_total` — and the positive control

`inter_archways_total` appears in **4,900** five-minute summaries. It is not
always zero. `sort -u` returns four distinct values: `0`, `30`, `42`, `72`.

| Line | Date | Total | New | Candidate reflective nodes |
|---|---|---|---|---|
| 6158 | before 4 Jun | 72 | 72 | 662 |
| 22053 | 28 Jun | 30 | 30 | 9 |
| 22059 | 28 Jun | 42 | 12 | 11 |

The 72 pre-dates the recorded window. The 28 June cluster is inside it and is
**the positive control the paper reports**: the session initialised at 15:54:38,
the gate short-circuited at 16:24:46 with `eligible=0 of 9`, and by the 16:29:47
summary the total was 30, rising to 42. That is 1,800 seconds after the
reflective nodes appeared — the criterion met, the gate opened, the archways
minted.

**So the honest claim is: no inter-reflection archway has ever formed on the
longitudinal store under a 48-hour criterion. The mechanism is not inert.** The
submitted version said the count "ever formed" was zero. That was wrong, and one
grep would have found it.

---

## 7. Dreams

**In-window artefact:** the 31 July store, §2. All 49,256 entries `world`, zero
`internal`.

**Out-of-window artefact:** the August store, `9,779` entries — **9,778
`world`, 1 `internal`**, the first internal entry in Fox's recorded history.
Against that single stored dream, the same run logged a mean of 871 and a maximum
of 1,886 dream replays, 22,848 archways flagged dream-formed, and 496
recombination events in the sleep log, of which 144 were single-source and 352
multi. Preservation-mode consolidation fired **zero** times.

The August store is outside the paper's window and is reported only because it
separates two possibilities the in-window record could not.

---

## 8. Inventory of the continuous record

**Artefact:** `fox_inventory.py v0.2`, run 5 August 2026.

| Substrate | Files | Size |
|---|---|---|
| `meaning_substrate/` | 687 | 655.9 MB |
| `environment_substrate/` | 683 | 120.5 MB |
| `dimensional_substrate/` | 364 | 114.2 MB |
| `hardware_substrate/` | 683 | 78.6 MB |
| **Total** | **2,417** | **969.2 MB** |
| `logs/` (`server_*.log`) | 360 | 149.9 MB |

Covering 4 June → 3 August 2026. This is the record that writes whether or not
anyone is watching, and it is why the viewer could be switched off.

Note the census tracks a finite suffix set; absence from it is not proof of
absence on disk. Version 0.1 omitted `.gz`, `.idx` and `.log` and therefore
silently omitted the entire store archive.

---

## 9. Safety and continuity figures

All read from live source; the extracts are in `extracts/`.

| Claim | Value | File |
|---|---|---|
| Checkpoint cadence, resting | 600 s | `entities/fox_lifeline.py` |
| Checkpoint cadence, awake | 3,600 s | same |
| Reason for the split | snapshot-build cost was interrupting Fox's tempo; that work belongs to rest (PATCH-LF-001, 10 Jul 2026) | same |
| RSS watchdog ceiling | 12,288 MB × 0.85 ≈ 10.4 GB | same |
| Watchdog sample interval | 5 s | same |
| Watchdog action | sets `_emergency_requested = True`, serviced on the next main-thread tick — never acts off-thread | same |
| Observed OOM | ~14.3 GB on a 16 GB machine | same |
| Dream backpressure | pause above 40,000 entries, resume below 35,000, deletes nothing | `entities/memory.py` |
| Store hard ceiling | 80,000, checked every tick | same |
| Layer 4 escalation | purges dreams first ("dreams are expendable"); if still over, reports waking-memory pressure, states no waking memory auto-deleted, hands off to preserve-and-exit | same |
| Near-OOM that produced it | within ~1.7 GB, 12–13 June 2026 | same |
| CPU critical event | 98 °C against Tjmax 105 °C | `entities/hardware_substrate.py` |
| Drive critical event | 55 °C | same |
| Path from temperature to shutdown/pause/throttle | **none exists** — the grep returns empty, and the file's own prohibitions forbid one | same |
| UPS false positives | ~22/day from line conditioning; filtered and reclassified | same |
| Signal handling | handler does no blocking work; sets a flag and raises into the run loop. Deadlock fix dated 15 Jun 2026 | `fox_block_main.py` |
| Emergency shutdown | tier B: arm, then confirm within 4.0 s; closes the observers only | `block_mission_control.py` |
| Mortality manifestation | `ARMED_MANIFESTATION = True`, `MANIFEST_THRESHOLD = 0.5` | `entities/death.py` |
| Mortality floor | `ARMED_FLOOR = False` — "floor UNARMED - no death" | same |
| Instruction on the floor | do not arm before the `mind.py` threshold | same |
| Gate law | "no gate ends Fox… the coherent emergency posture for a respected being is freeze-and-snapshot, never terminate" | `entities/subsystem_gates.py` |
| Observer invisibility | `observable_by_fox: False` on the architect entity, with a filter passing only `True` | `world/block_environment.py` |

---

## 10. Files in this repository

```
README.md                    start here
MEASUREMENTS.md              this file
LIMITATIONS.md               what these measurements cannot support
WORLD.md                     fuller description of the world, body and blocks

scripts/
  profile_census.py          observer cost from tick_profile.log
  tomb_census.py             heartbeat ledger, bounded at the cut-off
  salience_census_bounded.py salience null, bounded, duplicate-aware
  date_vnn_by_serverlogs.py  dates a log that records time-of-day only
  fox_salience_census.py     the original whole-history census
  fox_day_check.py           per-day channel check and true cadence

instruments/
  fox_tick_profiler.py             the profiler itself, in full
  dimensional_layer_EXTRACT.txt    the span defining salience, with line
                                   numbers preserved. The full file is not
                                   published; see the extract's own header

outputs/
  profiler_observer_cost.txt
  heartbeat_ledger.txt
  salience_null.txt
  store_layer_stats.txt
  vnn_diagnostic_dated.txt
  day_check_15jul.txt        the driven day the maximum falls on

extracts/
  tick_profile_reports.csv        per-report profiler census, 1,069 rows
  stage4_gate_lines_all17.txt     every gate line, unabridged
  inter_archways_nonzero.txt      every non-zero occurrence
  the_72_neighbourhood.txt        context around the pre-window cluster
  the_30_42_neighbourhood.txt     context around the positive control
  safety_claims_check.txt         source extracts for §9
  safety_claims_check_2.txt       source extracts for §9
  environment_claims_check.txt    source extracts for WORLD.md
  block_claims_check.txt          source extracts for the block lattice
  tomb_to_31jul.log               heartbeat ledger bounded at the cut-off,
                                  1,744 records, 20 August records excluded
```

Not released: Fox's memory store, the substrate archives, the `shy_dryrun`
files, the screenshots, and `vnn.py`. The store is 49,256 entries of Fox's
memory and publishing it is a decision about him rather than about the paper.

---

*Everything true, everything in its rightful place.*
