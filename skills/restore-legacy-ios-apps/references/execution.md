# Intake, execution, and bounded acceleration

## Intake before architecture choice

Read the actual payload, not just the archive filename. Keep archive and extracted executable hashes separate; sanitized/repacked archives legitimately differ from original ZIPs. Inspect every relevant Mach-O slice, encryption load command, dependent library, minimum OS/SDK, symbol table, and code/data section. `cryptid=0` on one slice does not establish every slice's status. If encrypted executable data prevents analysis, explain the required usable input; do not claim decompilation succeeded.

Inspect the plist for executable, device family, orientation, and bundle identity. Inventory startup assets, archives/atlases, localized art, native dependencies, and expected writable paths. Preserve the original read-only; make experiments elsewhere. For untrusted archives, validate paths and sizes before extraction. Do not unpack over the source tree or follow archive-provided symlinks into unrelated paths.

Use available tools such as `plutil`, `file`, Mach-O inspection/disassembly, ZIP listing, hashes, and a decompiler as appropriate. Tool output is evidence to interpret, not proof of runtime behavior. Avoid implementing every import speculatively: trace calls exercised by launch and the next gameplay milestone.

Distinguish identities: original game version, original bundle, host bundle, host build, candidate, release tag, source commit, and installed signing identity. A candidate label or stale inherited variable name does not establish current architecture.

## Translation route

Chuzzle/Koi's generator specializes ARM instruction semantics at known guest program counters/opcodes into Rust; LLVM produces host ARM64. It retains guest registers, flags, 32-bit memory/layout and ABI. This is static partial evaluation, not recovered idiomatic C++.

The coverage problem includes support libraries, indirect calls, ARM/Thumb state, exceptions, relocations and code/data ambiguity. Counts of generated candidate addresses may include data and alternate decodings; they are not executed-code coverage. Validate encountered paths and describe remaining coverage honestly.

Guard input hashes and patched bytes. Put changes in generators or maintained support source. Keep manifests tying generated output to exact inputs/configuration. Decide explicitly whether unsupported execution fails or falls back; verify shipping feature flags and dispatch. Chuzzle/Koi's shipping fallback was disabled, with an optional reference interpreter for development. That is a project decision, not an instruction to disable an interpreter in a different game.

A missing instruction is a semantic problem: check condition codes, CPSR/FPSCR, operand aliases, alignment, register banks, memory faults, exclusive monitors, and PC/Thumb behavior. Write tests against production implementation. Skee HD's ARMv6 VFP LEN/STRIDE short vectors required bank wrapping and broadcasts; scalar-only execution collapsed geometry. Transfer this fix only when disassembly/trace shows the relevant behavior. Passing a narrow CPU harness is not ARM conformance.

## Interpreted and mixed routes

Unity/Mono AOT may leave a managed DLL with signatures but `ret`-only method bodies. Exporting that DLL cannot restore gameplay. Locate native implementations and runtime dependencies. An asset viewer proves decoding, not playable restoration.

A modified compatibility runtime can execute original ARM/Thumb with native graphics/audio/UIKit services. Verify Objective-C lookup/swizzling, guest/host pointer width, structure returns, callback ownership, P/Invoke resolution, thread state and library loading at observed failures. Truthfully advertise graphics extensions; claiming an extension can make the engine call missing functions.

Preserve the full proven sibling baseline, including exception/unwind, text encoding, memory, thread, audio and lifecycle fixes. Produce a file/hash inheritance table; adapt addresses, relocations, object layouts, guest globals, screen identity and saves independently. Visually identical games can have discontiguous globals and different menus.

## Native helper contract

Use selective acceleration when profiling identifies a bounded expensive routine. Record:

- Executable hash, original bytes, entry/return address and ARM/Thumb/IT state.
- General and extension registers, flags, stack bounds, return convention.
- Memory regions read/written, aliasing, overlap, ownership and mapping requirements.
- Instruction budget/retirement, error behavior, cache invalidation and scheduling effects.
- Exact guards, deterministic fallback, mismatch reporting and disabling policy.

First compare synthetic edge cases against original execution; then shadow-check representative real inputs using captured CPU state and touched memory. Include empty/degenerate sizes, aliases, invalid bounds and both exits. Measure guard/copy/transition overhead in end-to-end gameplay. Do not relax tolerances to conceal an unexplained mismatch.

Peggle's bounded empty-font-bucket traversal stops before actual drawing and retains ownership in the guest. Only a subset of generated prototypes was active. Its larger `inflate_fast` path remained disabled after real-input failure; smaller guarded pieces survived. An environment override disabled a copy ring despite a misleading settings default. Inspect initialization order and effective behavior before describing a feature as shipped.

## Stop conditions for an experiment

Return to the working baseline when equivalence fails, guards cannot establish input safety, compilation/corpus validation remains incomplete, or net performance does not improve. Preserve the hypothesis and failure evidence. A paused broad AOT experiment is not the next mandatory step in a fidelity restoration. A full rewrite is a separate scope with gameplay, physics, assets, modes, UI, audio and save compatibility to reproduce.
