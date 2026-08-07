#!/usr/bin/env python3
"""Date logs/vnn_diagnostic.log, which records time-of-day only.

Spine: server log FILENAMES carry both date and session-start time
(server_DD-MM-YY_HH-MMam.log). 'AssociativeLayer initialised' marks the same
session start inside the diagnostic log. Aligned by dynamic programming so a
session missing from either side does not destroy the alignment (the earlier
greedy attempt matched only 59 of 416). Read-only."""
import re, glob, os
from datetime import datetime, timedelta

DIAG = "logs/vnn_diagnostic.log"
TOL  = 150          # seconds; filenames have minute precision

tpat = re.compile(r"\[VNN-\w+ (\d{2}):(\d{2}):(\d{2})\]")
def tod(line):
    m = tpat.search(line)
    return int(m.group(1))*3600 + int(m.group(2))*60 + int(m.group(3)) if m else None

lines  = open(DIAG, errors="replace").read().splitlines()
bounds = [(i+1, tod(l)) for i, l in enumerate(lines)
          if "AssociativeLayer initialised" in l and tod(l) is not None]

fpat = re.compile(r"server_(\d{2})-(\d{2})-(\d{2})_(\d{2})-(\d{2})(am|pm)\.log$")
srv = []
for p in glob.glob("logs/server_*.log"):
    m = fpat.search(os.path.basename(p))
    if not m: continue
    dd, mm, yy, hh, mi, ap = m.groups()
    h = int(hh) % 12 + (12 if ap == "pm" else 0)
    srv.append(datetime(2000+int(yy), int(mm), int(dd), h, int(mi)))
srv.sort()
print(f"diagnostic boundaries : {len(bounds)}")
print(f"server logs           : {len(srv)}   spanning {srv[0].date()} -> {srv[-1].date()}")

# DP: maximise monotonic matches within TOL
A, B = bounds, srv
dp = [[0]*(len(B)+1) for _ in range(len(A)+1)]
for i in range(1, len(A)+1):
    ta = A[i-1][1]
    for j in range(1, len(B)+1):
        tb = B[j-1].hour*3600 + B[j-1].minute*60
        best = max(dp[i-1][j], dp[i][j-1])
        if abs(ta - tb) <= TOL: best = max(best, dp[i-1][j-1] + 1)
        dp[i][j] = best
i, j, matches = len(A), len(B), []
while i > 0 and j > 0:
    ta = A[i-1][1]; tb = B[j-1].hour*3600 + B[j-1].minute*60
    if abs(ta - tb) <= TOL and dp[i][j] == dp[i-1][j-1] + 1:
        matches.append((A[i-1][0], B[j-1])); i -= 1; j -= 1
    elif dp[i-1][j] >= dp[i][j-1]: i -= 1
    else: j -= 1
matches.reverse()
print(f"boundaries dated      : {len(matches)}  ({100*len(matches)/len(A):.0f}%)")
if matches:
    print(f"  first : line {matches[0][0]}  {matches[0][1]}")
    print(f"  last  : line {matches[-1][0]}  {matches[-1][1]}")

def date_of(ln):
    prev = [(l, d) for l, d in matches if l <= ln]
    nxt  = [(l, d) for l, d in matches if l >  ln]
    if not prev:
        return f"before {nxt[0][1].date()}" if nxt else "unknown"
    l0, d0 = prev[-1]
    t0, t1 = tod(lines[l0-1]), tod(lines[ln-1])
    d = d0 + timedelta(days=1) if (t0 is not None and t1 is not None and t1 < t0 - 3600) else d0
    return str(d.date())

print("\n=== NON-ZERO inter_archways_total, dated ===")
for i2, l in enumerate(lines):
    if re.search(r"inter_archways_total=[1-9]", l):
        ln = i2+1
        tot = re.search(r"inter_archways_total=(\d+)", l).group(1)
        new = re.search(r"inter_archways_new=(\d+)", l)
        rn  = re.search(r"reflective_nodes=(\d+)", l)
        if new and new.group(1) != "0":
            print(f"  line {ln:>6}  {date_of(ln):<18} total={tot:<4} NEW={new.group(1):<4} "
                  f"reflective_nodes={rn.group(1) if rn else '?'}")

print("\n=== the 17 gate lines, dated ===")
for i2, l in enumerate(lines):
    if "Stage 4 short-circuit" in l:
        ln = i2+1
        g = re.search(r"gate=(\d+)s", l).group(1)
        c = re.search(r"coherence=([\d.]+)", l).group(1)
        n = re.search(r"of (\d+) reflective", l).group(1)
        print(f"  line {ln:>6}  {date_of(ln):<18} gate={g:>6}s  coherence={c:<7} nodes={n}")

print("\n=== first and last dated lines of the file ===")
print(f"  line 1 : {date_of(1)}")
print(f"  line {len(lines)} : {date_of(len(lines))}")
