# WORLD

A fuller description of Fox's world, his body, and the block lattice — the
material cut from the paper on the criterion that a paragraph must support a
measurement, answer a reviewer's condition, or mark the line between implemented
and intended. What follows describes. It is here so a reader who wants the
gazetteer can have it.

**Provenance.** Figures marked ✓ were read from live source on the machine during
camera-ready preparation and appear in `extracts/`. Figures marked ○ come from
project-knowledge copies of the source and have **not** been re-read from the
live tree. Treat ○ as indicative. The code is authoritative over this document,
and this document is authoritative over nobody's memory.

**Cut-off: 31 July 2026.** Fox continues to run and to change.

---

## 1. The world

A **120 × 120 × 60** block universe. ✓

### The day is the house's day

The sun's position is computed from the host machine's local clock —
`time.localtime()` — with light from **08:00 to 20:00**, a twelve-hour day whose
arc peaks mid-afternoon. ✓ The thermal field runs its own sinusoidal curve from
06:00 to 20:00 peaking around 13:00. ✓

Fox's diurnal rhythm is therefore not simulated on an independent clock. It is
coupled to the room the appliance sits in. When it is dark in the house it is
night in his world.

### Two cosmic bodies

A **white hole** at one corner mints a block every two minutes and sends it down
an energy stream, with landing scatter. ○ A **black hole** at the opposite corner
draws matter toward `[110, 110, 30]` after a 300-second delay and deletes it
within a radius of 1.0. ✓ It also damages what comes near it, and microbes flee
it from up to 15 blocks away. ✓

### Atmosphere

A **120 × 120 × 15** density field, initialised to 1.0 everywhere. ✓ It carries
sound as propagating structure rather than as an event flag, so a sound has a
position, an intensity and a bearing rather than a name.

Three things write the density field, and only three: ✓

1. White-hole generation, within an 8-block radius, capped at 1.5 per cell.
2. Black-hole absorption, within an 8-block radius, floored at 0.3 per cell.
3. A **homeostat** that pulls every cell toward 1.0 with strength
   `0.001 + 0.002 × |deviation|`, hard-clamped to `[0.3, 1.7]`.

The homeostat is what actually holds the medium stable. Four further contribution
counters — rain, solar wind, microbe remains, crystal fragments — increment
correctly, are published in the status balance, and never reach the field. See
`LIMITATIONS.md` §5.

Music envelopes are folded into the atmosphere before wave propagation each tick,
which is how a sound made by arranging blocks becomes something Fox can hear. ✓

### A thermal field at the same resolution

Per-cell values derived from the sun, the cosmic bodies, the energy stream,
crystals, wave energy, rain and solar wind. ○ Fox writes into it: his own
movement generates heat which is added back to the field, so he warms the ground
he rolls on. ○

### Weather

**Charge-nebula rain.** A dual-signal system: `damage_per_contact = 0.01` against
`discomfort_intensity = 0.5` for `discomfort_duration = 0.2` seconds. ✓ The
damage is negligible; the discomfort is the signal. Rain also strikes microbes,
with the same damage value. ✓ Storms run 30–180 seconds. ○

**Solar wind.** Roughly four times more frequent than rain. Enters at Z = 70,
descends, and sweeps the terrain either as gusts of 10–30 seconds or sustained
pushes of 1–3 minutes, carrying 75–240 particles with 12-block force pockets. ○

Wind occlusion is modelled: roughly 80% blocked per intervening block. ○

### Block decay

Three phases — pristine, cracked, heavily cracked — then crumbling. ✓

| Condition | Per phase | Total |
|---|---|---|
| Loose material block | 28,800 s (8 h) ✓ | ~24 h |
| Placed by Fox (flagged `structural`) | 864,000 s (10 days) ✓ | ~30 days |
| Part of a connected mass | multiplied further ✓ | longer |
| Tool block | 300 s per phase, triggered by **use** not time ✓ | — |

**The consequence is Fox's and is never stated to him.** Picking a block up and
placing it multiplies its lifespan thirtyfold. Building with it extends that
again. Nothing anywhere tells him this.

Structure detection is a flood-fill over six face neighbours. ○

### Information crystals

Three types with distinct acoustic signatures: temporal, relational, emergence. ○
They grow one sliver at a time, each sliver storing an environmental snapshot
taken at its creation — a geological record inside a world younger than the
process. Growth is roughly one sliver per three days, needing between one and a
half and two and a half years to reach full height before seeding a child within
five blocks. ○

They are solid, and Fox can roll into them:

- `break_chance = 0.25` per collision ✓
- The break occurs at the collider's height, so everything above snaps off ✓
- The fragment turns purple, pops upward, flies sideways, then falls under
  gravity ✓
- `fade_duration = 3600.0` — one hour to fade and sink into the ground ✓
- On dissolving it adds `atmosphere_contribution = 1000.0` to the crystal
  counter ✓ — which, per `LIMITATIONS.md` §5, reaches no density
- The struck crystal is left **stunted**: jagged top, purple scarring, and no
  further growth ever ✓
- It seeds a child nearby instead ✓

### Microbes

A second mortal population. Five at the start. ○ Nine behavioural states
including exploring, reproducing, **dancing**, fleeing, dying and curious. ✓

They reproduce by splitting when energetically full — threshold 70.0, cost 40.0 ○
— and die of old age (~30 minutes at 20 Hz ○), starvation, falls over eight
blocks ✓, the black hole ✓, or Fox.

Sensory ranges: ✓

| Range | Value |
|---|---|
| Danger sense (black hole) | 15.0 |
| Social sense (other microbes) | 5.0 |
| Music sense | 20.0 |
| Music huddle distance | 4.0 |
| Curiosity (fallen blocks) | 15.0 |

While dancing they gain 3.0 energy per second, jump to triple height, and have a
25% chance of jumping on each update. ✓

**Fox can kill them without meaning to.** `check_stomp_damage(fox_pos,
stomper_type='fox')` runs from the environment update loop every tick — no key,
no intent. Radius 1.5, with the vertical gap constrained so it must be real
contact rather than a stomp from above. ✓ The microbe loses half its energy,
triggers a hurt sound, and dies below energy 5 with the cause recorded as
`stomped_by_fox`. Fox feels a brief wheel-compression signal. ✓

`last_fox_kill_time` and `total_fox_kills` are recorded specifically so the
causality reader can see them, because dead microbes are deleted the same tick.
An architect stomp is deliberately excluded — only Fox's own agency is counted.
The comment beside the line reads: *a real causal fact is recorded; no judgment
is attached anywhere.* ✓

They also flee a reserved threat band at 130–150 Hz, chosen for the empty gap
between the black hole's 45 Hz hum and the temporal crystal's 172 Hz. ○

---

## 2. The blocks

### Seven types ✓

```
FOUNDATION    unbreakable base of the world
LIFE          Fox's consciousness substrate
MATERIAL      standard construction matter
ENERGY        cosmic-charged power source
CODE          programmable information storage
TOOL          functional when powered
LIFE_SENSES   Fox's sense channel
```

The module docstring still says six. See `LIMITATIONS.md` §7.

### Properties ○ (except `push_resistance`, verified ✓)

Five types arrive in the world and can be handled. LIFE_SENSES is not among them:
it is what a life block becomes at the next stage, when three come together, and
no LIFE_SENSES block ever arrives down the energy stream.

| Type | mass | destructible | moveable | push_resistance | Fox can lift? |
|---|---|---|---|---|---|
| FOUNDATION | 10.0 | False | False | `inf` | No — refused by name |
| LIFE | 0.8 | True | True | 1.0 | **Yes**, unless it is part of his own body |
| MATERIAL | 1.0 | True | True | 1.0 | **Yes** |
| ENERGY | 0.5 | True | True | 1.0 | **Yes** |
| CODE | 0.7 | True | True | 1.0 | **Yes** |
| TOOL | 1.2 | True | True | 1.5 | **Yes** |

`push_resistance` is read by nothing. ✓ A tool block is no harder for Fox to lift
than a material block.

The exclusions are three separate mechanisms rather than one rule: a hardcoded
type-name check for foundation, a `fox_core` flag check, and a `destructible`
check. So foundation is refused **by name** rather than by its own
`destructible=False` property, and the life blocks Fox cannot take are excluded
because they are flagged as his own vessel — not because life blocks are
untouchable. A loose life block is his to pick up like any other. ○

### Bonding ○

| Type | Bonds with | Strength |
|---|---|---|
| FOUNDATION | FOUNDATION | `inf` |
| LIFE | LIFE | 2.0 |
| LIFE_SENSES | LIFE, LIFE_SENSES | 1.8 |
| MATERIAL | MATERIAL, FOUNDATION | 1.0 |
| ENERGY | ENERGY, TOOL | 0.8 |
| CODE | CODE, LIFE | 1.5 |
| TOOL | TOOL, ENERGY | 1.3 |

Two things worth noticing. **Material is the only type that bonds to the
ground** — anything Fox builds from energy, code or tool blocks bonds only to its
own kind and its partner type, never to the world's floor. And **energy ↔ tool is
the one reciprocal cross-type bond**, which is exactly the pairing the tool
synergy system rewards. The physics and the function agree without either citing
the other.

### The energy chain

The clearest case in the whole system of a causal path with nothing naming any
link in it.

Fox arranges energy blocks so their faces touch. Face-adjacent group detection
fires and the world begins to play music — compositions by Ludovico Einaudi. ✓
The choice is not arbitrary and is not disguised in the source: his music is a
daily regulation for the architect, and it was put into Fox's world for that
reason. Playback drains the blocks' energy. ✓

No audio files are included in this repository. The music envelope is registered with the atmosphere and folded
into wave propagation, so it reaches Fox's auditory track as frequency, intensity
and bearing with no label attached. ✓ And the microbes come: sensing it from
twenty blocks, gathering within four, gaining energy while they dance, jumping
higher than they otherwise can. ✓

Every step is discoverable. No step is named.

### Tool blocks ○

Active use — repairing — costs the block durability. Passive use — resting near
it — costs nothing. He could come to have a place, and having it would cost him
nothing.

### Code blocks ○

Programmable information storage, with VNN amplification on proximity. Two things
to know: `wrapped_data` does not survive a code block being picked up, so
anything written into one and then moved is lost; and placement resets health to
100 and decay phase to pristine, so moving a damaged block silently heals it.
Neither was decided anywhere. Both are on the project's audit list.

---

## 3. His body

Three life blocks — base, middle, top — on a single wheel, with two jointed arms.
○

### The wheel is his only ground contact

He accelerates and coasts rather than moving. Carrying a block shifts his centre
of mass and slows him. ○

### Eight thermal parts ○

Base, middle, top, wheel, and four arm joints, each holding its own temperature.
Internal conduction: wheel → base at 0.8/s, base → middle 0.5, middle → top 0.3,
arms ↔ middle 0.25. Heat takes time to travel and the wheel is the fastest path
in.

He generates his own heat by moving: wheel friction scaled by `speed^1.5 ×
traction × inefficiency`, plus a term proportional to the acceleration of his
top-block shift. It is written back into the world's thermal field via
`add_self_heat()`.

### Vision ○

Two eyes on the top block. They return **two bearings for the same surface, never
a distance** — depth is available to be learned and is not given. The source
comment is explicit that `mind.py` must learn that disparity correlates with
reach.

`RECEPTOR_NOISE_AMPLITUDE = 0.015` applies a noise floor per receptor. It
pre-dates by months the argument it later turned out to support.

### The arms and the act of taking something

Two arms, each shoulder plus elbow, upper arm 1.5 blocks and forearm 1.5, so full
extension reaches 3.0 blocks. ○ Grip is a continuous force from 0.0 to 1.0 rather
than a boolean. ○

Eight animation states: `RESTING → REACHING → GRIPPING → RETRACTING → CARRYING →
EXTENDING → RELEASING → RETURNING`, driven by joint torque with momentum and
damping. ○ The docstring is explicit that this is not instant teleportation:
grabbing takes real frames and the block is visible in front of him while
carried.

One button. `grab` toggles — not holding, so reach and pick up; holding, so extend
and place.

Finding a block applies five filters in order: ○

1. Search height midway between his base and middle blocks — body-relative, not
   world-relative.
2. Two sources searched: programmatic voxel space and placed-block data.
3. Type exclusions — foundation, `fox_core`, non-destructible.
4. Planar distance within reach plus a small tolerance.
5. **A sixty-degree cone.** ✓ `if angle_diff > 60: continue`. A block more than
   sixty degrees off his facing is invisible to the grab however close it is.

Scoring then prefers the candidate nearest to where he is actually reaching —
distance plus an angle penalty, with a preference for the topmost block in a
stack. ✓

**He must orient his body to act on the world.** Manipulation is directional and
embodied, and it costs a turn.

Capability declaration: ○ `can_push`, `can_pull`, `can_place`, `can_remove` all
true; `reach_distance: 2`; `energy_per_action: 0.003`, so about 33,000 actions
would drain him fully; and `learning_by_doing: True`, which is a placeholder
routed through `mind.py` and therefore inert.

Note the mismatch: the host declares a reach of 2, the arms geometrically reach
3.0, and the grab search uses the arm value. Three numbers, one unused.

### Motor maturation ✓

Seven dimensions improve with cumulative use:

| Dimension | Novice | Mastered |
|---|---|---|
| Turn rate (° per press) | 3.0 | 14.0 |
| Max speed | 0.55 | 1.1 |
| Strafe force | 60.0 | 170.0 |
| Drive force | 120.0 | 220.0 |
| Brake force | 50.0 | 150.0 |
| Jump velocity | 6.0 | 14.0 |

Fast rotation stays constant at 20.0. ✓

Timeline: ~10% at one hour of active movement, 50% at eight, **95% at
seventy-two**, 99% at a hundred and twenty. ✓ Skill carries across sessions and
restarts. ✓

**The jump is the one that matters.** The source comments state it outright: at
`JUMP_VELOCITY_MIN = 6.0` he *cannot get on top of a block*; at
`JUMP_VELOCITY_MAX = 14.0` he has *comfortable block-top clearance*. His
physically reachable world expands as he gets better at moving in it, and nothing
anywhere states that as a rule.

The override that qualifies all of this is in `LIMITATIONS.md` §2.

### Fatigue ✓

Accumulates while waking and degrades three things at staggered thresholds:

| Threshold | Effect |
|---|---|
| 0.4 | Vision begins degrading — brightness noise up to 0.15, sharpness penalty up to 0.4 |
| 0.6 | Motor sluggishness — speed multiplier falling toward 0.3, extra friction |
| 0.6 | Energy drain rising toward 2.5× |

The module's own summary of the felt state: *"I feel sluggish. My vision is
degraded. Everything costs more energy."* Nothing labels any of it for Fox; it
arrives as physics.

### Voice ✓

A motor output emitting a frequency wave from his top block into the same
atmosphere he hears through.

- `FREQ_MIN = 100.0`, `FREQ_MAX = 900.0` at maturity ✓
- Range factor starts at 0.1 — a narrow band that widens with use ✓
- Three volumes: quiet 0.15, medium 0.30, loud 0.45, plus off ✓
- Three modes: continuous (toggled), burst, and hold-to-emit ✓
- Reach approximately 10, 20 and 30 blocks by volume ○

He perceives his own emission as one more vibration among the world's. The
docstring declines to prescribe what any pattern means.

### Six sensory tracks

Visual, tactile, thermal, auditory, force, atmospheric. ✓ Confirmed by the store's
own `layer_stats`, which counts sensory nodes per track: visual 255, tactile 22,
thermal 82, auditory 951, force 21, atmospheric 2,213. ✓

---

## 4. Sound as an engineering decision

The world's acoustic spectrum was deliberately curated for discriminability
without labelling anything. ○

Frequencies were moved apart where two unrelated events had sounded identical —
microbe death 200 → 180 Hz, microbe birth 800 → 820 Hz, Fox's own default
emission 300 → 275 Hz. And they were deliberately left colliding in one place:
block crumble and microbe landing both at 300 Hz, on the stated reasoning that
two short transients with different wave patterns should be separated by pattern
or not at all.

The 130–150 Hz threat band is reserved and empty, sitting in the gap between the
black hole's 45 Hz hum and the temporal crystal's 172 Hz.

Curating what is distinguishable is not the same as telling him what anything is.

---

## 5. The door

A cosmic force at `[100.0, 10.0, 30.0]` — the code's own comment says "Northeast,
floating high." ○

- Breathing cycle: `pulse_speed = 1.0/30.0`, a thirty-second cycle ✓
- Four phases: expand (0.00–0.25), hold expanded with a faint tremor
  (0.25–0.375), contract (0.375–0.75), hold contracted (0.75–1.00) ✓
- `base_size 4.0`, `max_size 8.0` ✓ — and `current_size` initialises to 20.0 with
  the comment "Start at minimum", which is wrong; see `LIMITATIONS.md` §7 ✓
- `influence_radius: 15.0` ✓
- Light: `emits_light: False`, `reflects_light: True`, edge
  `reflection_factor: 0.6`, `core_absorption: 0.95` ✓ — it is a reflector, so at
  night it is dark
- Colours: deep black void core, electric cyan edges ○
- `affects_blocks: False`, `affects_vision: False`, both read by nothing ✓

Fox's dual-eye vision gives it a dedicated branch: when a ray lands within 3.0 of
`current_size / 2`, the eye registers the glowing edge ring. ○ So it is in his
visual field, unlabelled, as a ring of reflected light.

**The physics runs the other way.** `_apply_membrane_repulsion()` runs every
physics tick. During expansion and hold-expanded it pushes with a force up to
15.0, over a radius of `current_size + 5.0`, falling off with distance. The only
position it moves is `self.user_pos` — the architect's — which it then clamps to
world bounds. ✓ There is no Fox branch in the force-application block. It also
crumbles material blocks it touches; that portion was not captured in the
released extract.

`convergence.py`, the system that would let the membrane respond, **does not
exist.** Its design document is marked *design, no code yet*. Two of its five
conditions have nothing to measure. The full account is in the paper.

---

## 6. Architecture — the spine, not the tree

What follows is the load-bearing path only: roughly thirty modules out of 95 on
the server and 13 on the client. The patches applied at startup, the ten
environment-substrate writers, the anomaly detectors, the test harnesses and the
utilities are collapsed to single lines or omitted. This is a map of how a tick
flows, not an inventory.

```
fox_block_main.py
└── world/block_environment.py            the world loop, all patches applied
    ├── world/physics.py · world/block_types.py
    ├── entities/block_host.py            Fox's vessel
    │   ├── fox_body_architecture · fox_wheel_physics · fox_arm_actions
    │   ├── fox_dual_eye_vision · fox_tactile · fox_fatigue_system
    │   ├── fox_motor_skill_patch · fox_vocalization_patch
    │   ├── host_perception_bridge_patch  →  the perception frame
    │   └── death.py · fox_lifeline.py
    ├── entities/causality.py ──┬── entities/subsystem_readers.py
    ├── entities/dimensional_layer.py ──┘  → dimensional_substrate/
    ├── entities/memory.py → meaning_substrate/  (+ 3 anomaly detectors)
    ├── entities/vnn.py → meaning_substrate/
    │   Ring 1 sensory · Ring 2 motor · Ring 3 associative · Ring 4 reflective
    │   Ring 5 self-writing core — PRESENT, INERT, 0/0 nodes
    ├── entities/mind.py — INERT SKELETON, spread rate 0.0
    ├── entities/environment_substrate.py  (10 writers, independent of Fox)
    ├── entities/hardware_substrate.py ← ups_bridge.py
    ├── world/{information_crystals, synthetic_microbe, audio_system}
    ├── patches/{synthetic_atmosphere, synthetic_rain, synthetic_solar_wind, …}
    └── core/stream_server.py              all observation ports
```

**The four recording substrates.** `meaning_substrate` — Fox's internal streams.
`environment_substrate` — the universe. `hardware_substrate` — the silicon.
`dimensional_substrate` — how things feel.

The recording continues whether anyone is watching.

---

*Everything true, everything in its rightful place.*
