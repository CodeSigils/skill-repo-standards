# Evidence-appraisal profile

Use this compact profile for a new behaviour-changing decision. It records a
human appraisal without claiming that a validator can determine whether that
appraisal is true.

```markdown
- Context: the question, scope, and affected decision
- Evidence appraisal: validity, likely impact, applicability, and material limitations
- Outcome check: the observable result or review that would confirm the choice
- Evidence profile: primary
```

`primary` requires at least one registered `official_docs` source in the
decision's `Sources` field. If no primary source is available, use:

```markdown
- Evidence profile: constrained
- Primary-source exception: why no applicable primary source was available
```

The profile is a structured aid to review, not an evidence score or a claim of
certainty. See [`STANDARD.md` §The anti-rot core](../../STANDARD.md#the-anti-rot-core).
