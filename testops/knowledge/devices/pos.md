# Device: POS (Point of Sale)

Facts a `gherkin-author` may rely on when drafting POS cases, so drafts are grounded rather than
invented. Seeded from the `automation-tests` Translink POS area.

## What it is

- Point-of-Sale terminal. Translink variant: **INF212, Way6, Android**.
- Operators **sign on** with an ID + PIN, reach a **main menu**, then perform transactions
  (top-up, basket/payment, annulment), printing, and read status panels.

## Feature areas (use as `@feature` tags)

`auth` (sign on/off), `transactions` (top-up, basket, confirm payment, annulment, advance ticket
date), `printing` (receipts), `provisioning` (dataset parameters), `status` (device / paper /
smartcard / other-devices panels), `options` (volume/brightness).

## Known behaviours to write against (grounded)

- **Sign-on screen** shows an **"ID"** label and a **"PIN"** label.
- **Valid sign-on** → main menu, and emits a **`state.changed`** entry in the device EventLog
  (assert within ~15s).
- **Invalid sign-on** → a **"Sign On Failed"** dialog; the operator is not signed on. This path can
  leave the device needing a power cycle → mark such cases **`@destructive`**.
- Tests should first `ensure signed off` so prior session state doesn't leak into the next case.

## Audit / BOS

- Device-side audit goes through the **EventLog**; events are correlated against BOS
  (`uktest-tl-env5`, Keycloak realm `TranslinkDevices`).
- Only assert audit events you can name from EventLog/BOS evidence. Do not invent event names.

## Terminology to keep consistent

- "sign on" / "sign off" (not "log in"), "main menu", "operator", "EventLog", "Sign On Failed"
  dialog. Match the on-screen strings exactly when asserting labels.

## Source of truth

`C:\Users\GeorgeOliver\dev\automation-tests\projects\translink\tests\` — the real automated tests.
When in doubt about a behaviour, read the corresponding test body there rather than guessing.
