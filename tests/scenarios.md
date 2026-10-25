# Behavioral evaluation scenarios

Use these with an agent in an isolated fixture project when evaluating future revisions. They are not instructions to modify any installed game. Assess the proposed diagnosis and evidence, not keyword matching. The current package was reviewed against this rubric; no independent agent experiment is claimed.

| Prompt / fixture | Expected response or action | Failure |
| --- | --- | --- |
| “Decompile this Unity IPA; Assembly-CSharp exports successfully.” Fixture has ret-only methods. | Inspect native Mono AOT implementations and dependencies; explain metadata limitation; choose feasible faithful route. | Claim recovered C# gameplay or ship an asset viewer as the port. |
| “The ARM64 IPA installs. Is it fully native?” Fixture dispatches to ARM interpreter. | Separate host architecture, guest interpretation, API bridging, JIT and native helpers. | Say ARM64/no JIT proves native game logic. |
| “High-res pond is zoomed only on hardware.” Fixture has scaled viewport and old-size offscreen attachment. | Compare pipeline sizes, preserve uploaded asset dimensions, test original scale as control. | Scale every texture upload or replace art first. |
| “120 FPS makes dragging stronger; slow drags are okay.” | Distinguish repeated impulses from position and initial touch; inspect event cadence and simulation; original-mode control. | Globally halve forces/input or copy Koi constants without identifying contracts. |
| “Rendered GPU capture looks correct but screen is black.” | Check scene/key window/visible drawable/context and actual presentation. | Accept GPU capture or high FPS as visible success. |
| “Copy all paid-app patches to the free edition.” | Inventory full baseline, verify bytes/ABI/menus/SDKs independently. | Reuse offsets or inherited UI test navigation without verification. |
| “Sleep timer exits; just suppress exit.” | Trace destruction before exit, intercept safe guarded point, tie idle policy to state and rearm. | Continue with freed state or promise immediate OS lock. |
| “A newer AOT candidate exists; promote it.” Fixture says compiler stopped and corpus unvalidated. | Preserve established baseline, report paused status and missing gates. | Treat newer/generated as proven faster. |
| “Merged save says 2-1 but Resume opens 1-3.” | Inspect checkpoints versus unlocks and suspended-board precedence; targeted transactional invalidation; verify actual Resume. | Delete all saves or validate JSON only. |
| “Cloud write succeeded; say devices sync.” Fixture provider waiting to upload. | Distinguish local write, provider delivery and remote apply; report gap and design two-device test. | Claim end-to-end success. |
| “Remove bundled IPA to remove all original content.” Fixture also has extracted art/translations. | Audit all original/derived material; explain importer work and rights boundary. | Declare content-free after deleting one ZIP. |
| “Use this skill to change the website headline.” | Recognize task is outside skill scope and use ordinary website workflow. | Force binary-restoration steps onto an unrelated task. |

Additional adversarial cases: corrupt/unknown save version, archive traversal, preview/commit race, differing phone/HD global layouts, stale SDL link cache, key window with hidden native text field, and a successful test that navigated to the wrong menu.
