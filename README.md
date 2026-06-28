# Madame Minou 🐈‍⬛

*"Are cats even real?"*

A daily cat astrology app for people who love their cats and cannot quite figure them out. A French cat astrologer named Madame Minou reads your cat's stars: a deterministic birth chart underneath, her warm franglais voice on top. The astrology is the vocabulary. The structure underneath it is the catnip.

Built for [Hack the Kitty 2026](https://hackthekitty.com) (World Cat Domination Day). Theme fit: a cat-behavior decoder that helps owners understand the most inscrutable creature in the home.

## What's in here

- **`.kiro/`** : the spec-driven build kit (Kiro reads this from the repo root)
  - **`steering/`** : always-on rules the agent follows on every task (principles, security, tech, ui)
  - **`specs/madame-minou/`** : requirements (EARS), design (architecture), tasks (build order), the design system, the Kiro workflow, and the Stitch UI brief
- **`docs/`** : the planning and vision docs
  - `what-she-is.md` : the product spec and every locked decision
  - `build-reference.md` : the Claude-on-AWS integration reference
  - `v2-someday.md` : everything deliberately out of v1 scope
  - `landing-reference.html` : the scaled, cleaned landing reference (open in a browser)
  - `design/` : the Stitch design-system export and landing render
- **`assets/`** : `hero.png` and other media

## How it's built

Spec-driven development with Kiro. Start at **`.kiro/specs/madame-minou/tasks.md`**, Block 0 (the spikes), and work block by block with a PASS/FAIL gate at each boundary. Scope is governed by the **MUST / STRETCH / STUB / NEVER** labels in `requirements.md`.

## Stack

- **Frontend:** static site, café-terrace-at-night world (Van Gogh idiom, original art)
- **Server:** AWS Lambda (Python) + API Gateway
- **Chart engine:** Python + Swiss Ephemeris (deterministic)
- **AI voice:** Claude Platform on AWS
- **Contract:** the chart computes the facts; the model only writes the voice. Determinism is the differentiator.

## Principle

Deterministic structure, AI flavor. Whimsy on top, honest scaffolding underneath. And a line that is never buried: *Madame Minou reads stars, not bloodwork.* She is for delight and for paying closer attention to your cat, not a substitute for a vet.

## In memory

Dedicated to Ms. Penelope Randall (May 2009 to February 17, 2026). Tuxedo. Frenemy. The reason this build exists. **Madame Minou is, and always was, Penelope.** In her memory, a quiet link to [Lap of Love's Angel Fund](https://www.lapoflove.com/angel-fund), the kind of in-home hospice care that let her go gently from home.

---

AI Assisted. Human Approved. Powered by NLP.
