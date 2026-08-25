# FBD-100293 — Product Group Usage (distilled)

**Source:** `Product Group Usage Specification (FBD-100293) V3.01` (30 Aug 2022, S. James).
Distilled testable facts only — raw spec held locally in `dev/translink-requirements/`, not committed.
Product groups control **how products are laid out and selected on each device**. Related: FBD-100261 (Multi-Journey uses these), FBD-100296 (route Product Group attribute), FBD-100268 (Product Category).

## The 4 product-group types
- **FLU** — ordered scrollable list of products/product groups (touchscreens, HHD). May contain any products or groups.
- **Menu** — assigns each item to a specific hardware **button (L1–L5 / R1–R5)** (non-touchscreen). May contain any Products (except FLU-type products) or FLU/Menu/Numeric-Entry groups.
- **Toggle** — ordered list on one button; toggles through the **first 4** products (wraps), `+` key expands full list. **Only FLU-type products** allowed.
- **Numeric Entry** — shows a numeric keypad; contains **one** Menu-type group or one product. If a product → typed value is a transaction quantity for that product; if a group → typed value meaning is use-case-specific, then that group's menu is shown next.

## Config rules (assertable)
- Each group has **Group Name**, **Device Type** (one type, or **"All"**), and an ordered item list. Group Name is often **used by the device** to locate a group or as on-screen text.
- **Default selection** available on **FLU and Toggle** groups only (any line item can be the default).
- **Display Name** field — extra device-facing text (used heavily in POS card issue, below).
- **Product Category** (`Select Category`, in product config): Passenger Type / Travel Type / Passenger Class — **only Passenger Type is currently used**; drives Adult/Child text on TVM.

## Default group / product resolution by device (naming conventions — very config-fragile)
- **ETM/POS bus main menu:** group named **`"Default " + <DeviceType> + " " + <OperatorName>"`** (e.g. `Default ETM Metro`, `Default POS Ulsterbus`). Route's **Default Product Group** attribute overrides it. Must be **FLU type** for Translink UX.
- **Default product on sign-on (ETM / POS bus):** first product in first item of LHS menu, unless a default is set.
- **POS rail / HHD rail:** default status **`Adult`**, default ticket **`Adult Single`**; located by searching product groups that belong to **NIR** operator, correct device type, containing groups (not products) → single **`Default POS Rail`** / **`Rail`** group.
- **HHD Glider:** search Glider-operator + HHD groups containing groups → single **`HHD Glider`** group (Single, Bus Rambler, Metro, Family & Friends).
- **TVM:** root group **`Tickets`** → operator groups **Glider / Metro / Ulsterbus / NIR**. Kiosk "Rail" → `NIR`; "Bus" → looks up route owner → `Metro` or `Ulsterbus`. Within each, groups named after home locations (`Metro TVM`, `Rail TVM`, …).

## POS card issue (Parkeon Card Type)
- Blank pre-encoded card → POS reads **`Parkeon Card Type`** and looks up group **`"ParkeonCardType " + <type>"`** (e.g. `ParkeonCardType 10`).
- Group content varies by card type (type 10 = Ulsterbus MJ / Metro MJ / Town Service Travelcard / Metro Travelcard; type 12 = Adult DayLink only).
- Rule of thumb: group **Display Name** → menu-option text; group **Name** → next-screen title. Ulsterbus MJ uses **Numeric Entry** groups within `ParkeonCardType 10` (adult) / `11` (child).

## Suite implications
- Add **default-group-resolution** cases per device: assert the exact naming convention (`Default ETM Metro`, `Default POS Rail`, `HHD Glider`, `ParkeonCardType 10`) resolves the right menu — a rename is a silent, high-impact break.
- Cover each **group-type behaviour**: FLU paging (>5 items toggles next 5), Toggle wrap after 4th product + `+`-key expand, Menu button mapping, Numeric-Entry product-vs-group branch.
- Assert **default selection** only offered on FLU/Toggle, and **Passenger Type** drives Adult/Child labels (other categories unused).
- POS card-issue: Display-Name→menu / Name→title mapping and Parkeon-Card-Type routing — ties to FBD-100261 Multi-Journey flows.
