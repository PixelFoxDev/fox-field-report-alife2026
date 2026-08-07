#!/usr/bin/env python3
"""Re-derive the observer-cost figures from logs/tick_profile.log.

Read-only on the log. Writes a per-report CSV into paper_evidence/.
NOTE: fox_tick_profiler.py formats numbers with thousands separators
({:,.1f} / {:,.2f}), so commas MUST be stripped before parsing or reports
with a smoothed tick over 1,000 ms are silently dropped.
All values in the log are EWMA-smoothed (alpha=0.1) per-tick aggregates;
no individual snapshot duration is ever recorded.
"""
import re, csv, statistics

LOG = "logs/tick_profile.log"
OUT = "paper_evidence/tick_profile_reports.csv"

hdr  = re.compile(r"\[PROFILE\s+([\d:]+)\]\s+ticks=([\d,]+)\s+tempo=([\d.,]+)\s*Hz\s*\(([\d.,]+)\s*ms/tick\)")
nums = re.compile(r"-?[\d,]+\.?\d*")
def N(s): return float(s.replace(",", ""))

def after(line, label):
    tail = line.split(label, 1)[1].replace("%", " ")
    return [N(x) for x in nums.findall(tail) if x.strip(",")]

reports, cur, snap_lines = [], None, 0
with open(LOG, errors="replace") as f:
    for line in f:
        m = hdr.search(line)
        if m:
            if cur: reports.append(cur)
            cur = {"time": m.group(1), "ticks": int(N(m.group(2))),
                   "tempo_hz": N(m.group(3)), "hdr_ms_tick": N(m.group(4)),
                   "whole_ms": None, "vnn_update_ms": None,
                   "snap_ms": None, "snap_pct_log": None, "snap_calls": None}
            continue
        if cur is None: continue
        if "[WHOLE TICK]" in line:
            v = after(line, "[WHOLE TICK]")
            if v: cur["whole_ms"] = v[0]
        elif "vnn.snapshot_build" in line:
            snap_lines += 1
            v = after(line, "vnn.snapshot_build")
            if len(v) >= 3:
                cur["snap_ms"], cur["snap_pct_log"], cur["snap_calls"] = v[0], v[1], v[2]
        elif "vnn.update" in line:
            v = after(line, "vnn.update")
            if v: cur["vnn_update_ms"] = v[0]
if cur: reports.append(cur)

for r in reports:
    r["ratio_calc"] = (100.0*r["snap_ms"]/r["whole_ms"]) if (r["snap_ms"] and r["whole_ms"]) else None

print(f"PROFILE headers parsed              : {len(reports)}")
print(f"vnn.snapshot_build lines seen       : {snap_lines}      <- grep -ci snapshot said 1,069")
active = [r for r in reports if (r["snap_calls"] or 0) > 0]
zero   = [r for r in reports if r["snap_calls"] == 0.0]
print(f"reports with snapshot calls > 0     : {len(active)}      <- paper says 1,041")
print(f"reports with snapshot calls == 0    : {len(zero)}")
print(f"reports missing a WHOLE TICK value  : {sum(1 for r in reports if r['whole_ms'] is None)}")

pct = [r["snap_pct_log"] for r in active if r["snap_pct_log"] is not None]
if pct:
    over = sum(1 for x in pct if x > 100.0)
    print("\nSnapshot share of the tick (the profiler's own % column)")
    print(f"  reports                           : {len(pct)}")
    print(f"  median                            : {statistics.median(pct):.1f}%   <- paper says 104%")
    print(f"  over 100%                         : {over} = {100.0*over/len(pct):.1f}%   <- paper says 60%")
    print(f"  maximum                           : {max(pct):.1f}%   <- paper says 208%")
    print(f"  90th percentile                    : {sorted(pct)[int(0.9*len(pct))]:.1f}%")
    print(f"  10th percentile                    : {sorted(pct)[int(0.1*len(pct))]:.1f}%   <- the F11 '~70%' console label")
ms = [r["snap_ms"] for r in active if r["snap_ms"]]
if ms:
    print(f"  largest smoothed snapshot ms/tick  : {max(ms):.2f} ms   <- paper calls this a single snapshot")

chk = [r for r in active if r["ratio_calc"] and r["snap_pct_log"]]
if chk:
    d = [abs(r["ratio_calc"]-r["snap_pct_log"]) for r in chk]
    print(f"\ncross-check, computed vs logged %  : median diff {statistics.median(d):.3f} pts, max {max(d):.2f} pts")

first = reports[0]
print(f"\nfirst report (the fresh-store baseline)")
print(f"  {first['time']}  ticks={first['ticks']}  tempo={first['tempo_hz']} Hz  "
      f"{first['hdr_ms_tick']} ms/tick  vnn.update={first['vnn_update_ms']} ms  "
      f"snapshot calls={first['snap_calls']}")

cols = ["time","ticks","tempo_hz","hdr_ms_tick","whole_ms","vnn_update_ms",
        "snap_ms","snap_pct_log","snap_calls","ratio_calc"]
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in reports: w.writerow({k: r.get(k) for k in cols})
print(f"\nper-report CSV written: {OUT}")
