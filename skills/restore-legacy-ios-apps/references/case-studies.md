# Case studies and transfer conditions

Snapshot: 25 October 2026. These are distilled source-report findings, not tests rerun while creating this skill. See [sources.md](sources.md) and the adjacent public evidence manifest for pinned implementations.

| App | Established approach | Important boundary |
| --- | --- | --- |
| Chuzzle | Static specialization of original ARM semantics; legacy API host; shipping interpreter fallback disabled | Not recovered clean C++ or a complete removal of compatibility code |
| Koi Pond | Same translation family; guarded render/timing/touch/sleep adaptations | Enhanced simulation approximates original behavior; original24 mode remains reference |
| Skee-Ball | Original Unity/Mono AOT ARM interpreted with native services/presentation | Native ARM64 host is not a native gameplay rewrite |
| Skee Free | Related interpreted runtime with independent offline-service fixes | Similarity did not remove free-only SDK or menu differences |
| Skee-Ball HD | ARMv6 interpreted Unity; VFP short-vector and iPad/scene fixes | Neither age nor branding proves same CPU requirements as phone siblings |
| Peggle / Peggle HD | Interpreted ARMv7 with guarded native hot routines and native management host | Broad AOT was paused; selected helper compilation is not whole-program translation |

## Failed approaches worth preserving

- Chuzzle recreation reproduced ordinary matching but lost original experience; user rejected it. Early recreation notes do not describe the final translated port.
- Unity managed metadata and extracted SceneKit scenes did not recover runnable original gameplay.
- Doubling Chuzzle update frequency doubled game speed. Extra renders alone did not create interpolation.
- Koi high resolution cropped an unscaled offscreen target. High input rate still amplified drag ripples after simulation coefficients were adjusted.
- Koi expanded logical height and upscaled assets were rejected; optional cropping is a different final feature.
- Skee direct presentation initially corrupted output through a host/guest texture-name collision. High FPS did not establish correct pixels.
- Removing visible online UI did not stop old SDK load hooks/lifecycle workers.
- Skee HD valid GPU output remained invisible in the unattached window; its collapsed glyphs separately needed VFP semantics.
- Peggle larger inflate acceleration failed on real inputs; guarded smaller work remained. Some generated UI prototypes cost more than original execution.
- Peggle settings defaults misrepresented effective copy-ring behavior because startup explicitly overrode them.
- Correct merged completion still resumed an older board until checkpoint precedence was handled.
- Local iCloud folder exchange did not establish remote provider delivery. This remained an explicit test gap at report time.

## Transfer matrix

| Finding | Reuse level | Required evidence |
| --- | --- | --- |
| Original input inventory and exact guards | General workflow | Hash the right layer and inspect each slice |
| Atomic writes, lifecycle state machine | General structure | Preserve app-specific API/errors/save semantics |
| Scene/key-window/drawable ownership | Broad host pattern | Test actual scene and cold launch on each display |
| Direct texture presentation | Conditional optimization | Context/state/lifetime/namespace correctness and measured cost |
| Koi empty-target scaling | Narrow patch | Identify same offscreen purpose and constraints |
| Koi move-impulse normalization | Narrow model | Identify event slots, strengths and original cadence |
| VFP short-vector handling | CPU semantic fix | Target actually uses LEN/STRIDE behavior; production tests |
| Unity expanded world/fixed UI | Rendering heuristic | Perspective/ortho conventions plus every interaction path |
| Retired service suppression | Binary-specific | Authorized feature scope and exact entry contracts |
| Native helpers | Routine/version-specific | Full machine-state equivalence and net benefit |
| Peggle semantic progression merge | Format/domain-specific | Parsed schema, identity and reset semantics |
| Public source packaging | General workflow | Actual dependency/source/input correspondence |

Do not transfer numerical offsets, guest addresses, touch constants, campaign ranges, timing thresholds or toolchain versions without re-derivation. Treat filenames, historical status text and UI copy as weaker evidence than current dispatch/configuration, guarded code and named tests. Do not invent quantitative comparisons when only user observations survived.
