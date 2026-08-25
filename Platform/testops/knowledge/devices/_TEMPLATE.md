# Device: <NAME> (<what it is>)

Copy this file to `knowledge/devices/<device>.md` and fill it in. Facts a `gherkin-author` may rely
on so drafts are grounded, never invented. If a fact isn't here and can't be confirmed, the draft
must say `TODO: confirm <x>` rather than guess.

## What it is
- `<one-line description: hardware, OS, who uses it, the core job it does>`.

## Feature areas (use as `@feature` tags)
- `<e.g. auth, transactions, printing, provisioning, status, sync, ...>`.

## Known behaviours to write against (grounded)
- `<screen names, on-screen wording, key flows, error/edge states — quote exact strings where they
  matter for assertions>`.

## Audit / back-office (if applicable)
- `<which actions emit audit/BOS events, how they're verified, event names — name them, don't invent>`.

## Terminology to keep consistent
- `<the exact words used on screen and in cases: e.g. "sign on" not "log in">`.

## Source of truth
- `<where to confirm behaviour: a sibling automation repo path, spec, or the design flows in
  knowledge/flows/>`.
