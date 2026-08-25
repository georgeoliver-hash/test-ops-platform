# FBD-100363 — Translink Ticket Editor (distilled)

**Source:** `FBD-100363 Translink Ticket Editor Specification V1.00` (8 Dec 2021, C. Warnes).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Requirements: REQ-1750.x, REQ-1774/1775/1779. Ticket Editor is a **CloudFare back-office tool** (device config), not on-device.

## What it is / device coverage
- CloudFare tool to build ticket **templates** from drag-and-drop building blocks with a live preview, for all four printing device types: **ETM, HHD, POS, TVM** — same UI regardless of device.
- **Separate templates per device type** because paper stock differs — **EXCEPT POS and ETM, which share the same printer spec** and can share a template (create for one, copy and switch device type to the other).
- On create: user supplies **template name + device type**; device type drives which **fonts** load and pre-loads **width/length/orientation** constraints. User may override defaults but **cannot exceed a constrained dimension**.

## Element types (testable behaviours)
- **Fixed/Free text:** manually typed; user picks font + justification (left/right/centre). Also used as labels preceding dynamic data ("Driver No: 1234").
- **Dynamic field:** device property (fare, boarding/alighting stage, route). Selected from a dropdown; shown **green** in preview. **Width must be set to the max character count — field is truncated at print if content overflows.** **No validation** that the property will exist at print time (e.g. BoardingStage on a Technician test-print with no signed-on route may error). Some dynamic fields emit **expiry/journey-low messages** ("Your card will expire on xxxx"), controlled by **CloudFare device-settings thresholds**.
- **Multi-line:** for list properties (e.g. end-of-shift operator totals); user sets number of lines. **Not recommended on length-constrained devices.**
- **Optional field:** context-dependent dynamic field, printed **only if applicable at runtime** (e.g. smartcard PSN only when a card is used; Euro cost only cross-boundary). Shown with **asterisk (*)** in dropdown and **red** in preview. **Device decides** whether to print it; **whitespace auto-removed when not printed** (no wasted paper). Avoids duplicate templates for cash vs smartcard variants.
- **Whitespace / new lines:** implicit from element placement; explicit trailing whitespace via blank free-text fields.
- **Separator lines:** point-and-click line tool; horizontal or vertical; width/length set; drag to place.
- **Barcode:** placement tool drops a **size-accurate representative image** (content illustrative only — device generates the real barcode per its config). **Advised to place at the very end of the ticket** — device currently only processes/prints the barcode at the end. Whitespace border (esp. above/below) auto-added by device and mirrored in preview.

## Editing behaviours
- **Drag-and-drop with an overlay grid** for alignment; double-click any element to edit its font/justification.
- **Instant preview**, bound to entered dimensions. Not true WYSIWYG (device fonts vary) but an accurate approximation.
- **Resize origin is the top-left corner** — reducing width trims the right edge; reducing length trims the bottom.
- **Delete** any highlighted element; **Ctrl+Z** undoes the last delete/move.

## Constraints
- Width/length constraints per device from config; **where none is set, that dimension is unlimited** (e.g. Way6S ETM roll = width constrained, length unconstrained → length 0 disables length validation). Exceeding a constraint → user informed, **max constrained value used instead**.
- **Orientation** default per device is auto-set but **overridable** (with a caution — wrong orientation misprints).

## Fonts / logos / dynamic properties (hierarchy + overwrite)
- **Fonts, logos, and dynamic-property lists** are all imported via Ticket Editor and **assigned to the device type chosen at template creation**; only assets for that device type are selectable.
- **Fonts must be loaded before adding text elements.** No validation that a font suits the printer (unsupported font may error at print). Multiple fonts per device = size/weight variants of one base font (e.g. Way6S ETM = Arial 8/10/12/Bold).
- **CloudFare hierarchy import rule:** an asset imported at the selected level is available **at that level and all sub-levels**. Publishing at **Metro** makes the template assignable to Metro products only; publishing at **Translink** (top) makes it available to both Ulsterbus and Metro.
- **Same-name import at the same level OVERWRITES** the existing font/logo (a same-named font imported at the higher Translink level does NOT overwrite a Metro-level one — level matters).
- Dynamic properties are maintained by **Flowbird**, typically applied to all device types, each with a friendly name shown in the dropdown.

## Save / publish / create-edit-copy
- **Save** = keep working state; **Publish** = make available in the **Product Editor** for assignment to a ticket type / product class (confirm dialog shows template name + device group).
- Three entry actions: **Create** (blank, per device type), **Edit** (open existing from dropdown), **Copy** (clone existing → name gets `_copy` suffix; device type can be changed e.g. ETM→POS; paper dimensions + orientation copied and NOT editable on a copy). **Unique naming is advised but NOT enforced.**

## Product Editor / Text1–Text8
- Templates are assigned to a ticket type/product class in the **Product Editor** (dropdown filtered to templates matching the selected device tab).
- **Text1–Text8**: product-specific static free-text fields. A template's `Text2` optional element resolves per product (Adult product Text2 = "Go Party", Child product Text2 = "Stay Safe") — lets one template serve multiple products. Presented as dynamic properties in the Ticket Editor list.

## Suite implications (POS suite 30253 + ETM/HHD/TVM print)
- Ticket Editor is a **BOS config tool** — most cases are back-office, but it defines **what the POS/ETM actually prints**, so template rules underpin on-device print-verification cases (Screen/Print Validation).
- Assert the **POS/ETM shared-printer** rule (one template can serve both via copy + device-type change) and, conversely, that TVM/HHD need their own templates.
- On-device print cases should cover **optional-field runtime behaviour**: optional field printed only when applicable (smartcard PSN present, Euro cost cross-boundary) with **whitespace collapse** when omitted — a likely gap.
- Cover **dynamic-field truncation** (content longer than the configured field width) and the **no-print-time-validation** failure mode (BoardingStage with no signed-on route).
- Cover **barcode-at-end** placement dependency (device only prints barcode at ticket end) — ties into FBD-100167 barcode suite.
- Assert **Text1–Text8** substitution per product on a shared template.
- Hierarchy publish/overwrite and same-name asset overwrite are BOS-admin cases (note for ABT-BOS/config suite, out of pure device suite).
