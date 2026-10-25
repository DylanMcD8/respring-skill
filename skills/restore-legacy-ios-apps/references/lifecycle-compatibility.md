# Lifecycle, audio, storage, and obsolete services

## Lifecycle state machine

Represent active, inactive, background, resuming and terminated states explicitly. Queue transitions into the runtime where appropriate; make duplicate notifications harmless. Cancel touches, pause guest scheduling/audio, preserve host event handling and rebase deadlines on resume. Do not map resign-active to exit: Control Center and interruptions are normal transitions.

Use an app-specific non-destructive save/checkpoint routine when backgrounding, with a bounded background task if needed. Do not call an original Quit routine just because it saves before destroying game objects. Test interruption, app switcher, repeated background/resume and cold-launch Continue; suspension cannot guarantee survival after OS eviction.

## Audio and sleep policy

A visual resume does not prove audio resumed. Trace session activation, interruption end, source/context state, queued buffers and timing. Cover all used APIs, not just the easiest music path. Keep buffer generation cadence independent of fast host polling: Skee's shorter repaint polling required its audio chunk cadence to remain bounded.

Idle-timer prevention should reflect product policy, foreground state and any in-app timer. Koi's expiry destroyed the game before exiting; suppressing only exit left invalid state. Intercept a guarded point before destruction, preserve game state, release `idleTimerDisabled`, and allow later input to rearm audio/keep-awake. Resume callbacks must not undo an expired timer. Account for existing gain when bridging fade to avoid double attenuation.

Releasing sleep prevention allows system Auto-Lock; it does not force an immediate screen lock. Keep accelerated timer fixtures separate from production constants. Test exact policy transitions and label physical Auto-Lock timing unverified unless observed.

Vibration forwarding must follow actual guest API calls; hardware and system settings constrain it. Do not infer every interaction should vibrate, or use an iPad as a haptic validation device.

## Compatibility errors and save integrity

Implement atomic writes as validated same-directory staging/replacement with appropriate flush/error semantics. Preserve old data if replacement fails; update guest filesystem bookkeeping only after success. Test interruption/failure cases for save paths. Atomic-write defects affect normal users, not only debugging.

Memory APIs need their real contract. Skee's Mono/Boehm GC required recognition of a subrange covered by adjacent compatible anonymous mappings. Non-fixed `mmap` hints can fail because a free address lacks a large enough gap; retry an alternative allocation for the appropriate errors. Do not relax fixed-map semantics or disguise genuine exhaustion. Test overlaps, edges, gaps and permissions relevant to the implementation; a targeted fix is not full POSIX coverage.

A plist-backed generic-password shim used for tickets is not a secure native Keychain. Label its storage/security boundary and keep sibling app stores distinct. Do not reuse it for sensitive credentials.

## Retired online SDKs

Within authorized scope, identify SDK startup hooks, singleton access, workers, lifecycle callbacks and UI entry points. Removing a login button alone leaves background paths active. Use exact binary identity/prologue guards and preserve required local return/object contracts. Trace crashes at the actual call site; do not add arbitrary nil returns across the framework.

Skee Free's extra rewards SDK needed independent suppression even when paid/free Plus+ prologues matched. Local zero-initialized accessors were retained while network paths were disabled. Do not invent successful rewards, purchases or account responses. Entitlement/theme changes are separate from removing dead login UI and need the user's relevant scope.

For a sibling port, verify engine version, slice, callbacks, globals and tests independently. Shared names and visuals are insufficient evidence.
