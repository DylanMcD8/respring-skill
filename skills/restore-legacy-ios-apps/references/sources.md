# Source provenance and confidence

This skill synthesizes two internal research reports dated 25 October 2026: *Legacy iOS Restoration Report* and *Peggle and Peggle HD Engineering Report*. Their original evidence indexes were used to construct the public-only [source manifest](source-evidence.json). Internal reports, local machine paths, device identifiers and player data are not included.

## Evidence levels

- **Source verified:** behavior/configuration present in the recorded maintained implementation. Not proof every branch executed.
- **Recorded:** historical test/measurement described in the report. Not rerun for this package.
- **Observed:** user/device experience, which can establish a symptom without a controlled benchmark.
- **Recommendation:** a reusable practice inferred from cases; requires validation in the new target.
- **Limit:** known missing coverage or incomplete/rejected experiment.

The manifest supplies commit-pinned public file locations and SHA-256 hashes. Hashes were checked against local source copies during preparation. Public URLs were constructed from the recorded repository/commit/path; this preparation did not independently fetch every remote URL. Internal-only historical evidence is summarized, not presented as a public source file.

## Recorded repositories

### Chuzzle

[Source snapshot](https://github.com/DylanMcD8/respring-chuzzle/tree/db11d651554ba212b90ce7d71306b8f6835740fc) — `db11d651554ba212b90ce7d71306b8f6835740fc`.

- [README.md](https://github.com/DylanMcD8/respring-chuzzle/blob/db11d651554ba212b90ce7d71306b8f6835740fc/README.md)
- [BUILDING.md](https://github.com/DylanMcD8/respring-chuzzle/blob/db11d651554ba212b90ce7d71306b8f6835740fc/BUILDING.md)
- [OriginalPort/generate_native.py](https://github.com/DylanMcD8/respring-chuzzle/blob/db11d651554ba212b90ce7d71306b8f6835740fc/OriginalPort/generate_native.py)
- [OriginalPort/native-manifest.json](https://github.com/DylanMcD8/respring-chuzzle/blob/db11d651554ba212b90ce7d71306b8f6835740fc/OriginalPort/native-manifest.json)

### Koi Pond

[Source snapshot](https://github.com/DylanMcD8/respring-koi-pond/tree/e48afd82a3b047edeb7a221851e6f15d5e5d9264) — `e48afd82a3b047edeb7a221851e6f15d5e5d9264`.

- [README.md](https://github.com/DylanMcD8/respring-koi-pond/blob/e48afd82a3b047edeb7a221851e6f15d5e5d9264/README.md)
- [BUILDING.md](https://github.com/DylanMcD8/respring-koi-pond/blob/e48afd82a3b047edeb7a221851e6f15d5e5d9264/BUILDING.md)
- [OriginalPort/native-manifest.json](https://github.com/DylanMcD8/respring-koi-pond/blob/e48afd82a3b047edeb7a221851e6f15d5e5d9264/OriginalPort/native-manifest.json)
- [OriginalPort/compatibility-core/src/frameworks/opengles/gles_guest.rs](https://github.com/DylanMcD8/respring-koi-pond/blob/e48afd82a3b047edeb7a221851e6f15d5e5d9264/OriginalPort/compatibility-core/src/frameworks/opengles/gles_guest.rs)

### Skee-Ball

[Source snapshot](https://github.com/DylanMcD8/respring-skee-ball/tree/fbcf52c3851857a83f5748dbed3ce460c060e69c) — `fbcf52c3851857a83f5748dbed3ce460c060e69c`.

- [BUILDING.md](https://github.com/DylanMcD8/respring-skee-ball/blob/fbcf52c3851857a83f5748dbed3ce460c060e69c/BUILDING.md)
- [CompatibilityProbe/Tests/check_swp.py](https://github.com/DylanMcD8/respring-skee-ball/blob/fbcf52c3851857a83f5748dbed3ce460c060e69c/CompatibilityProbe/Tests/check_swp.py)
- [CompatibilityProbe/compatibility-core/src/libc/sys/mman.rs](https://github.com/DylanMcD8/respring-skee-ball/blob/fbcf52c3851857a83f5748dbed3ce460c060e69c/CompatibilityProbe/compatibility-core/src/libc/sys/mman.rs)
- [CompatibilityProbe/compatibility-core/src/frameworks/opengles/skee_layout.rs](https://github.com/DylanMcD8/respring-skee-ball/blob/fbcf52c3851857a83f5748dbed3ce460c060e69c/CompatibilityProbe/compatibility-core/src/frameworks/opengles/skee_layout.rs)

### Skee Free

[Source snapshot](https://github.com/DylanMcD8/respring-skee-ball-free/tree/2d3e0c200b51789ca4da0ff405cf0751fb2270ec) — `2d3e0c200b51789ca4da0ff405cf0751fb2270ec`.

- [BUILDING.md](https://github.com/DylanMcD8/respring-skee-ball-free/blob/2d3e0c200b51789ca4da0ff405cf0751fb2270ec/BUILDING.md)

### Skee-Ball HD

[Source snapshot](https://github.com/DylanMcD8/respring-skee-ball-hd/tree/336a50c265c3e143a4bb418477305cc14477a907) — `336a50c265c3e143a4bb418477305cc14477a907`.

- [BUILDING.md](https://github.com/DylanMcD8/respring-skee-ball-hd/blob/336a50c265c3e143a4bb418477305cc14477a907/BUILDING.md)
- [CompatibilityProbe/compatibility-core/src/cpu/interpreter/vfp.rs](https://github.com/DylanMcD8/respring-skee-ball-hd/blob/336a50c265c3e143a4bb418477305cc14477a907/CompatibilityProbe/compatibility-core/src/cpu/interpreter/vfp.rs)

### Peggle

[Source snapshot](https://github.com/DylanMcD8/respring-peggle/tree/8f6629c3c1860bc9bc3902f3ff50d86a53373ee0) — `8f6629c3c1860bc9bc3902f3ff50d86a53373ee0`.

- [BUILDING.md](https://github.com/DylanMcD8/respring-peggle/blob/8f6629c3c1860bc9bc3902f3ff50d86a53373ee0/BUILDING.md)
- [docs/ICLOUD.md](https://github.com/DylanMcD8/respring-peggle/blob/8f6629c3c1860bc9bc3902f3ff50d86a53373ee0/docs/ICLOUD.md)
- [Scripts/package_ipa.py](https://github.com/DylanMcD8/respring-peggle/blob/8f6629c3c1860bc9bc3902f3ff50d86a53373ee0/Scripts/package_ipa.py)
- [Scripts/audit_release.py](https://github.com/DylanMcD8/respring-peggle/blob/8f6629c3c1860bc9bc3902f3ff50d86a53373ee0/Scripts/audit_release.py)

### Peggle HD

[Source snapshot](https://github.com/DylanMcD8/respring-peggle-hd/tree/fde8b99a34f2f1cb57ea59af2a4a722667578abd) — `fde8b99a34f2f1cb57ea59af2a4a722667578abd`.

- [BUILDING.md](https://github.com/DylanMcD8/respring-peggle-hd/blob/fde8b99a34f2f1cb57ea59af2a4a722667578abd/BUILDING.md)
- [docs/ICLOUD.md](https://github.com/DylanMcD8/respring-peggle-hd/blob/fde8b99a34f2f1cb57ea59af2a4a722667578abd/docs/ICLOUD.md)
- [Scripts/package_ipa.py](https://github.com/DylanMcD8/respring-peggle-hd/blob/fde8b99a34f2f1cb57ea59af2a4a722667578abd/Scripts/package_ipa.py)
- [Scripts/audit_release.py](https://github.com/DylanMcD8/respring-peggle-hd/blob/fde8b99a34f2f1cb57ea59af2a4a722667578abd/Scripts/audit_release.py)

## Limits that must survive reuse

No universal translator, complete CPU/framework conformance, exhaustive game parity, or long-duration thermal benchmark was established. Chuzzle/Koi generation counts are not executed coverage. Peggle broad AOT remained incomplete; the current report describes interpreted execution with guarded helpers. Peggle public folder tests established local coordinated exchanges, not end-to-end cloud delivery. A physical installation is not a gameplay/fold test. Historical user preferences on icons, aspect, deadlines and keep-awake are not global skill requirements.

Read the relevant pinned file and effective startup path before transferring a technique. A moving README, older status note, inherited symbol name or disabled prototype must not override current implementation evidence.
