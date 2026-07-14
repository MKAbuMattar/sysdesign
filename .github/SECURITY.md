# Security Policy

## Scope

sysdesign is a Claude Code plugin made of Markdown reference files and two JSON manifests. It
ships **no executable code, no dependencies, and no runtime** — so the attack surface is small.
The security concerns that do apply:

- **Malicious content** in a skill/command file that could steer an agent to take a harmful
  action (prompt-injection-style instructions, links to hostile resources).
- **Manifest tampering** (`plugin.json` / `marketplace.json`) pointing installs somewhere unexpected.
- **Supply-chain** of the marketplace source path.

## Supported versions

The latest published version on `main` is supported. Older versions are not patched — update to
the latest before reporting.

## Reporting a vulnerability

**Do not open a public issue for a security problem.**

1. Preferred: open a private report via **GitHub → Security → Report a vulnerability**
   (Private Vulnerability Reporting) on this repository.
2. Alternative: email **info@mkabumattar.com** with a description, affected file(s), and steps
   to reproduce.

You'll get an acknowledgement within **5 business days**. Valid reports are fixed on `main` and
credited in the release notes unless you ask to stay anonymous. Please give reasonable time to
patch before any public disclosure.

## Out of scope

- Findings that require an already-compromised local machine or a modified local copy of the plugin.
- Reports about ByteByteGo or bytebytego.com — this project only references the taxonomy; report
  those upstream.
