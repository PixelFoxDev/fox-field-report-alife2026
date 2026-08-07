#!/usr/bin/env python3
"""Salience census over the whole dimensional substrate.
Usage:  python3 fox_salience_census.py [dir]      (default ~/fox/dimensional_substrate)
Read-only. Streams every file; never loads a whole log into memory."""
import sys, os, gzip, ast, glob, datetime

d = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/fox/dimensional_substrate")
files = sorted(glob.glob(os.path.join(d, "dimensional_*")))
if not files:
    sys.exit(f"no dimensional_* files in {d}")

n = 0; nz = 0; mx = -1.0; mx_t = None; mx_f = None
t_first = None; t_last = None; bad = 0
coh_mx = -1.0

for fn in files:
    op = gzip.open if fn.endswith(".gz") else open
    try:
        fh = op(fn, "rt", errors="replace")
    except Exception as e:
        print(f"  ! skipped {os.path.basename(fn)}: {e}"); continue
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
            n += 1
            if s: nz += 1
            if s > mx: mx, mx_t, mx_f = s, t, os.path.basename(fn)
            c = rec.get("coherence")
            if c is not None and c > coh_mx: coh_mx = c
            if t_first is None or t < t_first: t_first = t
            if t_last  is None or t > t_last:  t_last  = t

f = lambda ts: datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
span = (t_last - t_first) if (t_first and t_last) else 0

print(f"files scanned      {len(files)}")
print(f"samples            {n:,}")
print(f"unparsed lines     {bad:,}")
print(f"window             {f(t_first)}  ->  {f(t_last)}   (local time)")
print(f"span               {span/86400:.1f} days")
print(f"effective rate     {n/span:.3f} Hz   (mean gap {span/max(1,n-1):.2f}s)")
print(f"salience MAX       {mx:.6f}")
print(f"  at               {f(mx_t)}   in {mx_f}")
print(f"salience nonzero   {nz:,} of {n:,}  ({100*nz/max(1,n):.1f}%)")
if coh_mx >= 0: print(f"coherence MAX      {coh_mx:.6f}   (this artefact only)")
print(f"threshold 0.15     {'NEVER CROSSED' if mx < 0.15 else '*** CROSSED ***'}")