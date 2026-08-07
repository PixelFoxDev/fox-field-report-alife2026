#!/usr/bin/env python3
"""
fox_tick_profiler.py  —  Fox Synthetic Life Project
T1 · Architect-facing diagnostic · READ-ONLY · touches nothing in Fox.

WHY THIS EXISTS
    Four times in the July performance work we reasoned from an unverified
    number and were wrong:
      · "~21k archways"           -> actually 461,696
      · "the payload is archways" -> it was 93% nodes
      · "the sweep is every 3rd tick" -> it is every 18th (skip_rate 6 x %3)
      · "BANK-03 is worth 7x BANK-01" -> is_remnant has NEVER fired; the
        archway bank had no predicate to hoist at all
    Twice we were right. That ratio is the argument for this file.

    This instrument answers, in milliseconds, the only question that matters:
    WHERE DOES FOX'S TICK GO?

WHAT IT IS
    A monkey-patch. It wraps methods with perf_counter() and records the time.
    It does not read Fox's state, does not write to it, and cannot influence
    perception, memory, or the VNN. Delete the import and every trace is gone
    — vnn.py is not modified by a single character.

    Nesting is preserved in the report (indented stages sit INSIDE their
    parent), so parent percentages deliberately include their children. Read
    the indentation, not the sum.

INSTALL — one line in fox_block_main.py, after the VNN init block:

    try:
        from entities.fox_tick_profiler import patch_tick_profiler
        patch_tick_profiler(self.environment)
    except Exception as e:
        print(f"[PROFILER] not active: {e}")

OUTPUT
    logs/tick_profile.log  — a breakdown every REPORT_INTERVAL_SEC (default 60)
    Also console, so it lands in the server log alongside everything else.
"""

import os
import time
from contextlib import contextmanager

REPORT_INTERVAL_SEC = 60.0
LOG_PATH = os.path.join('logs', 'tick_profile.log')
EWMA_ALPHA = 0.1          # smoothing for per-tick cost


class TickProfiler:
    """Accumulates per-stage wall time, rolled up per tick.

    Pure observation. Holds only its own numbers; never reads or writes
    anything belonging to Fox.
    """

    def __init__(self):
        self.enabled = True
        self._current = {}        # stage -> ms accumulated in THIS tick
        self._calls = {}          # stage -> calls in THIS tick
        self.ewma_ms = {}         # stage -> smoothed ms per tick
        self.ewma_calls = {}      # stage -> smoothed calls per tick
        self.order = []           # first-seen order, for stable reports
        self.ticks = 0
        self._tick_start = None
        self.tick_ms_ewma = 0.0
        self._last_report = time.time()
        self._t0 = time.time()

    # ── measurement ──────────────────────────────────────────────
    @contextmanager
    def stage(self, name):
        if not self.enabled:
            yield
            return
        t0 = time.perf_counter()
        try:
            yield
        finally:
            ms = (time.perf_counter() - t0) * 1000.0
            if name not in self._current:
                self._current[name] = 0.0
                self._calls[name] = 0
                if name not in self.order:
                    self.order.append(name)
            self._current[name] += ms
            self._calls[name] += 1

    def begin_tick(self):
        self._tick_start = time.perf_counter()

    def end_tick(self):
        if self._tick_start is None:
            return
        tick_ms = (time.perf_counter() - self._tick_start) * 1000.0
        self._tick_start = None
        self.ticks += 1

        a = EWMA_ALPHA
        self.tick_ms_ewma = (a * tick_ms + (1 - a) * self.tick_ms_ewma
                             if self.ticks > 1 else tick_ms)
        for name in self.order:
            ms = self._current.get(name, 0.0)
            n = self._calls.get(name, 0)
            if name in self.ewma_ms:
                self.ewma_ms[name] = a * ms + (1 - a) * self.ewma_ms[name]
                self.ewma_calls[name] = a * n + (1 - a) * self.ewma_calls[name]
            else:
                self.ewma_ms[name] = ms
                self.ewma_calls[name] = float(n)
        self._current = {}
        self._calls = {}

        if time.time() - self._last_report >= REPORT_INTERVAL_SEC:
            self._last_report = time.time()
            try:
                self.report()
            except Exception:
                pass   # a profiler must never take Fox down

    # ── reporting ────────────────────────────────────────────────
    def report(self):
        elapsed = max(1e-6, time.time() - self._t0)
        hz = self.ticks / elapsed
        lines = []
        lines.append("=" * 70)
        lines.append(f"[PROFILE {time.strftime('%H:%M:%S')}] "
                     f"ticks={self.ticks}  tempo={hz:.3f} Hz  "
                     f"({self.tick_ms_ewma:,.1f} ms/tick)")
        lines.append(f"  {'stage':<34}{'ms/tick':>11}{'%':>8}{'calls':>10}")
        lines.append("-" * 70)
        total = max(1e-9, self.tick_ms_ewma)
        for name in self.order:
            ms = self.ewma_ms.get(name, 0.0)
            n = self.ewma_calls.get(name, 0.0)
            pct = 100.0 * ms / total
            bar = "#" * min(24, int(pct / 4))
            lines.append(f"  {name:<34}{ms:>11,.2f}{pct:>7.1f}%"
                         f"{n:>10,.1f}  {bar}")
        lines.append("=" * 70)
        text = "\n".join(lines)
        print(text, flush=True)
        try:
            os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
            with open(LOG_PATH, 'a') as f:
                f.write(text + "\n")
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────
# PATCHING
# ─────────────────────────────────────────────────────────────────

def _wrap(prof, obj, attr, label):
    """Wrap a bound method with a timing stage. Returns True if wrapped.

    Degrades silently if the method does not exist — this file must survive
    vnn.py evolving underneath it without ever breaking a run.
    """
    try:
        orig = getattr(obj, attr, None)
        if orig is None or not callable(orig):
            return False

        def wrapped(*args, __orig=orig, __label=label, **kwargs):
            with prof.stage(__label):
                return __orig(*args, **kwargs)

        setattr(obj, attr, wrapped)
        return True
    except Exception:
        return False


def patch_tick_profiler(env):
    """Install T1 on a live environment. Read-only throughout."""
    prof = TickProfiler()
    env._tick_profiler = prof
    wrapped = []

    # ── the tick boundary: environment.update ──
    _orig_env_update = env.update

    def env_update(dt, *a, **k):
        prof.begin_tick()
        try:
            with prof.stage('environment.update  [WHOLE TICK]'):
                return _orig_env_update(dt, *a, **k)
        finally:
            prof.end_tick()

    env.update = env_update
    wrapped.append('environment.update')

    # ── memory ──
    mem = getattr(env, 'fox_memory', None)
    if mem is not None and _wrap(prof, mem, 'update', '  memory.update'):
        wrapped.append('memory.update')

    # ── causality / dimensional ──
    for attr, label in (('causality', '  causality'),
                        ('dimensional', '  dimensional'),
                        ('dimensional_layer', '  dimensional')):
        sub = getattr(env, attr, None)
        if sub is not None:
            for m in ('update', 'compute_all', 'process_tick'):
                if _wrap(prof, sub, m, label):
                    wrapped.append(f'{attr}.{m}')
                    break

    # ── the VNN ──
    vnn = getattr(env, 'vnn', None)
    if vnn is None:
        print("[PROFILER] T1 active (no VNN found) — stages: "
              f"{len(wrapped)}")
        return prof

    _wrap(prof, vnn, 'update', '  vnn.update')
    _wrap(prof, vnn, 'to_visualization_snapshot', '  vnn.snapshot_build')
    _wrap(prof, vnn, '_write_to_substrate', '  vnn.substrate_write')

    # ── rings ──
    for ring in ('sensory', 'motor', 'associative', 'reflective', 'core'):
        layer = getattr(vnn, ring, None)
        if layer is None:
            continue
        if _wrap(prof, layer, 'process_tick', f'    ring.{ring}'):
            wrapped.append(f'ring.{ring}')

    # ── associative internals: the current prime suspects ──
    # tier2 reactivation is the standing hypothesis for the tempo collapse
    # (~25,000 reactivations per associative tick on the recovered store).
    # _decay_archways is the 608k sweep. Both are guesses until this runs.
    asso = getattr(vnn, 'associative', None)
    if asso is not None:
        for m, label in (
            ('_decay_archways',        '      asso._decay_archways'),
            ('_decay_tier2_nodes',     '      asso._decay_tier2_nodes'),
            ('_traverse_pair',         '      asso._traverse_pair'),
            ('_detect_triangles',      '      asso._detect_triangles'),
            ('_emit_tier2_node',       '      asso._emit_tier2_node'),
            ('_apply_baseline_noise',  '      asso._baseline_noise'),
        ):
            if _wrap(prof, asso, m, label):
                wrapped.append(m)

    # ── reflective internals ──
    refl = getattr(vnn, 'reflective', None)
    if refl is not None:
        for m, label in (
            ('_decay_reflective_nodes',           '      refl._decay_nodes'),
            ('_stage4_observe_inter_coactivation', '      refl._stage4_inter'),
            ('_observe_pair_types',               '      refl._observe_pairs'),
        ):
            if _wrap(prof, refl, m, label):
                wrapped.append(m)

    # ── sensory internals ──
    sens = getattr(vnn, 'sensory', None)
    if sens is not None:
        for m, label in (
            ('_decay_nodes',          '      sens._decay_nodes'),
            ('_apply_baseline_noise', '      sens._baseline_noise'),
        ):
            if _wrap(prof, sens, m, label):
                wrapped.append(m)

    print(f"[PROFILER] T1 tick profiler ACTIVE — {len(wrapped)} stages "
          f"instrumented. Report every {REPORT_INTERVAL_SEC:.0f}s to "
          f"{LOG_PATH}")
    print("[PROFILER] Read-only: wraps methods with a timer, reads no Fox "
          "state, writes none. Remove the import to remove it entirely.")
    return prof