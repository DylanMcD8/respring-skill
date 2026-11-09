# Package validation

Prepared 25 October 2026.

- Read the Codex skill-creator guidance and an existing workflow skill to inform discovery, progressive references and verification structure.
- Synthesized both engineering reports, including explicit failed experiments and evidence limits; kept private raw reports outside the package.
- Checked all 126 public-source file hashes in the manifest against retained local repository files.
- Ran the package validator and Codex skill-creator's structure validator. Exercised the package validator with clean, broken-link and missing-entry-point fixtures.
- Reviewed the behavioral scenarios against the main workflow and references.

The checks validate documentation packaging and provenance, not game compatibility. No game builds, device tests, remote service tests or independent agent evaluation were run for this skill. Remote source links are commit-pinned pointers constructed from recorded metadata; they were not all fetched again. The skill has not been installed globally.

## Report library update — 9 November 2026

Added a canonical copyable report prompt, its README copy, reporting workflow and two sanitized public report editions covering seven apps. Read the source reports and reviewed publication edits; replaced private source links with pinned public links or explicit unavailable-evidence labels, removed unnecessary personal context and specific personal progress values, and retained technical limitations. Original private reports were not changed.

Ran the offline package validator and skill-creator structure validator. Checked report links against the existing public evidence manifest, reviewed staged text for private paths/identifiers/secret markers, and tested validator acceptance/rejection for URI links, broken local links and mismatched prompt copies. These checks are heuristic, not a guarantee of anonymity. Source snapshots and game test results remain those of the original reports; no app builds, device tests or historical benchmark reruns were performed for this update. No release tag was changed.
