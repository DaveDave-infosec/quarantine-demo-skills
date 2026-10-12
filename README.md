# quarantine-demo-skills

Demo fixture for Quarantine, a consensus-driven dependency containment dApp on GenLayer.

This repo holds one agent skill, `skills/payout_skill.py`, across three versions:

- 1.0 is safe
- 1.1 is intentionally compromised for the demo
- 1.2 is the patched release

Advisories live in `security/`.

Do not use this skill in any real deployment. Version 1.1 exists only to be detected and contained.
