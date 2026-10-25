<p align="center">
  <img src="docs/images/RespringSkillHeader.webp" width="800" alt="Respring Skill">
</p>

# Respring — Legacy iOS Restoration Skill

A reusable AI skill for restoring classic 32-bit iOS games while preserving their original behavior. Built from the Chuzzle, Koi Pond, Skee-Ball, Skee Free, Skee-Ball HD, Peggle and Peggle HD engineering reports.

It guides an agent through binary intake, execution-strategy selection, compatibility diagnosis, rendering and timing fixes, bounded native acceleration, save migration, and reproducible delivery. It does **not** include an emulator, automatic converter, game binaries, artwork, original source recovery, or a promise that every app can be restored.

## Contribute to Respring

After successfully converting an app, please consider contributing it to the Respring project! This can include sharing your GitHub repo on this website, adding your findings and work to the skill, or both. Send me an [email](mailto:respring@941archive.com) or [DM](https://twitter.com/DylanMcD8) to get started.

## Install

Copy `skills/restore-legacy-ios-apps` into your Codex skills directory, normally `~/.codex/skills/` (or `$CODEX_HOME/skills/` when configured). Keep its references, assets and agents folders together. Restart or reload your client's skill discovery as needed. Do not overwrite an existing installation without comparing your local changes.

For another agent that supports SKILL.md packages, use its documented skill directory. The Markdown guidance is portable; `agents/openai.yaml` supplies Codex interface metadata.

## Use

Examples:

- “Use $restore-legacy-ios-apps to inspect this IPA and choose a faithful restoration strategy before implementing it.”
- “Use $restore-legacy-ios-apps to diagnose why this port is zoomed on hardware but looks correct in the simulator.”
- “Use $restore-legacy-ios-apps to unlock rendering frequency without changing game speed or drag forces.”
- “Use $restore-legacy-ios-apps to compare these sibling editions and identify which compatibility fixes can transfer safely.”

Give the agent the exact input or existing project, desired behavior, available build environment and target devices. A working Apple toolchain/signing setup is needed for iOS builds; the skill itself is documentation and has no runtime dependencies.

## Contents

- [Main skill](skills/restore-legacy-ios-apps/SKILL.md): discovery and core workflow.
- [Case studies](skills/restore-legacy-ios-apps/references/case-studies.md): what worked, failed, and can transfer.
- [Source provenance](skills/restore-legacy-ios-apps/references/sources.md): pinned source evidence and confidence limits.
- [Investigation record](skills/restore-legacy-ios-apps/assets/investigation-record.md): reusable working template.
- [Evaluation scenarios](tests/scenarios.md): realistic prompts and expected behavioral boundaries.
- `scripts/validate_package.py`: offline structure/link/evidence checks; Python 3.9+ standard library.

The main skill routes to detailed references instead of requiring the agent to load the entire research history. Findings are separated from recommendations, and app-specific constants are not universal instructions. This package contains distilled guidance and public-source pointers, not private development reports or personal test data.

## Validate and maintain

Run `python3 scripts/validate_package.py` from this repository. If Codex's skill-creator tools are installed, also run their `quick_validate.py` against `skills/restore-legacy-ios-apps`.

For additions, record the symptom, exact input/source identity, root cause, guard conditions, test, result, limits and failed counterexample. Add a focused reference and update routing only when the finding changes a decision. Keep the entry point concise. Preserve user preferences as case history, not global rules. Update the evidence snapshot deliberately; branch-head changes must not silently rewrite historical claims.

The evaluation scenarios are a review rubric, not a claim of automated agent or device testing. See [VALIDATION.md](VALIDATION.md) for checks performed on this package.

## Attribution and rights

The implementation examples come from the Respring repositories linked in the source index, which include their own upstream attribution and notices. This package does not relicense those runtimes, original games or assets. No blanket software license is assigned by this preparation; choose a license for this guidance before offering explicit reuse terms. Publishing a GitHub repository by itself does not supply an open-source license.
