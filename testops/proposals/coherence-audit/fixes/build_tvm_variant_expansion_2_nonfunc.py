"""Build the follow-up TVM Data-variations expansion — Non-Functional (887793/887794/887795/887796)."""
from __future__ import annotations
from pathlib import Path
import yaml

HERE = Path(__file__).parent
DEFAULTS = {
    "template_id": 1,
    "custom_devtypes": [1],
    "custom_revstatus": 2,
    "custom_autoconfirmation": False,
}


def case(match, title, refs, objective, steps, expected):
    d = {}
    if match:
        d["match"] = match
    d["title"] = title
    d["refs"] = refs
    d["objective"] = objective
    d["steps"] = steps
    d["expected"] = expected
    return d


ems_tms_cases = []       # 887793
alarmboard_cases = []    # 887794
recycler_hopper_cases = []  # 887795
resilience_cases = []    # 887796

# C4103755: reboot / de-activate / re-activate — 3-way.
COMMANDS = ["reboot", "de-activate", "re-activate"]
orig_755 = "Remote Control — remote reboot, de-activate and re-activate"
for i, cmd in enumerate(COMMANDS):
    ems_tms_cases.append(case(
        orig_755 if i == 0 else None,
        f"Remote Control — remote {cmd}",
        ["FBD-100266"],
        f"This test is to confirm an operator can remotely {cmd} a TVM from CloudFare.",
        (
            "**GIVEN** a commissioned TVM in service\n"
            f"**WHEN** an operator issues a remote {cmd} command from CloudFare\n"
            "**THEN** the TVM performs the commanded action\n"
            "**AND** the resulting state is reported back to CloudFare"
        ),
        f"A remote {cmd} command drives the TVM to the expected state and reports back.\n\n[Automatable: No · Cross-check: CloudFare]",
    ))

# C4103757: report type — 3-way.
REPORTS = ["Cash Collection Report", "Bank Note Collection Report", "Coins Reload Report"]
orig_757 = "Cash Collection — prints collection and reload reports"
for i, rpt in enumerate(REPORTS):
    ems_tms_cases.append(case(
        orig_757 if i == 0 else None,
        f"Cash Collection — prints the {rpt}",
        ["REQ-2720.4", "REQ-2720.5", "REQ-2720.6 (TFTS Requirements Matrix, Signed-Off; Q34 resolved)"],
        f"This test is to confirm an Engineer can print the {rpt} from EMS.",
        (
            "**GIVEN** a TVM with an Engineer signed into EMS after a cash collection\n"
            f"**WHEN** the Engineer prints the {rpt} from the EMS menu\n"
            "**THEN** the report prints with the correct totals"
        ),
        f"The {rpt} prints with correct totals.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
    ))

# C4103766: increase / decrease brightness — 2-way.
BRIGHTNESS = ["increase", "decrease"]
orig_766 = "Screen Brightness — backlight change persists into the Sales App"
for i, direction in enumerate(BRIGHTNESS):
    ems_tms_cases.append(case(
        orig_766 if i == 0 else None,
        f"Screen Brightness — a backlight {direction} persists into the Sales App",
        ["REQ-0511.0", "REQ-0511.1 (TFTS Requirements Matrix, Signed-Off; Q34 resolved)"],
        f"This test is to confirm an Engineer's backlight {direction} made in EMS is maintained when the Sales App reloads.",
        (
            "**GIVEN** an Engineer signed into the EMS control panel\n"
            f"**WHEN** the Engineer {direction}s the screen backlight brightness and returns to the Sales App\n"
            "**THEN** the Sales App displays at the adjusted brightness"
        ),
        f"A backlight {direction} made in EMS carries through to the Sales App.\n\n[Automatable: No · Cross-check: CloudFare]",
    ))

# C4104118: burglary-trigger scenario — 4-way.
BURGLARY = [
    ("hopper door opened without authorisation", "the hopper door is opened without authorisation"),
    ("3 failed EMS login attempts", "3 EMS login attempts fail in succession"),
    ("TVM door opened after 3 failed EMS logins", "the TVM door is opened after 3 EMS login attempts have failed"),
    ("TVM door opened without any EMS login attempt", "the TVM door is opened with no EMS login attempted"),
]
orig_4118 = "Security — unauthorised door access or repeated failed EMS logins raises a burglary event"
for i, (label, action) in enumerate(BURGLARY):
    ems_tms_cases.append(case(
        orig_4118 if i == 0 else None,
        f"Security — {label} raises a burglary event",
        ["old-suite C1831725", "old-suite C1831215", "old-suite C1831216", "old-suite C1831218"],
        f"This test is to confirm the TVM raises the correct burglary event when {label}.",
        (
            "**GIVEN** the TVM is in service and not integrated with CloudFare\n"
            f"**WHEN** {action}\n"
            "**THEN** the TVM raises the correct burglary event"
        ),
        f"{label[0].upper() + label[1:]} raises a burglary event.\n\n[Automatable: Partial — Cross-check: CloudFare]",
    ))

# C4104121: with / without General Reboot — 2-way.
orig_4121 = "EMS — exit returns to Sales with or without a General Reboot"
REBOOT_OPTS = [
    ("without General Reboot", "\"Back to sales without Reboot\"", "without rebooting"),
    ("with General Reboot", "\"Back to sales with General Reboot\"", "after performing a General Reboot"),
]
for i, (label, menu_item, outcome) in enumerate(REBOOT_OPTS):
    ems_tms_cases.append(case(
        orig_4121 if i == 0 else None,
        f"EMS — exit returns to Sales {label}",
        ["old-suite C4041250", "old-suite C4041251", "old-suite C4041252", "old-suite C4041253"],
        f"This test is to confirm an Engineer can return the TVM from EMS to Sales mode {label}.",
        (
            "**GIVEN** an Engineer is signed into EMS with no other activity taken place\n"
            f"**WHEN** the Engineer selects {menu_item}\n"
            f"**THEN** the TVM returns to Sales mode {outcome}"
        ),
        f"EMS exit {label} returns the TVM to Sales mode {outcome}.\n\n[Automatable: Partial — Cross-check: CloudFare]",
    ))

# C4103769: ticket-tray / payment LED — 2-way.
LEDS = ["ticket-tray", "payment"]
orig_769 = "Alarmboard — an Engineer tests the status LEDs"
for i, led in enumerate(LEDS):
    alarmboard_cases.append(case(
        orig_769 if i == 0 else None,
        f"Alarmboard — an Engineer tests the {led} LED",
        [],
        f"This test is to confirm an Engineer can test the Kiosk alarmboard {led} LED from EMS.",
        (
            "**GIVEN** an Engineer signed into EMS on a Kiosk TVM at the Alarmboard maintenance screen\n"
            f"**WHEN** the Engineer runs the {led} LED test\n"
            "**THEN** the selected LED illuminates"
        ),
        f"The {led} LED test illuminates the LED.\n\n[Automatable: No · Cross-check: CloudFare]",
    ))

# C4103772: door state / sensor test — 2-way.
DOOR_SENSOR = ["door state", "sensor"]
orig_772 = "Alarmboard — an Engineer runs the door and sensor tests"
for i, test in enumerate(DOOR_SENSOR):
    alarmboard_cases.append(case(
        orig_772 if i == 0 else None,
        f"Alarmboard — an Engineer runs the {test} test",
        [],
        f"This test is to confirm an Engineer can run the {test} supplementary test on the Kiosk alarmboard.",
        (
            "**GIVEN** an Engineer signed into EMS on a Kiosk TVM at the Alarmboard maintenance screen\n"
            f"**WHEN** the Engineer runs the {test} supplementary enclosure test\n"
            "**THEN** the alarmboard reports the current reading"
        ),
        f"The {test} supplementary test reports the current enclosure reading.\n\n[Automatable: Yes · Cross-check: CloudFare]",
    ))

# C4103775: TL80 / IML5 printer model — 2-way.
PRINTERS = ["TL80", "IML5"]
orig_775 = "Printer — an Engineer adjusts the print alignment"
for i, model in enumerate(PRINTERS):
    alarmboard_cases.append(case(
        orig_775 if i == 0 else None,
        f"Printer — an Engineer adjusts the {model} print alignment",
        ["old suite C1865202 (Printer Test — IML5 & TL80); consolidation-completeness audit 2026-07-23"],
        f"This test is to confirm an Engineer can adjust the {model} printer alignment from EMS on a Kiosk TVM.",
        (
            f"**GIVEN** an Engineer signed into EMS on a Kiosk TVM at the {model} printer maintenance screen\n"
            "**WHEN** the Engineer adjusts the print alignment and prints a test ticket\n"
            "**THEN** the test ticket prints at the adjusted alignment"
        ),
        f"The {model} alignment adjustment is applied and confirmed on a test ticket.\n\n[Automatable: Partial — Cross-check: CloudFare]",
    ))

# C4103779: cassette-reload method — 2-way.
orig_779 = "Coin Recycler Hopper — reloading updates recorded cash content"
RELOAD_METHODS = [
    ("set to full cassette", "sets the hopper level to a full cassette (value taken from TMS)"),
    ("set to empty then manually corrected", "sets the hopper level to empty and then manually corrects it"),
]
for i, (label, action) in enumerate(RELOAD_METHODS):
    recycler_hopper_cases.append(case(
        orig_779 if i == 0 else None,
        f"Coin Recycler Hopper — reloading updates recorded cash content ({label})",
        ["REQ-2720.6 (TFTS Requirements Matrix, Signed-Off; Q34 resolved)"],
        f"This test is to confirm reloading a coin recycler hopper, {label}, updates the TVM's recorded coin content.",
        (
            "**GIVEN** a Kiosk TVM with an Engineer signed into EMS at the Load Hoppers screen\n"
            f"**WHEN** the Engineer reloads a coin hopper and {action}\n"
            "**THEN** the recorded coin content is updated to the set level"
        ),
        f"Reloading a coin recycler hopper ({label}) updates the TVM's recorded coin content to the set level.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT]",
    ))

# C4103780: degraded hardware component — 3-way.
COMPONENTS = ["Ingenico card reader", "coin selector", "banknote acceptor"]
orig_780 = "Degraded Service — payment hardware failure transitions to amber"
for i, comp in enumerate(COMPONENTS):
    resilience_cases.append(case(
        orig_780 if i == 0 else None,
        f"Degraded Service — {comp} failure transitions to amber",
        [],
        f"This test is to confirm the TVM enters a degraded (amber) state and disables the affected payment method when the {comp} fails.",
        (
            "**GIVEN** a TVM in service accepting cash and card\n"
            f"**WHEN** the {comp} fails\n"
            "**THEN** the TVM transitions to a degraded amber status\n"
            "**AND** the affected payment method is no longer offered"
        ),
        f"A {comp} failure moves the TVM to amber and withdraws the affected payment method.\n\n[Automatable: No]",
    ))

# C4103786: ticket type at lockout — 2-way.
TICKET_TYPES = ["paper ticket", "discounted ticket"]
orig_786 = "Device Lockout — cash sale at the lockout limit goes Out of Service"
for i, tt in enumerate(TICKET_TYPES):
    resilience_cases.append(case(
        orig_786 if i == 0 else None,
        f"Device Lockout — a {tt} cash sale at the lockout limit goes Out of Service",
        ["REQ-2690.0 (TFTS Requirements Matrix, Signed-Off; Q34 resolved)"],
        f"This test is to confirm the TVM goes Out of Service when a {tt} cash transaction meets or exceeds the configured lockout sales limit.",
        (
            "**GIVEN** a TVM whose cumulative cash sales are just below the configured lockout sales limit (example limit £250)\n"
            f"**WHEN** a {tt} cash sale takes the cumulative total to the lockout limit\n"
            "**THEN** the sale completes\n"
            "**AND** the TVM goes Out of Service"
        ),
        f"A {tt} cash sale that reaches the configured lockout limit completes, then the TVM locks out of service.\n\n[Automatable: Partial · Cross-check: CloudFare / MERIT / SmartTrack]",
    ))

# C4103796: Bus / Rail home — 2-way.
MODES_796 = ["Bus", "Rail"]
orig_796 = "Multi-Modal Home — selecting Bus or Rail shows the right home"
for i, m in enumerate(MODES_796):
    resilience_cases.append(case(
        orig_796 if i == 0 else None,
        f"Multi-Modal Home — selecting {m} shows the {m} home",
        [],
        f"This test is to confirm selecting {m} on the multi-modal home shows the {m} home screen.",
        (
            "**GIVEN** an in-service TVM showing the multi-modal home with a mode-of-transport choice\n"
            f"**WHEN** the customer selects {m}\n"
            f"**THEN** the {m} home screen is displayed"
        ),
        f"Selecting {m} displays the {m} home screen.\n\n[Automatable: Yes]",
    ))

# C4103797: payment-input audio feedback — 3-way (cash / card / contactless). The first step
# (workflow speech prompts) is common context and stays on every sibling; only the payment-input
# feedback line varies.
PAY_INPUTS = ["cash", "card", "contactless"]
orig_797 = "Audio Prompts — speech prompts and payment feedback play"
for i, pin in enumerate(PAY_INPUTS):
    resilience_cases.append(case(
        orig_797 if i == 0 else None,
        f"Audio Prompts — speech prompts play and {pin} input gets audible feedback",
        ["REQ-0279.0", "REQ-0279.1", "REQ-0279.2", "REQ-1687.0 (TFTS Requirements Matrix, Signed-Off; Q34 resolved)"],
        f"This test is to confirm the TVM plays speech prompts on workflow screens and audible feedback on a {pin} payment input.",
        (
            "**GIVEN** an in-service TVM with audio enabled at the configured volume\n"
            "**WHEN** the customer works through the purchase screens\n"
            "**THEN** the speech prompt for the current screen plays\n"
            f"**WHEN** the customer makes a {pin} payment input\n"
            "**THEN** audible feedback confirms the payment input"
        ),
        f"Speech prompts play on workflow screens and audible feedback confirms a {pin} payment input.\n\n[Automatable: No · Cross-check: CloudFare / MERIT]",
    ))

# C4103798: workflow — 2-way (Quick Select / Buy Other Tickets).
WORKFLOWS = ["Quick Select", "Buy Other Tickets"]
orig_798 = "Performance — workflows launch from idle within tolerance"
for i, wf in enumerate(WORKFLOWS):
    resilience_cases.append(case(
        orig_798 if i == 0 else None,
        f"Performance — {wf} launches from idle within tolerance",
        [],
        f"This test is to confirm the TVM launches the {wf} workflow from idle within the expected response time.",
        (
            "**GIVEN** an in-service TVM at the idle screensaver\n"
            f"**WHEN** a customer starts the {wf} workflow from idle\n"
            "**THEN** the first workflow screen is displayed within the expected response tolerance"
        ),
        f"The {wf} workflow opens from idle within the expected response time.\n\n[Automatable: No · Cross-check: CloudFare / MERIT / SmartTrack]",
    ))


def write_family(stem, header, sections):
    doc = {
        "suite": "**NEW** TVM Test Suite",
        "suite_id": 30284,
        "defaults": DEFAULTS,
        "sections": sections,
    }
    out = HERE / f"{stem}.cases.yaml"
    out.write_text(header + "\n" + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
    print(f"{stem}: {sum(len(s['cases']) for s in sections)} cases -> {out}")


write_family(
    "tvm-variant-expansion-2-nonfunc",
    "# TVM variant expansion, follow-up batch 2026-07-24 — Non-Functional: EMS & TMS Maintenance\n"
    "# (887793), Alarmboard & Enclosure / Kiosk only (887794), Coin Recycler Hopper / Kiosk only\n"
    "# (887795), Resilience (887796). See tvm-variant-expansion-2.changelog.md for the rationale.",
    [
        {"path": ["Non-Functional", "EMS & TMS Maintenance"], "cases": ems_tms_cases},
        {"path": ["Non-Functional", "EMS & TMS Maintenance", "Alarmboard & Enclosure / Kiosk only"], "cases": alarmboard_cases},
        {"path": ["Non-Functional", "EMS & TMS Maintenance", "Coin Recycler Hopper / Kiosk only"], "cases": recycler_hopper_cases},
        {"path": ["Non-Functional", "Resilience"], "cases": resilience_cases},
    ],
)

print("ems_tms:", len(ems_tms_cases), "alarmboard:", len(alarmboard_cases), "recycler_hopper:", len(recycler_hopper_cases), "resilience:", len(resilience_cases))
print("TOTAL:", len(ems_tms_cases) + len(alarmboard_cases) + len(recycler_hopper_cases) + len(resilience_cases))
