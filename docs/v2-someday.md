# Madame Minou: V2 / Someday

*The future-growth doc. Everything here is deliberately OUT of the 14-day hackathon scope. Kept separate so v1 stays clean and the MUST line stays honest. Most of these are STUBs in v1: a comment, a paywall moment, a note in the README. Build later, when enthusiasm and runway are present.*

*Last updated: June 23, 2026*

---

## The rule for this doc

If it's here, it is NEVER in v1, but it can have a **stub** in v1 (a comment with implementation notes, a disabled UI state, a documented "coming soon"). NEVER means never for the behavior in this sprint, not never for the life of the app.

---

## Accounts and identity

- Real user accounts (Cognito or equivalent).
- The moment accounts exist, cross-device sync becomes possible and localStorage stops being the source of truth.
- v1 stub: a "Sign in" / "Create account" button that opens a "Premium, coming soon" panel.

## Cross-device / premium tier

- Use Madame Minou across phone, laptop, tablet, with the cat profiles and behavior history following the user.
- This is the headline premium feature. localStorage is single-device by nature, so cross-device *requires* accounts.
- v1 stub: paywall moment in the UI, no real payment, no real sync.

## Real monetization

- Actual subscription billing (Stripe or equivalent) for the premium tier.
- Metered behavior reads beyond the free daily allowance.
- Free trial logic (e.g. 7 days, then convert).
- v1 stub: show the gate and the upgrade prompt, comment-stub the payment integration. No payment processor wired this week.

## Expanded shareable cards

- A library of card styles beyond the v1 count.
- Seasonal/event cards (Halloween tuxedo, Bastille Day beret, "Mercury retrograde survival" card).
- Animated or video cards for social.
- v1 ships 1 (or a small set) of polished styles; everything beyond that lives here.

## More delivery channels

- Push notifications (needs a PWA or native app).
- SMS nudges (expensive, premium-only if ever).
- In-app notification center.
- v1 is email only.

## Multi-cat households

- More than one cat per owner, each with its own chart and behavior log.
- Comparative reads ("your two cats are in a Mars square this week, expect chaos").
- v1 assumes one cat in the core demo.

## Behavior history and trends

- A timeline of logged behaviors with astrological context over weeks/months.
- Pattern surfacing ("she gets clingy every full moon" as an observed, owner-confirmed pattern).
- This is where the genuine positive-impact story deepens: longitudinal observation can flag real health changes early. Powerful, but it needs persistence and accounts, so it's v2.

## Community / broader theme angles

- **Adopt-a-Minou (parked).** Originally a v1 secondary feature; replaced in v1 by the quiet in-Penelope's-memory hospice acknowledgment (see what-she-is). Could return later as an option: seeded local adoptable cats, or a live shelter API (Petfinder / RescueGroups, longevity-check first) with adoption-promo cards. Not a priority; the memorial angle is the current heart.
- Shelter and rescue tie-ins more broadly (TNR mapping, shelter volunteer coordination).
- Cat-lover community board around shared cards.
- The seeded v1 version proves the concept; the live-API + national reach is the v2 lift.

## Platform / distribution

- Native mobile app.
- PWA install.
- Public API for cat astrology data (ties to the "for developers" theme bucket).

---

## Parking lot (unsorted, revisit later)

- Voice INPUT (user dictates answers to the consultation). Speech-to-text for the cat name is cute, but the birthday is a parsing trap and browser support is uneven, so it stays v2. (Note: audio OUTPUT, Madame speaking via AWS Polly French neural, was pulled forward to v1 as an optional opt-in button. See what-she-is.)
- Breed-specific flavor packs.
- Gift a reading.
- Memorial mode: a quiet way to keep a passed cat's chart (this one is close to the heart, handle with care).

---

## Why this separation matters

v1's job is to win a 14-day hackathon: one core loop that works, polished, secure, documented, demo-able. Every item above is a reason to be excited later, and a reason to *not* get distracted now. The strongest v1 is a small thing done completely, with this doc proving the thinking went further than the build did. That's a Documentation and Innovation asset on its own: "here's the roadmap, here's why I drew the line where I did."
