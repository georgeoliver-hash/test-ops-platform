import json
import sys
sys.path.insert(0, r'C:\Users\GeorgeOliver\Documents\GitHub\system-test-ops')
from system_test_ops.testrail.client import TestRailClient

ids = [4101079,4101020,4101001,4101093,4101082,4101088,4100999,4101019,4101006,
       4103563,4101084,4101087,4101016,4101080,4101095,4102428,4101094,4101078,
       4103568,4100998,4101002]

client = TestRailClient()

out = {}
for cid in ids:
    c = client.get_case(cid)
    out[cid] = c

outp = r'C:\Users\GeorgeOliver\Documents\GitHub\system-test-ops\reports\tfts-system-test\new-pv-acceptance-test-suite\2026-07-21\case-bodies.json'
json.dump(out, open(outp, 'w', encoding='utf-8'), indent=2)
print('wrote', outp)
