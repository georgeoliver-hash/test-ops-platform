"""Read a requirement document from a LOCAL spec library (never committed).

The full requirement docs are confidential and large, so they live locally per engineer and
are NEVER stored in this repo. This tool opens them on demand so authoring/audit can ground on
the real spec text (with paragraph indices for citation). The committed artefacts are: this tool,
a lightweight index, and the cited `knowledge/**/*.md` notes — not the docs themselves.

Point it at your local library via --dir or the REQS_DIR env var. It reads either loose files or
`.zip` bundles in that directory.

Usage:
  set REQS_DIR=C:\\Users\\me\\Downloads            (or pass --dir)
  python tools/extract_req.py --find "FBD-100317"                        # list matching doc entries
  python tools/extract_req.py --entry "<path substring>" --terms a,b     # print matching paragraphs
  python tools/extract_req.py --entry "<path substring>" --all           # print all paragraphs

.docx -> paragraph text (index shown, stable for citing). .xlsx -> sheet/cell dump (needs openpyxl).
.pdf  -> best effort (pdfminer/PyPDF2 if installed). Prefers newest non-Archive when several match.
"""
import argparse, io, os, re, zipfile
from pathlib import Path

from dotenv import load_dotenv

def reqs_dir(cli):
    load_dotenv()  # no-op if there's no .env; real env vars take precedence
    d = cli or os.environ.get("REQS_DIR")
    if not d:
        raise SystemExit("error: set REQS_DIR env var or pass --dir to your local spec library.")
    p = Path(d)
    if not p.is_dir():
        raise SystemExit(f"error: REQS_DIR '{d}' is not a directory.")
    return p

def iter_entries(root):
    # loose files
    for f in root.rglob("*"):
        if f.is_file() and f.suffix.lower() in (".docx",".doc",".xlsx",".pdf",".txt",".csv",".pptx"):
            yield ("FILE", str(f), f.stat().st_size, f)
    # zip bundles
    for zp in root.glob("*.zip"):
        try:
            z = zipfile.ZipFile(zp)
        except Exception:
            continue
        for e in z.infolist():
            if e.file_size > 0 and Path(e.filename).suffix.lower() in (".docx",".doc",".xlsx",".pdf",".txt",".csv",".pptx"):
                yield ("ZIP", e.filename, e.file_size, (zp, e.filename))

def read_bytes(handle_kind, handle):
    if handle_kind == "FILE":
        return Path(handle).read_bytes()
    zp, name = handle
    with zipfile.ZipFile(zp) as z:
        return z.read(name)

def docx_paragraphs(data):
    z = zipfile.ZipFile(io.BytesIO(data))
    xml = z.read("word/document.xml").decode("utf-8","ignore")
    out = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        t = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S))
        t = (t.replace("&amp;","&").replace("&lt;","<").replace("&gt;",">")
              .replace("&quot;",'"').replace("&#39;","'"))
        if t.strip():
            out.append(t.strip())
    return out

def xlsx_text(data):
    try:
        import openpyxl
    except ImportError:
        return ["[xlsx: openpyxl not installed]"]
    wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
    out = []
    for ws in wb.worksheets:
        out.append(f"### sheet: {ws.title}")
        for row in ws.iter_rows(values_only=True):
            cells = [str(c) for c in row if c is not None]
            if cells:
                out.append(" | ".join(cells))
    return out

def pdf_text(data):
    try:
        from pdfminer.high_level import extract_text
        return extract_text(io.BytesIO(data)).splitlines()
    except Exception:
        try:
            import PyPDF2
            r = PyPDF2.PdfReader(io.BytesIO(data))
            return [(pg.extract_text() or "") for pg in r.pages]
        except Exception as e:
            return [f"[pdf: no extractor available ({e})]"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir")
    ap.add_argument("--find")
    ap.add_argument("--entry")
    ap.add_argument("--terms", default="")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    root = reqs_dir(a.dir)
    entries = list(iter_entries(root))
    if a.find:
        s = a.find.lower()
        for kind, name, sz, _ in entries:
            if s in name.lower():
                print(f"{kind}\t{sz//1024}KB\t{name}")
        return
    if not a.entry:
        raise SystemExit("pass --find or --entry")
    s = a.entry.lower()
    cands = [(kind,name,h) for kind,name,sz,h in entries
             if s in name.lower() and name.lower().endswith((".docx",".doc",".xlsx",".pdf",".txt",".csv"))]
    if not cands:
        print("no entry matched"); return
    non_arch = [c for c in cands if "/archive/" not in c[1].lower() and "\\archive\\" not in c[1].lower()]
    pool = non_arch or cands
    pool.sort(key=lambda c: c[1])
    kind, name, h = pool[-1]
    print(f"[DOC] {name}\n")
    data = read_bytes(kind, h)
    ext = name.lower().rsplit(".",1)[-1]
    paras = (docx_paragraphs(data) if ext in ("docx","doc")
             else xlsx_text(data) if ext == "xlsx"
             else pdf_text(data) if ext == "pdf"
             else data.decode("utf-8","ignore").splitlines())
    terms = [t.strip().lower() for t in a.terms.split(",") if t.strip()]
    for i, p in enumerate(paras):
        if a.all or not terms or any(t in p.lower() for t in terms):
            print(f"[{i}] {p}")

if __name__ == "__main__":
    main()
