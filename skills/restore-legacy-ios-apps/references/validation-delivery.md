# Validation, portable builds, and delivery

## Layered acceptance

| Layer | Evidence required | Does not prove |
| --- | --- | --- |
| Build/package | Successful compile, intended platform/architecture, resources/config | Launch or guest correctness |
| CPU/helper/API tests | Production implementation and edge-case assertions | Every instruction/API/game mode |
| Simulator integration | Visible scene, actual gestures, persisted guest outcome | Physical-device speed or hardware services |
| Device gameplay | Launch, input, round/level, modal, save/relaunch, lifecycle | Every device or full game parity |
| Performance | Defined metric and controlled comparable samples | Physical scanout from submission counts |
| Remote service | Upload, remote receipt, application, convergence | Proven by local writes alone |
| Distribution | Final source/artifact identity, clean signing/package audit | A gameplay test of a different build |

Choose checks for the changed layer. A README edit does not justify a full game rebuild. A renderer or timing patch needs visible/input checks, not only compilation. Stop broad retesting when relevant checks pass unless new evidence warrants it.

UI automation should assert the intended screen and result. Paid/free menu positions differ; a test named Redeem can accidentally test Loot. Realistic gestures need duration and event cadence. Track new panic log entries against baseline, not just file existence. A surviving native host may contain a stopped guest. Keyboard success requires forwarded/persisted text, not only responder flags.

For geometry, test original aspect and a materially different aspect, repeated rotation, cold launch on each display, live transitions and corner/edge touch targets. For lifecycle test audio, timer state, saved progress and the next input after resume. Mute output without bypassing audio execution when quiet testing is requested.

## Build correctness

Read the actual repository's BUILDING instructions. Discover installed Xcode/SDK, Rust targets/toolchain and build system; pin known-working requirements per project. Historical report versions are not universal requirements. Keep build outputs outside provider-managed/iCloud trees and separate sibling output roots. Quote paths with spaces; use an encoded flags mechanism where ordinary shell splitting breaks compiler arguments.

Practical interpreter/translated Debug builds may still need optimized Rust. Do not copy optimization levels blindly. Verify external static SDL/library changes invalidate Rust's link cache. Hash relevant source/config/archive inputs or force the appropriate relink; a timestamp alone is weak evidence.

Assign one producer to the final Info.plist. Preserve build-setting expansion for selected identity and compiled icon metadata. Shell payload copies should not overwrite Xcode's processed root plist. Keep editable icons and buildable generated-input provenance.

Use an Xcode scheme with the actual destination for device provisioning; a target-only invocation can ignore destination selection. Verify selected device, installed bundle/build and profile membership. A locked device or OS automation prompt requires the user at the device; continue independent work and never request the passcode itself.

## Portable public source and IPA

When publication is in scope, prepare a standalone source root with maintained host/runtime/generators, exact required inputs, dependencies/notices, build instructions and user-owned documentation. Test for accidental sibling/absolute path dependencies. Preserve lockfiles and vendor checksum-sensitive files; Git line-ending conversion and export-ignore can break otherwise plausible source ZIPs.

Separate private signed tests from staged unsigned distribution. Audit nested archives for account/provisioning sidecars as well as the host. Preserve original input inventories. Embedded ARMv7 guest data is expected in an ARM64 host; distinguish loadable host binaries from interpreted input instead of deleting the guest to pass an architecture check. Verify device platform versus ARM64 simulator platform.

Removing one original IPA does not remove extracted assets or game-derived translated code. A user-imported-input design requires a real importer/generation/build workflow and testing. Sanitization is not relicensing: retain upstream notices and describe mixed-content rights accurately. Do not add a blanket license over proprietary game material.

Freeze intended source/configuration, package matching source and binaries, hash final artifacts and inspect uploaded identity if upload is authorized. Keep old published tags/releases reproducible; inspect uncertain upload state before retry. Preserve user README and changelog edits. Internal device logs, save files, profiles, keys, account metadata and machine paths stay out of public packages.

## Workbench cleanup and handoff

Classify authoritative source, original inputs, irreplaceable evidence, releases, reproducible caches and temporary outputs before deleting. Resolve symlinks, verify replacement copies and use specific paths. Update the authority note after moves. Do not delete an old folder just because it is large or a public snapshot exists elsewhere.

Record active jobs and stop task-owned tests/captures/keep-awake processes. Honor the user's current duration/deadline rules; the source projects had different preferences and neither is universal. Do not kill another task's processes. A final report should distinguish completed, user-confirmed, historical, inferred and untested results.
