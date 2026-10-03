# VERSA UI V4 — approved pixel portrait direction

Based on dev commit 2a1657cbf952d5eed335bae4774e5f8566956e11. Saved on a separate review branch; not merged or deployed.

## Scope
- Compact dark/gold application layout, mode/topic/persona controls and anchored composers.
- Nine AI-generated pixel portraits, selected figure panel and two/three-person debate lineups.
- Existing backend, API contracts and persona definitions unchanged.
- Portrait masters in assets/portraits. The application HTML embeds the images to remain compatible with existing asset routing.

## Artwork
Generated with OpenAI image generation. Marx is the approved style reference. All portraits are illustrative, not authenticated historical portraits. Ancient/medieval figures are interpretive depictions. Artwork was approved by the project owner in chat; no claim of verified historical likeness.

## Testing and limitations
Local Chrome/Flask testing with explicitly mocked provider responses: 324 recorded checks passed across UI, figure mapping, offline assets and backend fixtures. No real conversation-provider calls were made. Tested viewport widths 320, 390, 768 and 1440; ordinary PDF exports tested. Vision inspection was unavailable, so no independent likeness approval is asserted.

Existing backend security and PWA issues identified in the separate audit are outside this visual-only change. This branch is not a production security release. Embedded original-resolution PNGs make the HTML large; optimize asset delivery before a public release. No secrets, local configuration, environment directories, or generation request metadata are included in this change.
