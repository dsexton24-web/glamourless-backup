import re, docx, pypdf
SKIP = re.compile(r'(?i)^(glamourless systems$|build your profit scaffold|20\d\d .*(update|gate)|vendor lock-in|important notice|disclaimer|how to use this|current (platform )?sources|sources|the last word|closing|a final word|table of contents|contents|about the author|copyright|legal|notice|appendix|glossary|index|references)')
NUMS = 'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty twenty-one twenty-two twenty-three twenty-four twenty-five twenty-six twenty-seven twenty-eight twenty-nine thirty'.split()
WORDS = '(?:' + '|'.join(sorted(NUMS, key=len, reverse=True)) + ')'
def _num(x):
    return int(x) if x.isdigit() else NUMS.index(x.lower()) + 1
def _clean(t):
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'^(?:chapter|part|section)\s+(?:\d+[A-Za-z]?|' + WORDS + r')\b\s*[:.\-–—]?\s*', '', t, flags=re.I).strip(' :.-–—')
    t = re.sub(r'\s+\d{1,3}$', '', t).strip()
    if t.isupper():
        t = t.title().replace("'S ", "'s ").replace("'T ", "'t ")
        t = re.sub(r'(?<=\s)(And|Or|Of|The|To|In|On|For|A|An|At|By|With|Vs|From|Into)(?=\s)', lambda m: m.group(1).lower(), t)
    return t
def _ok(t): return t and 4 <= len(t) <= 90 and not SKIP.match(t)
def from_docx(path):
    d = docx.Document(path)
    def sty(p):
        try:
            return p.style.name if p.style is not None else ''
        except Exception:
            return ''
    paras = [(sty(p), p.text.strip()) for p in d.paragraphs if p.text.strip()]
    found = {}
    for st, t in paras:
        m = re.match(r'^chapter\s+(\d{1,2}|' + WORDS + r')\b\s*[:.\-–—]?\s*(.*)$', t, re.I)
        if m and len(t) < 120:
            n = _num(m.group(1))
            if n not in found and _ok(_clean(m.group(2))): found[n] = _clean(m.group(2))
    if len(found) >= 5:
        return [found[k] for k in sorted(found)]
    # table of contents lines like 'TITLE<tab>12'
    toc = []
    for st, t in paras:
        m = re.match(r'^(.{4,100}?)\t+\s*\d{1,3}\s*$', t)
        if m:
            c = _clean(m.group(1))
            if _ok(c): toc.append(c)
    toc = list(dict.fromkeys(toc))
    if 6 <= len(toc) <= 80:
        return toc
    for lvl in ('Heading 1', 'Heading 2'):
        hs = [_clean(t) for st, t in paras if st == lvl]
        hs = [h for h in hs if _ok(h)]
        hs = list(dict.fromkeys(hs))
        if 6 <= len(hs) <= 60:
            return hs
    # last resort: short all-bold paragraphs
    bold = []
    for p in d.paragraphs:
        t = p.text.strip()
        try:
            rs = [r for r in p.runs if r.text.strip()]
        except Exception:
            rs = []
        if rs and len(t) < 85 and all(r.bold for r in rs) and not t.endswith(('.', ':')):
            c = _clean(t)
            if _ok(c): bold.append(c)
    bold = list(dict.fromkeys(bold))[1:]
    return bold if len(bold) >= 6 else []
def from_pdf_outline(r):
    out = []
    try: ol = r.outline
    except Exception: ol = []
    for x in ol:
        if isinstance(x, list): continue
        t = _clean(x.title)
        if _ok(t): out.append(t)
    return out
def chapters(pdf_path, docx_path):
    r = pypdf.PdfReader(pdf_path)
    out = from_pdf_outline(r)
    if docx_path and (len(out) < 10 or len(out) > 60):
        d = from_docx(docx_path)
        if d and (len(out) < 6 or len(out) > 60 or len(d) > len(out)): out = d
    return len(r.pages), out
