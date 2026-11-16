# iBlast Moki (v1.0) — Legacy iOS Restoration Engineering Report

**Report prepared:** 2026-11-15  
**Evidence cutoff:** 2026-11-15  
**Status:** Investigation documented; no completed 64-bit restoration established  
**Publication status:** Sanitized local draft only; owner review required

> **Evidence discipline.** This report distinguishes **SOURCE** (maintained implementation inspected), **RECORD** (retained historical project result), **OBSERVATION** (directly observed package/environment fact or user/device report), **INFERENCE** (reasoned explanation), and **UNVERIFIED** (not established). No maintained restoration source checkout was available in the inspected workspace during report preparation. Accordingly, no app-specific source implementation is represented as inspected, and no patch is represented as executed.

## Topic index

- [1. Executive findings and current status](#1-executive-findings-and-current-status)
- [2. Inputs and environment](#2-inputs-and-environment)
- [3. Architecture](#3-architecture)
- [4. Restoration history](#4-restoration-history)
- [5. Detailed fixes and investigations](#5-detailed-fixes-and-investigations)
- [6. Technical areas](#6-technical-areas)
- [7. Performance](#7-performance)
- [8. Build and delivery](#8-build-and-delivery)
- [9. Validation matrix](#9-validation-matrix)
- [10. Transfer to the Respring Skill](#10-transfer-to-the-respring-skill)
- [11. Source index](#11-source-index)
- [12. Privacy and publication review](#12-privacy-and-publication-review)

---

## 1. Executive findings and current status

### 1.1 Conclusion

**RECORD:** The project began with a request to rebuild iBlast Moki for 64-bit iOS. Historical investigation reported an original ARMv6/32-bit executable, native Objective-C/C++ implementation, Box2D, 18 framework/library dependencies, and 463 unresolved external symbols. The project history subsequently stated that no working ARM64 build had been produced.

**RECORD:** The prior investigation reported that Xcode and an iOS SDK were unavailable in its working environment. It therefore did not complete compilation, signing, device installation, or gameplay validation.

**OBSERVATION:** The original iBlast Moki v1.0 package supplied for this report contains a thin ARMv6 Mach-O executable. Its inspected encryption load command has `cryptid=0`. Its Info.plist identifies bundle version `1.0`, minimum iOS `2.2.1`, and `DTSDKName` `iphoneos3.0`.

**OBSERVATION:** The current archive inspection finds 20 direct dynamic-library load commands. The historical count of 18 is retained as a discrepancy, not silently overwritten: the earlier counting scope is unavailable.

**SOURCE:** No iBlast Moki restoration source, maintained generator, compatibility runtime, host project, build guide, source commit, or release configuration was available for direct inspection in the report-preparation workspace. This report therefore cannot identify a final source commit or assert that any restoration patch is present in a maintained implementation.

### 1.2 What works / what remains limited

| Area | Status | Evidence |
|---|---|---|
| Original IPA can be opened and inventoried | Established for the supplied archive | OBSERVATION |
| Original executable is ARMv6 32-bit | Established | OBSERVATION |
| Inspected executable slice is not encrypted according to its encryption load command | Established for that slice | OBSERVATION |
| Original game uses native code and Box2D | Historical investigation finding; implementation not re-inspected here | RECORD |
| 64-bit host build | Not established; historical status says none produced | RECORD |
| ARMv6 guest execution on a modern host | Not established | UNVERIFIED |
| Framework/API compatibility | 463 unresolved symbols reported historically; no maintained resolution map available | RECORD |
| Rendering, input, audio, saves, lifecycle | No retained app-specific passing tests available | UNVERIFIED |
| Device install, gameplay, performance, distribution | Not established | UNVERIFIED |

### 1.3 Most transferable lessons

1. **Separate host ABI from guest ABI.** A 64-bit app container does not make an ARMv6 game executable natively executable. Any restoration must explicitly account for guest instruction execution and guest-to-host API boundaries.
2. **Treat unresolved imports as a dependency graph, not a checklist to stub blindly.** Each required symbol needs a correct calling convention, ownership/lifetime behavior, return contract, and test at a real game transition.
3. **Do not equate archive analysis with a playable restoration.** Package inspection, successful host compilation, installation, launch, visible gameplay, persistence, and release delivery are separate acceptance layers.
4. **Do not claim a source-level fix without maintained source and a regression result.** No app-specific fix can be attributed to a commit in the evidence currently available.
5. **Preserve the original input and baseline.** A new host, generated guest code, or reconstructed gameplay should be tracked separately from the original app identity and original package.

### 1.4 Scope boundary

This is a report about the iBlast Moki v1.0 restoration effort represented by the project history and the supplied iBlast Moki package. A separate Flappy Bird IPA was also present in the current upload set. It has a different bundle identifier and is not treated as an iBlast Moki edition or as evidence of this restoration. No Flappy Bird analysis is incorporated into the technical conclusions.

---

## 2. Inputs and environment

### 2.1 Original app identity

| Field | Finding | Evidence |
|---|---|---|
| Display name | iBlast Moki | OBSERVATION: Info.plist |
| Executable name | `iBlastMoki` | OBSERVATION: Info.plist and archive path |
| Bundle identifier | `com.godzilab-games.iBlastMoki` | OBSERVATION: Info.plist |
| `CFBundleVersion` | `1.0` | OBSERVATION |
| `CFBundleShortVersionString` | Not present in inspected Info.plist | OBSERVATION |
| Minimum OS | `2.2.1` | OBSERVATION |
| SDK metadata | `iphoneos3.0` | OBSERVATION |
| Device family | Not established from the inspected keys | UNVERIFIED |
| Engine | Native Objective-C/C++ with Box2D, per historical investigation | RECORD |
| Original executable ABI | ARMv6, 32-bit, thin Mach-O | OBSERVATION |
| Encryption | `cryptid=0` in inspected `LC_ENCRYPTION_INFO` | OBSERVATION |
| Executable size | 2,053,344 bytes | OBSERVATION |
| App archive size | 9,959,233 bytes | OBSERVATION; not a public/shareable artifact hash |

The inspected Mach-O CPU type is ARM (`0x0c`) and subtype is ARMv6 (`0x06`). The encryption command reports `cryptoff=4096`, `cryptsize=983040`, and `cryptid=0`. This establishes the encryption flag for the inspected executable, not a universal statement about other copies, repackagings, or other slices.

### 2.2 Direct dependencies

The inspected executable contains 20 direct load commands naming these dependencies:

- Foundation
- QuartzCore
- AudioToolbox
- OpenAL
- `libsqlite3`
- OpenGLES
- CoreAudio
- CoreGraphics
- UIKit
- SystemConfiguration
- Security
- AddressBook
- AVFoundation
- MediaPlayer
- MessageUI
- `libstdc++.6`
- `libgcc_s.1`
- `libSystem`
- `libobjc`
- CoreFoundation

**OBSERVATION:** These names are present in the Mach-O load commands. Their presence does not prove that every imported symbol is reached during gameplay, that the matching modern host API exists, or that a compatibility implementation is complete.

**RECORD:** The earlier investigation described 18 framework/library dependencies. The current inspection enumerates 20 load-command entries. Whether the difference reflects counting conventions, omitted system libraries, or a different analysis snapshot is **UNVERIFIED**.

### 2.3 Host build and toolchain

**RECORD:** The historical investigation environment lacked Xcode and an iOS SDK. No compile, sign, install, or device test was completed there.

**OBSERVATION (report-preparation container only):** The available command lookup found `clang`, `clang++`, `swift`, and `llvm-objdump`; it did not find `xcodebuild`, `xcrun`, `rustc`, or `cargo`. This describes only the current report-preparation container and must not be mistaken for a full inventory of the earlier project host.

| Item | Status |
|---|---|
| Xcode version used for restoration | UNVERIFIED; historical note says unavailable |
| iOS SDK version used for host build | UNVERIFIED; no host build established |
| Rust toolchain / target | UNVERIFIED |
| C/C++ compiler version used historically | UNVERIFIED |
| Dependency lockfiles / provenance | UNVERIFIED |
| Build guide | Not available in inspected workspace |
| Host bundle identifier / host build number | UNVERIFIED |
| Release tag | UNVERIFIED |
| Final source commit | UNVERIFIED |
| Final host configuration / feature flags | UNVERIFIED |

### 2.4 Devices and operating systems

No retained device model, iOS version, simulator destination, physical-device test record, or device identifier was available in the inspected evidence. No device-specific claims are made. Simulator and physical-device validation are both **UNVERIFIED**.

---

## 3. Architecture

### 3.1 What is established

**OBSERVATION:** The supplied original executable is an ARMv6 Mach-O. It is not a native ARM64 executable.

**RECORD:** Historical analysis classified the game as native Objective-C/C++ and identified Box2D. It also reported 463 unresolved external symbols in the attempted restoration analysis.

**INFERENCE:** A viable modern 64-bit restoration would need either (a) a guest ARMv6 execution environment with the necessary iOS framework compatibility, or (b) a separately scoped reconstruction of the game. A simple 64-bit relink cannot turn ARMv6 machine code into ARM64 machine code.

### 3.2 Execution flow — required model, not verified implementation

The following is a conceptual architecture for evaluating a future implementation. It is **not** a diagram of an inspected or proven iBlast Moki host.

```text
Modern iOS host application (ARM64)
        |
        +-- Host lifecycle / window / input
        |
        +-- Guest execution boundary
        |       |
        |       +-- ARMv6 guest CPU state and memory
        |       +-- Guest Objective-C / C ABI boundary
        |       +-- Original iBlast Moki code and Box2D
        |
        +-- Compatibility services (required where imported/reached)
        |       +-- Foundation / UIKit / CoreGraphics
        |       +-- OpenGLES / QuartzCore
        |       +-- AudioToolbox / OpenAL / CoreAudio
        |       +-- SQLite / filesystem / Security / other APIs
        |
        +-- Host presentation, audio output, persistence
```

No evidence establishes which of these layers were implemented in this project, how guest calls were dispatched, or whether the guest was interpreted, statically translated, or partly replaced with native helpers.

### 3.3 Execution strategy classification

| Execution category | iBlast Moki status |
|---|---|
| Original ARMv6 interpreted | UNVERIFIED |
| Original ARMv6 statically translated / AOT specialized | UNVERIFIED |
| Guest API calls bridged to native iOS APIs | UNVERIFIED |
| Guarded native helper replacements | UNVERIFIED |
| Reconstructed native gameplay | No evidence of a completed reconstruction |
| Native ARM64 host package | No completed build established |

Do not describe this project as “fully native gameplay.” No guest execution implementation was available for inspection. No pseudocode or decompiler output is treated as recovered original source.

### 3.4 Shipping defaults versus experiments

No host configuration, dispatch table, feature flag, build scheme, or release manifest was available. Consequently, shipping defaults, optional/debug paths, abandoned branches, and active code paths cannot be classified. Source presence itself would not prove runtime dispatch; here even source presence could not be inspected.

### 3.5 Sibling inheritance

No iBlast Moki sibling edition or independently validated sibling port was established in the available project evidence. The separate Flappy Bird package is a different game and is not a sibling baseline. No code, ABI assumptions, offsets, assets, or behavior should be transferred from it.

---

## 4. Restoration history

| Date | Milestone | Evidence and outcome |
|---|---|---|
| 2026-11-08 | User requested an immediate 64-bit rebuild | RECORD: project history |
| 2026-11-09 | Original IPA triage reported | RECORD: ARMv6/32-bit, decrypted, native Objective-C/C++, Box2D, dependencies and assets inventoried; no Xcode/iOS SDK, so no build/sign/device test |
| 2026-11-11 | External-symbol investigation reported | RECORD: 463 unresolved external symbols; restoration described as requiring ARMv6 execution plus iOS API compatibility |
| By 2026-11-11 | Working ARM64 build status clarified | RECORD: no working ARM64 build produced |
| 2026-11-15 | Engineering report preparation | OBSERVATION: supplied archive independently inspected; maintained source checkout not available; no app code changed and no restoration experiment resumed |

### 4.1 Baseline selection

The only baseline that can be identified is the original iBlast Moki v1.0 package supplied for this report. No hash is published because this is a cracked/proprietary game package and is not an appropriate shareable artifact. No extracted or repackaged baseline is claimed.

A host build baseline, known-good source commit, last playable candidate, or rollback point is **UNVERIFIED**.

### 4.2 Rejected or incomplete approaches

No sufficiently detailed retained record of individual rejected code approaches, candidate builds, or measured failure modes was available. The known incomplete direction is the 64-bit rebuild itself: the historical investigation exposed a guest CPU/ABI and framework-compatibility problem, but did not establish a working execution path.

No claim is made that a rewrite, broad AOT conversion, interpreter, or compatibility shim was implemented and then rejected.

---

## 5. Detailed fixes and investigations

No app-specific maintained source was available, so this section documents established blockers and the exact missing evidence rather than inventing patches. For each issue, “maintained implementation path” is explicitly unavailable.

### 5.1 ARMv6 guest execution versus ARM64 host

- **Symptom / reproduction:** The project goal is a 64-bit rebuild of a package whose executable is ARMv6. No successful modern host execution result is retained.
- **Baseline/input:** Supplied iBlast Moki v1.0 executable; thin ARMv6 Mach-O.
- **Hypothesis:** Directly treating the original guest executable as an ARM64 host binary is incompatible with the architecture boundary.
- **Root cause / layer:** CPU instruction-set and ABI mismatch. This is a format/architecture fact, not a measured gameplay crash.
- **Original semantics:** Original ARMv6 instructions, guest register state, memory layout, calling conventions, and framework interactions must be preserved if original game code is to execute.
- **Maintained implementation path:** UNVERIFIED. No interpreter, translator, dispatch implementation, or host bridge source was available.
- **Exact applicability / byte / state guards:** No patch or guard was established. The observed executable identity is ARMv6 subtype `0x06`; this is an input classification, not a patch guard.
- **Regression procedure / counterexample:** Not run. A future test must execute representative original guest code and compare register/flag/memory effects with a trusted reference. A host launch screen alone is not a counterexample or proof.
- **Actual result:** No working ARM64 build established (RECORD).
- **Limitations:** No CPU semantic coverage, exception behavior, thread state, memory mapping, or guest ABI test is retained.
- **Rollback / fallback:** Preserve the original IPA unchanged. No working restoration fallback is known.
- **Transfer prerequisites:** Establish guest instruction coverage, ARM/Thumb state handling, flags, memory faults, callbacks, and the complete guest/host calling convention before porting game logic.

### 5.2 Unresolved framework and library symbols

- **Symptom / reproduction:** Historical symbol analysis reported 463 unresolved external symbols. The exact original diagnostic output and symbol-by-symbol inventory are unavailable here.
- **Baseline/input:** Historical iBlast Moki v1.0 analysis; current package independently confirms 20 direct dependency load commands.
- **Hypothesis:** The original executable expects framework/library APIs that the proposed host/runtime did not yet provide or resolve.
- **Root cause / layer:** Guest dynamic linking and framework compatibility are the likely responsible layers. The exact root cause for each of the 463 symbols is **UNVERIFIED**.
- **Original semantics:** Each import may carry ABI, ownership, callback, object lifetime, threading, error, and side-effect requirements. A matching symbol name alone is insufficient.
- **Maintained implementation path:** UNVERIFIED. No symbol resolver, compatibility implementation, or source map was available.
- **Exact applicability / byte / state guards:** No guards or per-symbol applicability conditions are available.
- **Regression procedure / counterexample:** Not run. A future test should resolve and exercise imports along launch and a concrete gameplay transition, then include an unimplemented/unsupported symbol case that fails explicitly rather than returning fabricated success.
- **Actual result:** 463 unresolved symbols were reported historically (RECORD); no completed resolution is established.
- **Limitations:** The original symbol list, import ordinals, call sites, and runtime reachability are unavailable. The number does not prove all 463 are used during ordinary gameplay.
- **Rollback / fallback:** No project fallback is established. Avoid generic nil/zero stubs for unknown contracts.
- **Transfer prerequisites:** Obtain the original symbol report, map imports to actual call sites, classify required APIs, and test each compatibility implementation at the real boundary.

### 5.3 Build-toolchain blocker

- **Symptom / reproduction:** Historical work did not complete a host compile, signing, installation, or device test.
- **Baseline/input:** Historical project environment; exact machine and toolchain inventory unavailable.
- **Hypothesis:** Missing Xcode/iOS SDK prevented building and signing an iOS host artifact.
- **Root cause / layer:** Build environment and platform SDK availability.
- **Original semantics:** Not applicable; this is a delivery blocker rather than a game behavior patch.
- **Maintained implementation path:** No build guide or project file was available to inspect.
- **Exact guards:** No build configuration or target guards available.
- **Regression procedure / counterexample:** Not run. A compiler executable alone is not a valid counterexample; an actual Xcode/iOS SDK destination and successful project build are required.
- **Actual result:** No compile/sign/device test in the historical investigation (RECORD).
- **Limitations:** Current report-preparation tool availability is not the same as the historical build host.
- **Rollback / fallback:** Keep the original package and do not claim a new IPA.
- **Transfer prerequisites:** Recover the authoritative source checkout and build guide; identify supported Xcode, SDK, target, dependencies, and signing requirements.

### 5.4 Gameplay, graphics, input, audio, lifecycle and persistence

- **Symptom / reproduction:** No app-specific failure reproduction or passing gameplay test was retained.
- **Baseline/input:** Original iBlast Moki v1.0 package.
- **Hypothesis / root cause:** Not established.
- **Original semantics:** Not established beyond the fact that original game code and resources are present in the package.
- **Maintained implementation path:** Not available for inspection.
- **Guards:** None established.
- **Regression procedure / counterexample:** None retained.
- **Actual result:** UNVERIFIED.
- **Limitations:** The presence of assets, SQLite linkage, audio frameworks, or OpenGLES imports does not prove their runtime behavior.
- **Rollback / fallback:** No restoration-specific fallback known; preserve the original input.
- **Transfer prerequisites:** Build a transition-based test plan covering Play, actual interaction, modal dismissal, level completion, save/relaunch, interruption/resume, and rotation where supported.

---

## 6. Technical areas

| Area | Evidence status | What can responsibly be said |
|---|---|---|
| CPU / ABI | Partially established | Original executable is ARMv6 32-bit; guest execution implementation and semantic coverage unknown |
| ARM/Thumb instruction coverage | UNVERIFIED | No translated corpus, interpreter tests, or execution trace available |
| Exceptions / unwinding | UNVERIFIED | No retained evidence |
| Memory / threads | UNVERIFIED | No guest memory or threading implementation available |
| Filesystem / SQLite | Partially observed | `libsqlite3` is a direct dependency; actual schema and save semantics uninvestigated |
| Framework compatibility | Partially established | 20 direct dependencies observed; 463 unresolved symbols reported historically |
| Scene / window / keyboard / touch | UNVERIFIED | No host scene or input source/tests available |
| OpenGL ES / offscreen targets | Partially observed | OpenGLES is linked; render-target behavior and presentation are uninvestigated |
| Resolution / aspect / rotation | UNVERIFIED | No measured guest canvas, drawable, or rotation result |
| Simulation / input / render clocks | UNVERIFIED | No instrumentation or timing record |
| Audio | Partially observed | AudioToolbox, OpenAL, and CoreAudio are linked; playback and interruption behavior untested |
| Lifecycle / background / sleep | UNVERIFIED | No retained transition tests |
| Save transactions / import / sync | UNVERIFIED | SQLite linkage does not establish save format, atomicity, or cloud sync |
| Retired online services | UNVERIFIED | No SDK inventory or disabled-service evidence |

### 6.1 Investigation priorities

The most efficient next technical sequence, once source and build prerequisites are recovered, is:

1. Establish one minimal guest execution milestone with a visible and repeatable transition.
2. Trace only the imports reached by that transition.
3. Verify ABI and ownership semantics at those boundaries.
4. Add a real gameplay interaction and a discriminating counterexample.
5. Only then broaden to graphics, audio, lifecycle, and persistence paths.

These are recommendations, not work completed in this project.

---

## 7. Performance

No valid performance result is available.

| Required benchmark field | Evidence |
|---|---|
| Bottleneck and profiler | UNVERIFIED |
| Scene / level | UNVERIFIED |
| Guest and host build identity | UNVERIFIED |
| Rendering resolution | UNVERIFIED |
| Device class / OS | UNVERIFIED |
| Warm-up | UNVERIFIED |
| Duration / sample count | UNVERIFIED |
| Before / after | UNVERIFIED |
| Correctness checks during measurement | UNVERIFIED |
| Timer callbacks / simulation steps | UNVERIFIED |
| Render submissions / GPU completion | UNVERIFIED |
| Physical display scanout | UNVERIFIED |

No FPS, frame-time, CPU utilization, startup-time, or battery claim is made. No simulator performance is inferred. No callback or submission count is presented as physical scanout. Performance work should follow correctness and use comparable device/scene/settings samples.

---

## 8. Build and delivery

### 8.1 Current build status

No host build, signed app, unsigned IPA, release tag, or reproducible source/configuration pair is established. There is no project `BUILDING.md` available in the inspected workspace. Consequently, a truthful project-specific build command cannot be supplied.

### 8.2 Reproduction template for a future source checkout

The following is a **template only**, not a command verified against this project:

```sh
cd <PROJECT_ROOT>
# Read the project's actual BUILDING.md before building.
xcodebuild -list -project <HOST_PROJECT>.xcodeproj
xcodebuild \
  -project <HOST_PROJECT>.xcodeproj \
  -scheme <HOST_SCHEME> \
  -configuration <CONFIGURATION> \
  -destination '<SUPPORTED_DESTINATION>' \
  build
```

Do not infer that this project uses Xcode project format, a particular scheme, Rust, or any specific build system until the maintained source is recovered.

### 8.3 Dependency and artifact handling

- Preserve the original IPA as read-only evidence.
- Keep generated translation output separate from maintained source.
- Record exact guest input identity and generator/configuration identity for any generated code.
- Keep build caches and outputs outside the source checkout where the project's build guide recommends it.
- Do not bundle proprietary original game inputs, extracted system art, personal saves, or signing material in a public report.
- Distinguish unsigned host artifacts from signed device artifacts.
- Verify host architecture and embedded guest architecture separately.
- A successful compile does not establish installability or gameplay.
- No signing capabilities, entitlements, provisioning, distribution, or App Store acceptance are established.

---

## 9. Validation matrix

No tests were run against a restored app during report preparation. The current archive was inspected statically only.

| Test / transition | Build/configuration | Environment | Result | Evidence label | Remaining gap |
|---|---|---|---|---|---|
| Open original IPA / list entries | Original supplied iBlast Moki v1.0 package | Report-preparation container | Completed | OBSERVATION | Does not establish execution |
| Read app Info.plist | Same input | Report-preparation container | Completed | OBSERVATION | No source/build identity |
| Inspect Mach-O header and load commands | Same input | Report-preparation container | Completed | OBSERVATION | No runtime trace |
| Determine executable architecture | Same input | Report-preparation container | ARMv6 thin Mach-O | OBSERVATION | No guest execution |
| Inspect encryption command | Same input | Report-preparation container | `cryptid=0` | OBSERVATION | Applies to inspected executable only |
| Historical initial triage | Historical project baseline | Environment not retained | Reported completed | RECORD | Raw report/log unavailable |
| Historical unresolved-symbol analysis | Historical project baseline | Environment not retained | 463 unresolved symbols reported | RECORD | Exact symbol list unavailable |
| Host compile | No established host source/config | Not established | Not completed in historical record | RECORD | Recover source and toolchain |
| Install / launch | No restored artifact | Device not established | UNVERIFIED | UNVERIFIED | Requires built artifact and target |
| Actual gameplay | No restored artifact | Device not established | UNVERIFIED | UNVERIFIED | Requires Play-to-gameplay validation |
| Modal dismissal / touch input | No restored artifact | Device not established | UNVERIFIED | UNVERIFIED | Requires interaction test |
| Save / relaunch | No restored artifact | Device not established | UNVERIFIED | UNVERIFIED | Requires game-visible persistence test |
| Background / resume / rotation | No restored artifact | Device not established | UNVERIFIED | UNVERIFIED | Requires device lifecycle test |
| Performance | No restored artifact | No benchmark environment | UNVERIFIED | UNVERIFIED | Requires controlled physical-device samples |
| Service delivery / distribution | No release artifact | Not established | UNVERIFIED | UNVERIFIED | Requires separate delivery verification |

### 9.1 Report-preparation tests, separated from historical tests

Performed on 2026-11-15:

- Opened both supplied IPA archives and enumerated their contents.
- Read the iBlast Moki app Info.plist.
- Inspected the iBlast Moki executable Mach-O header, architecture subtype, direct dependency load commands, and encryption information.
- Compared current package facts with retained historical project findings.
- Checked the available report-preparation command environment for common build tools.
- Inspected the report text and performed a targeted scan for obvious path, secret, and personal-identifier patterns.

Not performed:

- No app was built, installed, launched, or played.
- No restoration source was modified.
- No abandoned experiment was resumed.
- No simulator or device test was run.
- No performance test was run.
- No remote repository was cloned or published.
- No source commit or artifact hash was invented.

---

## 10. Transfer to the Respring Skill

### 10.1 General principles supported by this case

| Proposed principle | Supporting evidence | Suggested skill treatment |
|---|---|---|
| Identify the exact guest architecture before selecting a 64-bit strategy | OBSERVATION: ARMv6 executable; RECORD: failed-to-complete 64-bit restoration | Reinforce intake and guest/host ABI separation |
| Treat unresolved symbols as a call-contract investigation | RECORD: 463 unresolved symbols | Require call-site reachability and ABI/ownership analysis before stubbing |
| Distinguish package triage from a working restoration | RECORD: no host build/device test; OBSERVATION: package inspection possible | Reinforce layered acceptance matrix |
| Keep source commit, host build, original input, and release tag separate | No host commit/build/release identity could be recovered | Require explicit identity fields in investigation records |
| Preserve missing evidence as missing | No maintained source, raw logs, or device test records available | Encourage explicit UNVERIFIED labels rather than filling gaps |

### 10.2 Engine/version-specific conclusions

The ARMv6 architecture finding applies to this inspected iBlast Moki v1.0 executable only. The native Objective-C/C++ and Box2D characterization is historical evidence for this app, not a general rule for similarly dated games. No app-specific compatibility patch is proposed.

### 10.3 Narrow additions or corrections suggested

1. In the investigation record, add a field for **direct Mach-O load-command count and counting method**, so historical dependency counts can be reconciled.
2. Record **exact unresolved symbol count, raw inventory location, symbol type, call-site reachability, and resolution status** separately.
3. Require an explicit statement of **guest execution strategy**: interpreted, statically translated, bridged, or reconstructed. Allow “not established.”
4. Make the build/delivery record distinguish **source commit**, **host build identity/configuration**, **original input identity**, and **release tag**.
5. Keep the validation matrix layered: archive inspection, compile, install, launch, gameplay, persistence, performance, and distribution are separate results.

### 10.4 Counterexamples and guardrails

- A 64-bit host package containing a 32-bit guest is not automatically a native gameplay port.
- A `cryptid=0` result on one executable does not prove every copy or slice is unencrypted.
- A dependency load command does not prove the API is reached.
- An unresolved-symbol count does not prove every symbol is required for first gameplay.
- A successful host launch does not prove the guest is running.
- Asset extraction or a menu recreation does not prove original gameplay was restored.
- Generated candidate counts do not establish execution coverage.
- A local database write does not establish remote synchronization.
- A public source link does not prove a historical device test unless the test evidence is independently available.

### 10.5 Recommended regression cases for a future implementation

These are recommendations, not completed tests:

- Verify ARMv6 guest instruction and calling-convention behavior with production runtime code.
- Exercise imports reached during cold launch, Play, and one complete gameplay interaction.
- Include an unsupported import that fails explicitly and diagnostically.
- Verify rendering output and touch-coordinate mapping at original aspect ratio and a materially different aspect ratio.
- Test modal dismissal and touch cancellation.
- Test audio start, interruption, and resume.
- Test save, terminate, relaunch, and game-visible resume.
- Test background/foreground transitions and rotation if supported by the host.
- Compare performance only after correctness, on physical hardware, with defined metrics and samples.

### 10.6 Open questions

- Where is the authoritative maintained iBlast Moki source checkout?
- What exact commit/configuration, if any, was the last working baseline?
- What is the original 463-symbol report and which symbols were actually reached?
- Was an interpreter, translator, or compatibility runtime ever implemented beyond analysis?
- What were the rejected experiments and their exact failure evidence?
- Which host bundle/build identity and Xcode/SDK versions were intended?
- Were any physical-device or simulator tests performed outside the retained history?
- What source and asset licensing/redistribution terms apply to the original game content?

---

## 11. Source index

### 11.1 Project evidence

| Label | Description | Availability |
|---|---|---|
| `PRIVATE_EVIDENCE: original iBlast Moki v1.0 package` | Supplied original app archive and its Info.plist / Mach-O executable | Local conversation upload; not linked or redistributed |
| `PRIVATE_EVIDENCE: historical iBlast Moki triage` | Prior investigation summary dated 2026-11-09 | Prior project conversation; raw report/log unavailable |
| `PRIVATE_EVIDENCE: historical unresolved-symbol finding` | Prior report of 463 unresolved external symbols dated 2026-11-11 | Prior project conversation; symbol inventory unavailable |
| `PRIVATE_EVIDENCE: historical build limitation` | Prior report that Xcode/iOS SDK were unavailable and no build/sign/device test completed | Prior project conversation |
| `UNAVAILABLE: maintained iBlast Moki source` | Authoritative source checkout, runtime, generator, host, build guide, and source history | Not present in inspected workspace |
| `UNAVAILABLE: device evidence` | Device logs, screenshots, test reports, and performance captures | Not available |

No public repository URL, commit hash, source path, symbol source reference, or release tag could be verified for iBlast Moki. None is invented here.

### 11.2 Reference methodology

The installed Respring Skill references were consulted for general methodology:

- `references/execution.md`
- `references/rendering-input.md`
- `references/timing-performance.md`
- `references/lifecycle-compatibility.md`
- `references/save-files-sync.md`
- `references/validation-delivery.md`
- `references/case-studies.md`
- `references/sources.md`
- `assets/investigation-record.md`

These are skill guidance and case-study references, not iBlast Moki source evidence. Their other-app patches and measurements are not attributed to this project.

### 11.3 Hash policy

No SHA-256 hashes are published. The supplied cracked/proprietary game archives are not shareable app artifacts, and no maintained source artifact was available to hash. No player data, credentials, or secrets were hashed.

---

## 12. Privacy and publication review

### 12.1 Sanitization performed

- Replaced unavailable private evidence references with descriptive `PRIVATE_EVIDENCE` / `UNAVAILABLE` labels.
- Did not include personal names, private usernames, emails, account identifiers, home paths, hostnames, IP/MAC addresses, device UDIDs/serials/UUIDs, signing identifiers, private repository links, or unrelated personal details.
- Did not include credentials, tokens, passwords, private keys, certificates, provisioning profiles, cookies, authorization headers, or signed download URLs.
- Did not include player names, scores, progress, save contents, account state, notifications, location data, raw logs, or shell history.
- Did not attach the IPA, extracted artwork, system art, personal saves, or signing materials.
- Kept the original public app bundle identifier and relevant technical metadata because they identify the software, not a personal account.
- Did not publish an evidence index containing raw local paths or private identifiers.

### 12.2 Review limitations

The report-preparation environment did not contain the maintained source checkout or original raw historical logs. Therefore a full repository-history secret scan, source-file review, and verification of historical device evidence could not be performed. The targeted scan of this report is not proof that an unavailable source repository or its history is safe to publish.

No public source links are included, so no claim of remote source verification is made. The original cracked IPA is not redistributed, licensed, or made public by preparing this report.

### 12.3 Owner review required

Before sharing this report with Respring, the owner should verify that the project identity and historical findings are correct, supply or identify the authoritative source checkout if one exists, and review whether any additional private project context should remain omitted. **Preparing this report does not authorize publication, repository changes, uploads, pull requests, or licensing of original game assets.**
