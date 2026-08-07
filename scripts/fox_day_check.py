#!/usr/bin/env python3
"""Per-day dimensional check + true in-run sampling cadence.

  python3 fox_day_check.py 2026-07-15        # one day
  python3 fox_day_check.py                   # whole history cadence only

Read-only. Streams. Gaps longer than GAP_CUT are treated as Fox not running,
so the reported cadence is the in-run rate, not calendar-time / samples."""
import sys, os, gzip, ast, glob, statistics as st

GAP_CUT = 60.0   # seconds; longer than this is downtime, not a sample interval
IDLE_AROUSAL = 0.003

d = os.path.expanduser("~/fox/dimensional_substrate")
day = sys.argv[1] if len(sys.argv) > 1 else None
pat = f"dimensional_{day}*" if day else "dimensional_*"
# CHANGED for release (7 Aug 2026): the substrate directory contains
# byte-identical "- Copy" duplicates of 17-18 June. The original glob
# matched them, which is the origin of the 987,838 sample count corrected
# to 946,222 in the paper. They are excluded here.
files = sorted(f for f in glob.glob(os.path.join(d, pat))
               if not f.endswith(".idx") and "Copy" not in f)
if not files: sys.exit(f"no files matching {pat} in {d}")

rows = []
for fn in files:
    op = gzip.open if fn.endswith(".gz") else open
    try: fh = op(fn, "rt", errors="replace")
    except Exception as e: print(f"  ! {os.path.basename(fn)}: {e}"); continue
    with fh:
        for line in fh:
            p = line.split("|", 2)
            if len(p) < 3: continue
            try:
                t = float(p[0].strip()); r = ast.literal_eval(p[2].strip())
            except Exception: continue
            rows.append((t, r))
rows.sort(key=lambda x: x[0])
if not rows: sys.exit("no parsable records")

gaps = [rows[i+1][0]-rows[i][0] for i in range(len(rows)-1)]
inrun = [g for g in gaps if 0 < g <= GAP_CUT]
downs = [g for g in gaps if g > GAP_CUT]

g = lambda k: [r[1].get(k) for r in rows if r[1].get(k) is not None]
sal, aut, aff = g("salience"), g("autonomic_arousal"), g("affective_arousal")

print(f"files            {len(files)}")
print(f"samples          {len(rows):,}")
print(f"--- cadence (in-run, gaps > {GAP_CUT:.0f}s excluded as downtime) ---")
print(f"median gap       {st.median(inrun):.2f}s   -> {1/st.median(inrun):.2f} Hz")
print(f"mean gap         {st.mean(inrun):.2f}s")
print(f"downtime gaps    {len(downs):,}  totalling {sum(downs)/3600:.1f}h")
print(f"in-run time      {sum(inrun)/3600:.1f}h")
if sal:
    print(f"--- channels ---")
    print(f"salience         max {max(sal):.6f}")
    print(f"autonomic        max {max(aut):.6f}   median {st.median(aut):.6f}")
    print(f"affective        max {max(aff):.6f}   median {st.median(aff):.6f}")
    busy = sum(1 for a in aut if a > IDLE_AROUSAL)
    print(f"autonomic above {IDLE_AROUSAL}: {busy:,} of {len(aut):,}  ({100*busy/len(aut):.1f}%)")
    print(f"  -> {'DRIVEN / active day' if busy/len(aut) > 0.25 else 'consistent with an idle day'}")