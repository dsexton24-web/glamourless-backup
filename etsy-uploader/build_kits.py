#!/usr/bin/env python3
"""Build one Etsy draft package per SKU: the full supporting-document kit sold as one zip.

Images are built here. The zip itself is built on Doug's computer by
"GS Etsy Kit and Course Builder.ps1" from GS Etsy Supporting Docs\\<SKU folder>,
using kit list.csv written by this script.
Manifest items: key 'KIT-GS-XXXX', kind 'kit'. Also removes the pilot 'doc' singles.
"""
import csv, collections, json, os, re, shutil, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/claude/etsy')
import build_docs as bd

SRC = bd.SRC
OUT = bd.OUT
LOG = SRC + 'Supporting Docs Score Log.csv'
WORK = '/home/claude/etsy/kitwork/'
PRICE = 30.00
NAVY, NAVY2, STEEL, WHITE, ACCENT, PAPER = bd.NAVY, bd.NAVY2, bd.STEEL, bd.WHITE, bd.ACCENT, bd.PAPER
F = lambda b, s: ImageFont.truetype(bd.FONTB if b else bd.FONT, s)

SPECIAL = {  # non-business titles: (kit name, audience line, short subject for tags)
    'GS-0113': ('ShoreHaul 78 Micro Skiff Build Toolkit', 'for building and running the ShoreHaul 78 micro skiff', 'boat build'),
    'GS-0245': ('Helping Hands Career Entry Toolkit', 'for getting hired in healthcare and helping careers', 'career change'),
    'GS-0246': ('Tech Career Entry Toolkit', 'for breaking into an entry level tech job', 'tech career'),
    'GS-0272': ('Skilled Trade Career Entry Toolkit', 'for getting into a skilled trade', 'skilled trades'),
    'GS-0273': ('First Career Toolkit', 'for landing your first real career job', 'first job'),
    'GS-0284': ('Career Pivot Toolkit', 'for switching careers with a plan', 'career change'),
}

CATS = [
    ('Contracts and agreements', r'agreement|contract|terms|consent|release|waiver|addendum|disclosure|clause|warranty|authori[sz]ation|paperwork|legal'),
    ('Pricing and money tools', r'pric|calculat|quote|estimat|rate|margin|profit|cost|budget|financ|tax|deal math|economics|takeoff|yield|invoice'),
    ('Trackers and logs', r'track|log\b|dashboard|ledger|record|register|inventory|pipeline'),
    ('Checklists and forms', r'checklist|inspection|intake|form|sheet|report|assessment|scoping|qualification'),
    ('Scripts and sales', r'script|outreach|template|email|follow|referral|proposal|pitch|sales|marketing|prospect|objection|review|copy'),
    ('Plans and guides', r'.'),
]

def cat_of(name):
    n = name.lower()
    for c, rx in CATS:
        if re.search(rx, n): return c
    return 'Plans and guides'

def head_of(item):
    return item['title'].split(',')[0].strip()

def niche_from(head):
    n = re.sub(r'\s+Business Blueprint$', '', head)
    n = re.sub(r'^Start an? ', '', n)
    return n

def clean_doc(fn, niche):
    n = os.path.splitext(fn)[0]
    n = re.sub(r'^SD-GS-\d{4}-\d{2}\s+', '', n)
    n = re.sub(r'^\d{2}\s+', '', n)
    n = re.sub(r'\s+-\s+Wayne Thomas$', '', n)
    n = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', n)           # split CamelCase
    n = n.replace(' - ', ' ').replace('_', ' ')
    n = re.sub(r'^The\s+', '', n)
    for pre in sorted({niche, re.sub(r'^The\s+', '', niche), niche + ' Blueprint'}, key=len, reverse=True):
        if pre and n.lower().startswith(pre.lower() + ' ') and len(n) > len(pre) + 6:
            n = n[len(pre):].strip(); break
    n = re.sub(r'\s+', ' ', n).strip()
    return n[:1].upper() + n[1:]

def load_log():
    by = collections.defaultdict(list)
    for x in csv.DictReader(open(LOG, encoding='utf-8-sig')):
        by[x['SKU']].append(x)
    return by

def wrap(d, t, f, w): return bd.wrap(d, t, f, w)

def footer(d, H, W):
    ft = F(1, 40)
    d.text((110, H - 110), 'GLAMOURLESS SYSTEMS', font=ft, fill=STEEL)
    d.text((W - 110 - d.textlength('INSTANT DOWNLOAD', font=ft), H - 110), 'INSTANT DOWNLOAD', font=ft, fill=ACCENT)

def save(im, path):
    im.convert('RGB').save(path, quality=88, optimize=True)

def img_cover(path, name, aud, n, nw, nx, cats, page_png):
    W = H = 2000
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    badge = f'{n} EDITABLE FILES  ·  ' + ('WORD + EXCEL' if nx else 'WORD')
    fb = F(1, 44); bw = d.textlength(badge, font=fb)
    d.rounded_rectangle([110, 100, 110 + bw + 60, 180], radius=18, fill=ACCENT)
    d.text((140, 114), badge, font=fb, fill=NAVY)
    y = 240; ft = F(1, 100)
    for ln in wrap(d, name, ft, 1780)[:3]:
        d.text((110, y), ln, font=ft, fill=WHITE); y += 120
    fs = F(0, 50)
    for ln in wrap(d, 'Ready-made templates ' + aud, fs, 1780)[:2]:
        d.text((110, y + 10), ln, font=fs, fill=STEEL); y += 64
    top = y + 90
    # left: category counts, right: real page preview
    fc, fn_ = F(1, 112), F(0, 44)
    cy = top + 10
    for c, k in cats[:5]:
        d.text((110, cy), str(k), font=fc, fill=ACCENT)
        for i, ln in enumerate(wrap(d, c, fn_, 520)[:2]):
            d.text((270, cy + 18 + i * 52), ln, font=fn_, fill=WHITE)
        cy += 190
    p = Image.open(page_png).convert('RGB')
    ph = H - top - 190; s = ph / p.height
    p = p.resize((int(p.width * s), ph))
    if p.width > 1080: p = p.crop((0, 0, 1080, ph))
    x = W - 110 - p.width
    d.rectangle([x - 8, top - 8, x + p.width + 8, top + p.height + 8], fill=ACCENT)
    im.paste(p, (x, top))
    footer(d, H, W); save(im, path)

def img_preview(path, page_png, docname):
    W = H = 2000
    im = bd.framed(page_png, W, H - 160)
    full = Image.new('RGB', (W, H), PAPER); full.paste(im, (0, 160))
    d = ImageDraw.Draw(full)
    d.rectangle([0, 0, W, 160], fill=NAVY)
    f = F(1, 52)
    t = 'Sample page: ' + docname
    while d.textlength(t, font=f) > 1800 and len(t) > 20: t = t[:-4] + '...'
    d.text((100, 50), t, font=f, fill=WHITE)
    save(full, path)

def img_contents(path, name, docs, part=None):
    W = H = 2000
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 300], fill=NAVY2)
    d.text((110, 90), 'Every file in this kit' + (f'  ({part})' if part else ''), font=F(1, 84), fill=WHITE)
    d.text((110, 205), name, font=F(0, 46), fill=STEEL)
    two = len(docs) > 12
    fi = F(0, 40 if two else 48); fchip = F(1, 30 if two else 34)
    colw = 860 if two else 1700
    xs = [110, 1040] if two else [110]
    per = (len(docs) + 1) // 2 if two else len(docs)
    for ci, x in enumerate(xs):
        y = 370
        for nm, ext in docs[ci * per:(ci + 1) * per]:
            chip = 'XLSX' if ext == '.xlsx' else 'DOCX'
            cw = d.textlength(chip, font=fchip) + 28
            d.rounded_rectangle([x, y + 6, x + cw, y + (48 if two else 56)], radius=10, fill=(ACCENT if chip == 'XLSX' else STEEL))
            d.text((x + 14, y + 12), chip, font=fchip, fill=NAVY)
            lines = wrap(d, nm, fi, colw - cw - 30)[:2]
            for ln in lines:
                d.text((x + cw + 22, y), ln, font=fi, fill=WHITE); y += (50 if two else 60)
            y += 22 if two else 30
    footer(d, H, W); save(im, path)

def img_howto(path, name, bp_head, nx):
    W = H = 2000
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    d.text((110, 120), 'How it works', font=F(1, 92), fill=WHITE)
    steps = [
        ('Buy and download', 'Etsy gives you one zip file right away on your Purchases page. Nothing is shipped.'),
        ('Unzip it', 'Double click the zip on a computer, or tap it in the Files app on a phone or tablet.'),
        ('Open and edit', 'Word files open in Microsoft Word, Google Docs or LibreOffice.' + (' Excel files open in Excel, Google Sheets or LibreOffice.' if nx else '')),
        ('Make it yours', 'Add your business name, prices and terms. Save a copy and reuse it for every customer.'),
    ]
    y = 330; fh, fb_ = F(1, 58), F(0, 46)
    for i, (h, b) in enumerate(steps, 1):
        d.ellipse([110, y, 210, y + 100], fill=ACCENT)
        d.text((160 - d.textlength(str(i), font=F(1, 60)) / 2, y + 14), str(i), font=F(1, 60), fill=NAVY)
        d.text((260, y), h, font=fh, fill=WHITE)
        yy = y + 78
        for ln in wrap(d, b, fb_, 1620)[:3]:
            d.text((260, yy), ln, font=fb_, fill=STEEL); yy += 58
        y = yy + 60
    d.rounded_rectangle([110, y + 10, 1890, y + 250], radius=24, outline=ACCENT, width=4)
    fl = F(0, 44)
    yy = y + 50
    for ln in wrap(d, f'These are the working documents from the {bp_head}. The full step by step blueprint is sold separately in our shop.', fl, 1700)[:3]:
        d.text((150, yy), ln, font=fl, fill=WHITE); yy += 56
    footer(d, H, W); save(im, path)

SHORT = {'Contracts and agreements': 'Contracts', 'Pricing and money tools': 'Pricing Tools', 'Trackers and logs': 'Trackers',
         'Checklists and forms': 'Checklists', 'Scripts and sales': 'Scripts', 'Plans and guides': 'Guides'}
def etsy_title(name, short, n, cats=(), nx=0):
    w = [SHORT[c] for c, _ in cats][:3]
    mix = (', '.join(w[:-1]) + ' and ' + w[-1]) if len(w) > 1 else (w[0] if w else 'Forms')
    fmt = 'Word and Excel' if nx else 'Word'
    for t in (f'{name}, {n} Editable Templates, {mix}, {fmt} Small Business Forms Bundle',
              f'{name}, {n} Editable Templates, {mix}, Small Business Forms',
              f'{name}, {n} Editable Business Templates, Instant Download',
              f'{name}, {n} Editable Templates'):
        if len(t) <= 140: return t
    return bd.cut(name, 140)

def tags_for(short, nx, special):
    t = []
    def add(x):
        x = x.lower().strip()
        if 3 <= len(x) <= 20 and x not in t: t.append(x)
    w = [x for x in re.sub(r'[^a-z0-9 ]', ' ', short.lower()).split() if x not in ('and', 'the', 'a', 'of', 'for')]
    add(' '.join(w[:2])); add(' '.join(w[:2]) + ' business'); add(' '.join(w[:3]))
    if special: add(special)
    for g in ['business templates', 'business forms', 'contract template', 'startup toolkit', 'small business kit',
              'business checklist', 'editable templates', 'word template'] + (['excel tracker'] if nx else []) + \
             ['side hustle', 'business bundle', 'digital download', 'business planner']:
        if len(t) >= 13: break
        add(g)
    return t[:13]

def description(name, aud, bp_head, groups, n, nw, nx):
    L = [f'{name}: {n} ready-made, editable documents {aud}. Skip the blank page. Open a file, put in your details, and use it today.', '',
         "WHAT'S INSIDE"]
    for c, docs in groups:
        L.append(f'{c} ({len(docs)})')
        L += ['- ' + x for x in docs]
    L += ['', 'WHAT YOU GET',
          f'- One zip file with all {n} documents',
          f'- {nw} editable Word document' + ('s' if nw != 1 else '') + (f' and {nx} Excel workbook' + ('s' if nx != 1 else '') if nx else ''),
          '- A Read Me First file that lists every document by type',
          '- Works in Microsoft Word, Google Docs, Excel, Google Sheets and free LibreOffice',
          '', 'HOW IT WORKS',
          'This is a digital download. Nothing is shipped. After you buy, Etsy gives you the zip file right away on your Purchases page. Unzip it, open any file, and edit it like a normal document.',
          '', 'PART OF A BIGGER SYSTEM',
          f'These are the working documents from the {bp_head} by Glamourless Systems. The blueprint is the full step by step plan and is sold separately. This kit works on its own, and it works best next to the blueprint.',
          '', 'GOOD TO KNOW',
          'These templates are for education and planning. They are not legal, tax or financial advice. Contracts and agreements are starting points: have a local attorney review them before you rely on them, and check the rules where you work.',
          'Written by Wayne Thomas for Glamourless Systems, with help from AI writing tools.',
          '', 'Because this is a digital file, all sales are final. If something is wrong with your download, message us and we will make it right.']
    return '\n'.join(L)

def readme(name, bp_head, docs):
    L = [name, 'Glamourless Systems', '', 'START HERE', 'Every file in this zip is an editable template. Open it, save your own copy, and fill it in.',
         'Word files (.docx) open in Microsoft Word, Google Docs or LibreOffice.',
         'Excel files (.xlsx) open in Microsoft Excel, Google Sheets or LibreOffice.', '',
         'WHAT EACH FILE IS FOR']
    for c, ds in docs:
        L.append(''); L.append(c.upper())
        L += ['- ' + x for x in ds]
    L += ['', 'THE FULL PLAN', f'These documents come from the {bp_head}. The blueprint walks through the whole business step by step and is sold separately in our Etsy shop.',
          '', 'GOOD TO KNOW', 'These templates are for education and planning, not legal, tax or financial advice. Have a local attorney review any contract or agreement before you use it.',
          '', 'Questions or a problem with a file? Message us on Etsy and we will make it right.']
    return '\r\n'.join(L) + '\r\n'

def page_png_for(sku, rows, wd):
    v = [x for x in rows if x['Document'].lower().endswith('.docx')]
    v.sort(key=lambda x: -int(x['Score']))
    for x in v:
        src = os.path.join(SRC, x['Folder'], x['Document'])
        if os.path.exists(src):
            pdf = bd.to_pdf(src, wd)
            if pdf:
                pngs = bd.render(pdf, os.path.join(wd, 'pg'), 1)
                if pngs: return pngs[0], x['Document']
    return None, None

def build(sku, rows, bp):
    head = head_of(bp)
    if sku in SPECIAL:
        name, aud, special = SPECIAL[sku]; short = name.replace(' Toolkit', '')
    else:
        niche = niche_from(head); name = f'{niche} Business Toolkit'; aud = 'for running ' + bd.art(niche) + ' business'
        short = niche; special = None
    if len(name) > 60: name = name[:60].rsplit(' ', 1)[0]
    key = 'KIT-' + sku
    rows = [r for r in rows if os.path.splitext(r['Document'])[1].lower() in ('.docx', '.xlsx')]
    rows.sort(key=lambda r: r['Document'])
    docs = []
    for r in rows:
        ext = os.path.splitext(r['Document'])[1].lower()
        docs.append((clean_doc(r['Document'], short if not special else ''), ext))
    n = len(docs); nx = sum(1 for _, e in docs if e == '.xlsx'); nw = n - nx
    g = collections.OrderedDict((c, []) for c, _ in CATS)
    for nm, e in docs: g[cat_of(nm) if e != '.xlsx' or not re.search(r'pric|calc|profit|cost|budget', nm.lower()) else 'Pricing and money tools'].append(nm)
    groups = [(c, v) for c, v in g.items() if v]
    cats = sorted([(c, len(v)) for c, v in groups], key=lambda x: -x[1])
    wd = os.path.join(WORK, key); shutil.rmtree(wd, ignore_errors=True); os.makedirs(wd)
    png, pdoc = page_png_for(sku, rows, wd)
    if not png: print(key, 'NO PREVIEW'); return None
    od = os.path.join(OUT, key); shutil.rmtree(od, ignore_errors=True); os.makedirs(od)
    imgs = []
    def P(nm): imgs.append(f'{key}/{key} {nm}.jpg'); return os.path.join(od, f'{key} {nm}.jpg')
    img_cover(P('Cover'), name, aud, n, nw, nx, cats, png)
    img_preview(P('Sample Page'), png, clean_doc(pdoc, short if not special else ''))
    if n > 26:
        img_contents(P('Contents'), name, docs[:26], 'part 1'); img_contents(P('Contents Two'), name, docs[26:], 'part 2')
    else:
        img_contents(P('Contents'), name, docs)
    img_howto(P('How It Works'), name, head, nx)
    open(os.path.join(od, 'Read Me First.txt'), 'w', encoding='utf-8').write(readme(name, head, groups))
    zipname = bd.safe(name) + '.zip'
    return {
        'key': key, 'sku': key, 'kind': 'kit', 'parent': sku,
        'title': etsy_title(name, short, n, cats, nx),
        'description': description(name, aud, head, groups, n, nw, nx),
        'price': PRICE, 'quantity': 999,
        'tags': tags_for(short, nx, special), 'images': imgs, 'files': [f'{key}/{zipname}'],
        'docs': n, 'source_folder': rows[0]['Folder'] if rows else '',
    }

def main(only):
    mpath = os.path.join(OUT, 'manifest.json'); m = json.load(open(mpath))
    bps = {i['sku']: i for i in m['items'] if i['kind'] == 'blueprint'}
    log = load_log(); new = []
    for sku in sorted(bps):
        if only and sku not in only: continue
        if sku not in log: print(sku, 'no docs'); continue
        it = build(sku, log[sku], bps[sku])
        if it: new.append(it); print(it['key'], it['docs'], '|', it['title'][:90], flush=True)
    keys = {i['key'] for i in new}
    m['items'] = [i for i in m['items'] if i['key'] not in keys and i['kind'] != 'doc'] + new
    json.dump(m, open(mpath, 'w'), indent=1)
    with open(os.path.join(OUT, 'kit list.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['Key', 'SourceFolder', 'ZipName'])
        for i in sorted([x for x in m['items'] if x['kind'] == 'kit'], key=lambda x: x['key']):
            w.writerow([i['key'], i['source_folder'], i['files'][0].split('/', 1)[1]])
    print('manifest items', len(m['items']), 'kits', sum(1 for i in m['items'] if i['kind'] == 'kit'))

if __name__ == '__main__':
    main(sys.argv[1:])
