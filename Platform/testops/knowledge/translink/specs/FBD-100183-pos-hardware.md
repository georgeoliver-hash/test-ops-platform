# FBD-100183 — POS Hardware Specification (distilled)

**Source:** `POS Hardware Specification (FBD-100183) V6.00` (16 Apr 2021, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Hardware only — captured for behaviour-affecting constraints (transports, peripheral presence, print/scan capability).

## POS console (Way6)
- POS = standard Flowbird **Way6 ETM** platform with integrated **top-mounted smartcard reader**, desk-fixed via Way6 mounting tray + base plate.
- CPU **1GHz Freescale iMX53 (ARM Cortex-A8)**, **1GB SDRAM**, **128KB FRAM**. (Confirms the POS is the Way6 platform referenced in the POS_WAY6 memory notes.)
- **Main display 5.7" colour 640×480** + backlight; **secondary passenger display 2 rows × 16 chars**.
- **Contactless smartcard reader: Mifare CLRC663**, supports **Mifare 1K/4K, Ultralight, Desfire**; **ISO 14443 2-4** compliant.
- Storage/comms: **two 4GB SD cards**, **4G modem** (cellular), **Ethernet**. Interfaces: **2× RS485, 1× RS232, external USB** on the tray.
- Printer: **K60 thermal**, max **150 mm/s**, **50mm paper roll** (width-constrained, length-unconstrained roll → matches the Ticket Editor "length 0 = no length limit" rule and the shared POS/ETM printer spec).
- Power: 24V desktop PSU → Way6 tray, IEC + UK plug to mains. Locks into tray with a security key.

## Peripherals (presence affects available behaviour)
- **External passenger display — Bixolon BCD-2000** (grey): only **80 of the POS estate** get one (vs the integrated 2×16 display on every console). Visual area allows **4 lines × 30 chars**. USB-powered via the hub, screwed to desk (M3).
- **Payment terminal — Miura M020**: contactless EMV, chip & PIN, mag-stripe. **EMV L1, EMV L2, P2PE certified**; **ISO 14443 A/B**. 2.3" 240×320 display, 0–9 keypad + red cancel / yellow clear / green enter. Connects via desktop cradle → **USB** through the hub. **Required for card payment/refund** (see refund spec: card refund needs live PSP/network).
- **Barcode reader — BCR002 (Zebra DS457 fixed-mount)**: decodes all major **1D + 2D** (QR, **Aztec**, DataMatrix); reads **paper and phone-screen** barcodes. Connects/powered via **RS232 (2m)** direct to the console (not USB). Mounted customer-side. (Aztec support aligns with FBD-100167 barcode validation.)
- **USB hub — StarTech 4-port USB 3.0**, own 5V UK-plug PSU; aggregates passenger display + payment terminal.

## Unit volumes (Appendix A — scope indicator)
- POS consoles **160** (143 live + 17 spare); PSUs 160. **M020 payment terminals 95** (76 live + 19 spare); cradles/mounts 95; **barcode readers 95**; **passenger displays 80**.
- **Implication:** not every POS has a payment terminal (95) or external passenger display (80) — **card payment and external-display behaviours are configuration/hardware-dependent, not universal** across the estate.

## Environment
- Console + all peripherals are **indoor-office** rated only.

## Suite implications (POS suite 30253)
- Ties test assertions to **real hardware capability**: card refund/payment cases require the **M020** (present on ~95 units, not all) and a live network; barcode-scan cases rely on the **BCR002 (RS232)** with **Aztec/QR/DataMatrix + phone-screen** reads; contactless smartcard cases assume **Mifare CLRC663 / DESFire/Ultralight**.
- The **shared K60 printer + 50mm roll (width-constrained, length-unconstrained)** underpins the FBD-100363 POS↔ETM shared-template rule — print-layout cases can be reused across POS and ETM.
- Flag **peripheral-optional** behaviours: POS without an M020 (cash-only site) and POS without the external Bixolon display — coverage should not assume every POS can take card or drive a 4×30 passenger display.
- Mostly reference material; no standalone device-behaviour cases required beyond capability preconditions for functional cases.
