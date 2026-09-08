import json

p = r'C:\Users\GeorgeOliver\.claude\projects\C--Users-GeorgeOliver\e391e534-cf56-4875-a9db-5fd650b94492\tool-results\mcp-claude_ai_Atlassian_Rovo-searchJiraIssuesUsingJql-1784624936990.txt'
d = json.load(open(p, encoding='utf-8'))
nodes = {n['key']: n['fields'] for n in d['issues']['nodes']}
need = ['TIBU-22311','TIBU-22312','TIBU-24196','TIBU-22316','TIBU-22317','TIBU-22318','TIBU-22319',
        'TIBU-22322','TIBU-22323','TIBU-28098','TIBU-28386','TIBU-21950','TIBU-24428','TIBU-25446',
        'TIBU-25691','TIBU-26048','TIBU-26303','TIBU-26522','TIBU-26531','TIBU-27289','TIBU-27324',
        'TIBU-28139','TIBU-28240','TIBU-28649','TIBU-28805','TIBU-29191','TIBU-31287','TIBU-31705',
        'TIBU-30923','TIBU-25444','TIBU-31722','TIBU-32037']
out = []
for k in need:
    f = nodes.get(k, {})
    itype = f.get('issuetype', {}).get('name')
    status = f.get('status', {}).get('name')
    summary = f.get('summary')
    desc = f.get('description') or '(no description)'
    out.append("### {} [{}] ({})\n{}\n\n{}\n".format(k, itype, status, summary, desc))
outp = r'C:\Users\GeorgeOliver\Documents\GitHub\system-test-ops\reports\tfts-system-test\new-pv-acceptance-test-suite\2026-07-21\jira-descriptions.md'
open(outp, 'w', encoding='utf-8').write('\n---\n'.join(out))
print('wrote', outp)
