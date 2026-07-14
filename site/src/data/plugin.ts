// Single source of truth for the plugin's commands, topics, and install steps.

export const commands: readonly (readonly [string, string])[] = [
  ["plan", "design end to end: full interview → complete plan"],
  ["explain", "what it is, when to use it, the tradeoff"],
  ["compare", "options compared, one recommended for a constraint"],
  ["review", "pressure-test a design for SPOFs and safeguards"],
  ["choose", "pick a DB / queue / cache / deploy under constraints"],
  ["estimate", "back-of-envelope QPS, storage, bandwidth, memory"],
  ["tradeoffs", "name what a choice gains and gives up"],
  ["diagram", "sketch the architecture as Mermaid or ASCII"],
  ["interview", "7-step framework, estimates, tradeoffs"],
  ["cheatsheet", "condense an area into a scannable sheet"],
  ["help", "list commands and reference topics"],
] as const;

export const topics: readonly string[] = [
  "api-web", "data-storage", "caching-performance", "distributed-systems",
  "security-auth", "devops-k8s", "architecture-patterns", "case-studies",
  "networking", "os-concurrency", "payments", "ai-ml-systems", "dev-tools", "interview",
] as const;

export const INSTALL_1 = "plugin marketplace add mkabumattar/sysdesign";
export const INSTALL_2 = "plugin install sysdesign@sysdesign";
