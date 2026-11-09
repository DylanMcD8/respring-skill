# Legacy iOS restoration findings for a reusable AI skill

> Public edition prepared 9 November 2026 from the 25 October 2026 report. Historical test results were not rerun for this edition. Private workspace references were removed or replaced with pinned public source; private evidence remains explicitly unavailable. Original app identifiers and technically relevant device models are retained. No personal saves, credentials, device identifiers, raw logs or test media are included. This review does not establish exhaustive game parity.

Prepared 25 October 2026. Scope: Chuzzle, Koi Pond, Skee-Ball, and Skee Free, with Skee-Ball HD as a supplemental case study. This is a technical synthesis for combining restoration findings, not a new release announcement. It excludes the Respring website and does not assess the independently developed Peggle projects.

The main result is that preserving original behavior did not require recovering clean original source. Chuzzle and Koi Pond run statically translated original instructions inside a legacy API compatibility environment. Skee-Ball and Skee Free retain CPU interpretation of the original Unity/game binary, while native host services provide presentation, input, audio, and lifecycle integration. Both approaches produced installable ARM64 applications without runtime JIT generation. Neither is a ground-up native rewrite.

The useful reusable unit is a method with applicability conditions and verification evidence—not a directory of patches copied into every game. The report distinguishes current source, historical measurements, user-confirmed behavior, and proposed future practice. The public source manifest records selected shareable implementation files, hashes and pinned commits; private historical records are not distributed. Source labels below resolve in the final section.

## Topic index

- [1. Architecture and terminology](#1-architecture-and-terminology)
- [2. Intake and feasibility investigation](#2-intake-and-feasibility-investigation)
- [3. What the Chuzzle-style translation actually does](#3-what-the-chuzzle-style-translation-actually-does)
- [4. Chuzzle case study](#4-chuzzle-case-study)
- [5. Koi Pond case study](#5-koi-pond-case-study)
- [6. Skee-Ball case study](#6-skee-ball-case-study)
- [7. Skee Free case study](#7-skee-free-case-study)
- [8. Supplemental Skee-Ball HD findings](#8-supplemental-skee-ball-hd-findings)
- [9. Modern windows, rotation, and foldable displays](#9-modern-windows-rotation-and-foldable-displays)
- [10. Measurement and regression practice](#10-measurement-and-regression-practice)
- [11. Build, signing, and release lessons](#11-build-signing-and-release-lessons)
- [12. Transfer matrix](#12-transfer-matrix)
- [13. Proposed structure for the later skill](#13-proposed-structure-for-the-later-skill)
- [14. Gaps to resolve when merging other reports](#14-gaps-to-resolve-when-merging-other-reports)
- [15. Source index](#15-source-index)


## 1. Architecture and terminology

| Application | Original workload | Current execution model | Logical canvas and presentation |
| --- | --- | --- | --- |
| Chuzzle | ARMv6, symbol-rich native C++/Objective-C; original 1.0, iPhone OS 2.2.1 metadata | Static specialization of original ARM semantics; translated support-library ARM/Thumb candidates; shipping interpreter fallback disabled | 320×480; centered 2:3 canvas; optional uniform crop-to-fill; 60 Hz gameplay |
| Koi Pond | Original 2.5 native game with custom raster/water passes | Same static-translation family; guarded timing/input/sleep adaptations; shipping fallback disabled | 320×480; centered 2:3 or optional uniform crop; original 24 FPS or enhanced 60/120 FPS |
| Skee-Ball | Original 2.5, Unity 3.3.0f4; ARMv6/ARMv7 slices; game methods compiled with Mono AOT | ARM/Thumb interpreter plus native legacy-API and graphics bridge | Original 320×480 UI; optional expanded 3D scene in both axes; live resizing |
| Skee Free | Original 2.5 sibling Unity application, with additional retired SDKs | Same interpreter family with independently guarded offline patches | Separate app/saves; centered 320×480 UI and expanded world |
| Skee-Ball HD | Older iPad 1.0 ARMv6 Unity application | Interpreter with additional VFP short-vector semantics | Original 768×1024 UI; iPad-specific identity and expanded-world adaptation |

Native ARM64 packaging says what architecture the executable runs on, not whether original game logic is interpreted. “No JIT” means no runtime machine-code generation; an interpreter also satisfies that description. “Static translation” means original instruction semantics are compiled ahead of execution. “Compatibility runtime” means the old ABI, pointers, objects, frameworks, files, graphics calls, and related services still need implementation. Removing the CPU interpreter does not remove these dependencies. [C1, C2, K1, K2, S1, F1, H1]

Do not report an unexplained “96% native” or “4% emulated.” Specify the denominator: executed instructions on a named trace, translated candidate addresses, elapsed time, API calls, or code size. These quantities are not interchangeable. API bridges should not be counted as unexplained interpreter fallback.

## 2. Intake and feasibility investigation

Preserve the input archive and inventory its payload before experimenting. Record provenance, archive/executable hashes, bundle ID, app version, architectures, encryption load commands, minimum OS/SDK metadata, dependent libraries, symbols, assets, and save expectations. Keep clean input, experiment output, signed device products, and public packaging separate.

Chuzzle’s inspected executable was unencrypted (`cryptid=0`) and retained useful local C++ symbols. Its initial analysis exported 194 functions and 25,624 lines of Ghidra pseudocode. That was informative, not recompilable source: ARMv6 VFP decoding and inferred C++ parameters were incomplete. The early Swift recreation reconstructed ordinary matching and movement but did not reproduce the full original experience. The user explicitly rejected that direction. Those early reverse-engineering notes remain valuable historical evidence, but their provisional scoring, gravity, and feature limitations do not describe the final translated port. [C3]

Skee-Ball offered an important counterexample. Assembly-CSharp.dll contained 1,384 methods with IL bodies consisting only of `ret`; gameplay implementations had been compiled to native ARM through Mono AOT. Exporting the assembly therefore produced metadata skeletons, not recoverable C# gameplay. Ghidra pseudocode for 1,252 native game-related functions also required extensive reconstruction. A separate SceneKit preview displayed extracted meshes, textures, and cameras but never established that gameplay was recovered. [S1]

A future skill should choose among three paths:

1. Static translation when instruction coverage, binary structure, and compatibility work are tractable.
2. Interpretation when the original engine/runtime is much larger or translation would delay faithful gameplay disproportionately.
3. Reconstruction only when the user accepts behavioral differences or independent gameplay implementation is the actual objective.

A small-looking app is not necessarily a small binary. Familiar engine assets are not proof that executable behavior survives in portable form. A missing framework should be investigated at its observed call sites; a long unresolved-import list is not itself evidence that every import must be implemented before launch.

## 3. What the Chuzzle-style translation actually does

The generator parses Mach-O sections and symbols, enumerates candidate instruction addresses, and emits Rust dispatch functions specialized for constant program counters and opcode words. LLVM compiles those semantics into ARM64 code. Guest registers, flags, memory accesses, 32-bit layouts, pointer arithmetic, and legacy call conventions remain represented explicitly. This is partial evaluation of an instruction implementation, not automatic recovery of high-level C++ source. [C4, C5]

The current Chuzzle native manifest records 1,460 named functions, 167,779 translated word addresses, and 657 pages. Koi Pond records 322 functions, 19,113 word addresses, and 75 pages. These are generation statistics, not proof of complete behavioral coverage. The support-library manifest explicitly warns that its 77,831 ARM and 155,661 Thumb candidates include data and alternate instruction interpretations. It covers the included libgcc/libstdc++ inputs at defined guest slides, guarded by PC, execution state, and instruction bytes. [C5, K3]

The original executable hashes recorded by the native generators are:

- Chuzzle: `c2c017d34c5858d1857e5e8b947d7f16325a46f5e9db32219a3c28689040cd08`
- Koi Pond: `0f375e3e96e748faac4505a05924e458e1fadd69d2726bf02b6de3b31d99d8d6`

These identify executables, not the outer IPAs. Do not use them to validate a different archive layer.

Shipping Chuzzle/Koi builds stop on unhandled code instead of silently falling back to interpretation. A development-only `aot-reference` configuration can provide comparison execution and diagnostic counters. The runtime contains code named `InterpreterCpu` and directories named `interpreter`; names alone cannot establish the shipping execution path. Check Cargo features, build defaults, and dispatch logic. Conversely, the Skee ports deliberately enable the interpreter-related configuration and must not inherit Chuzzle’s “fallback disabled” release settings. [C2, C6, K2, S2]

All functional patches should live in generators or maintained runtime/host source. Hand-editing a generated page makes regeneration destructive and leaves release provenance misleading. Guard modified instruction/data sites with expected words and whole-input identity where available. Fail clearly for a different binary; do not search-and-replace loosely by address.

## 4. Chuzzle case study

### Fidelity and assets

The original 320×480 coordinate system and original artwork were retained. Early asset recovery identified iSplat sprite metadata: little-endian name lengths, NUL-terminated names, frame counts, page indices, and floating UV rectangles. RGB JPEG/GIF pages combine with grayscale `_alpha.gif` companions. The investigation recovered 445 frames in 196 groups. This explains how assets can be inspected without confusing a reconstructed renderer with the original game. [C3]

The early recreation and the final original-code port must remain separate in future reports. Original special pieces, modes, animation behavior, and score logic are substantially safer to preserve through original execution than to infer from a small successful demo.

### Remaining runtime responsibilities

The native host/runtime supplies old UIKit/Foundation behavior, guest filesystem access, audio, graphics, events, and lifecycle. Translating the game and support libraries removes an instruction-interpreter dependency, not the need to bridge those services. Elimination of the entire layer would require replacing these contracts or rewriting the app.

### Frame rate

Chuzzle’s update function discards its float argument and invokes one fixed game tick. Calling it 120 times per second doubles gameplay speed. An experiment rendered extra frames while retaining 60 updates, temporarily selecting a guarded no-op update slot on intermediate draws. It did not create intermediate animation poses. The final choice was 60 Hz. [C7, C8]

This is a strong rule for future work: separately measure timer callbacks, actual simulation updates, render submissions, display-link callbacks, and visible animation progress. Never market a doubled callback rate as doubled animation quality.

### Lifecycle and saves

The old host mapped resign-active to termination. Opening Control Center could therefore end the process. The replacement lifecycle queues transitions, cancels touches, pauses guest timers and audio, keeps host event handling available, rebases deadlines on resume, and makes duplicate transitions harmless. Actual backgrounding calls the original save routine with the current game object and synchronizes defaults without invoking destructive Quit/termination behavior. A bounded background task supports the checkpoint. This preserves suspension and cold-launch Continue behavior; it does not prevent later OS eviction. [C7]

Atomic Foundation writes also required real atomic replacement rather than truncating the old file before the new contents were safe. The current `NSData` path delegates atomic writes through guest-filesystem validation to the replacement helper and updates the filesystem node only after success. Save correctness is ordinary user-data behavior, not merely diagnostic infrastructure. [C9]

### High-resolution performance

The retained rendering notes describe an M4 iPad Pro in More Space mode with a 2400×3200 reported backing surface. An integer 7× target is 2240×3360, presented into a centered 2133×3200 viewport. Physical panel size alone would have selected the wrong budget. The launch-time scale has an 8× cap. [C8]

A copy-based high-resolution candidate ran at roughly 27 FPS. Texture-backed presentation avoided per-frame full-screen copying. A documented 70-second sample measured 59.9 updates/submissions and 59.91 display-link callbacks per second after excluding the first interval. This is a specific measurement, not a guarantee across devices or a physical scanout measurement. Linking the current SDL archive before the Rust archive also prevented stale bundled SDL objects from undermining incremental changes. [C8]

## 5. Koi Pond case study

### Fix the offscreen pipeline before increasing resolution

The apparent zoom bug was not simply a presentation rectangle problem. Koi renders the bed, fish, and shadows into an empty texture, then samples it during water distortion. The viewport was being scaled while the offscreen attachment retained its old dimensions. This cropped the intermediate scene and magnified it in the water pass. [K4]

The retained fix scales level-zero empty texture allocations for this specific bundle; image uploads with non-null pixel data keep their original sizes. Scaling every uploaded texture would corrupt asset data assumptions. Power-of-two render scales 1/2/4/8 are used for this app’s render-target constraints. Those constraints must not be generalized to Chuzzle’s integer-scale policy. [K4, K5]

Diagnosis should inspect dimensions at each stage: logical scene, offscreen color attachment, depth/stencil attachments where applicable, viewport, scissor, sample coordinates, final drawable, and host backing scale. A correct final viewport cannot repair an already-cropped intermediate pass.

### Original versus enhanced timing

The original timer fires at 24 Hz while much of the simulation advances by a fixed 1/30-second step. Enhanced modes preserve the historical speed by scaling from the actual original cadence rather than “correcting” it to an assumed 30 Hz baseline. Guarded data variants change timer constants and per-step coefficients. [K6]

With `r = 24 / targetFPS`, the current patch scales fixed steps and linear ramps by `r`, water spring strength by `r²`, damping exponentially, and random acceleration by `r^1.5`. A smoothing coefficient becomes `1 − 0.93^r`; water velocity damping becomes `0.96^r − 1`. These model the original behavior more closely at new timesteps but are explicitly not bit-identical simulations. The 24 FPS mode remains the reference behavior.

### Dragging and ripple energy

A timing patch alone did not fix touch interactions. At 120 FPS, dragging a lily pad or finger injected more disturbances. Slow drags looked closer between modes, helping distinguish repeated event injection from a uniform amplitude error. [K7; historical user comparison, not publicly attached]

The current production helper maintains timing per touch slot. Original touch-down strength 2 remains unchanged. Repeated move strength 1 is multiplied by `clamp((now − previous) × 24, 0, 1)` in enhanced mode. Non-touch slots used by rain/fish/food retain their strengths. Sparse events are not amplified; positions still update at full input rate. Tests exercise 24/60/120/240 Hz streams, irregular intervals, independent fingers, new touches, original mode, and untouched non-touch impulses. [K7]

This is an app-specific normalization rule, not a universal input formula. A new game may require distance-based impulses or a different time model. Preserve the distinction between one-shot events, sustained forces, positions, and per-event impulses.

### Sleep timer

The original timer expiration follows a path that destroys the game and then exits. Merely suppressing `exit` leaves destroyed state. The fix intercepts the exact guarded expiration branch before destruction, retains the game, and releases native sleep prevention. Native touches restore keep-awake and audio while forwarding input so the original timer resets normally. Foreground callbacks preserve the expired policy instead of unconditionally disabling Auto-Lock again. [K8]

The original quadratic audio fade is bridged with existing source gain accounted for, avoiding double attenuation. The documented accelerated UI tests used separate test IPA copies with a shortened minutes-to-seconds constant; production kept 60 seconds per minute. Tests passed at 24 and 120 FPS, but physical Auto-Lock timing was not separately measured. This implements “allow the system to sleep,” not an immediate private screen-lock command.

### Audio, vibration, icons, and rejected experiments

Interruption/resume must restore audio-session and source state, not just restart visuals. The current AudioServices shim forwards the legacy vibration sound ID to native iOS; actual haptics depend on hardware and system policy. Do not infer vibration on iPad or claim that every fish interaction triggers it without tracing the guest call. [K9]

The original info button was supplied by UIKit rather than necessarily bundled game art. Recovering a historical system asset and using a stylistically compatible help icon can improve fidelity, but an extracted system image is not automatically an unrestricted distribution asset. Editable Icon Composer documents were retained independently of original iTunesArtwork/home-screen icon differences.

The user rejected both an expanded logical-height pond and attempted asset upscales. The final approach preserves the original simulation canvas; the later optional fill mode uniformly crops that canvas rather than extending the simulated world. Higher rasterization resolution and higher-resolution source imagery are separate interventions. The unsuccessful upscale experiment should not be presented as a shipped enhancement.

## 6. Skee-Ball case study

### Restore the original engine before replacing it

The practical port executes original ARMv7 Unity/game code through the interpreter. Work included Objective-C method lookup/replacement and bridges for startup swizzling; internal executable-symbol lookup for Mono P/Invoke; bundle/filesystem queries; table/toolbar state; default pthread attributes; and selected Foundation services. OpenGL extension reporting was narrowed to supported behavior so Unity would not choose nonexistent extension entry points. These were targeted compatibility implementations, not complete Apple-framework replacements. [S1]

CPU support expanded around observed instructions, including swap/exclusive operations, selected ARM/Thumb arithmetic and bitwise operations, and NEON operations. The SWP regression harness compiles production CPU source and recorded 116 cases per configuration. Passing those tests is evidence for those operations, not a complete ARM conformance claim. [S1, S3]

### Disable retired services narrowly

Plus+ entry points were disabled only with user authorization and symbol/prologue guards. Later lifecycle failures showed why suppressing a visible login button was insufficient: the SDK’s load-time hooks and workers remained alive. Nil-returning singleton patches, startup/lifecycle suppression, and limited selector workarounds removed the obsolete paths while retaining local gameplay. Original IPA bytes were preserved; some patches apply to loaded guest memory. [S1]

Do not fabricate successful purchases, rewards, account state, or network responses. Preserve local contracts needed by the game and report unavailable online features honestly.

### Saves and memory failures

The Security compatibility implementation persists supported generic-password queries in a guest Documents plist. It serves this game’s inventory/ticket storage; it is not native secure Keychain storage and must not be reused for sensitive credentials. Sibling ports retain independent identifiers and containers. Debugging ticket injection was explicitly requested by the user and is not a production default. [S1, F1]

End-of-round and popup crashes exposed memory-mapping semantics. Mono/Boehm GC can replace subranges covered by adjacent anonymous mappings. Coverage must consider the union of compatible intervals, not require one map to contain the whole range. Separately, a non-fixed allocation hint can point to a free address whose following gap is too small. Both `AddressUnavailable` and `NoSpace` require retry elsewhere for non-fixed requests. Fixed-address behavior is not relaxed indiscriminately. [S1, S4]

The retained implementation is limited: it is not general overlapping MAP_FIXED support or a full page-protection implementation. This limitation belongs with any transferred patch.

### Performance without translating more gameplay

Fast Unity repaint requests were delayed by 16 ms run-loop polling. Reducing active polling to 2 ms helped reach near-60 presentation throughput; inactive handling remains slower. Audio production must not inherit that fast graphics cadence: packet accumulation of at least 10 ms and an eight-buffer queue limit prevented audio-buffer exhaustion. AudioUnit pause/resume and OpenAL context/session restoration were needed across backgrounding. [S1]

At 1280×2784, the copy-based presentation path measured a median 25.625 FPS in one short sample. Direct texture-backed rendering improved a later sample to median 59.565 FPS. The first direct-texture attempt was visibly wrong because Unity reused texture name 1 and replaced a host drawable texture with a 4×4 texture. A separate high-number host texture range resolved this app’s collision; that reservation is not a general namespace-virtualization design. Host presentation also preserves/restores active texture selectors and additional texture-unit state. [S1]

High FPS from a blank frame is not success. Source readbacks, actual screenshots, and gameplay state were necessary to validate the optimization. Rendering became faster; original Unity code remained interpreted.

### Expanded world with preserved UI

An initial full-height logical canvas improved the 3D view but broke UI positions. The accepted hybrid distinguishes perspective scene rendering from orthographic UI: expand the perspective viewport/projection, center the original UI rectangle, and map input consistently. Later work expanded both axes and reallocated targets on live changes. The current layout helper computes a fit scale from host width/height, derives expanded world dimensions, and centers the original 320×480 UI within them. [S5]

This is a heuristic for the observed rendering conventions. It can expose awkward geometry, overlays, or menu composition and is not a universal Unity widescreen conversion. Validate all menus and interaction regions. A Home gesture guard is appropriate for repeated upward ball throws; the user requested its removal from Chuzzle and Koi Pond, where that gesture conflict was not relevant.

## 7. Skee Free case study

Skee Free inherited the working runtime, graphics, timing, memory, and offline-service changes, but remained a separate project with separate saves. All 11 initial ARMv7 offline-hook prologues matched the paid version; that evidence justified those specific transfers. It did not establish full binary or UI identity. [F1]

Free-edition SuperRewards startup still failed in URL construction. Additional guarded patches suppressed the points object’s network initializer/request and offer-wall entry points while retaining a zero-initialized local object for accessors. No rewards were fabricated. This demonstrates why sibling apps need an independent startup and runtime pass even when their engine and many symbols match.

The free edition omits Ranking and shifts the Redeem menu location. An inherited UI test opened Loot while claiming to validate prize redemption. Correcting the navigation and inspecting screenshots was essential. The final recorded device test covered gameplay, an unaffordable 2,600-ticket prize, popup interaction, and menu return. Earlier sessions covered a completed round and background/resume. A short final gameplay sample recorded median 59.45 FPS, not exhaustive store or thermal validation. [F1]

A stale copied-product signature appeared in an incremental Xcode signing build. A clean signing build fixed it. Use clean staging and verify the signed product; do not assume a successful earlier binary build means its copied app bundle is still validly signed.

## 8. Supplemental Skee-Ball HD findings

HD is valuable because it exposes assumptions not stressed by the iPhone siblings. Its older ARMv6 Unity transform function uses FPSCR LEN/STRIDE and VFP short vectors. Scalar-only execution updated X while leaving Y/Z unchanged, collapsing scoreboard glyph quads. Implementing register-bank wrapping, scalar destinations, source broadcasts, and the relevant short-vector arithmetic/moves preserved the original rendering code. The recorded regression harness covers the actual transform sequence and related cases. This fix should be transferred when the target instruction behavior requires it, not merely because an app is old. [H1]

A black-screen failure had a separate cause: frames rendered into a window not attached to the foreground UIWindowScene. GPU content was valid while the user saw a placeholder. Attach the actual drawable window, then repair geometry; a GPU capture alone does not prove visible presentation.

Additional HD changes normalized legacy BGRA uploads, rotated texture coordinates around the image center, restored color masks/texture-coordinate state, and supplied iPad identity through legacy UIDevice/sysctl/uname APIs. `uname` needed to write its result into guest memory. Device identity affected Unity prefab selection. [H1]

A 13-inch iPad shares the original 4:3 shape closely enough to conceal layout bugs. Testing an 11-inch iPad and changing window orientation gave a more discriminating test. The user confirmed the adapted layout. Historical device tests documented a completed nine-ball round, tickets/achievement, prize popup dismissal, and preserved results after backgrounding. Gameplay was generally in the mid-to-high 50s FPS, not a guaranteed 60 FPS.

## 9. Modern windows, rotation, and foldable displays

The recurring half-rounded compatibility window was not fixed solely by building with a newer SDK. The retained host configuration explicitly changes legacy fullscreen behavior starting with the recorded OS version. Once native resizing is enabled, host orientation and guest orientation must be handled separately. Original portrait coordinates can remain fixed while the surrounding window rotates or changes displays. [C10, K5]

Use current scene bounds, not a cached startup UIScreen size. Reset view transforms before changing bounds/center, then reapply presentation transforms. For uniform cropping of a 320×480 canvas:

`fit = min(W/320, H/480)`

`fill = max(W/320, H/480)`

`cropZoom = fill / fit`

UIKit can invert view transforms for `locationInView:`; ensure later normalization does not apply the inverse twice. Letterbox offsets, world expansion, scissor, and input must share one geometry model. Skee’s expanded 3D/centered UI model is distinct from Koi/Chuzzle’s uniform crop.

Test portrait → landscape → portrait, repeated rotation, fold/unfold without restart, inner/outer displays, and input after transitions. A cold launch in one orientation misses stale geometry. Native presentation resizing also does not prove render-target scale changes dynamically: Chuzzle’s retained scale is selected at launch even though presentation geometry updates afterward. [C8]

A later recorded session installed the four requested apps on a physical Duo successfully. That installation is not evidence of new on-device fold/rotation gameplay tests. Earlier user confirmations apply to the explicitly tested simulator/device sessions, not every future OS build.

## 10. Measurement and regression practice

Useful evidence combines state, pixels, timing, and persistence:

- Instruction-level tests for flags, aliases, invalid memory, short-vector lanes, and exclusive monitors.
- Pure geometry tests for original/cropped/full-world layouts, repeated sizes, and inverse touch mapping.
- Timing tests for fixed updates, stalls, irregular event rates, one-shot versus repeated impulses, and original-mode invariance.
- Guest logs and a persistent panic log, with pre/post hashes rather than an assumption that old entries are new failures.
- Real gameplay: start, several gestures, full round/level, save, relaunch, modal dismiss, background/resume, and another interaction.
- Visual checks of the actual app surface plus offscreen captures when diagnosing rendering.
- Device measurements with warm-up exclusions, sample count, resolution, refresh mode, and diagnostic settings documented.

A live host process can contain a failed guest and show black. XCTest reporting success can coexist with wrong navigation, wrong screenshots, or result-collection stalls. Assert actual outcomes: score/ball counts, dialog state, retained game state, no new panic entries, and correct input positions. Automated instantaneous drags once produced zero-distance Skee throws; gestures need realistic duration and event cadence.

Simulator tests are useful for startup, layout, determinism, and integration. They were dramatically slower for these legacy graphics paths and should not set device-performance expectations. Mute simulator output without skipping audio work, or lifecycle defects can disappear from the test. Do not leave UI testing or keep-awake processes running after the work finishes.

## 11. Build, signing, and release lessons

The public projects evolved from private workbenches with sibling dependency paths into standalone source packages. Portable projects vendor Cargo dependencies and modified SDL sources, pin the Rust toolchain, use offline locked builds after toolchain installation, and keep outputs outside File Provider-managed source trees. Original internal `CHUZZLE_` variable names persist in sibling ports; names do not establish architectural equivalence. [C2, K2, S2]

Both Debug and Release need optimized translated/interpreted Rust for practical execution. A normal Xcode Debug label is not a reason to run the entire emulated workload unoptimized. Compiler optimization level itself is app-specific: Koi’s documented completed configuration uses optimization level 1. Do not blindly change it to match another app.

Xcode’s processed Info.plist and a shell copy phase must not compete for the final root plist. Expand bundle IDs/executables from build settings, preserve compiled Icon Composer metadata, and exclude the copied root plist when appropriate. Keep editable `.icon` documents in the project. High-resolution exports of low-resolution icons do not recover lost original detail.

For public downloads, stage a copy of the app; remove signing/profile and purchase/account sidecars, including nested archive metadata; retain required assets and dependency notices; verify ARM64 device platform rather than simulator platform. Sanitizing metadata does not remove copyrighted game content or grant a new license. Removing only the bundled original IPA also does not remove derived translations. A user-supplied-input design would need explicit implementation and validation. [P1]

For new-device installs, use the correct Xcode scheme and destination with provisioning updates/device registration enabled. In the Duo installation performed in this thread, `xcodebuild -target` ignored the supplied destination and selected profiles that did not include the device. Installation failed with profile integrity errors. Switching to `-scheme` honored the destination and all four installations succeeded. Do not solve that failure by altering gameplay or repeatedly reinstalling the same improperly provisioned artifact.

Keep private signing data, device identifiers, raw notifications, saves, and test media out of public source. Release documentation should describe what actually ships and distinguish signed private test builds from unsigned downloadable IPAs. Preserve user-authored release notes and README prose. Historical source ZIPs are snapshots; do not silently replace them when updating documentation.

## 12. Transfer matrix

| Technique | Transfer potential | Prerequisite and main caution |
| --- | --- | --- |
| Mach-O/provenance inventory | Broad | Inventory the exact input and all relevant slices |
| Static opcode specialization | Conditional | Supported semantics, guarded inputs, manageable code size, library coverage |
| Interpreter fallback as development oracle | Conditional | Keep comparison instrumentation separate from shipping execution claims |
| Atomic write implementation | Broad runtime fix | Preserve guest permissions and replacement/error semantics |
| Lifecycle/audio state machine | Broad structure | Correct delegate order, app-specific saves, all active audio APIs |
| Texture-backed presentation | Broad optimization | Attachment lifecycle, guest texture names, complete graphics-state restoration |
| Koi empty-target scaling | Narrow current patch | Known render-target purpose; never scale arbitrary image uploads |
| Koi 24 Hz touch budget | Narrow current patch | Identified event strengths/slots and comparable dynamics |
| VFP short-vector semantics | CPU-level candidate | Evidence the target executes these instructions; production-source tests |
| Unity expanded world/centered UI | Narrow rendering heuristic | Perspective/orthographic behavior and all input/menu paths validated |
| Retired SDK suppression | Binary-specific | User intent, symbols, byte guards, return semantics, local state preservation |
| Non-fixed mmap hint retry | Broad semantic fix | Do not relax MAP_FIXED or hide true exhaustion |
| Scene attachment/live geometry | Broad host fix | Multiple windows, active scenes, coordinate mapping, target recreation |
| Home gesture deferral | Product-specific | Keep for throw gestures; avoid imposing it on unrelated apps |
| Settings resolution/FPS controls | Broad interface pattern | Default policy, original reference mode, restart versus live behavior explicit |

## 13. Proposed structure for the later skill

The final skill should be assembled after the other reports arrive. A useful structure is:

1. Intake and source-evidence template.
2. Execution-strategy decision tree and definitions.
3. Compatibility investigation loop with crash/log capture.
4. Static-translation adapter and interpreter adapter, separately gated.
5. Rendering-resolution and state-restoration checklist.
6. Timing/input normalization checklist.
7. Lifecycle, audio, storage, and offline-service checklist.
8. Device/scene/rotation test matrix.
9. Reproducible build, signing, packaging, and attribution workflow.
10. App-specific reference cases and regression harnesses.

Each reusable fix should carry: symptom, triggering workflow, exact input identity, root cause, changed layer, guarded assumptions, maintained implementation location, regression procedure, observed result, limitations, rollback, and candidate transfer targets. Preserve both failures and successful outcomes; a patch without its failed counterexample is easy to misuse.

Acceptance gates should prevent the following shortcuts: calling pseudocode recovered source; calling asset viewers playable ports; calling ARM64 hosts fully native games; accepting a black but alive guest; claiming 120 FPS from timer callbacks alone; copying binary offsets between siblings; disabling safety checks to bypass incomplete semantics; and treating install success as a gameplay test.

## 14. Gaps to resolve when merging other reports

The present work does not establish a general automated translator for arbitrary stripped iOS binaries, full ARM/NEON conformance, general Unity widescreen behavior, or exhaustive Foundation/UIKit implementations. It also does not provide controlled long-duration thermal benchmarks or full parity testing of every mode and prize.

Compare other app reports on exception handling, Objective-C ABI details, memory ownership, threading, storage migration, audio interruptions, imported engine versions, generated code size, clean-build time, and deterministic reference execution. Identify repeated fixes implemented differently across forks before designing a shared runtime. Deduplicate by semantics and tests, not file similarity or inherited project names.

Old status files and README copy can contain stale defaults or copy/paste mistakes. For example, some Skee sibling README Settings paths still name Skee Free. Such wording is not implementation evidence. Current source, manifests, named test results, and actual artifacts should decide the merged skill’s claims. No app source, releases, or repositories were changed to produce this report.

## 15. Source index

Public implementation references below point to the original snapshot commits. Entries marked historical/private were reviewed for the original report but are unavailable to readers; they are not independently reproducible public test evidence. Historical status records can contain superseded entries.

- **C1** — [Current Chuzzle architecture and features](https://github.com/DylanMcD8/respring-chuzzle/blob/db11d651554ba212b90ce7d71306b8f6835740fc/README.md)
- **C2** — [Chuzzle build, execution, and packaging](https://github.com/DylanMcD8/respring-chuzzle/blob/db11d651554ba212b90ce7d71306b8f6835740fc/BUILDING.md)
- **C3** — Historical Chuzzle recreation and asset analysis — historical/private evidence; not published
- **C4** — [Static game translation generator](https://github.com/DylanMcD8/respring-chuzzle/blob/db11d651554ba212b90ce7d71306b8f6835740fc/OriginalPort/generate_native.py)
- **C5** — [Chuzzle generation statistics](https://github.com/DylanMcD8/respring-chuzzle/blob/db11d651554ba212b90ce7d71306b8f6835740fc/OriginalPort/native-manifest.json)
- **C6** — [Translated execution and optional reference interpreter](https://github.com/DylanMcD8/respring-chuzzle/blob/db11d651554ba212b90ce7d71306b8f6835740fc/OriginalPort/compatibility-core/src/cpu/interpreter/mod.rs)
- **C7** — Historical timing experiment and lifecycle implementation — historical/private evidence; not published
- **C8** — [Final rendering and timing policy and measurements](https://github.com/DylanMcD8/respring-chuzzle/blob/db11d651554ba212b90ce7d71306b8f6835740fc/docs/RENDERING.md)
- **C9** — [Guest filesystem atomic-write routing](https://github.com/DylanMcD8/respring-chuzzle/blob/db11d651554ba212b90ce7d71306b8f6835740fc/OriginalPort/compatibility-core/src/fs.rs)
- **C10** — Chuzzle window adaptation history — historical/private evidence; not published
- **K1** — [Koi execution and features](https://github.com/DylanMcD8/respring-koi-pond/blob/e48afd82a3b047edeb7a221851e6f15d5e5d9264/README.md)
- **K2** — [Koi build and test entry points](https://github.com/DylanMcD8/respring-koi-pond/blob/e48afd82a3b047edeb7a221851e6f15d5e5d9264/BUILDING.md)
- **K3** — [Koi generation statistics](https://github.com/DylanMcD8/respring-koi-pond/blob/e48afd82a3b047edeb7a221851e6f15d5e5d9264/OriginalPort/native-manifest.json)
- **K4** — [Koi offscreen texture scaling](https://github.com/DylanMcD8/respring-koi-pond/blob/e48afd82a3b047edeb7a221851e6f15d5e5d9264/OriginalPort/compatibility-core/src/frameworks/opengles/gles_guest.rs)
- **K5** — Koi scene and cropped presentation changes — historical/private evidence; not published
- **K6** — [Guarded timing coefficients and frame-rate variants](https://github.com/DylanMcD8/respring-koi-pond/blob/e48afd82a3b047edeb7a221851e6f15d5e5d9264/OriginalPort/patch_framerate.py)
- **K7** — [Production per-touch disturbance normalization](https://github.com/DylanMcD8/respring-koi-pond/blob/e48afd82a3b047edeb7a221851e6f15d5e5d9264/OriginalPort/compatibility-core/src/cpu/interpreter/koi_touch_timing.rs)
- **K8** — Sleep timer root cause and recorded validation — historical/private evidence; not published
- **K9** — [Native vibration forwarding](https://github.com/DylanMcD8/respring-koi-pond/blob/e48afd82a3b047edeb7a221851e6f15d5e5d9264/OriginalPort/compatibility-core/src/frameworks/audio_toolbox/audio_services.rs)
- **S1** — Chronological Skee-Ball findings and measurements — historical/private evidence; not published
- **S2** — [Current Skee-Ball interpreter build](https://github.com/DylanMcD8/respring-skee-ball/blob/fbcf52c3851857a83f5748dbed3ce460c060e69c/BUILDING.md)
- **S3** — [Production CPU semantic regression harness](https://github.com/DylanMcD8/respring-skee-ball/blob/fbcf52c3851857a83f5748dbed3ce460c060e69c/CompatibilityProbe/Tests/check_swp.py)
- **S4** — [Guest memory-map semantics](https://github.com/DylanMcD8/respring-skee-ball/blob/fbcf52c3851857a83f5748dbed3ce460c060e69c/CompatibilityProbe/compatibility-core/src/libc/sys/mman.rs)
- **S5** — [Live world dimensions and centered UI viewport](https://github.com/DylanMcD8/respring-skee-ball/blob/fbcf52c3851857a83f5748dbed3ce460c060e69c/CompatibilityProbe/compatibility-core/src/frameworks/opengles/skee_layout.rs)
- **F1** — Free-edition differences and recorded device tests — historical/private evidence; not published
- **H1** — HD-specific CPU, scene, identity and validation findings — historical/private evidence; not published
- **P1** — Internal distribution and evidence rules — historical/private evidence; not published

Public companion: [source manifest](../skills/restore-legacy-ios-apps/references/source-evidence.json). The original private evidence index is excluded.
