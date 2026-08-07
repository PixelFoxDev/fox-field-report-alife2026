#!/usr/bin/env python3
"""Heartbeat ledger census from logs/tomb.log, bounded at the paper's cut-off.
Read-only. tomb.log is newline-delimited JSON; session_start is the run boundary.
The store rolled over to a new longitudinal store in August, so every figure in
the paper must be read from records on or before 31 July 2026."""
import json, statistics
from datetime import datetime

LOG   = "logs/tomb.log"
CUTOFF = "2026-08-01T00:00:00"

recs, bad = [], 0
for line in open(LOG, errors="replace"):
    line = line.strip()
    if not line: continue
    try:
        r = json.loads(line)
        if "ts" in r: recs.append(r)
        else: bad += 1
    except Exception:
        bad += 1

recs.sort(key=lambda r: r["ts"])
print(f"records parsed        : {len(recs)}   (unparseable lines: {bad})")
print(f"full file spans       : {recs[0]['ts'][:19]}  ->  {recs[-1]['ts'][:19]}")
inb = [r for r in recs if r["ts"] < CUTOFF]
print(f"records on/before 31 Jul : {len(inb)}   ({len(recs)-len(inb)} August records excluded)")
if not inb: raise SystemExit("nothing inside the window")
print(f"bounded span          : {inb[0]['ts'][:19]}  ->  {inb[-1]['ts'][:19]}")

d0 = datetime.fromisoformat(inb[0]["ts"]); d1 = datetime.fromisoformat(inb[-1]["ts"])
print(f"calendar span         : {(d1-d0).days} days")
print(f"distinct active dates : {len({r['ts'][:10] for r in inb})}      <- paper says 46 days")

# sessions: session_start opens one; duration is the largest session_sec inside it
sessions, cur = [], None
for r in inb:
    if r.get("event") == "session_start":
        if cur is not None: sessions.append(cur)
        cur = {"start": r["ts"], "dur": 0.0, "last": r}
        continue
    if cur is None:
        cur = {"start": r["ts"], "dur": 0.0, "last": r}
    s = r.get("session_sec") or 0.0
    if s > cur["dur"]: cur["dur"] = s
    cur["last"] = r
if cur is not None: sessions.append(cur)

durs = [s["dur"] for s in sessions]
print(f"\nsessions              : {len(sessions)}          <- paper says 257")
print(f"total hours           : {sum(durs)/3600:.1f} h        <- paper says 342.8 h")
print(f"longest run           : {max(durs)/3600:.1f} h         <- paper says 67.3 h")
print(f"under one hour        : {sum(1 for d in durs if d < 3600)}          <- paper says 223")
print(f"median session        : {statistics.median(durs)/60:.1f} min       <- paper says 5.2 min")
lg = max(sessions, key=lambda s: s["dur"])
print(f"  longest run began   : {lg['start'][:19]}")

# the 31 July shutdown record — the paper's node/archway corroboration
print("\n31 July records that are not routine heartbeats:")
for r in [x for x in inb if x["ts"][:10] == "2026-07-31" and x.get("event") != "checkpoint:heartbeat"]:
    print(f"  {r['ts'][:19]}  {r.get('event')}  store={r.get('store_size')}  "
          f"nodes={r.get('vnn_nodes')}  archways={r.get('vnn_archways')}")

peak = max(inb, key=lambda r: r.get("vnn_nodes") or 0)
print(f"\npeak vnn_nodes in window : {peak.get('vnn_nodes')} at {peak['ts'][:19]} "
      f"(archways={peak.get('vnn_archways')}, store={peak.get('store_size')})")
print("  paper says nodes=114,411  archways=545,340  store=49,256")
print(f"\nlast record in window  : {inb[-1]['ts'][:19]}  {inb[-1].get('event')}  "
      f"store={inb[-1].get('store_size')}  nodes={inb[-1].get('vnn_nodes')}  "
      f"archways={inb[-1].get('vnn_archways')}")
print(f"last record in FILE    : {recs[-1]['ts'][:19]}  {recs[-1].get('event')}  "
      f"store={recs[-1].get('store_size')}  nodes={recs[-1].get('vnn_nodes')}  "
      f"archways={recs[-1].get('vnn_archways')}   <- August store; NOT the paper's figure")
