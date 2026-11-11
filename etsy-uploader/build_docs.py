#!/usr/bin/env python3
"""Build one Etsy draft package per supporting document (sold individually).

Usage: python3 build_docs.py GS-0001 GS-0002 ...
Reads staged docs from  /mnt/user-data/uploads/Glamourless Systems Main/GS Etsy Supporting Docs/<SKU folder>/
Writes   OUT/SD-GS-XXXX-NN/  with:
  <key> Cover.png          branded cover with page one preview
  <key> Page One.png       full page one
  <key> Page Two.png       page two (when there is one)
  <key> Whats Inside.png   section list
  <Doc Name>.docx|.xlsx    the editable file
  <Doc Name>.pdf           printable copy (Word docs only)
Adds manifest items with key 'SD-GS-XXXX-NN', kind 'doc'.
"""
import json, os, re, subprocess, sys, glob, shutil
from PIL import Image, ImageDraw, ImageFont
import docx, openpyxl

SRC = '/mnt/user-data/uploads/Glamourless Systems Main/GS Etsy Supporting Docs/'
OUT = '/home/claude/etsy/out/GS Etsy Upload Packages/'
WORK = '/home/claude/etsy/docwork/'
CAT = json.load(open('/home/claude/etsy/catalog.json'))
FONT = '/usr/share/fonts/opentype/inter/Inter-Regular.otf'
FONTB = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
NAVY, NAVY2, STEEL, WHITE, ACCENT, PAPER = '#061529', '#0E2A52', '#9DB4CF', '#FFFFFF', '#5B9BFF', '#F4F6FA'
PRICE_DOC, PRICE_XLSX = 5.00, 7.00

def cut(s, n):
    if len(s) <= n: return s
    return s[:n].rsplit(' ', 1)[0].rstrip(' ,')

def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def art(n):
    return ('an ' if n[:1].upper() in 'AEIOU' else 'a ') + n

def niche_of(sku):
    t = CAT.get(sku, {}).get('title', '')
    t = re.sub(r'\s*Blueprint$', '', t).strip()
    t = re.sub(r'^The\s+', '', t)
    return t

def doc_name(fn, niche):
    n = os.path.splitext(fn)[0]
    n = re.sub(r'^SD-GS-\d{4}-\d{2}\s+', '', n)
    n = re.sub(r'\s+-\s+Wayne Thomas$', '', n)
    n = re.sub(r'^The\s+', '', n)
    return n.strip()

def safe(s):
    s = re.sub(r'[^A-Za-z0-9 ._-]', '', s)
    return re.sub(r'\s+', ' ', s).strip()

def to_pdf(src, outdir):
    os.makedirs(outdir, exist_ok=True)
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', outdir, src],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    p = os.path.join(outdir, os.path.splitext(os.path.basename(src))[0] + '.pdf')
    return p if os.path.exists(p) else None

def render(pdf, prefix, pages=2):
    subprocess.run(['pdftoppm', '-png', '-r', '110', '-f', '1', '-l', str(pages), pdf, prefix], check=True)
    return sorted(glob.glob(prefix + '*.png'))

def page_count(pdf):
    out = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    m = re.search(r'Pages:\s+(\d+)', out)
    return int(m.group(1)) if m else 0

def sections_docx(path):
    d = docx.Document(path)
    hs = [p.text.strip() for p in d.paragraphs if p.style.name.startswith('Heading') and p.text.strip()]
    words = sum(len(p.text.split()) for p in d.paragraphs) + sum(len(c.text.split()) for t in d.tables for r in t.rows for c in r.cells)
    return hs, len(d.tables), words

def sections_xlsx(path):
    wb = openpyxl.load_workbook(path)
    return wb.sheetnames

def framed(page_png, W, H):
    im = Image.new('RGB', (W, H), PAPER)
    p = Image.open(page_png).convert('RGB')
    s = min((W - 200) / p.width, (H - 200) / p.height)
    p = p.resize((int(p.width * s), int(p.height * s)))
    x, y = (W - p.width) // 2, (H - p.height) // 2
    d = ImageDraw.Draw(im)
    d.rectangle([x + 14, y + 14, x + p.width + 14, y + p.height + 14], fill='#C9D2DE')
    im.paste(p, (x, y))
    return im

def cover(path, name, niche, kind, page_png):
    W, H = 2000, 2000
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    fb = ImageFont.truetype(FONTB, 92); fs = ImageFont.truetype(FONT, 50); ft = ImageFont.truetype(FONTB, 42); fbadge = ImageFont.truetype(FONTB, 44)
    badge = 'EDITABLE EXCEL TRACKER' if kind == 'xlsx' else 'EDITABLE WORD TEMPLATE  +  PRINTABLE PDF'
    bw = d.textlength(badge, font=fbadge)
    d.rounded_rectangle([110, 100, 110 + bw + 60, 180], radius=18, fill=ACCENT)
    d.text((140, 114), badge, font=fbadge, fill=NAVY)
    y = 240
    for ln in wrap(d, name, fb, 1780)[:3]:
        d.text((110, y), ln, font=fb, fill=WHITE); y += 112
    for ln in wrap(d, ('For an ' if niche[:1].upper() in 'AEIOU' else 'For a ') + niche + ' business', fs, 1780)[:2]:
        d.text((110, y + 10), ln, font=fs, fill=STEEL); y += 62
    top = y + 80
    p = Image.open(page_png).convert('RGB')
    ph = H - top - 170
    s = ph / p.height
    p = p.resize((int(p.width * s), ph))
    if p.width > 1780:
        p = p.crop((0, 0, 1780, ph))
    x = (W - p.width) // 2
    d.rectangle([x - 6, top - 6, x + p.width + 6, top + p.height + 6], fill=ACCENT)
    im.paste(p, (x, top))
    d.text((110, H - 110), 'GLAMOURLESS SYSTEMS', font=ft, fill=STEEL)
    d.text((W - 110 - d.textlength('INSTANT DOWNLOAD', font=ft), H - 110), 'INSTANT DOWNLOAD', font=ft, fill=ACCENT)
    im.save(path, optimize=True)

def inside(path, name, items, kind, pages):
    W, H = 2000, 2000
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 300], fill=NAVY2)
    fh = ImageFont.truetype(FONTB, 84); fi = ImageFont.truetype(FONT, 50); fs = ImageFont.truetype(FONT, 44); ft = ImageFont.truetype(FONTB, 40)
    d.text((110, 100), "What's inside", font=fh, fill=WHITE)
    sub = (f'{len(items)} tabs' if kind == 'xlsx' else f'{pages} pages  ·  {len(items)} sections') + '  ·  ' + cut(name, 60)
    d.text((110, 210), sub, font=fs, fill=STEEL)
    y = 380
    for it in items[:14]:
        lines = wrap(d, it, fi, 1650)[:2]
        d.ellipse([115, y + 18, 139, y + 42], fill=ACCENT)
        for ln in lines:
            d.text((175, y), ln, font=fi, fill=WHITE); y += 64
        y += 34
        if y > H - 260: break
    if len(items) > 14:
        d.text((175, y), f'plus {len(items) - 14} more', font=fi, fill=STEEL)
    d.text((110, H - 110), 'GLAMOURLESS SYSTEMS', font=ft, fill=STEEL)
    im.save(path, optimize=True)

def etsy_title(name, niche, kind):
    tail = 'Editable Excel Spreadsheet' if kind == 'xlsx' else 'Editable Word Template and Printable PDF'
    for t in (f'{name}, {niche} Business Template, {tail}',
              f'{name} for {niche} Business, {tail}',
              f'{name}, {niche} Business, {tail}',
              f'{name}, {tail}'):
        if len(t) <= 140: return t
    return cut(f'{name}, {tail}', 140)

GENERIC = ['business template', 'small business', 'editable template', 'digital download', 'business forms', 'side hustle', 'startup checklist', 'business planner', 'printable template']

def tags_for(name, niche, kind):
    t = []
    def add(x):
        x = x.lower().strip()
        if 3 <= len(x) <= 20 and x not in t: t.append(x)
    nm = re.sub(r'[^a-z0-9 ]', ' ', name.lower())
    words = [w for w in nm.split() if w not in ('and', 'the', 'a', 'of', 'for', 'to', 'pack', 'kit')]
    add(' '.join(words[-2:]))
    for i in range(len(words) - 1): add(words[i] + ' ' + words[i + 1])
    nw = [w for w in re.sub(r'[^a-z0-9 ]', ' ', niche.lower()).split() if w not in ('and', 'the', 'a', 'of')]
    add(' '.join(nw[:2])); add(' '.join(nw[:2]) + ' business')
    if kind == 'xlsx': add('excel template'); add('spreadsheet tracker')
    else: add('word template'); add('printable pdf')
    for g in GENERIC:
        if len(t) >= 13: break
        add(g)
    return t[:13]

def description(name, niche, kind, items, pages, sku):
    bp = CAT.get(sku, {}).get('title', '')
    lead = (f'{name} is a ready-to-use Excel workbook for running {art(niche)} business. Fill in your own numbers and it does the tracking for you.'
            if kind == 'xlsx' else
            f'{name} is a ready-to-use template for running {art(niche)} business. Open it, fill in your details, and use it as is or change it to fit how you work.')
    lines = [lead, '', "WHAT'S INSIDE"]
    lines += ['- ' + i for i in items[:12]]
    if len(items) > 12: lines.append(f'- plus {len(items) - 12} more')
    lines += ['', 'WHAT YOU GET']
    if kind == 'xlsx':
        lines += [f'- The editable Excel workbook ({len(items)} tabs)', '- Works in Microsoft Excel, Google Sheets and LibreOffice']
    else:
        lines += [f'- The editable Word document ({pages} pages)', '- The same document as a printable PDF', '- Works in Microsoft Word, Google Docs and any free word processor']
    lines += ['', 'HOW IT WORKS',
              'This is a digital download. Nothing is shipped. After you buy, Etsy gives you the files right away on the Purchases page.',
              '', 'PART OF A BIGGER SYSTEM',
              f'This template comes from the {bp} by Glamourless Systems, a full step-by-step plan for starting and running this business. You can find the full blueprint in our shop.',
              '', 'GOOD TO KNOW',
              'This template is for education and planning. It is not legal, tax or financial advice. Check the rules where you live before you rely on it.',
              'Written by Wayne Thomas for Glamourless Systems, with help from AI writing tools.',
              '', 'Because this is a digital file, all sales are final. If something is wrong with your download, message us and we will make it right.']
    return '\n'.join(lines)

def build(sku):
    dirs = [d for d in os.listdir(SRC) if d.startswith(sku + ' ')]
    if not dirs: print(sku, 'no folder staged'); return []
    folder = os.path.join(SRC, dirs[0]); niche = niche_of(sku)
    items_out = []
    for fn in sorted(os.listdir(folder)):
        m = re.match(r'^(SD-GS-\d{4}-\d{2})\s', fn)
        ext = os.path.splitext(fn)[1].lower()
        if not m or ext not in ('.docx', '.xlsx'): continue
        key = m.group(1); kind = ext[1:]
        name = doc_name(fn, niche)
        src = os.path.join(folder, fn)
        wd = os.path.join(WORK, key); shutil.rmtree(wd, ignore_errors=True); os.makedirs(wd)
        pdf = to_pdf(src, wd)
        if not pdf: print(key, 'PDF conversion failed'); continue
        pages = page_count(pdf)
        pngs = render(pdf, os.path.join(wd, 'pg'), 2)
        if kind == 'docx':
            secs, ntab, words = sections_docx(src)
        else:
            secs = sections_xlsx(src); words = 0
        if not secs: secs = [name]
        od = os.path.join(OUT, key); shutil.rmtree(od, ignore_errors=True); os.makedirs(od)
        base = safe(f'{key} {cut(name, 40)}')
        cover(os.path.join(od, f'{key} Cover.png'), name, niche, kind, pngs[0])
        imgs = [f'{key}/{key} Cover.png']
        framed(pngs[0], 2000, 2000).save(os.path.join(od, f'{key} Page One.png'), optimize=True); imgs.append(f'{key}/{key} Page One.png')
        if len(pngs) > 1:
            framed(pngs[1], 2000, 2000).save(os.path.join(od, f'{key} Page Two.png'), optimize=True); imgs.append(f'{key}/{key} Page Two.png')
        inside(os.path.join(od, f'{key} Whats Inside.png'), name, secs, kind, pages); imgs.append(f'{key}/{key} Whats Inside.png')
        fname = safe(cut(name, 60))
        if len(fname) < 3: fname = key
        shutil.copy(src, os.path.join(od, fname + ext)); files = [f'{key}/{fname}{ext}']
        if kind == 'docx':
            shutil.copy(pdf, os.path.join(od, fname + '.pdf')); files.append(f'{key}/{fname}.pdf')
        items_out.append({
            'key': key, 'sku': key, 'kind': 'doc', 'parent': sku,
            'title': etsy_title(name, niche, kind),
            'description': description(name, niche, kind, secs, pages, sku),
            'price': PRICE_XLSX if kind == 'xlsx' else PRICE_DOC, 'quantity': 999,
            'tags': tags_for(name, niche, kind), 'images': imgs, 'files': files,
            'pages': pages, 'words': words,
        })
        print(key, kind, pages, 'pages', words, 'words |', items_out[-1]['title'])
    return items_out

def main(skus):
    mpath = os.path.join(OUT, 'manifest.json')
    m = json.load(open(mpath))
    new = []
    for s in skus: new += build(s)
    keys = {i['key'] for i in new}
    m['items'] = [i for i in m['items'] if i['key'] not in keys] + new
    json.dump(m, open(mpath, 'w'), indent=1)
    print('manifest items', len(m['items']), 'added/updated', len(new))

if __name__ == '__main__':
    main(sys.argv[1:])
