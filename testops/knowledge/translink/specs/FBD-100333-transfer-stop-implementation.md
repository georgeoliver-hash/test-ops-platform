# FBD-100333 — Transfer Stop Implementation (distilled)

**Source:** `FBD-100333 Transfer Stop Implementation Specification V0.03` (1 Jul 2021, K. Horton).
Distilled testable facts only — raw spec held locally, not committed. Related documents: None cited.

> **Maturity warning:** This document is an **unfinished template stub (v0.03)** — nearly all body sections
> are placeholder "Text [Insert…]" boilerplate. The only real content is three requirements, a constraint,
> and two worked scenarios. Treat rules below as **draft / needs-confirmation**, not settled behaviour.
> The concrete transfer logic that actually shipped lives in the Tap-On specs (Glider transfers in
> FBD-100651 CR123; free bus↔rail transfers in FBD-100690 CR133/CR064). Cross-check before authoring.

## Requirements captured
- **REQ-2121.2** — Staff can flag routes known to issue **paper transfer tickets** so the passenger-journey / revenue-reporting system can **reallocate paper-ticket revenue**.
- **REQ-2121.3** — Staff can identify **transfer points** on a route.
- **REQ-3425.0** — Admin can **configure routes that include transfers**, so that when a passenger transfers **within the configured transfer time** the correct fare is retrieved.

## Core rule (constraint)
Two ABT journeys are treated as a **single transaction for fare calculation only if the second boarding is within a configurable "transfer time" variable** of the first; outside that window they are calculated **separately/individually**.

## Worked scenarios (fare-matrix behaviour)
- **Scenario 1 — single through journey** (A→C, e.g. Belfast→Portaferry): ABT finds the established A→C fare directly. No issue.
- **Scenario 3 — two buses, two legs** (A→B then, within transfer time, B→X; e.g. Holywood→Bangor then Bangor→Newtownards): **no A→X fare exists** (no such service) ⇒ ABT charges them as **two separate fares even though within the transfer time**. (Note: spec's own numbering skips "Scenario 2".)

## Suite implications (ABT/BOS suite 30279)
- **Low authority — do not base new cases on this stub alone.** Use it only for the *intent* (configurable transfer time; through-fare vs two-leg fare-matrix lookup; paper-transfer-ticket revenue reallocation) and take actual transfer behaviour from FBD-100651 / FBD-100690.
- The one durable, testable idea worth a case: **when no combined origin→final fare exists in the matrix, two legs within the transfer window are still charged as two separate fares** — a boundary that contradicts a naive "transfer = always one fare" assumption. Worth an explicit assertion.
- **Coverage gap flag:** paper-transfer-ticket **revenue reallocation** (REQ-2121.2) and staff configuration of **transfer points** (REQ-2121.3) are not elaborated anywhere in the Tap-On specs — likely genuinely uncovered; mark as "needs requirement clarification" rather than authoring speculative cases.
