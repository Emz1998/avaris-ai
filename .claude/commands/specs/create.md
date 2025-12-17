---
name: specs
description: Create or update specification documents (prd, tech-specs, or ux-specs)
allowed-tools: Read, Write, Glob, Grep
argument-hint: <specs-type>
model: opus
---

<specs-type> $ARGUMENTS </specs-type>

<dependency-chain>
brainstorm-summary.md → prd.md → tech-specs.md → ui-ux.md
</dependency-chain>

<instruction>

- Use `specs-creator` skill to generate <specs-type> specification document
- If <specs-type> is not specified, generate all specification documents (prd, tech-specs, and ux-specs)

</instruction>

<rules> Must use `specs-creator` skill to generate <specs-type> specification document </rules>
