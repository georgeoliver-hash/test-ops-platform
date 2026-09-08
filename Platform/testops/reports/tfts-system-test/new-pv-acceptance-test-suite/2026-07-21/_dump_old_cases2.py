import json
import sys
sys.path.insert(0, r'C:\Users\GeorgeOliver\Documents\GitHub\system-test-ops')
from system_test_ops.testrail.client import TestRailClient

ids = [4069405, 4091894, 4091897, 4091905, 4091910]

client = TestRailClient()
out = {}
for cid in ids:
    try:
        out[cid] = client.get_case(cid)
    except Exception as e:
        out[cid] = {"error": str(e)}

outp = r'C:\Users\GeorgeOliver\Documents\GitHub\system-test-ops\reports\tfts-system-test\new-pv-acceptance-test-suite\2026-07-21\old-suite-case-bodies2.json'
json.dump(out, open(outp, 'w', encoding='utf-8'), indent=2)
print('wrote', outp)
