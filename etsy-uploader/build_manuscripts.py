#!/usr/bin/env python3
"""Build Etsy draft packages for the 14 GS ebooks (kind 'book', key 'BK-GS-XXXX-NN'). Ships the PDF only."""
import glob, json, os, re, shutil, subprocess, sys
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/claude/etsy')
import build_docs as bd, build_kits as bk, docx

SRC = '/mnt/user-data/uploads/Glamourless Systems Main/GS Etsy Manuscripts/'
WORK = '/home/claude/etsy/mswork/'
OUT = bd.OUT
NAVY, NAVY2, STEEL, WHITE, ACCENT, PAPER = bd.NAVY, bd.NAVY2, bd.STEEL, bd.WHITE, bd.ACCENT, bd.PAPER
F = bk.F
BOOKS = {
 'SD-GS-0119-01': ('Answer Every Call', 'Capture More Leads and Stop Losing Revenue From Missed Calls', ['missed calls', 'lead capture', 'call handling', 'phone sales']),
 'SD-GS-0119-02': ('Community Before Ads', 'Win Customers Through Local Communities, Trust and Referrals', ['community building', 'local marketing', 'referral marketing', 'word of mouth']),
 'SD-GS-0119-03': ('How to Stay Valuable in the Age of AI', 'Build Skills, Income and Work That Machines Cannot Easily Replace', ['ai career', 'future of work', 'career guide', 'ai skills']),
 'SD-GS-0119-04': ('Survive AI Search', 'Keep Your Business Visible as Google and AI Search Change the Rules', ['ai search', 'local seo', 'google visibility', 'seo guide']),
 'SD-GS-0119-05': ('The Anti Slop Content Playbook', 'Human Content, Trust and Proof in a World of AI Noise', ['content marketing', 'content strategy', 'ai content', 'social media guide']),
 'SD-GS-0119-06': ('The One Person Operator Stack', 'Run Intake, Quoting, Scheduling and Follow Up Without a Big Team', ['solopreneur', 'business automation', 'small business tools', 'ai automation']),
 'SD-GS-0197-01': ('The No Drop Pipeline', 'The Follow Up and Sales Pipeline Operating System', ['sales pipeline', 'follow up system', 'crm guide', 'lead tracking']),
 'SD-GS-0197-02': ('The Objection Diagnosis and Prevention Playbook', 'Find the Real Concern and Close More Deals', ['sales objections', 'sales training', 'closing deals', 'sales playbook']),
 'SD-GS-0197-03': ('The No Chase Close', 'A Practical Sales System Without Pressure or Endless Follow Up', ['sales system', 'closing deals', 'sales training', 'sales playbook']),
 'SD-GS-0197-04': ('Universal Contracts and Paperwork Toolkit', 'Agreements, Templates and Forms for Any Small Business', ['contract templates', 'business contracts', 'service agreement', 'business forms']),
 'SD-GS-0197-05': ('Admin Booster', 'Business Credit and Financial Foundation Playbook', ['business credit', 'llc setup', 'business finance', 'business admin']),
 'SD-GS-0197-06': ('Glamourless Copy Lab', 'The Plain Spoken Copywriting Playbook for Small Business', ['copywriting', 'sales copy', 'marketing copy', 'copywriting guide']),
 'SD-GS-0197-07': ('The Cold Call Playbook', 'Reach Decision Makers and Win New Business by Phone', ['cold calling', 'sales scripts', 'b2b sales', 'phone sales']),
 'SD-GS-0197-08': ('How to Actually Get Customers', 'The Customer Acquisition Playbook for Local, B2B and Online Businesses', ['get customers', 'marketing plan', 'customer acquisition', 'small biz marketing']),
}

def chapters(path):
    d = docx.Document(path); out = []
    for p in d.paragraphs:
        t = p.text.strip()
        if not t or len(t) > 90: continue
        st = p.style.name if p.style is not None else ''
        if st.startswith('Heading 1') or re.match(r'^(Chapter|Part|Section)\s+\d+\s*:', t, re.I):
            t = re.sub(r'\s+', ' ', t)
            if t.isupper(): t = t.title()
            if t not in out: out.append(t)
    return out

def render(pdf, wd, pages, r=110):
    out = []
    for pg in pages:
        pre = os.path.join(wd, f'r{pg}')
        subprocess.run(['pdftoppm', '-png', '-r', str(r), '-f', str(pg), '-l', str(pg), pdf, pre], check=True)
        out.append(sorted(glob.glob(pre + '*.png'))[0])
    return out

def img_cover(path, cover_png, pages, nch):
    W = H = 2000
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    p = Image.open(cover_png).convert('RGB')
    w, h = p.size; top = int(h * 0.022); p = p.crop((0, top, w, h - int(h * 0.03)))  # trim running header/footer
    s = 1680 / p.height; p = p.resize((int(p.width * s), 1680))
    x = 140
    d.rectangle([x + 22, 182, x + p.width + 22, 182 + p.height], fill='#020A16')
    im.paste(p, (x, 160))
    rx = x + p.width + 90
    fb, fs = F(1, 64), F(0, 40)
    y = 300
    for big, small in [('EBOOK', 'instant PDF download'), (str(pages), 'pages'), (str(nch), 'chapters and parts'), ('PDF', 'phone, tablet, computer')]:
        d.text((rx, y), big, font=fb, fill=ACCENT); y += 80
        for ln in bd.wrap(d, small, fs, W - rx - 80)[:2]: d.text((rx, y), ln, font=fs, fill=WHITE); y += 50
        y += 70
    d.text((140, H - 90), 'GLAMOURLESS SYSTEMS  ·  BY WAYNE THOMAS', font=F(1, 36), fill=STEEL)
    im.save(path, quality=88, optimize=True)

def img_toc(path, title, chs):
    W = H = 2000
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 300], fill=NAVY2)
    d.text((110, 90), 'Inside the book', font=F(1, 84), fill=WHITE); d.text((110, 205), title, font=F(0, 46), fill=STEEL)
    two = len(chs) > 12; fi = F(0, 40 if two else 48)
    xs = [110, 1040] if two else [110]; colw = 840 if two else 1700
    show = chs[:28]; per = (len(show) + 1) // 2 if two else len(show)
    for ci, x in enumerate(xs):
        y = 370
        for t in show[ci * per:(ci + 1) * per]:
            d.rectangle([x, y + 18, x + 16, y + 34], fill=ACCENT)
            for ln in bd.wrap(d, t, fi, colw - 50)[:2]: d.text((x + 40, y), ln, font=fi, fill=WHITE); y += 52 if two else 60
            y += 20
    if len(chs) > 28: d.text((150, H - 200), f'plus {len(chs) - 28} more sections', font=F(0, 44), fill=STEEL)
    bk.footer(d, H, W); im.save(path, quality=88, optimize=True)

def img_page(path, png, cap):
    W = H = 2000
    im = bd.framed(png, W, H - 160)
    full = Image.new('RGB', (W, H), PAPER); full.paste(im, (0, 160))
    d = ImageDraw.Draw(full); d.rectangle([0, 0, W, 160], fill=NAVY); d.text((100, 50), cap, font=F(1, 52), fill=WHITE)
    full.save(path, quality=88, optimize=True)

def find_page(pdf, pattern, start=3):
    n = bd.page_count(pdf)
    for pg in range(start, n + 1):
        t = subprocess.run(['pdftotext', '-f', str(pg), '-l', str(pg), pdf, '-'], capture_output=True, text=True).stdout
        if re.search(pattern, t) and len(t.split()) > 250: return pg
    return min(start + 2, n)

def build(path):
    key0 = os.path.basename(path)[:13]; title, sub, kw = BOOKS[key0]
    key = 'BK-' + key0[3:]
    wd = os.path.join(WORK, key0); os.makedirs(wd, exist_ok=True)
    pdf = (glob.glob(wd + '/*.pdf') or [None])[0] or bd.to_pdf(path, wd)
    pages = bd.page_count(pdf); chs = chapters(path)
    p1 = find_page(pdf, r'.', max(3, round(pages * 0.18)))
    p2 = find_page(pdf, r'.', max(p1 + 1, round(pages * 0.45)))
    cover, a, b = render(pdf, wd, [1, p1, p2])
    od = os.path.join(OUT, key); shutil.rmtree(od, ignore_errors=True); os.makedirs(od)
    imgs = []
    def P(n): imgs.append(f'{key}/{key} {n}.jpg'); return os.path.join(od, f'{key} {n}.jpg')
    img_cover(P('Cover'), cover, pages, len(chs))
    img_toc(P('Contents'), title, chs)
    img_page(P('Sample Page'), a, 'Sample page')
    img_page(P('Sample Page Two'), b, 'Sample page')
    fname = bd.safe(title) + ' by Wayne Thomas.pdf'
    shutil.copy(pdf, os.path.join(od, fname))
    et = None
    for t in (f'{title}, {sub}, {pages} Page Ebook PDF, Small Business Guide',
              f'{title}, {sub}, Ebook PDF', f'{title}, {pages} Page Small Business Ebook PDF'):
        if len(t) <= 140: et = t; break
    tags = []
    for g in kw + ['ebook', 'small business', 'business ebook', 'pdf ebook', 'business guide', 'entrepreneur', 'side hustle', 'digital download', 'business book']:
        g = g.lower()
        if 3 <= len(g) <= 20 and g not in tags and len(tags) < 13: tags.append(g)
    D = [f'{title}: {sub}. A plain spoken, practical {pages} page ebook by Wayne Thomas for people who run, or want to run, a small business.', '',
         "WHAT'S INSIDE"] + ['- ' + c for c in chs[:30]] + ([f'- plus {len(chs) - 30} more sections'] if len(chs) > 30 else []) + ['',
         'WHAT YOU GET', f'- The full book as a {pages} page PDF', '- Reads on any phone, tablet, e-reader app or computer, and prints cleanly', '',
         'HOW IT WORKS', 'This is a digital download. Nothing is shipped. After you buy, Etsy gives you the PDF right away on your Purchases page.', '',
         'GOOD TO KNOW', 'This book is for education and planning. It does not promise any income or results, and it is not legal, tax or financial advice. Check the rules where you live before you act on it.',
         'Written by Wayne Thomas for Glamourless Systems, with help from AI writing tools.', '',
         'Because this is a digital file, all sales are final. If something is wrong with your download, message us and we will make it right.']
    if key0 == 'SD-GS-0197-04':
        D.insert(-4, 'The contract and agreement templates in this book are starting points. Have a local attorney review any contract before you use it.')
    return {'key': key, 'sku': key, 'kind': 'book', 'parent': key0[3:10], 'title': et, 'description': '\n'.join(D),
            'price': 14.00 if pages >= 85 else 12.00, 'quantity': 999, 'tags': tags, 'images': imgs,
            'files': [f'{key}/{fname}'], 'pages': pages, 'chapters': len(chs)}

def main():
    mpath = os.path.join(OUT, 'manifest.json'); m = json.load(open(mpath)); new = []
    for f in sorted(glob.glob(SRC + '*/*.docx')):
        it = build(f); new.append(it); print(it['key'], it['pages'], 'pages', it['chapters'], 'ch', it['price'], '|', it['title'], flush=True)
    keys = {i['key'] for i in new}
    m['items'] = [i for i in m['items'] if i['key'] not in keys] + new
    json.dump(m, open(mpath, 'w'), indent=1)
    print('manifest items', len(m['items']))

if __name__ == '__main__':
    main()
