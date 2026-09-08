import json
import sys
sys.path.insert(0, r'C:\Users\GeorgeOliver\Documents\GitHub\system-test-ops')
from system_test_ops.testrail.client import TestRailClient

ids = [2700890, 4073875, 4091898, 4091908, 4091911, 4091912, 4091913, 4060881,
       3275577, 3275969, 3275939, 4073767, 2224519, 2224520, 2668205, 2668235]

client = TestRailClient()
out = {}
for cid in ids:
    try:
        out[cid] = client.get_case(cid)
    except Exception as e:
        out[cid] = {"error": str(e)}

outp = r'C:\Users\GeorgeOliver\Documents\GitHub\system-test-ops\reports\tfts-system-test\new-pv-acceptance-test-suite\2026-07-21\old-suite-case-bodies.json'
json.dump(out, open(outp, 'w', encoding='utf-8'), indent=2)
print('wrote', outp)
