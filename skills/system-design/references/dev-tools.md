# Dev Tools & Productivity

> **Ask first** (`AskUserQuestion`, options + "Other"): branching model (trunk-based vs git-flow), CI/CD platform, and how code ships to prod. They set the team's workflow.

## Git mental model

Three places a change lives before it leaves your machine:

- **Working directory**: files as they are on disk, edited freely.
- **Staging (index)**: the next commit you're composing. `git add` moves a change here.
- **Commit**: a snapshot plus a parent pointer, addressed by a content hash.

History is a **DAG**, not a line: each commit points at its parent(s), a merge commit has two. The rest are movable labels:

- **HEAD**: where you are now, usually pointing at a branch.
- **Branch**: a pointer to one commit that moves forward as you commit.
- **Tag**: a pointer that never moves: pin a release (`v2.3.0`) to an exact commit.

The snapshot model is why branching is cheap (one pointer) and why a "lost" commit is usually still reachable via `git reflog`.

## Merge vs rebase

Two ways to integrate another branch, and they trade the same axis: truthful history vs readable history.

- **Merge**: writes a merge commit joining two lines. History is traceable (you see exactly when branches met) at the cost of a lattice of criss-crossing lines.
- **Rebase**: replays your commits onto a new base, producing one straight line. Readable and bisect-friendly, but it rewrites commit hashes.

Decision: rebase your own local work to tidy it before review; merge to integrate. Never rebase a branch someone else has pulled — rewriting shared history forces everyone downstream into conflict recovery. You give up either a clean graph (merge) or the guarantee that a pushed commit is immutable (rebase).

## Branching strategies

Match the strategy to release cadence and CI maturity, not to fashion.

| Team/context | Strategy |
| --- | --- |
| Small team, strong CI, deploys many times/day | **Trunk-based**: commit to main behind feature flags; branches live hours |
| Most product teams, PR review culture | **GitHub-flow**: short-lived branch per change, merge via PR, deploy from main |
| Versioned releases, QA gates, slower cadence | **Git-flow**: long-lived `develop`/`release`/`hotfix` branches, heavier ceremony |

Trunk-based buys speed and tiny merges but demands flags and a green pipeline to stay safe; git-flow buys release control and staging discipline at the cost of merge pain and slower flow.

**Git vs GitHub**: Git is the version-control tool that runs on your machine. GitHub (or GitLab, Bitbucket) is a host: a remote plus PRs, issues, CI hooks, access control. Git works fully offline; the host adds collaboration.

## Linux essentials

**Permissions**: every file has `rwx` (read/write/execute) for owner, group, other. Octal encodes it as `r=4 w=2 x=1`, summed per role:

- **755** (`rwxr-xr-x`): owner edits, everyone runs. Scripts, binaries.
- **644** (`rw-r--r--`): owner edits, everyone reads. Config, data files.
- **600**: owner only. Secrets, keys.

**Filesystem layout**: `/etc` config, `/var` changing state (logs, spool), `/usr` installed programs, `/proc` a virtual view of kernel and process state (`/proc/<pid>/`), `/tmp` scratch.

**Commands by job**:

- **Inspect**: `ls -la`, `cat`, `less`, `stat`, `df -h`, `du -sh`.
- **Find**: `find . -name '*.log'`, `grep -rn pattern`, `rg` if installed.
- **Pipe**: `cmd | grep x | sort | uniq -c | sort -rn`: chain small tools; each reads stdin, writes stdout.
- **Monitor**: `top`/`htop`, `ps aux`, `journalctl -u svc -f`, `netstat -tlnp`/`ss`.

## Debugging on a box

First read the vitals: `uptime` gives load averages (1/5/15 min); a load above core count means saturation. `free -h` for memory pressure and swap; `top` to find the CPU hog.

Common causes of one process pinning 100% CPU:

- **Busy loop**: code spinning without yielding or blocking on I/O.
- **GC thrash**: heap near full, collector running constantly; check memory before blaming logic.
- **Lock contention**: threads spinning on a contended lock (see os-concurrency.md).

Then follow the logs: `tail -f` or `journalctl -f` while you reproduce, and `grep` the timestamp window around the incident.

## Diagram-as-code

Write architecture diagrams as text and commit them beside the code.

- **Mermaid**: renders in Markdown and PR views; low effort, good for flows and sequence diagrams.
- **PlantUML**: richer UML (class, component, deployment); needs a render step.
- **D2**: modern layout engine, clean output; separate toolchain.

The tradeoff: authoring text is slower than dragging boxes, and complex layouts fight the auto-layout engine. What you get back is a diagram that diffs, reviews in a PR, and never drifts from the code — a binary `.png` does none of these and rots the day someone renames a service.

## Shipping to production

The path: **local → CI → artifact → deploy**. Build and test locally, let CI rebuild deterministically and produce one immutable artifact, then promote that same artifact through environments — never rebuild per stage.

**Feature flags** decouple deploy from release: ship code dark, flip it on for 1% of users, ramp or kill without a redeploy. The cost is flag debt — dead conditionals pile up unless you delete them after rollout.

CI/CD pipelines and deploy strategies (rolling, blue-green, canary) — see devops-k8s.md.
