# Framework Architecture

The deeper companion to `CLAUDE.md`. Read CLAUDE.md first.

## Layers

```
                  ┌──────────────────────┐
                  │       Tests          │   pytest discovers under projects/**
                  │  (project-tagged,    │
                  │   device-typed)      │
                  └──────────┬───────────┘
                             │ uses fixtures
                  ┌──────────▼───────────┐
                  │      Fixtures        │   framework/fixtures.py + root conftest.py
                  │  device, transport,  │
                  │  ui, bos             │
                  └──────────┬───────────┘
                             │ resolves via registry
                  ┌──────────▼───────────┐
                  │      Registry        │   projects/<name>/devices.yaml
                  │  Project, Device,    │   framework/registry/
                  │  Transport, UI       │
                  └──────────┬───────────┘
              ┌──────────────┼──────────────┐
              │              │              │
       ┌──────▼─────┐  ┌─────▼──────┐  ┌────▼──────┐
       │ Transport  │  │     UI     │  │    BOS    │
       │  ssh, adb  │  │ android,web│  │   audits  │
       └────────────┘  └────────────┘  └───────────┘
```

## Test selection

Two orthogonal axes: **project** and **device type**.

- Markers: `@pytest.mark.project("translink" | "common")` and `@pytest.mark.device_types("TVM", "POS", ...)`.
- Root `conftest.py`:
  - Filters tests by `PROJECT` env var (deselects tests for other projects; keeps `common`).
  - Parametrizes the `device` fixture across every device in the project that matches the test's `device_types`.
- Result: one test definition can produce N test invocations — one per matching device.

## Adding a project

1. Create `projects/<name>/devices.yaml`.
2. Create `projects/<name>/tests/` (can start empty).
3. Optionally create `projects/<name>/conftest.py` for project-specific fixtures.
4. Run: `$env:PROJECT="<name>"; pytest`.

## Adding a device

1. Append to the project's `devices.yaml`.
2. If the device introduces a new transport or UI kind, that's a framework change — use the `framework-architect` subagent.

## Adding a test

Use the `test-author` subagent (`.claude/agents/test-author.md`).

## Why this shape

- **Registry as YAML:** infra people manage devices, not by editing Python.
- **Markers as the only project/device coupling:** no per-project test trees needed for shared code; `_common/` carries the cross-project suite.
- **ABC at every boundary:** swapping ADB for `fastboot`, or Appium for `uiautomator2`, is a one-class change.
- **BOS as a first-class fixture:** the audit verification is the test's reason to exist; making it ergonomic is the whole point.

## BOS auth flow

Devices in the field authenticate to BOS via Keycloak (per the on-device `backofficeagent.config.json`). For tests, the framework mirrors that:

```
test → bos fixture → BOSClient ──┬─► Keycloak realm /protocol/openid-connect/token
                                 │     (client_credentials or password grant)
                                 └─► BOS API with Bearer <access_token>
```

`KeycloakTokenClient` caches the access token until 60s before expiry. Credentials come from env vars (`KEYCLOAK_CLIENT_ID/SECRET` or `KEYCLOAK_USERNAME/PASSWORD`); the realm URI comes from the project's `devices.yaml`.

Override path for early bring-up: set `BOS_API_TOKEN` to a static bearer token; the client uses it directly and skips Keycloak.

## Open questions

- BOS audit endpoint path + query shape — TBD with George.
- Keycloak realm/client to use for the *test framework* (the `TranslinkDevices` realm is for device onboarding; tests likely need a service account in that realm or a sibling realm).
- Whether tests should run in parallel across devices (`pytest-xdist -n auto`) or serially per device. Likely depends on whether actions interfere (printing, money handling). Default to serial until proven safe.
- Per-device locking when running parallel tests — needed once xdist is on. Out of scope for v0.1.
- On-device audit verification: read `Audit/BOSRecords` from the device over ADB as a complement to (or fallback for) the BOS API check. Useful when BOS is slow, batching, or unreachable — the device's local ledger should still have the record.
