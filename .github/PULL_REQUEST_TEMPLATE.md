<!-- What does this change, and why? One or two lines. -->

## Summary

## Checklist

- [ ] `bash scripts/validate.sh` passes (manifests parse + versions match, zero external links in `skills/`, every reference mapped in SKILL.md, frontmatter present, prose lint clean)
- [ ] Any new/changed reference file has its **Ask first** note **and** a row in the SKILL.md reference map
- [ ] Any new command has a `description` + `argument-hint` and is listed in the `help` card
- [ ] If content or the command set changed, the version is bumped in **both** `plugin.json` and `marketplace.json`, and `CHANGELOG.md` is updated
- [ ] Original prose only — no copied *System Design 101* text or images, no external links inside `skills/`
- [ ] Conventional-commit messages, no `Co-Authored-By` / AI-assistant trailer
