# Timing, interaction energy, and measurement

## Separate the clocks

Instrument timer callbacks, simulation steps, render submissions, display-link callbacks, input delivery and audio production separately. Define whether FPS means callbacks, accepted buffer submissions, GPU completion or physical scanout. A count of draw markers is not necessarily a count of frames.

Determine whether updates use elapsed time, discard it, or mix fixed and variable coefficients. Chuzzle ignored its delta argument; 120 updates doubled gameplay. Rendering 120 with 60 updates did not create intermediate animation poses, so 60 remained the retained policy. Interpolation requires state suitable for interpolation; do not insert extra physics steps merely to fill display refreshes.

Koi's original timer was 24 Hz even though some fixed steps were 1/30. Preserve observed original speed, not a guessed intended cadence. Its enhanced patch used `r=24/targetFPS`: linear steps ×r, spring strength ×r², damping `0.96^r - 1`, smoothing `1-0.93^r`, random acceleration ×r^1.5. These are **case-specific approximations**, not a generic integrator recipe or bit-identical result. Retain an original-mode control and derive another game's coefficients from its equations.

Test stalls, resume and irregular deltas. Avoid unbounded catch-up after backgrounding. Keep power/thermal policy separate from game time and report effective rate rather than a requested ceiling.

## Event-rate-dependent effects

For dragging bugs, separate position updates from forces and one-shot impulses. Ask whether the symptom follows event frequency, velocity, distance, duration or frame count. Compare stationary hold, slow/fast drag, one tap, multiple fingers and synthetic irregular input.

Koi's repeated move impulses injected excess ripple energy at high input rates. The retained helper keeps per-touch timestamps and scales repeated strength-1 moves by `clamp(deltaSeconds*24,0,1)` in enhanced mode. Initial strength-2 touches and rain/fish slots remain unchanged, sparse events never amplify, and positions stay responsive. Original mode remains unchanged.

Test 24/60/120/240-event streams, fresh touches, independent slots, cancellation and pauses. A different app may need distance normalization or accumulated impulses per simulation step. Do not throttle all input or weaken every event to hide the bug.

## Performance workflow

Measure cold host launch, Play-to-first-frame, interactive readiness, gameplay and individual menus separately. A loading animation can become smoother while actual startup gets slower. Peggle used the observed loader-thread lifetime to reduce startup contention, then restored normal pacing. Avoid guessed startup sleeps and global speed changes.

Profile CPU emulation/translation, API dispatch, texture uploads, copies/readbacks, draw/state volume, waits, logging and UI traversal. Optimize measured costs before broad code conversion. Menus can cost more than gameplay through interpreted glyph lookup and many small draws. Verify static native archives actually relink after changes.

For each comparison record device/OS, source build, exact scene, resolution, original/enhanced policy, power/thermal state, diagnostics, duration, warm-up exclusion, sample count and metric. Keep settings and scene comparable; label historical/user observations separately from controlled tests. Prefer distributions/frame-time outliers to a single peak FPS. Simulator slowness is not a hardware benchmark.

Historical Chuzzle and Skee samples improved from roughly mid-20s to near60 submissions after direct presentation; these motivate investigation, not a performance guarantee. Peggle reports of near120 gameplay and slower menus were user observations, not a controlled table. No source counts or benchmark in this skill establish a universal native percentage.
