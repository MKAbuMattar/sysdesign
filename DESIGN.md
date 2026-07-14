---
name: sysdesign
description: Editorial system for a self-contained, tradeoff-first system-design knowledge skill.
register: reference
voice:
  stance: "opinionated senior engineer, not a neutral encyclopedia"
  default: "state the constraint → pick the fitting option → name what you gave up"
  person: "second-person imperative ('reach for', 'don't ship'), never marketing 'we'"
  length: "terse; every sentence earns its place; cut the paragraph that defends a simplification"
structure:
  unit: "one reference file per topic, standalone, ~40–60 lines"
  section: "## H2 per sub-topic; no deep nesting"
  anatomy: "concept → when to use / when not → the tradeoff → concrete example or numbers"
formatting:
  definition-list: "- **Term**: explanation"
  option-table: "| Need | Reach for |  — decision-first, not feature-first"
  emphasis: "**bold** for the named term only; no italics for emphasis"
  numbers: "concrete figures over 'many'/'significant'; latency/QPS orders of magnitude"
  em-dash: "≤ ~3 per 300 words; prefer colon in definition lists"
bans:
  - "external links anywhere inside skills/ (the knowledge is self-contained)"
  - "copied ByteByteGo text or reproduced diagrams/images (CC BY-NC-ND)"
  - "AI tells: leverage/utilize/delve/foster/robust, filler adverbs, negative parallelism"
  - "best-practice lists with no stated tradeoff"
---

# Editorial System: sysdesign

## 1. Overview

**Creative North Star: "The Tradeoff Ledger"**

This skill reads like a senior engineer's notebook, not a textbook or a vendor page. Every
entry states a decision and the price of that decision — the option next to what it costs
you (consistency, ops burden, latency, money). Energy comes from precision and restraint:
short sentences, decision-first tables, concrete numbers. Nothing hedges, nothing pads.

It is built for an agent answering a real design question under real constraints, so it
commits to being **self-contained**: the knowledge lives in the file, never behind a link.
Attribution to ByteByteGo's *System Design 101* is one line; the prose is original. This
system rejects the **listicle** reflex (a wall of best practices with no tradeoff), the
**encyclopedia** reflex (neutral, exhaustive, opinion-free), and the **marketing** reflex
(hype adjectives, "we", CTAs). Reference here is quiet command, not coverage.

**Key characteristics:**
- Tradeoff-first: no option is named without the constraint it fits and the cost it carries.
- Self-contained: zero external links inside `skills/`; a reader never clicks out.
- Terse: dense original prose, tables for choices, numbers over vague quantifiers.
- Consistent house style: colon definition lists, decision-first tables, em-dash discipline.
- License-clean: inspired by *System Design 101*, never copied from it.

## 2. Voice

**Stance:** an opinionated senior engineer who has been paged at 3am. Recommend, don't survey.
**Default move:** state the constraint → pick the fitting option → name what you gave up.
**Person:** second-person imperative ("reach for Postgres", "don't shard before you index").
Never the marketing "we"; never "it depends" without then deciding.

### Named Rules
**The Tradeoff Rule.** A choice named without its cost is unfinished. Every recommendation
carries the thing it sacrifices — a design with no stated tradeoff hasn't been reasoned about.

**The Restraint Rule.** If an explanation is longer than the point it makes, cut it. Every
paragraph defending a simplification is complexity smuggled back in as prose.

## 3. Structure

One topic, one file under `references/`, standalone (~40–60 lines). A file is a stack of `##`
sub-topics, each following the same anatomy: **concept → when to use / when not → the tradeoff
→ a concrete example or the numbers**. No deep nesting; if a sub-topic needs its own tree, it
is probably its own file.

### Named Rules
**The Standalone Rule.** Each reference file answers its topic without depending on another
file or an external page. Cross-reference a sibling by name (`see caching-performance.md`)
only for genuinely adjacent detail, never to complete a thought.

**The Map Rule.** Every reference file has a matching row in the `SKILL.md` reference map.
Adding a file without the row makes it invisible to the router.

## 4. Formatting

- **Definition list:** `- **Term**: explanation` — colon, not em dash. This is the house list.
- **Option table:** `| Need | Reach for |` — decision-first columns (the situation, then the
  answer), never a feature matrix.
- **Emphasis:** `**bold**` for the named term only. No italics-for-emphasis, no ALL CAPS.
- **Numbers:** concrete figures beat "many"/"significant". Give orders of magnitude
  (QPS, GB/day, ns/µs/ms) where a decision hinges on scale.
- **Em dashes:** a real tool, but ≤ ~3 per 300 words. In lists, prefer the colon. Uniform
  `**X** —` lead-ins across a whole list read as machine-generated — use the colon list.

### Named Rules
**The Decision-First Rule.** Tables lead with the situation and end with the call. The reader
scans the left column for their case and reads across to the answer.

**The Density Rule.** Prefer a table or a tight definition list to a paragraph when the content
is a set of choices. Prose is for reasoning; lists are for options.

## 5. Bans

- **No external links inside `skills/`.** The knowledge is self-contained. Attribution to
  ByteByteGo is a single line in `SKILL.md` and nothing more. (`grep -rc bytebytego.com/guides skills` must be 0.)
- **No copied source text or diagrams.** *System Design 101* is CC BY-NC-ND 4.0 — write original
  prose, never reproduce its wording or images.
- **No AI tells.** Banned vocab (`leverage`, `utilize`, `delve`, `foster`, `robust`, `seamless`),
  filler adverbs (`fundamentally`, `essentially`, `ultimately`), and negative parallelism
  ("it's not X, it's Y"). Run the forensic + strict humanizer pass on new prose.
- **No tradeoff-free best-practice lists.** A bullet list of "9 best practices" with no cost
  stated is the listicle reflex this system rejects.

## 6. Do's and Don'ts

### Do:
- **Do** name the constraint, pick the fitting option, and state its cost — in that order.
- **Do** keep every reference file self-contained; the reader never needs to click out.
- **Do** use colon definition lists and decision-first tables; put numbers where scale decides.
- **Do** write original prose inspired by the taxonomy, and attribute ByteByteGo once.
- **Do** run the humanizer (forensic + strict) and validate both JSON manifests before commit.

### Don't:
- **Don't** add external links inside `skills/` or make a file depend on another to be complete.
- **Don't** copy ByteByteGo text or reproduce its diagrams (**CC BY-NC-ND**).
- **Don't** ship a best-practice list with no tradeoff, or hedge with "it depends" and stop there.
- **Don't** use hype vocab, filler adverbs, negative parallelism, or uniform `**X** —` list lead-ins.
- **Don't** create a new skill for a new intent — add a `commands/*.md` wrapper over the one skill.
