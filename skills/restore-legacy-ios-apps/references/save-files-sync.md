# Save-file migration and synchronization

Use this module only when requested features require import/export, migration or sync. Basic restoration does not require a new cloud system.

## Model the data before transport

Separate in-game user identity, host transactional generations, preferences, user detail, scores, campaign completion, checkpoint, unlocked level and suspended board/replay. Trace precedence: a newer user record can lose to an older resume file.

Peggle phone/HD shared relevant version-25 serialization semantics, but indexes/preferences/identities were edition-specific. Semantic field keys in disassembly were not serialized byte offsets; variable-length strings move positions. Walk and validate the actual format, version, counts, encoding, embedded structures and exact end. Patch only supported spans, reparse output, and verify untouched bytes remain identical. Unknown versions should fail clearly rather than guessing offsets.

A donor directory can mix user identity, entitlement, theme and progress. Copy only the authorized understood state. Keep original extraction immutable and perform conversions in a temporary working copy. Android backup success in one app/device does not establish universal unrooted extraction; OS confirmation stays on the device, never solicit passcodes in chat.

## Transactional import

Separate preview, validation and commit. Bind the preview to fingerprints/context so changed inputs cannot silently replace reviewed content. Prevent mutation of live guest files with an exclusive session lease or equivalent. Stage a complete approved generation before publishing the active root. Retain recovery information; check fingerprints before rollback so it cannot overwrite subsequent edits.

Reject archive traversal, symlinks, foreign layouts, nonregular files, truncated/oversized data and unreasonable counts. Bound actual reads, not just declared lengths. Select limits based on real formats rather than copying Peggle's constants. Test interrupted writes, repeated import, preview/commit races and rollback after changes.

Treat missing, valid-empty and corrupt indexes separately. Do not manufacture an in-game user to make sync appear successful. Save-manager generation numbers are not users.

## Canonical semantic model

Prefer `local binary -> validated semantic document -> merge -> local adapter` over opaque cross-edition directory sync when only understood fields are portable. Version the schema and explicitly enumerate local-only fields. Preserve unsupported local data.

Peggle's additive model merged checkpoint/furthest progression by maximum, completion by OR, and trophies/cleared/aced levels by union. Verify associativity, commutativity and idempotence in meaning. This cannot propagate resets/deletions or separate unrelated people automatically. Those requirements need identity/conflict/tombstone design, not an extra max field.

When a checkpoint advances, invalidate only its selected user's affected campaign resume board; otherwise preserve it. Verify actual guest Resume after applying. Do not call a JSON merge a successful gameplay migration.

## Capture, apply, transport

A read-only semantic capture can run at a verified safe point with no writer open. Concurrent JSON merging is different from mutating live game files. Apply after ending/restarting the guest through the controlled transaction path. Model disabled/unlinked/checking/pending/deferred/applying/error states, and discard stale async completions after account/folder/context changes.

Link users explicitly; identical names do not prove identity. Explain which completion is combined and whether an unfinished board will restart. Deferred changes are not deletions. Keep automatic success quiet when that fits the product; report actionable errors without exposing internal candidate state.

CloudKit requires actual installed signed entitlements, container access, environment, account and server availability. An Info.plist toggle or copied container name grants none. A capability parser is not OS signature validation. Re-signing can remove entitlement support. Test public distribution separately from a developer's personal build.

For user-selected folder transport: persist/refresh security-scoped bookmarks, balance access, coordinate I/O, handle placeholders/downloads and conflicts, bound reads, serialize writes and use atomic replacement. Distinct per-installation writer files can prevent offline devices from overwriting unseen contributions. Keep writer identity out of backups when restoration must create a new owner. Do not delete other writers on disable/reselection. Treat malformed recognized data explicitly rather than silently publishing a partial merge.

Local coordinated write success is not cloud upload, remote download, or application in the other game. Verify all stages with divergent supported progress on two devices, offline/reconnect, restart/apply and actual guest state. The source Peggle report explicitly did **not** establish end-to-end iCloud Drive delivery; retain that limitation when citing it.
