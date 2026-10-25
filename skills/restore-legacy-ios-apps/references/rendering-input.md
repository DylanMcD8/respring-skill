# Rendering, geometry, and input

## Track every coordinate space

Write down guest logical canvas, offscreen render targets, viewport/scissor, texture sampling coordinates, drawable backing pixels, UIKit points, scene bounds and device display scale. Physical panel dimensions need not equal the render budget; display scaling can yield larger backing surfaces.

For an original canvas `(Gw, Gh)` and current host area `(W, H)`:

- `fit = min(W/Gw, H/Gh)` preserves all content with letterboxing.
- `fill = max(W/Gw, H/Gh)` uniformly crops while retaining the guest aspect.
- Center offsets are `((W - scale*Gw)/2, (H - scale*Gh)/2)`.
- Inverse mapping is `(hostPosition - offset)/scale` when input is still in host coordinates.

UIKit `locationInView:` may already invert the view transform. Do not invert twice. Reject or intentionally handle touches in letterbox space. Keep host controls and keyboard roots outside the scaled drawable.

Distinguish three changes: more raster pixels; crop-to-fill of the same canvas; expansion of the actual world/layout. None implies either of the others. Settings must say which is enabled and whether relaunch is needed.

## Resolution mismatch diagnosis

Inspect attachments before blaming the final viewport. Koi rendered bed/fish/shadows to an empty texture then distorted it in a water pass. Scaling only the viewport cropped that texture and made objects appear zoomed. The retained fix scaled known empty level-zero render targets, not ordinary uploads with pixel data. Koi required power-of-two scales; Chuzzle allowed integer scales. Neither policy is universal.

Check color/depth/stencil allocation, framebuffer completeness, UVs, scissor and each pass's scale. Test original resolution as a control. A source image's resolution limits texture detail even when geometry and effects render at full resolution. Upscaling assets may damage alpha, atlas boundaries or the original style.

Trace a visual element to font rendering, atlas coordinates, localized bitmap or a UIKit system image before changing it. Chuzzle had RGB plus separate alpha atlases; Peggle ribbon lettering was baked into localized images. Increasing font quality cannot improve precomposed letters. Preserve editable `.icon` source separately from screenshots, iTunesArtwork and web exports.

## Direct presentation

Measure readback/full-frame copy cost. Sharing a texture-backed drawable can avoid expensive copies, but requires correct context, attachment lifetime and host/guest state separation.

Preserve bindings, active/client texture units, coordinate arrays, color masks, viewport/scissor and every state touched by the presenter. Recreate dependent targets on size changes if the design supports live allocation. Restore the previously bound renderbuffer/framebuffer after querying actual backing metrics.

Unity once reused texture name 1 and replaced a host texture with a 4×4 image. A high-number reservation fixed that specific port; robust shared runtimes need namespace ownership/virtualization, not faith that large names never collide. Validate actual visible content: a blank frame can report excellent FPS.

## Black screens and modern windows

Check in order: guest progress/panic, foreground scene attachment, key window, visible view hierarchy, current context, actual drawable backing, framebuffer state and successful presents. GPU capture can contain valid frames while the attached screen stays black. A native launch/management screen does not validate the game's separate GL view.

Use the actual foreground `UIWindowScene` and its current geometry. Avoid cached startup `UIScreen` dimensions or display-0 identity assumptions. Reset transforms before updating bounds/center, then reapply. Use supported current SDK/Info.plist behavior for fullscreen/resizing; merely raising the SDK version may leave compatibility presentation active. Verify the selected platform's current requirements rather than copying historical version literals.

Test cold launch on each display as well as portrait → landscape → portrait and live fold/unfold/window resizing. A launch-selected render scale can coexist with live presentation changes; document whether pixels reallocate.

## Expanded 3D world with fixed UI

Skee's accepted hybrid expanded perspective world projection/viewport in both axes while retaining a centered original orthographic UI. Input and scissor followed that geometry. Simply enlarging guest height broke menu layout.

Treat perspective/orthographic classification as an app-specific heuristic. Verify menu, HUD, modal, gameplay, prizes, edge targets and both orientations. An old iPad's 4:3 ratio can conceal problems on a modern 13-inch model; test a different aspect, compact window or 11-inch display. Supply consistent legacy device identity when the game chooses iPad prefabs through UIDevice/sysctl/uname; writing host output without copying it into guest memory is insufficient.

## Keyboard and gesture ownership

Peggle's native keyboard failed because SDL focus depended on cached screen equality. Focus should follow the actual key window. A stable root owns the hidden text field while GL children change. Validate responder acceptance, visible keyboard, forwarded text/Return and persisted guest user independently. XCTest `typeText` failing to target a hidden field is not proof that actual keyboard input fails.

Keep touch cancellation, multiple fingers, realistic drag duration and post-rotation mapping in coverage. Home-gesture deferral is product-specific: useful for upward Skee throws, unnecessary for the final Koi/Chuzzle design. Do not copy it into every app.
