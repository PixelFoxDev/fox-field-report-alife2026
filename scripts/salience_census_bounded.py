#!/usr/bin/env python3
"""Salience census bounded to the paper's window (4 Jun - 31 Jul 2026).

Read-only. Dimensional logs are Python dict repr (single quotes), not JSON.
Rate is derived from consecutive-sample gaps, NOT calendar span / count.

IMPORTANT: the substrate directory contains duplicate 'dimensional_*.log - Copy.gz'
files. A glob of 'dimensional_*' matches them and double-counts their samples.
This script counts the canonical .log.gz set, then reports the duplicates
separately so the effect is visible rather than silent."""
import os, gzip, ast, glob, statistics, datetime, re

D       = os.path.expanduser("~/fox/dimensional_substrate")
CUTOFF  = "2026-07-31"
GAP_MAX = 60.0

datepat = re.compile(r"dimensional_(\d{4}-\d{2}-\d{2})")

def scan(files):
    """Return (n, nonzero, bad, timestamps, max tuple, per-day peaks)."""
    n = nz = bad = 0; mx = -1.0; mx_t = mx_f = None; ts = []; per_day = {}
    for fn in files:
        op = gzip.open if fn.endswith(".gz") else open
        try: fh = op(fn, "rt", errors="replace")
        except Exception as e:
            print(f"  ! unreadable {os.path.basename(fn)}: {e}"); continue
        with fh:
            for line in fh:
                p = line.split("|", 2)
                if len(p) < 3: continue
                try:
                    t = float(p[0].strip()); rec = ast.literal_eval(p[2].strip())
                except Exception:
                    bad += 1; continue
                s = rec.get("salience")
                if s is None: continue
                n += 1; ts.append(t)
                if s: nz += 1
                d = datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d")
                if s > per_day.get(d, -1.0): per_day[d] = s
                if s > mx: mx, mx_t, mx_f = s, t, os.path.basename(fn)
    return n, nz, bad, ts, (mx, mx_t, mx_f), per_day

# ---- inventory ----
every = sorted(os.listdir(D))
canon, post, idx, copies, other = [], [], [], [], []
for name in every:
    full = os.path.join(D, name)
    if "Copy" in name:                      copies.append(full)
    elif name.endswith(".idx"):             idx.append(full)
    elif name.endswith(".log.gz") or name.endswith(".log"):
        m = datepat.search(name)
        (canon if (m and m.group(1) <= CUTOFF) else post).append(full)
    else:                                   other.append(full)

print("=== directory inventory ===")
print(f"  canonical logs in window   {len(canon)}")
print(f"  canonical logs post-cutoff {len(post)}")
print(f"  .idx index files           {len(idx)}")
print(f"  'Copy' duplicates          {len(copies)}")
for c in copies: print(f"      {os.path.basename(c)}")
print(f"  anything else              {len(other)}")
for o in other: print(f"      {os.path.basename(o)}")
print(f"  TOTAL entries              {len(every)}")

# ---- canonical census ----
n, nz, bad, ts, (mx, mx_t, mx_f), per_day = scan(canon)
F = lambda t: datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")
ts.sort()
gaps  = [b - a for a, b in zip(ts, ts[1:])]
inrun = [g for g in gaps if 0 < g <= GAP_MAX]
down  = [g for g in gaps if g > GAP_MAX]

print("\n=== canonical set, 4 Jun - 31 Jul 2026 ===")
print(f"samples            {n:,}      <- paper says 987,838")
print(f"unparsed lines     {bad:,}")
print(f"window             {F(ts[0])}  ->  {F(ts[-1])}")
print(f"salience MAX       {mx:.6f}   at {F(mx_t)}  in {mx_f}")
print(f"salience nonzero   {nz:,} ({100*nz/max(1,n):.1f}%)")
print(f"threshold 0.15     {'NEVER CROSSED' if mx < 0.15 else '*** CROSSED ***'}  "
      f"({0.15/mx:.1f}x below)")
print(f"in-run cadence     {len(inrun)/sum(inrun):.3f} Hz  (median gap "
      f"{statistics.median(inrun):.2f}s, {sum(inrun)/3600:.1f} h in run)")
print(f"  downtime gaps    {len(down):,} totalling {sum(down)/3600:.1f} h")
print(f"  naive span/count {n/(ts[-1]-ts[0]):.3f} Hz   <- the misleading method")
print("top 6 days by peak salience")
for d, v in sorted(per_day.items(), key=lambda kv: -kv[1])[:6]:
    print(f"  {d}   {v:.6f}")

# ---- duplicates, counted separately ----
if copies:
    cn, _, cbad, cts, (cmx, cmx_t, _), _ = scan(copies)
    cts.sort()
    print("\n=== 'Copy' duplicates, counted separately ===")
    print(f"samples in copies  {cn:,}   (unparsed {cbad:,})")
    if cts:
        print(f"their date range   {F(cts[0])}  ->  {F(cts[-1])}")
        print(f"their salience max {cmx:.6f}")
    print(f"canonical + copies {n + cn:,}      <- does this equal 987,838?")
    print(f"difference from paper figure: {987838 - (n + cn):,}")

# ---- do the .idx files yield anything? ----
if idx:
    inw = [f for f in idx if (lambda m: m and m.group(1) <= CUTOFF)(datepat.search(os.path.basename(f)))]
    idn, _, idbad, _, _, _ = scan(inw)
    print(f"\n.idx files in window: {len(inw)}  ->  parseable salience samples: {idn:,} "
          f"(unparsed {idbad:,})")
