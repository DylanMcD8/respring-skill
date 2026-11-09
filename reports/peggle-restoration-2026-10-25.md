# Peggle and Peggle HD: engineering findings and reusable lessons
Research report for a future legacy-app restoration AI skill
Snapshot: 25 October 2026

> Public edition prepared 9 November 2026 from the 25 October 2026 report. Historical test results were not rerun for this edition. Private workspace references were removed or replaced with pinned public source; private evidence remains explicitly unavailable. Original app identifiers and technically relevant device models are retained. No personal saves, credentials, device identifiers, raw logs or test media are included. This review does not establish exhaustive game parity.

## Topic index

- [Purpose and how to use this report](#purpose-and-how-to-use-this-report)
- [1. PROJECT IDENTITY AND VERIFIED SNAPSHOT](#1-project-identity-and-verified-snapshot)
- [2. ARCHITECTURE: WHAT ACTUALLY RUNS](#2-architecture-what-actually-runs)
- [3. BASELINE DISCIPLINE AND THE HD-TO-PHONE PORT](#3-baseline-discipline-and-the-hd-to-phone-port)
- [4. PERFORMANCE FINDINGS AND THEIR EVIDENCE LIMITS](#4-performance-findings-and-their-evidence-limits)
- [5. STARTUP OPTIMIZATION WITHOUT CHANGING GAME SPEED](#5-startup-optimization-without-changing-game-speed)
- [6. GUARDED NATIVE HELPERS: CONTRACT AND FALLBACK](#6-guarded-native-helpers-contract-and-fallback)
- [7. EXPERIMENTS THAT MUST NOT BE MISTAKEN FOR SHIPPED IMPROVEMENTS](#7-experiments-that-must-not-be-mistaken-for-shipped-improvements)
- [8. PRESENTATION, FRAME PACING, AND HONEST FPS TELEMETRY](#8-presentation-frame-pacing-and-honest-fps-telemetry)
- [9. PHONE LAYOUT, CROP, AND MULTIPLE DISPLAY SCENES](#9-phone-layout-crop-and-multiple-display-scenes)
- [10. KEYBOARD BUG: REAL INPUT FOCUS VERSUS LEGACY SCREEN IDENTITY](#10-keyboard-bug-real-input-focus-versus-legacy-screen-identity)
- [11. LAUNCH IMAGE ORIENTATION AND ORIGINAL ASSET HANDLING](#11-launch-image-orientation-and-original-asset-handling)
- [12. PEGGLE NIGHTS: ENTITLEMENT AND THEME ARE DIFFERENT STATE](#12-peggle-nights-entitlement-and-theme-are-different-state)
- [13. NATIVE SAVE-FILE MANAGEMENT UI](#13-native-save-file-management-ui)
- [14. TEXT REVIEW AND USER-FACING TERMINOLOGY](#14-text-review-and-user-facing-terminology)
- [15. LOCAL SAVE-FILE MODEL AND TRANSACTIONAL IMPORT](#15-local-save-file-model-and-transactional-import)
- [16. PHONE AND HD SAVE FORMATS: WHAT MATCHES AND WHAT DOES NOT](#16-phone-and-hd-save-formats-what-matches-and-what-does-not)
- [17. CANONICAL SYNC DOCUMENT: CONTROLLED SEMANTICS](#17-canonical-sync-document-controlled-semantics)
- [18. THE CHECKPOINT BUG: WHY CORRECT PROFILE MERGE WAS NOT ENOUGH](#18-the-checkpoint-bug-why-correct-profile-merge-was-not-enough)
- [19. IN-GAME USERS AND AUTOMATIC APPLICATION](#19-in-game-users-and-automatic-application)
- [20. PERSONAL CLOUDKIT TRANSPORT AND CAPABILITY DETECTION](#20-personal-cloudkit-transport-and-capability-detection)
- [21. PUBLIC ICLOUD DRIVE FOLDER TRANSPORT](#21-public-icloud-drive-folder-transport)
- [22. ANDROID SAVE-FILE RECOVERY CASE](#22-android-save-file-recovery-case)
- [23. BUILD REPRODUCIBILITY AND CACHE TRAPS](#23-build-reproducibility-and-cache-traps)
- [24. REPRODUCIBLE COMMAND COOKBOOK](#24-reproducible-command-cookbook)
- [25. TEST MATRIX AND WHAT WAS ACTUALLY ESTABLISHED](#25-test-matrix-and-what-was-actually-established)
- [26. PUBLIC REPOSITORIES, LICENSING, AND RELEASE INTEGRITY](#26-public-repositories-licensing-and-release-integrity)
- [27. DISK CLEANUP AND WORKSPACE AUTHORITY](#27-disk-cleanup-and-workspace-authority)
- [28. COLLABORATION, DEVICE PERMISSIONS, AND LONG-RUN WORK](#28-collaboration-device-permissions-and-long-run-work)
- [29. REUSABLE DIAGNOSTIC CASES](#29-reusable-diagnostic-cases)
- [30. INPUT FOR THE FUTURE MULTI-APP AI SKILL](#30-input-for-the-future-multi-app-ai-skill)
- [31. SOURCE AND EVIDENCE INDEX](#31-source-and-evidence-index)
- [Report validation](#report-validation)


## Purpose and how to use this report

This report describes the Respring work on the original iPhone Peggle 1.7.2 and
Peggle HD 2.0.9. It is source material for a separate thread that will combine
reports from several applications into a reusable AI skill. It is not the skill
itself, a claim that every legacy app can use these techniques, or a replacement
for the repositories' build instructions.

The most transferable result is a method: retain an established working runtime,
identify a specific incompatibility or measured bottleneck, change the smallest
responsible layer, compare against the original behavior, and distinguish local
correctness from real-device and service-level validation. The project also
demonstrates why packaging, input focus, save-file semantics, and signing deserve
the same attention as the interpreter.

Evidence labels used below:

```text
SOURCE: verified in the maintained source snapshot or its tests.
RECORD: documented in retained development or release validation records.
OBSERVATION: user/device observation; not necessarily a controlled benchmark.
RECOMMENDATION: a reusable practice inferred from this work.
LIMIT: an unverified claim, incomplete experiment, or boundary of coverage.
```

Some early HD records are no longer available at their original paths. The
October 22 HD handoff was requested historically but could not be located during
this report's preparation. Its baseline instructions survive in the conversation;
the later phone inheritance inventory and maintained source provide independent
evidence for the retained runtime. Missing historical benchmark data is not
reconstructed or replaced with invented performance numbers.

This report contains no private provisioning profiles, device identifiers,
credentials, or actual player save-file contents. The companion source manifest
identifies public source files and their hashes. The applications, READMEs,
graphics, and user-facing strings were not modified to prepare this report.


## 1. PROJECT IDENTITY AND VERIFIED SNAPSHOT

Application             Original guest                 Public release
Peggle                   iPhone 1.7.2                   revision-2
Peggle HD                iPad 2.0.9                     revision-3
Both host builds         54.1024.22

Peggle guest identity: com.popcap.Peggle, build 4824.14.07.16.01.
HD guest identity: com.popcap.ios.PeggleHD, build 4840.14.07.16.01.
Host bundle identifiers are separate and may change with signing/distribution.
Do not confuse the original game version, host build number, release revision,
candidate label, and signed installation identity.

Pinned source repositories:

```text
Peggle:
https://github.com/DylanMcD8/respring-peggle/tree/8f6629c3c1860bc9bc3902f3ff50d86a53373ee0
Peggle HD:
https://github.com/DylanMcD8/respring-peggle-hd/tree/fde8b99a34f2f1cb57ea59af2a4a722667578abd
```

These commits, rather than a moving branch or the user's in-progress README,
define this report's source snapshot. The companion manifest gives a direct
commit-pinned URL for each selected source file in both repositories.

The latest public artifacts are unsigned ARM64 iOS IPAs with public folder-based
sync. Separate personal builds retain properly provisioned CloudKit support.
They use the same game compatibility work but different sync configuration.
The iPhone 18 Pro installation performed while preparing this report used the
personal Peggle build 54.1024.22. Installation success is not a gameplay or
CloudKit synchronization test on that device.

This report concerns iOS compatibility applications, not ports of desktop editions. The shipped iOS hosts do not require Rosetta:
their native ARM64 code interprets an ARMv7 iOS guest and calls selected guarded
native helpers. Do not generalize that into a result for unrelated Mac binaries.


## 2. ARCHITECTURE: WHAT ACTUALLY RUNS

SOURCE: The implementation combines a modified touchHLE compatibility core in
Rust, a UIKit/Objective-C host, modified SDL2, OpenGL ES integration, and original
game executable/assets treated as input data. It is not a SwiftUI rewrite of
Peggle, a source port of PopCap's complete game, or a whole-program AOT build.

Conceptual execution path:

```text
UIKit scene and host settings
  -> native save-file management / optional automatic sync preparation
  -> exclusive approved guest data-root lease
  -> Rust entry point and compatibility environment
  -> ARM/Thumb interpretation plus HLE frameworks
  -> selected, version-guarded native routines
  -> guest graphics/audio/input through host implementations
  -> SDL/UIKit drawable presentation on the actual window scene
```

The game remains responsible for its own gameplay, menus, user creation, and
assets. The wrapper supplies compatibility, display policy, save-file management,
sync transport, modern host UI, and selected acceleration. Guest networking is
disabled in the documented entry path; this is not a restoration of the original
online service ecosystem.

The compatibility baseline includes recursive dynamic-library loading,
libgcc/C++ exception and unwind support needed by the observed game paths,
memory/thread/synchronization/filesystem behavior, and HLE framework fixes.
Inherited correctness work also covers audio pitch/rate ABI handling, wide-string
and UTF-32 behavior, time/replay handling, GL state/context ownership, texture
sharing, touch cancellation, keyboard entry, rotation, and lifecycle behavior.
RECORD: These were inherited from the finished HD baseline. This is not proof
that every theoretical exception path or framework API has been implemented.

Key source groups:

```text
Compatibility/ios/main.m
Compatibility/ios/rust-entry/src/lib.rs
Compatibility/compatibility-core/src/environment.rs
Compatibility/compatibility-core/src/dyld.rs
Compatibility/compatibility-core/src/frameworks/
Vendor/SDL2/src/video/uikit/
```


## 3. BASELINE DISCIPLINE AND THE HD-TO-PHONE PORT

Historical scope decisions:

```text
C54: established gameplay and wrapper baseline.
C59: separately preserved practical candidate; conservative retained choices.
C62-C64: diagnostic expanded-AOT experiments.
C64: compiler stopped; full-corpus validation never completed; no meaningful
     end-to-end AOT improvement established. Broad AOT was not resumed.
```

RECORD: The iPhone 1.7.2 port was made from the complete finished HD 54.1022.5
runtime and wrapper, rather than layering a few recent optimizations onto an
earlier phone prototype that had only reached a title screen. A historical
file-by-file inheritance inventory recorded 2,271 identical files, 59 adapted
files, and only a missing Finder .DS_Store. These are historical baseline counts,
not the file count of today's public repositories.

This was the answer to the user's request to inherit EVERYTHING relevant from
the HD work. An explicit inventory is much stronger evidence than remembering
the most recent patches. Adapted areas included executable identity, symbols,
global addresses, instruction boundaries, return points, relocation literals,
screen geometry, bundle identity, and save-file validation.

Phone global regions were not a simple contiguous translation of HD globals.
Native vertex validation accounted for that difference. Generated phone pipeline
implementations were recorded as 295 blocks and 2,282 instructions across ten
guarded functions. These figures describe the bounded translated helpers, not
the percentage of the game converted to native code.

RECOMMENDATION: For a sibling app/version port, produce an inheritance table with
unchanged/adapted/excluded files and hashes. Re-derive binary-specific contracts.
Do not copy address constants because the games appear visually similar. Preserve
the old working baseline and record what an experimental candidate actually
proved before promoting it.

Legacy filenames and symbols containing C53, candidate numbers, CHUZZLE, or HD
remain in shared code. Read the effective initialization path before interpreting
those labels as current feature state, app identity, or build provenance.


## 4. PERFORMANCE FINDINGS AND THEIR EVIDENCE LIMITS

OBSERVATION: The user reported substantially faster startup after the practical
startup work. The user also reported gameplay, including aiming and shooting,
often near 120 FPS on a ProMotion iPad while menus fell near 60 and the statistics
screen into the 50s. Several later changes were not visibly better, although the
user did not observe a regression. These are useful symptoms, not controlled
benchmark tables.

Why a visually simple menu can cost more than gameplay:

```text
- Repeated interpreted text layout/glyph lookup can dominate CPU time.
- Many small draw/state operations can cost more than a larger batched scene.
- A menu may traverse empty buckets or legacy widget trees every draw.
- Frame policy, waiting, presentation, and simulation are separate clocks.
- A 60-FPS result can be a policy decision, not proof of a GPU limit.
```

These are diagnostic explanations, not proof that each was the final limiting
factor on every screen. The report does not claim the statistics menu achieved
120 FPS or that all menu performance problems were solved.

RECORD/SOURCE: Retained work includes startup loading/pacing changes, reduced
verbose diagnostics, cached GL symbol/binding lookup, direct presentation,
guarded image/math/text helpers, and bounded UI traversal helpers. A retained
font-bucket optimization is narrower than replacing the game's font system.

RECOMMENDATION: Measure separately:

```text
cold launch -> host management UI;
Play -> first guest frame;
first frame -> loaded interactive menu;
gameplay frame cadence;
individual menu cadence;
callback work, wait time, composition time, and actual presentation counts.
```
Compare identical binaries/settings, scenes, thermal state, power state, and
device orientation. Record first-run and warm-run behavior. A simulator is useful
for correctness and diagnostics but is not evidence of physical-device speed.


## 5. STARTUP OPTIMIZATION WITHOUT CHANGING GAME SPEED

SOURCE: The compatibility environment recognizes the original asset loader via
the exported LoadingThreadProcStub entry point and live guest thread state. No
guest drawable also counts as loading. This lets startup animation work yield to
the loader and restores normal cadence when the worker exits. The phone source
retains HD-named helpers but checks the phone's actual bundle identity.

The important boundary is between presentation/loading scheduling and gameplay
time. Reducing startup animation contention is not permission to change simulation
ticks, physics, ball speed, replay timing, or the meaning of guest timers.

Other retained startup work reduces expensive logging and repeated GL binding
resolution. Detailed instrumentation is optional; bounded normal diagnostics
remain available for failures and effective configuration.

RECOMMENDATION: Prefer an observable loader lifecycle signal over a fixed sleep,
a guessed number of frames, or a permanently relaxed timing limit. Verify that
the loading path exits on normal completion and that gameplay timing returns to
the established baseline. A change that only makes the loading animation smoother
may still delay actual readiness; measure readiness explicitly.


## 6. GUARDED NATIVE HELPERS: CONTRACT AND FALLBACK

SOURCE/RECORD: Acceleration is selective. Retained helpers cover matrix math,
endpoint indexing/comparison, collision geometry/swap/pair construction,
glyph/kerning/mapped-character lookup, empty font buckets, PNG allocator/zlib
integration, bounded inflate loops, PNG row filters, premultiplication, pixel
packing, JPEG YCC/IDCT, a GIF island, vertex packing, clipping, and selected
UI/loading/pipeline routines.

A safe helper needs more than a matching return value. The contract can include:

```text
exact executable identity and original instruction bytes;
ARM/Thumb and IT-state expectations;
entry/return address and calling convention;
general registers, CPSR, extension registers, and FPSCR where relevant;
guest memory reads/writes and permitted aliasing;
stack bounds and overlap checks;
instruction budget / retired instruction accounting;
error/fallback behavior and code-cache invalidation.
```

SOURCE: Native batch validation captures CPU state and touched memory, exercises
a synthetic corpus, and compares original execution with native execution on
real inputs. The active UI/loading subset is nine routines from a larger set of
15 prototypes. Compiling a routine does not mean the production path uses it.

SOURCE: The empty ImageFont bucket helper does not retain font/image ownership
or perform the final drawing. It walks a bounded empty region and stops before
real draw work. It checks code, mapped memory, stack overlap, execution state,
and available instruction budget. It predicts register/flag/memory effects and
instruction retirement. The first 64 checks for each of two exit classes and
periodic checks every 4,096 calls compare behavior; mismatches disable the path.
These thresholds describe this implementation, not universal tuning constants.

RECOMMENDATION: Build a helper in this order:

```text
1. Identify the expensive routine with a trace and original disassembly.
2. Describe the complete input/state/memory contract.
3. Retain an original execution path and deterministic fallback.
4. Verify byte identity before installing a trampoline.
5. Test synthetic edge cases, including aliasing and degenerate sizes.
6. Shadow-check real inputs before trusting the helper.
7. Measure net benefit including guards, copies, and validation overhead.
8. Disable on mismatch and preserve actionable bounded diagnostics.
```

Do not hide a mismatch by expanding tolerances without understanding it. Do not
assume a microbenchmark win survives frequent guest/host transitions. If a
bounded interpreter traversal is already cheap, the validation boundary can
cost more than the work it replaces.


## 7. EXPERIMENTS THAT MUST NOT BE MISTAKEN FOR SHIPPED IMPROVEMENTS

Whole inflate_fast: remains disabled by the conservative runtime default.
Guarded smaller inflate/LZ-copy work remains. Historical real-input failure of
the larger path is a reason to preserve the working smaller path.

Copy ring: the runtime-settings table alone is misleading. The current entry
point explicitly sets PEGGLE_HD_COPY_RING=0 before settings initialization,
preserving the single-buffer transfer path. Report effective behavior, not a
default constant found in isolation.

Six higher-overhead UI prototypes: retained original interpreted paths rather
than promoting all generated helpers. The existence of generated code is not
proof of production use or a speed improvement.

Later font-setup, TexBlt, timing-instrumented, and JIT/security experiments:
the retained port inventory identifies them as excluded from the practical
baseline. It does not supply enough surviving measurements to quantify each
experiment's failure. Do not invent individual speedup/regression percentages.

C62-C64 expanded AOT: paused diagnostic work, not a validated shipping pipeline.
Compiler completion, corpus correctness, and end-to-end speed were not all
established. The user explicitly preferred finishing the practical app.

RECOMMENDATION: Maintain a rejected/paused experiment ledger containing hypothesis,
baseline, code/configuration, correctness result, performance result, and reason
for exclusion. A future agent must not automatically resume an expensive abandoned
branch because its label sounds newer.


## 8. PRESENTATION, FRAME PACING, AND HONEST FPS TELEMETRY

RECORD: The validated direct presentation route shares textures and avoids a
per-frame CPU readback/frame copy. Historical phone diagnostics reported
640x960 with copy=false and readback=false. This does not mean all paths in the
repository are zero-copy or that copying is never needed in an emulator.

SOURCE: The wrapper's frame policy distinguishes the original 30-FPS preference
from an unlocked presentation policy. Unlocking permits up to 60 FPS or 120 FPS
on suitable displays, subject to device capability, loading, power/thermal state,
and work-time recovery. It is not a guarantee of 120 FPS on every screen.

Current policy details include:

```text
original-rate preference -> 30 FPS;
severe thermal state -> 30, elevated thermal or low-power state -> 60;
loading -> 60;
maximum refresh below 120 -> 60 (or 30 below 60);
callback work excludes credited wait time and includes composition;
a stall over 100 ms causes a recovery hold;
repeated stalls or repeated work over roughly 9.2 ms can hold 60 for longer.
```
The source also has a policy-disabled fallback and inactive behavior. These are
implementation details to inspect during diagnosis, not a public guarantee.

SOURCE: FPS overlay telemetry counts successful tagged EAGL game-buffer
submissions over a rolling half-second. It is not a physical scanout measurement.
Passive scene markers record draw routes/cadence; multiple markers may occur in
one frame, and a marker is not necessarily the uniquely visible foreground view.
CPU elapsed diagnostics are not GPU duration measurements.

The public FPS toggle was removed at the user's request. Diagnostic machinery
remains available for development. Avoid exposing internal candidate switches or
raw runtime metrics as ordinary product settings.

RECOMMENDATION: Every performance number should carry its metric definition,
device/build/settings, scene, sample duration, and limitations. Frame-rate
unlocking must not accelerate simulation. Test audio, animation, collisions,
pause/resume, and replay behavior after timing changes.


## 9. PHONE LAYOUT, CROP, AND MULTIPLE DISPLAY SCENES

SOURCE: Phone layout choices are 3.5-inch (320x480 logical portrait, 640x960
internal raster) and 4-inch (320x568, 640x1136). The original app then chooses
the assets/layout appropriate to that guest screen. This is different from
stretching the same render to fill a larger modern display.

Fill Screen applies an aspect-preserving crop/zoom to the presented drawable.
The guest still uses its selected iPhone aspect ratio, so edges can be cut off.
The permanent root, keyboard ownership, and host overlays must not be scaled
along with that GL drawable. Touch conversion and keyboard positioning must
use compatible coordinate spaces.

The 3.5-inch option is the phone default and was the user's preferred Duo layout.
Layout/crop choices are latched at guest startup; close/reopen lets the original
game rebuild resources and hierarchy. HD remains a separate guest/layout; do not
replace phone art with HD art to make its viewport larger.

RECORD: A cold launch on the Duo inner screen displayed black after Continue,
while the outer screen worked. Legacy SDL display-0/screen-identity assumptions
prevented attachment to the active inner window scene. The fix selected the
foreground UIWindowScene and used actual scene bounds for root/GL layout.
The user confirmed the corrected build worked. A related iPad Play black-screen
failure was resolved during release organization.

SOURCE: Backing-size queries bind the currently presented drawable and restore
previous GL bindings. SDL WMInfo's permanent root is deliberately not the GL
view; its colorbuffer is not the correct source for presented backing metrics.

RECOMMENDATION: Diagnose a black screen by checking, in order, guest execution,
scene attachment, key window, visible view hierarchy, current GL context,
drawable backing size, framebuffer bindings, and successful presents. A host
management screen rendering correctly does not prove the guest GL view is
attached correctly. Test cold launch on each display state, not only transitions
after a successful launch on the default screen.


## 10. KEYBOARD BUG: REAL INPUT FOCUS VERSUS LEGACY SCREEN IDENTITY

RECORD/SOURCE: The game could show its name-entry UI while no iPhone keyboard
appeared. SDL's UIKit ShowWindow path assigned input focus only when a cached
SDL screen equaled UIScreen.mainScreen. That condition can fail for the actual
scene/key window on modern multi-display configurations. SDL_StartTextInput then
has no correctly focused window.

The fix assigns SDL mouse/keyboard focus based on the actual UIWindow being key
after makeKeyAndVisible. The permanent generic SDL root owns the hidden native
UITextField, while GL child views can change without replacing that root or
reparenting the field. Native responder diagnostics report state/counts, not
entered user text.

Validation was layered:

```text
actual first-responder acceptance on the key window;
visible native keyboard in simulator;
native key taps and Return creating an in-game user;
persisted users.dat/user details inspected for the expected synthetic entry;
physical Duo confirmation from the user.
```

An automation trap: XCTest app.typeText could not target SDL's hidden input field
even when the keyboard existed. That failure was not proof the keyboard fix
failed. Actual key/button interaction plus persisted game state was the decisive
test. Some automated screenshots also had orientation/cropping limitations.

RECOMMENDATION: Separate text-entry plumbing into window focus, responder state,
native keyboard visibility, text forwarding, guest encoding, and persisted
result. Fixing one layer does not validate the others. Include Unicode/backspace/
Return and rotation in future broader coverage; this report does not claim all
possible text-input cases were exercised.


## 11. LAUNCH IMAGE ORIENTATION AND ORIGINAL ASSET HANDLING

OBSERVATION: The initial launch image appeared upside down but corrected itself
once the game started. This illustrates separate presentation paths for splash
content and guest frames. A correct gameplay orientation cannot validate the
pre-game image path. Current environment code explicitly handles interface/device
orientation differences, including the opposite landscape conventions.

LIMIT: The exact isolated historical patch and before/after image evidence for
this complaint were not located during this report. Treat the symptom and
separate-path diagnostic lesson as established; do not claim an independently
reproduced root-cause analysis from the available records.

The original assets were retained. In particular, the user asked whether 100%
and ACE ribbons were text. The retained investigation identified lettering baked
into original localized ribbon images (including Dialog_loc.txz) and separate
small ribbon images for the level selector. HD resource identifiers include
IMAGE_DLG_ACEDRIBBON, IMAGE_BLUERIBBON, IMAGE_TINYACEDRIBBON, and
IMAGE_TINYBLUERIBBON. Changing a font renderer would not redraw lettering already
present in those pixels. No ribbon assets were changed.

RECOMMENDATION: Before promising improved text quality or localization, trace
the specific element to a font/glyph path, sprite/atlas rectangle, or precomposed
image. Inspect localized assets as well as generic art. Visual similarity is
not enough to infer how an element is generated.


## 12. PEGGLE NIGHTS: ENTITLEMENT AND THEME ARE DIFFERENT STATE

RECORD/SOURCE: Nights content was already included in the original iOS payload.
The implementation did not need to copy an archive's donor Documents/Library
folders wholesale. The selected guest preference store receives the Nights
entitlement value, preserving unrelated local preferences and in-game users.

The user wanted access to Nights without the entire app adopting Nights theming.
Those concerns could be separated. A host preference controls the theme; default
is off. The theme-suppression path checks the expected executable/routine bytes
and changes a narrowly scoped in-memory presentation-flag store. Theme enabled
leaves that original code path alone. Original game input files remain unchanged.

This case is useful because a downloaded donor data directory may mix entitlement,
theme, user identity, settings, and save files. Copying it indiscriminately would
be a poor migration strategy. The minimum authorized change was isolated instead.

Boundary for a future skill: this is a version-specific finding for content the
project was explicitly authorized to restore. It is not a universal instruction
to unlock purchases in arbitrary apps. Preserve mixed-content licensing and
distinguish bundled content from content that would need separate acquisition.


## 13. NATIVE SAVE-FILE MANAGEMENT UI

SOURCE/RECORD: The management interface uses UIKit and Objective-C, not SwiftUI.
It follows the user's sketch: header illustration/title and a single header Play
button, with Import, Export, and iCloud cards. On wide layouts the three cards
have equal heights with flexible blank space; compact layouts stack them.
Headings are semibold. Accent color is #F67527.

The HEIC image supplied for the interface is distinct from the actual Icon
Composer app icon. An initial icon replacement was reverted; the original
editable Icon Composer source remains authoritative. A future agent must ask
what an asset is for rather than applying an interface illustration globally.

The scroll layout uses UIKit layout guides:
contentLayoutGuide defines scroll content height, frameLayoutGuide controls
width, the scroll view extends to the full bottom view edge, and automatic safe
area insets permit content to scroll under the bottom region without a hard cut.
Content constraints, scroll-frame constraints, and safe-area behavior are
separate decisions. Nested fixed heights can defeat this design.

The iOS 26+ header Play button uses a prominent glass style with large sizing;
older OS versions use a filled fallback. Explicit Dynamic Type sizing corrected
clipping seen in an intermediate build. The bottom duplicate Play button was
removed. New UI styles require availability checks and accessibility-size tests.

Import/export/manual operation outcomes use UIAlertController rather than
replacing explanatory UI copy with transient status messages. Successful
automatic startup sync stays quiet; immediate issues can alert. A durable last
sync/check subtitle is appropriate state, not an operation-result replacement.
Folder name occupies its own subtitle line; the enable toggle is above the
folder chooser. Detailed setup caveats live in the setup alert/help instead of
three repetitive paragraphs in the card.

SOURCE: Show Save File Management on Launch defaults to enabled. Enabling
automatic sync changes that preference to disabled for a more automatic launch;
the user can re-enable it in Settings. Errors may still require management UI.
Thus 'enabled by default' and 'not appearing after I enabled sync' are compatible.


## 14. TEXT REVIEW AND USER-FACING TERMINOLOGY

The user requested an editable inventory of all strings, where they appear, and
removal of unused strings. Review catalogs use stable identifiers, original and
replacement text, occurrence/location information, and app applicability.
Entries marked for review were to be listed and reverted to the prior wording
pending a decision. This catalog is a review artifact, not proof that all source
literals have been converted into a localized string-resource system.

Preferred terminology:

```text
'save files', not 'saves';
'in-game users', not vague 'progress slots';
explicit Adventure checkpoints, cleared/aced levels, and challenge completion
instead of a broad unexplained claim to sync all 'progress'.
```

The public iCloud card's chosen description is:

```text
Sync Adventure checkpoints, cleared and aced levels, and challenge completion
between Respring's versions of Peggle and Peggle HD.
```

The experimental qualifier belongs in the cell title/settings context as
requested, not redundantly in the in-app toggle. Future work should inspect the
actual current catalog before changing wording; this report is not a replacement
catalog or a claim that every older internal status literal was removed.

The latest empty-user error is:

```text
Start the game and create an in-game user before syncing save files.
```

This is emitted for a genuinely missing or valid-empty user index, before a
generic snapshot error. Corrupt indexes remain a distinct validation failure.
The host does not silently manufacture a user to make syncing appear successful.

RECOMMENDATION: Find literals in active code, resource plists, generated UI, and
error paths; map call sites and conditions, not merely grep counts. Remove dead
catalog entries only after checking dynamic construction. Report all user-facing
string changes at the end of development updates, as requested for this project.


## 15. LOCAL SAVE-FILE MODEL AND TRANSACTIONAL IMPORT

SOURCE: Save management has two different concepts that must not be conflated:

```text
- An in-game user is the game's own named player/profile.
- A host save-manager slot is an internal transactional data-root generation.
```
The UI should not call either one an unexplained 'progress slot'.

The guest uses Documents/userdata, including users.dat, user<ID>.dat, suspended
board files, and other game data. Preferences select the current user and carry
local configuration. Host management state lives outside the original game data
and selects an approved guest root.

Import/export supports validated backups and raw file/folder selections. Merge
and overwrite are different operations. Overwrite can restore an appropriately
validated local backup; semantic merge combines supported achievements/checkpoints
without copying unrelated fields from a foreign edition. A file containing only
scores or unfinished board state cannot serve as a semantic user merge source.

SOURCE: The manager uses an exclusive session lease to keep import/restore from
mutating live guest files. Preview tokens bind validated inputs to a pending
operation. Fingerprints and state checks detect changes between preview and
commit. New data is written into a complete staged slot before the active state
is published. Recovery receipts and the previous slot support rollback, with
fingerprint checks rather than blindly restoring a changed directory.

Validation boundaries include path allowlists, symlink rejection, regular-file
checks, archive member validation, bounded counts/sizes, and rejection of foreign
or unsupported layouts. Current manager limits include 16 MiB per file, 128 MiB
aggregate, 4,096 files, and a separate 2 MiB metadata limit. Canonical sync has
smaller limits described below. These are implementation bounds, not permission
to allocate an archive's advertised size without validating actual reads.

RECOMMENDATION: Test interrupted writes, preview/commit races, malformed archive
paths, truncated files, foreign identities, rollback after unexpected changes,
and repeated operations. The user's statement that current test save files are
unimportant permits disposable test fixtures; it does not justify shipping a
restore algorithm that corrupts other users' data.


## 16. PHONE AND HD SAVE FORMATS: WHAT MATCHES AND WHAT DOES NOT

RECORD: Disassembly comparisons found the two editions share version-25
PlayerInfo serialization semantics for the fields used by the adapters. Several
serialization routines were identical or differed in position-independent
relocations. This enabled a common semantic adapter, not a blanket assertion
that all game data directories are interchangeable.

SOURCE: The adapter walks a variable-length serialized record. It checks the
version, counts, string lengths/encoding, embedded statistics structure, and
exact end of file. It records field spans, modifies only supported fields, then
re-parses output and verifies untouched spans remain byte-identical.

Crucial distinction: labels such as 0x10 or 0x28c in the decoder are semantic
field keys derived from object layout, NOT universal byte offsets into user.dat.
Variable-length fields change serialized positions. A future agent must not
seek to those numbers in a file and overwrite bytes.

Relevant field keys in the verified adapter:

```text
Classic furthest stage/level: 0x10 / 0x14
Classic last checkpoint:     0x18 / 0x1c
Classic completion counter:  0x30
Classic trophy IDs:          0xa8
Classic cleared/aced names:  0x14c / 0x164
Nights furthest stage/level: 0x28c / 0x290
Nights last checkpoint:     0x294 / 0x298
Nights completion counter:  0x29c
Nights trophy IDs:          0x128
Nights cleared/aced names:  0xf8 / 0x110
```

The supported decoder expects version 25 and specific embedded structures.
Unknown versions/trailing data fail closed. Bundle identity, preference keys,
user selection, raw backup identity, and suspended board semantics still need
edition-aware handling. Copying one app's entire Library directory to the other
would bypass those distinctions.


## 17. CANONICAL SYNC DOCUMENT: CONTROLLED SEMANTICS

The user explicitly preferred a stable app-owned document over allowing iCloud
to manipulate live legacy files. The implementation follows that design:

```text
original local files -> validated semantic snapshot -> canonical JSON
-> transport/merge -> validated local adapter -> controlled restart.
```

SOURCE: Current documents use format 'RespringPeggleProgress', schema 2, and
scope 'adventure-progress'. Schema 1 with 'unlock-progress' is accepted as a
limited older input. Internal format identifiers retain the word progress for
compatibility; user-facing text can be more precise without renaming the format.

Top-level fields are format, schema, scope, profile_label, classic, and nights.
Each campaign includes checkpoint (nullable stage/level), furthest_stage,
furthest_level, adventure_completed, trophies, cleared_levels, and aced_levels.
Names are validated, level identifiers normalized/compared case-insensitively,
duplicates rejected, and unsupported or extra fields rejected by strict parsing.
The document limit is 512 KiB. Campaign ranges are edition-specific and checked.

Merge behavior:

```text
later checkpoint wins;
furthest stage/level wins;
completion is logical OR;
trophy IDs and cleared/aced level identifiers use set union.
```

These operations are additive, order-independent in meaning, and idempotent.
They support offline convergence much more naturally than last-writer-wins
replacement of opaque binary save files. They do NOT propagate intentional
resets/deletions or maintain independent histories for several unrelated users.
Do not advertise this as a full backup or arbitrary bidirectional file mirror.

Individual challenge completion is included through the per-challenge trophy
identifier collection. The explicit regression test is named
individual_challenge_completions_merge_independently_in_both_campaigns.
This is more precise than saying a single total trophy count is synchronized.

Local-only material includes scores/statistics not represented in the canonical
schema, user names/identity selection, display/account configuration, and opaque
unfinished board/replay state. Game Center credentials or achievements are not
recreated by copying this JSON. Original Game Center service behavior was not
restored as a new host service.

RECOMMENDATION: Define and test the semantic boundary before choosing a cloud
API. Preserve unknown local data, version the document, and make merge algebra
explicit. A future requirement for separate people, resets, or exact score
history needs a new identity/conflict model rather than a casual extra field.


## 18. THE CHECKPOINT BUG: WHY CORRECT PROFILE MERGE WAS NOT ENOUGH

OBSERVATION: One device reached a newer Adventure checkpoint while another
continued resuming an older level. Personal progress values are omitted. A canonical record could show newer completion while the game still resumed
an older serialized board. Testing only the merged JSON would miss the bug.

SOURCE: The final model distinguishes last Adventure checkpoint from furthest
unlocked level. When an incoming checkpoint advances a campaign, the adapter
updates the corresponding fields and removes that campaign's selected user's
stale suspended-board file. The next game start enters the newer level from its
beginning. If the checkpoint did not advance, the unfinished board is preserved.

Only the relevant campaign/user board is invalidated. Wholesale deletion of
userdata or all unfinished boards would be broader than necessary. Existing
field-preservation and transaction checks remain in force.

RECOMMENDATION: Identify precedence among local files. A user-detail record,
cached preference, separate resume file, and in-memory state may all represent
different layers of the apparent 'current level'. Validate the actual resumed
game after import, not only the bytes or UI summary produced by the adapter.


## 19. IN-GAME USERS AND AUTOMATIC APPLICATION

SOURCE: Automatic sync links one selected in-game user per installation. It does
not automatically match users by name across devices. Names may differ while
the linked users share one accumulated canonical campaign state. Linking another
user to the same CloudKit record or folder combines that user's supported
completion with the existing shared state; it is not a separate account slot.

If the linked user is no longer selected/available, the wrapper explains that
the user should select it or explicitly relink. Ordinary startup does not create
a synthetic user. Test fixtures are a separate concern.

During play, the compatibility run loop can capture a read-only semantic snapshot
at a safe point with no userdata writer open while retaining the session lease.
Pure JSON merging can happen concurrently with play because it does not mutate
guest files. Applying to the actual local files requires leaving the running
guest session and using the manager's controlled path.

Incoming changes while playing offer Later or Apply and Restart. Later defers
that pending document until a subsequent launch; it is not treated as rejection
or deletion. Apply and Restart uses the runtime reload mechanism. A later
checkpoint can replace an older unfinished board and start the new level over,
which the alert explains.

SOURCE: The current code has bounded startup waiting, periodic capture/checks,
retry delays, persisted pending/deferred state, linked-user checks, and epoch/
context guards. For orientation, capture eligibility is throttled around two
seconds, successful exchanges schedule another check around 30 seconds, and
failures retry around 15 seconds. These are current policy values, not claims
of guaranteed network delivery or background execution.

RECOMMENDATION: Treat automatic sync as a state machine, including disabled,
unlinked, checking, local-only, pending remote, deferred, applying, and error
states. Cancel/ignore stale completions after changing account/folder/context.
Do not label a local capture 'synced' before transport succeeds, or transport
success 'applied' while the game still has older state in memory.


## 20. PERSONAL CLOUDKIT TRANSPORT AND CAPABILITY DETECTION

SOURCE/RECORD: Personal builds use a shared CloudKit container/private database
for the same Apple Account and environment. The canonical document is stored
in a record of type PeggleProgress; the implementation retains the historical
record identifier prototype-unlocks-v1. This is a shared semantic record, not
a directory of the game's raw data files.

The build flag PEGGLE_CLOUDKIT_ENABLED=YES configures the personal route. A
matching bundle Info key alone does not establish capability. The host inspects
the installed thin ARM64 Mach-O's embedded signed XML entitlements and requires
CloudKit service, the configured container, and a recognized Development or
Production environment. Malformed/unknown layouts fail closed. Re-signing may
remove those entitlements, so capability must be checked after installation.

This parser is a capability inspection, not a replacement for OS signature trust
or a guarantee that the account/network/server schema is usable. It handles the
specific shipped executable/signature layout; it is not a universal Mach-O or
DER-entitlement reader for every app format.

Six native capability tests cover real ad-hoc signatures, absent/re-signed
entitlements, container mismatch, and malformed input. Actual provisioning still
requires a developer account/team with container access. Another developer
cannot gain access merely by copying the container string into an Info.plist.

LIMIT: Personal development-environment behavior was tested. This report does
not claim CloudKit production schema deployment or public entitlement access
was validated for arbitrary sideloading services. That constraint motivated
the separate public folder approach.


## 21. PUBLIC ICLOUD DRIVE FOLDER TRANSPORT

SOURCE: Public builds use a folder selected through the Files document picker.
The user grants access and the app stores a security-scoped bookmark. The
implementation checks that the selected directory is an iCloud ubiquitous item.
This does not silently create an arbitrary app container without user action.
Both installations must select the same intended folder.

Each installation writes `Peggle-Save-<UUID>.json` and reads/merges all recognized
files. The writer identity is excluded from device backups so a restored device
does not inherit another device's writer ownership. Public documents use a
generic profile label rather than exporting the local in-game user's name.

Why one file per installation: if two offline devices overwrite one shared JSON,
the file provider can choose a winner before the app sees both states. Separate
writers retain both contributions; additive merging converges when both become
visible. This is a simple application-level convergence protocol on top of a
file provider, not an assumption that iCloud merges JSON fields.

The native implementation:

```text
resolves and refreshes bookmarks, balances security-scoped access;
serializes folder operations and uses NSFileCoordinator;
sorts recognized files and validates each document through the Rust engine;
rejects symlinks/nonregular files, oversized or unsupported documents;
requests download of cloud placeholders and retries rather than treating them
as empty data;
merges known unresolved file versions without deleting unread versions;
re-reads its own file under the write claim before publishing;
writes atomically and skips byte-identical writes;
bounds coordination/time and discards results for an obsolete folder context.
```

Current limits: 512 KiB per canonical file, 128 recognized files, 8 MiB aggregate
read budget, up to 16 unresolved conflict versions per file, and approximately
25-second coordination/deadline controls. A malformed recognized file aborts
the exchange rather than silently publishing a partial merge.

Folder changes/disable operations do not delete other devices' files. Pending
state is scoped to the selected context. Personal and folder preference keys
are separated to avoid accidental cross-transport state reuse.

The UI must distinguish 'last checked/exchanged locally' from confirmation that
iCloud uploaded the file or another device downloaded/applied it. Files can show
'Waiting to upload' after the app successfully writes. No entitlement workaround
can force the provider to deliver immediately.

RECORD: Both test apps were signed with ordinary provisioning without CloudKit
entitlements. The Duo selected a folder, read/wrote data, enabled automatic
checks, reopened using its bookmark, and performed quiet startup/manual-alert
flows. Native tests exercised offline/concurrent writers and real coordinated
file I/O using the actual Rust merge engine.

LIMIT, STILL OPEN: The retained test session did not establish actual iCloud
Drive delivery from Duo to iPad/Mac. The test folder remained waiting to upload.
The user later authorized publication with that limitation communicated. The
release's existence is not proof that this missing end-to-end test passed.

RECOMMENDATION: A future test must create divergent supported completion on two
devices, confirm provider upload/download, exchange both writer files, restart/
apply on both, and inspect actual game state. Repeat offline, after reconnect,
and after folder reselection. Test absence of CloudKit entitlements separately
from provider availability and delivery.


## 22. ANDROID SAVE-FILE RECOVERY CASE

RECORD: The source device was a first-generation Surface Duo, unrooted, with
sideloaded Peggle 1.0 under package com.popcap.peggle. An ADB backup of the app
succeeded after the user approved Android's on-device backup prompt. Original
backup material and hashes were retained privately.

The Android users.dat index used a different header/name encoding, including
UTF-16 names. Conversion normalized the index only in a temporary working copy.
The supported version-25 user-detail record could then be interpreted by the
semantic adapter. The transfer output was the canonical JSON, not a copied
Android application data directory.

An isolated iOS-format import/export round trip verified that the recovered
supported completion survived conversion, including individual challenges and
Adventure state. Actual names/scores/counts are intentionally omitted here.
The original Android files were not mutated to make the adapter accept them.

LIMIT: This is a successful case on that installed app/device. ADB backup is not
universally available across Android versions or apps; package backup settings
and OS behavior matter. A future skill must inspect the actual device/package
and explain required OS confirmation, not promise unrooted extraction everywhere.
Never request that a user send a device passcode or backup password in chat.

RECOMMENDATION: Separate extraction, format identification, temporary conversion,
canonical export, isolated round-trip validation, and destination import. A file
with the same basename can have a different container/index encoding while
sharing useful underlying semantic records.


## 23. BUILD REPRODUCIBILITY AND CACHE TRAPS

SOURCE: Both repositories contain BUILDING.md, Xcode projects, direct build
scripts, original sanitized payload/hash inventory, vendored dependencies, tests,
package/audit scripts, icon sources, and notices. No private sibling checkout
is required by the documented public build.

Snapshot toolchain requirements: full Xcode selected through xcode-select,
Python 3.11+, Rust via rustup (documented 1.99.0), ARM64 iOS and Apple-silicon
simulator targets, CMake, and Ninja. Installing tools requires network; compilation
uses locked/offline vendored dependencies. Debug and Release use optimized Rust.
These are the repository's verified snapshot requirements, not a prediction of
the best toolchain for a later OS release.

Build in a local output path outside File Provider/iCloud-managed folders.
File coordination caused real development hangs. Separate Peggle and HD build
roots so similarly named artifacts or cached libraries cannot cross-contaminate.

An external-library trap: changes to modified SDL2 can rebuild its static archive
without Cargo noticing that sdl2-sys needs relinking. The archive hash must
invalidate the relevant Rust cache. An optional reuse witness covered a narrower
SDL source subset, so it is not sufficient after arbitrary UIKit SDL edits.
RECOMMENDATION: fingerprint all relevant source/configuration or force a clean
SDL/link rebuild after those changes; verify the resulting app, not just timestamps.

Xcode processes Info.xcode.plist; the shell build phase excludes the final root
Info.plist so two build steps do not claim the same output. Preserve Icon Composer
compiled metadata and editable sources. Paths with spaces are normal in this
workspace; CARGO_ENCODED_RUSTFLAGS and proper shell quoting avoid splitting flags.

The original ARMv7 executable is embedded as data; host code is ARM64. Packaging
reconstructs the nested original IPA after checking Original/payload-sha256.json.
Do not 'fix' architecture audits by deleting the guest executable because it is
ARMv7. Distinguish loadable host code from emulated input.


## 24. REPRODUCIBLE COMMAND COOKBOOK

These commands are taken from the maintained Peggle build layout. Run from a
verified checkout, inspect its current instructions first, and use a separate
output root for HD. They are documentation, not commands executed during this
report preparation.

Toolchain targets:

```text
rustup target add --toolchain 1.99.0 aarch64-apple-ios aarch64-apple-ios-sim
```

Simulator build:

```text
xcodebuild -project Peggle.xcodeproj -scheme Peggle -configuration Release \
  -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath /tmp/Peggle-sim CODE_SIGNING_ALLOWED=NO
```

Unsigned device build:

```text
PEGGLE_NATIVE_BUILD=/tmp/Peggle-build bash Compatibility/ios/build.sh iphoneos
python3 Scripts/package_ipa.py /tmp/Peggle-build/iphoneos/Peggle.app \
  --output release-output/Peggle.ipa
python3 Scripts/audit_release.py release-output/Peggle.ipa
```

Save-file tests:

```text
cargo test --manifest-path Tests/SaveManager/Cargo.toml --offline --locked
```

Installed-signature capability tests on Apple-silicon macOS:

```text
python3 Tests/CloudCapability/test_capability.py
```

Native folder tests with the real merge engine:

```text
cargo build --manifest-path Tests/FolderSync/Cargo.toml --offline --locked
python3 Tests/FolderSync/test_folder_sync.py \
  Tests/FolderSync/target/debug/libpeggle_folder_sync_tests.a
If CARGO_TARGET_DIR is set, pass the actual resulting library path instead.
```

Device inventory/install pattern:

```text
xcrun devicectl list devices
xcrun devicectl device install app --device <verified-device-id> <signed-app>
```

Use the actual requested device identity; an 'iPhone Duo' in the Apple toolchain
and an Android Surface Duo in ADB are not interchangeable. Verify app build,
bundle, entitlements, and provisioning-device membership before installation.
Do not print credentials or copy private profiles into public evidence.


## 25. TEST MATRIX AND WHAT WAS ACTUALLY ESTABLISHED

Historical phone inheritance validation (RECORD):

```text
45 save-manager tests;
29 font/interpreter/memory tests, one benchmark intentionally ignored;
two viewport tests;
simulator user creation, Adventure, aiming/shooting, collisions, rotation,
background/resume, menus, and real save-file export/restore/rollback;
direct presentation diagnostics and active helper guards/shadow checks.
```

Display update validation (RECORD):

```text
three Rust geometry tests and twelve C crop/touch combinations;
user-confirmed physical Duo inner/outer startup fix.
```

Current folder/keyboard release validation (RECORD):

```text
69 save-manager tests for each app, including no-user/empty/corrupt distinction;
thirteen native coordinated folder-I/O tests per source variant;
six capability tests per source variant;
device/simulator packaging and original-payload audits;
real Duo folder selection/bookmark restart/local exchange;
native keyboard entry persisted in simulator and user-confirmed Duo fix;
personal Peggle/HD and separate public folder-test installation checks.
```

Not established by these results:

```text
a complete playthrough of every Classic/Nights level and challenge;
speed equivalence on every physical iPhone/iPad;
every optional helper/input class exercising its fast path;
every keyboard/localization/accessibility case;
reliable live cross-device iCloud Drive delivery;
CloudKit production deployment for arbitrary public signing;
benefit from paused expanded AOT;
gameplay on the newly installed iPhone 18 Pro during this report task.
```

Recommended release acceptance layers:

```text
(1) compile/package integrity;
(2) deterministic unit/native boundary tests;
(3) simulator UI/lifecycle and persisted guest-state checks;
(4) physical launch/input/rotation/display checks;
(5) physical controlled performance comparison;
(6) actual service/device-to-device convergence;
(7) final uploaded artifact identity and reproducibility.
```
Passing one layer does not substitute for another. Re-run only the appropriate
layers for the change, broadening when failures or new concerns justify it.


## 26. PUBLIC REPOSITORIES, LICENSING, AND RELEASE INTEGRITY

The user requested two public repositories matching the other Respring projects,
with private development/shared materials outside them. Each public repository
is buildable independently. Shared private development artifacts can live in a
separate local directory without making the public build depend on that folder.

Mixed-content licensing matters: the host/compatibility source and dependency
licenses do not relicense the original PopCap executable/artwork/audio. Keep
notices and source attribution accurate. Do not copy another project's claim
that an app is fully AOT when this runtime is interpreted with guarded helpers.

Packaging uses a staged copy to strip host signatures, provisioning, and original
account metadata from public artifacts, without mutating source game inputs.
Original payload inventories were audited (1,318 phone entries and 798 HD entries
in the retained release checks). Historical raw-IPA hashes can differ from a
sanitized reconstructed IPA; use the appropriate inventory for the artifact.

Each current release has four assets: unsigned IPA, complete source archive,
runtime-source archive, and SHA256SUMS. The complete source archive is assembled
from tracked files because git archive/export-ignore behavior can omit vendored
files needed for an offline build. Validate tracked blob contents, modes/symlinks,
ZIP integrity, source commit identity, and asset hashes rather than assuming a
successful upload is sufficient.

The user supplies README prose, graphics, and changelog wording. Preserve those
unless explicitly asked to edit them. Wrapper build numbers and public revision
tags are separate. Previous published releases should remain reproducible.

Release case study: the .21 drafts were still unpublished when a keyboard fix
required .22. Unpublished tags were advanced with an expected-old-SHA lease.
GitHub changed draft/tag association after target updates, creating detached
untagged drafts; the actual API state was inspected and only superseded drafts
from this operation were removed. Historical published releases stayed intact.
RECOMMENDATION: freeze the final source commit before creating a release, and
inspect API state after edits. Never assume a tag edit updated every draft link.

Final release records verify the two pinned commits and all four asset sizes/
GitHub SHA-256 digests. This report did not publish or alter releases.


## 27. DISK CLEANUP AND WORKSPACE AUTHORITY

The compatibility workspace had grown to about 65 GB during iteration. Cleanup
removed unneeded build caches/obsolete packages while retaining maintained
public sources, private evidence needed for future diagnosis, original inputs,
and useful final artifacts. The user's old HD development path subsequently
was missing; the user reported not deleting it. The surviving public source
remained available. The report does not assign an unproven cause to that loss.

RECOMMENDATION: Before cleanup, classify files as authoritative source, original
input, irreplaceable evidence, released artifact, reproducible build output,
or disposable temporary material. Keep a manifest, verify replacement copies,
and update a READ-FIRST authority note. Delete specific redundant artifacts,
not a broad path based only on its size. Resolve symlinks before removal.

A project's new canonical location should be explicit. One-time retargeting
scripts can become destructive if rerun against already transformed source;
retain them as evidence and label them accordingly. A portable public build
should not depend on legacy symlinks or the original developer's absolute paths.


## 28. COLLABORATION, DEVICE PERMISSIONS, AND LONG-RUN WORK

The user repeatedly authorized development, testing, installation, and release
steps. Re-asking generic permission at each reversible step obstructed the work.
Existing task authorization should be carried forward within scope. OS/device
gates are different: locked devices, XCTest automation passcode prompts, and
Android backup confirmation require the human at the device.

When a genuine gate appears, identify the exact blocker and continue independent
preparation. Do not claim the assistant can dismiss a passcode prompt, request
the passcode in chat, or attribute a tool/platform restriction to user indecision.
The user asked to prefer simulator testing where it is suitable; physical speed
and multi-display behavior still need hardware checks.

Long-run constraints are project-specific. Honor current deadlines and keep-awake
permissions, and stop when requested. Record active compilers, test runners and
captures at handoff rather than leaving unexplained processes running.

Unrelated concurrent user work must be respected. During this report the user
was editing READMEs and graphics. Those files were left untouched. The additional
iPhone 18 Pro installation was handled without dropping the report objective.


## 29. REUSABLE DIAGNOSTIC CASES

Symptom: Startup slower than expected.
Check: Loader lifetime, animation contention, repeated binding lookup, logging.
Proven direction: Loader-aware pacing and reduced overhead; user saw faster start.
Avoid: Globally speeding guest time or declaring animation FPS the launch metric.

Symptom: Menus much slower than active gameplay.
Check: Interpreted text/buckets, draw/state-call volume, policy decisions, waits.
Proven direction: Bounded guarded helpers and honest telemetry.
Limit: No evidence all menus reached 120 FPS; broad font rewrite was not shipped.

Symptom: Black screen only on inner display / certain iPads after Play.
Check: Actual UIWindowScene, key window, drawable/backing/context, legacy screen
identity assumptions.
Proven direction: Foreground scene attachment and actual presented drawable.
Avoid: Reinstall loops, deleting save files, or changing the renderer blindly.

Symptom: Name entry visible but no native keyboard.
Check: SDL input focus and actual key window before inspecting guest text code.
Proven direction: Key-window focus, stable root/text-field ownership.
Validation: Native key taps plus persisted in-game user, not app.typeText alone.

Symptom: Sync says newer state but Resume opens an older level.
Check: Suspended board precedence, checkpoint versus furthest unlocked level.
Proven direction: Advance checkpoint and invalidate only the stale related board.

Symptom: Public re-signed app has unusable CloudKit controls.
Check: Actual installed signed entitlements, container and environment.
Proven direction: Capability gating and a separate user-selected folder route.
Avoid: Treating an Info.plist feature flag as provisioning authorization.

Symptom: Folder exchange succeeds but another device sees nothing.
Check: Files upload/download status, bookmarks, selected folder identity, provider
delivery, then semantic merge/application.
Limit: Local write success cannot establish remote delivery.

Symptom: A UIKit/SDL source fix appears absent from the new app.
Check: External static library and Cargo link cache invalidation.
Proven direction: Verify archive hash/relink and app identity, not build exit alone.


## 30. INPUT FOR THE FUTURE MULTI-APP AI SKILL

Suggested modules to synthesize from this report and the other applications:

A. Intake and provenance
Identify platform/version/architecture, original input hashes, ownership of
assets/source, known working baseline, required behavior, and explicit exclusions.
Separate original app, compatibility runtime, wrapper, and distribution identities.

B. Baseline and evidence management
Preserve a runnable baseline, inventory inherited/adapted files, label experiments,
keep a compact authoritative handoff, and distinguish recorded from inferred facts.

C. Compatibility diagnosis
Trace the exact failing ABI/framework/input/scene path before a broad rewrite.
Inspect original symbols/serialization/assets when available; validate assumptions
against runtime behavior. Do not treat two sibling versions as address-compatible.

D. Bounded acceleration
Require complete state contracts, exact byte guards, original fallback, synthetic
and real-input equivalence, and end-to-end measurements before enabling helpers.
Stop when correctness fails or the cost exceeds benefit. Keep paused AOT paused
unless the user deliberately chooses it as new scope.

E. Native shell and lifecycle
Use actual scene/key-window/drawable state, preserve keyboard ownership and
coordinate transforms, handle launch images separately, and test cold launch,
rotation, background/resume, and screen transitions.

F. Semantic save-file adapters
Map versions and precedence, retain unknown local fields, stage transactions,
separate in-game identity from host recovery slots, and verify game-visible state.
Use canonical versioned documents for cross-edition data, not opaque directory sync.

G. Sync transports
Choose transport based on installed capability, not developer-machine privileges.
Specify merge algebra/identity/reset semantics, safe capture/apply boundaries,
offline writers, stale-result cancellation, user alerts, and provider-delivery tests.

H. Packaging and publication
Build outside provider-managed caches, vendor real dependencies, invalidate native
archive caches, sanitize staged packages, preserve licenses/attribution, verify
commit/artifact identity, and retain prior published releases.

I. Product text and collaboration
Maintain string inventories, use precise terminology, keep success quiet when
automatic, explain actionable errors, preserve user-owned prose/assets, and
honor device access and time limits without repetitive approval requests.

Do NOT turn these app-specific facts into universal skill rules:

```text
Peggle version-25 field keys or campaign ranges;
exact trampolines, routine hashes, or object layouts;
a requirement that every app use UIKit/OpenGL ES/touchHLE;
the specific timing thresholds and candidate labels;
the assumption that all games' completion merges monotonically;
the assumption that ADB backup works on every unrooted Android;
the assumption that file-provider access proves cloud delivery;
the claim that selected native helpers constitute whole-program AOT;
permission to reuse original proprietary assets under the host code's license.
```

Useful questions for the other app reports:
What was the authoritative input and working baseline? Which fixes changed the
runtime versus the wrapper? What failed and why? What did physical testing prove
that simulation did not? What binary/state contracts are version-specific? What
data must remain local? Which release inputs were private? What remains unproven?


## 31. SOURCE AND EVIDENCE INDEX

Public source paths below are relative to either pinned repository in section 1.
The public source manifest linked below resolves selected files to
commit-pinned URLs with SHA-256 hashes. It includes tests and implementation,
not private logs or user data.

Build/distribution:

```text
BUILDING.md; docs/ICLOUD.md; Scripts/package_ipa.py; Scripts/audit_release.py
Original/payload-sha256.json; Compatibility/ios/build.sh
```

Host/scene/input/layout/UI:

```text
Compatibility/ios/main.m; save_manager.m; keyboard_bridge.m
Compatibility/ios/wrapper_preferences.m; phone_display_policy.h
Vendor/SDL2/src/video/uikit/SDL_uikitwindow.m
Vendor/SDL2/src/video/uikit/SDL_uikitview.m
Vendor/SDL2/src/video/uikit/SDL_uikitviewcontroller.m
Vendor/SDL2/src/video/uikit/SDL_uikitopenglview.m
```

Timing/telemetry/runtime policy:

```text
Compatibility/ios/frame_pacing_policy.c; frame_pacing.m; fps_overlay.m
Compatibility/ios/rust-entry/src/lib.rs; runtime_settings.rs
Compatibility/compatibility-core/src/environment.rs; diagnostics.rs
Compatibility/compatibility-core/src/peggle_ui_cadence.rs
```

Native acceleration examples:

```text
Compatibility/compatibility-core/src/font_bucket.rs
Compatibility/compatibility-core/src/peggle_native_batch.rs
Compatibility/compatibility-core/src/peggle_font_lookup.rs
Compatibility/compatibility-core/src/peggle_mapped_char.rs
Compatibility/compatibility-core/src/peggle_inflate_fast.rs
See repository for additional generated kernels and individual helpers.
```

Save-file semantics/transactions/tests:

```text
Compatibility/ios/rust-entry/src/save_manager.rs; save_manager_bridge.rs
Compatibility/ios/rust-entry/src/raw_import.rs; raw_import_tests.rs
Compatibility/ios/rust-entry/src/progress.rs; progress_tests.rs
Compatibility/ios/rust-entry/src/save_manager_tests.rs; nights.rs
Tests/SaveManager; Tests/progress/README.md
```

Sync orchestration/transports/capability:

```text
Compatibility/ios/auto_progress.m; cloud_progress.m; cloud_capability.m
Compatibility/ios/folder_sync.m
Tests/CloudCapability/test_capability.py
Tests/FolderSync/native_driver.m; test_folder_sync.py
```

Historical/private evidence reviewed for the original report (unavailable to readers):

```text
source inheritance inventory; display, theme and settings validation;
save-format comparisons; UI and sync validation records;
Android conversion validation; release validation and publishing records.
```
These private records are summarized, not distributed or independently verified
by the public source manifest.

Historical conversation evidence supplies the user's baseline/AOT scope, observed
performance, device confirmations, UI/text requirements, and project scope limits. It does not substitute for missing quantitative measurements.

## Report validation
This document was checked against the maintained source and selected retained
records. Source references and companion hashes were mechanically verified.
No game rebuild, performance benchmark, new sync experiment, or release occurred
as part of writing it. The recorded installation success did not establish a new gameplay test.
All app user-facing strings remained unchanged.

Public companion: [source manifest](../skills/restore-legacy-ios-apps/references/source-evidence.json).
