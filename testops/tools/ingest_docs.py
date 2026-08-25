#!/usr/bin/env python
"""Ingest a project's requirement documents into readable text for distillation.

Repeatable, project-agnostic. Point it at a LOCAL folder of documents (e.g. a
Google Drive for Desktop mount synced to the project's requirements area) and it:
  1. de-duplicates by version family (keeps the highest version per document),
  2. skips archive/superseded/video/CAD/Visio/milestone-cert noise,
  3. converts .docx/.xlsx/.pdf/.csv/.txt -> plain UTF-8 text,
  4. writes a reconciliation (what was kept / dropped / excluded, and why).

Output text lands in <work>/_text (default: dev/<project>-requirements/_text), which
Claude then reads to distil into knowledge/<project>/specs/*.md (cited, no raw dumps).
Raw docs and _text stay LOCAL and are never committed.

Usage:
  python tools/ingest_docs.py --project translink --src "G:/.../UK-Flowbird TFTS _3 Requirements & Design"
  python tools/ingest_docs.py --project edinburgh-trams --src "H:/.../Edinburgh Requirements" --work C:/dev/edi-reqs

Deps (install once in the venv): pip install python-docx openpyxl pypdf
"""
import argparse, os, re, glob, sys

KEEP_EXT = {'.docx', '.xlsx', '.csv', '.pdf', '.pptx', '.txt', '.doc'}
VER = re.compile(r'[ _\-]v(\d+)\.(\d+)', re.I)
VER2 = re.compile(r'[ _\-]v(\d+)(?!\d)', re.I)

def excluded_reason(rel):
    low = rel.lower(); ext = os.path.splitext(low)[1]
    if '0_archive/' in low or '/archive/' in low: return 'archive'
    if 'milestone certificate' in low: return 'milestone-cert'
    if ext == '.mp4': return 'video'
    if ext in ('.jpg', '.jpeg', '.png', '.gif', '.bmp'): return 'image (readable on demand, not bulk-converted)'
    if ext in ('.stp', '.3dxml'): return 'cad'
    if ext in ('.vsd', '.vsdx', '.vsdm'): return 'visio'
    if ext == '.mpp': return 'ms-project'
    if ext not in KEEP_EXT: return 'other'
    return None

def version_of(name):
    m = VER.search(name); n = VER2.search(name)
    if m: return (int(m.group(1)), int(m.group(2)))
    if n: return (int(n.group(1)), 0)
    return (-1, -1)

def family_key(rel):
    folder, fn = os.path.split(rel); base = os.path.splitext(fn)[0]
    base = VER.sub('', base); base = VER2.sub('', base)
    base = re.sub(r'\b(unsigned|signed|clean|final|draft)\b', '', base, flags=re.I)
    base = re.sub(r'\s+', ' ', base).strip(' -_')
    return folder + '||' + base.lower()

def to_text(path, ext):
    if ext in ('.docx', '.doc'):
        import docx
        d = docx.Document(path)
        out = [p.text for p in d.paragraphs if p.text.strip()]
        for t in d.tables:
            for row in t.rows:
                cells = [c.text.strip() for c in row.cells]
                if any(cells): out.append(' | '.join(cells))
        return '\n'.join(out)
    if ext == '.xlsx':
        import openpyxl
        wb = openpyxl.load_workbook(path, data_only=True, read_only=True); out = []
        for ws in wb.worksheets:
            out.append(f'### SHEET: {ws.title}'); n = 0
            for r in ws.iter_rows(values_only=True):
                cells = [str(c).strip() for c in r if c is not None and str(c).strip()]
                if cells: out.append(' | '.join(cells)); n += 1
                if n > 400: out.append('... (truncated)'); break
        wb.close(); return '\n'.join(out)
    if ext == '.pdf':
        from pypdf import PdfReader
        return '\n'.join((pg.extract_text() or '') for pg in PdfReader(path).pages)
    if ext in ('.csv', '.txt'):
        return open(path, encoding='utf-8', errors='replace').read()
    return ''

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project', required=True)
    ap.add_argument('--src', required=True, help='local folder of the project requirement docs')
    ap.add_argument('--work', help='working dir (default dev/<project>-requirements)')
    args = ap.parse_args()
    src = os.path.abspath(args.src)
    work = args.work or os.path.join(os.path.dirname(os.getcwd()), f'{args.project}-requirements')
    text_dir = os.path.join(work, '_text')
    os.makedirs(text_dir, exist_ok=True)

    # pass 1: gather + dedupe
    fam = {}; excluded = {}
    for path in glob.glob(os.path.join(src, '**', '*'), recursive=True):
        if os.path.isdir(path): continue
        rel = os.path.relpath(path, src).replace('\\', '/')
        r = excluded_reason(rel)
        if r: excluded[r] = excluded.get(r, 0) + 1; continue
        ver = version_of(os.path.basename(rel))
        k = family_key(rel)
        if k not in fam or ver > fam[k][0]: fam[k] = (ver, path, rel)

    # pass 2: convert winners
    kept = 0; failed = 0
    for k, (ver, path, rel) in fam.items():
        ext = os.path.splitext(path)[1].lower()
        target = os.path.join(text_dir, rel) + '.txt'
        os.makedirs(os.path.dirname(target), exist_ok=True)
        try:
            open(target, 'w', encoding='utf-8').write(to_text(path, ext)); kept += 1
        except Exception as e:
            failed += 1; print(f"  [fail] {rel[:70]} :: {type(e).__name__}")

    print(f"project={args.project}  src={src}")
    print(f"KEPT current docs -> text: {kept}  (failed {failed})")
    print("Excluded (noise / not-bulk-convertible):")
    for r in sorted(excluded, key=lambda x: -excluded[x]): print(f"   {excluded[r]:4d}  {r}")
    print(f"\nText ready in: {text_dir}")
    print(f"Next: distil into knowledge/{args.project}/specs/*.md (cite the FBD/spec id), then re-audit the suite.")

if __name__ == '__main__':
    main()
