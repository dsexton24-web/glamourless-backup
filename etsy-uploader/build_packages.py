"""GS Etsy package builder.

For each eligible blueprint SKU it writes, into  out/GS Etsy Upload Packages/<SKU>/ :
  - "<SKU> Start Here.pdf"    the one-page guide that goes in every download (brings buyers back to GS)
  - "<SKU> Whats Inside.png"  a listing photo with the page and chapter count and chapter names
and one manifest.json listing every Etsy item, with file paths relative to the
"Glamourless Systems Main" Drive folder that Doug picks in the uploader page.

Inputs:
  catalog.json   SKU metadata from the website library (title, category, description ...)
  sources.json   per SKU: {dir, pdf, docx, cover, mockup}  (paths relative to Glamourless Systems Main)
  pdf files      staged copies of each Print Edition PDF (for page count and chapter list)
"""
import json, shutil, os, re, sys, textwrap
import pypdf
from chapters import chapters as chapter_list
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

STAGE = '/mnt/user-data/uploads/Glamourless Systems Main/'
OUT = 'out/GS Etsy Upload Packages/'
PKG_REL = 'GS Etsy Upload Packages/'
PRICE_BLUEPRINT = 27.00

pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
FONT = '/usr/share/fonts/opentype/inter/Inter-Regular.otf'
FONTB = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'

NAVY, NAVY2, STEEL, WHITE, ACCENT = '#061529', '#0E2A52', '#9DB4CF', '#FFFFFF', '#5B9BFF'


def safe_file_name(name):
    # Etsy digital file names: 3 to 70 characters, letters, numbers, spaces, hyphens, underscores, periods
    base, ext = os.path.splitext(name)
    base = re.sub(r"[^A-Za-z0-9 ._-]", "", base)
    base = re.sub(r"\s+", " ", base).strip()
    return base[:70 - len(ext)].rstrip() + ext


def clean_title(t):
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def short_name(title):
    n = re.sub(r'\bBlueprint\b', '', title)
    n = re.sub(r'^The\s+', '', n.strip())
    return re.sub(r'\s+', ' ', n).strip(' -')


def chapters_of(pdf_path):
    r = pypdf.PdfReader(pdf_path)
    out = []
    for x in r.outline:
        if isinstance(x, list):
            continue
        t = re.sub(r'\s+', ' ', x.title).strip()
        t = re.sub(r'^Chapter\s+\d+\s*[:.-]\s*', '', t)
        if not t or re.match(r'(?i)^(disclaimer|how to use this book|current platform sources|sources|the last word|closing)', t):
            continue
        out.append(t)
    return len(r.pages), out


def first_paragraph(pdf_path):
    r = pypdf.PdfReader(pdf_path)
    for i in range(2, min(6, len(r.pages))):
        txt = r.pages[i].extract_text() or ''
        if 'DISCLAIMER' in txt.upper()[:200]:
            continue
        lines = [l.strip() for l in txt.split('\n')[2:] if l.strip()]
        para = ' '.join(lines)
        para = re.sub(r'\s+', ' ', para)
        sents = re.split(r'(?<=[.!?])\s+', para)
        s = ' '.join(sents[:2]).strip()
        if len(s) > 60:
            return s
    return ''


def etsy_title(title):
    base = short_name(title)
    base = re.sub(r'\s+Business$', '', base)
    t = f'{base} Business Blueprint, Step by Step Startup Plan, Printable PDF and Editable Word Guide'
    if len(t) > 140:
        t = f'{base} Business Blueprint, Startup Plan, PDF and Editable Word'
    if len(t) > 140:
        t = f'{base} Business Blueprint PDF'[:140]
    for ch in '%:&+':  # Etsy allows each of these once at most
        if t.count(ch) > 1:
            t = t.replace(ch, ' ')
    return re.sub(r'\s+', ' ', t).strip()


def tags_for(meta):
    base = short_name(meta['title']).lower()
    cand = []
    words = [w for w in re.findall(r"[a-z0-9']+", base) if w not in {'the', 'and', 'a', 'of', 'to', 'for', 'on', 'in', 'your'}]
    if len(base) <= 20:
        cand.append(base)
    for two in ([' '.join(words[:2]), ' '.join(words[-2:])] if len(words) > 2 else []):
        if len(two) <= 20:
            cand.append(two)
    for w in (meta.get('secondary', ''), meta.get('category', '')):
        w = re.sub(r"[^a-z0-9 '-]", '', w.lower()).strip()
        if w and len(w) <= 20:
            cand.append(w)
    cand += ['business plan', 'startup guide', 'small business', 'side hustle', 'business blueprint',
             'start a business', 'business template', 'entrepreneur gift', 'digital download']
    out = []
    for c in cand:
        c = re.sub(r'\s+', ' ', c).strip()
        if c and c not in out and len(c) <= 20:
            out.append(c)
    return out[:13]


def unit(ch, pages=999):
    return 'chapters' if len(ch) <= 40 and len(ch) <= pages * 0.75 else 'sections'


def description(meta, pages, chapters, opener):
    name = clean_title(meta['title'])
    lead = meta.get('description') or opener
    if opener and len(lead) < 120:
        lead = (lead.rstrip('.') + '. ' + opener).strip()
    who = []
    if meta.get('customer') == 'B2B':
        who.append('Built for people who want to sell a service to other businesses.')
    elif meta.get('customer') == 'B2C':
        who.append('Built for people who want to serve households and everyday customers.')
    if meta.get('location') == 'REMOTE':
        who.append('You can run it from home or online.')
    elif meta.get('location') == 'LOCAL':
        who.append('You run it as a local business in your own area.')
    if meta.get('budget'):
        who.append('Starting budget: ' + meta['budget'].replace('Under ', 'under ') + '.')
    show = chapters[:14]
    more = len(chapters) - len(show)
    lines = [
        lead,
        '',
        f'{name} is a complete written business plan you can follow step by step. It is {pages} pages long and walks through {len(chapters)} {unit(chapters, pages)}, from the first decision to steady customers.',
        '',
        "WHAT'S INSIDE",
    ] + ['- ' + c for c in show] + ([f'- plus {more} more {unit(chapters, pages)}'] if more > 0 else []) + [
        '',
        'WHAT YOU GET',
        '- The full blueprint as a printable PDF',
        '- The same blueprint as an editable Word document, so you can make it your own',
        '- A one-page Start Here guide',
        '',
    ]
    if who:
        lines += ['WHO IT IS FOR', ' '.join(who), '']
    lines += [
        'HOW IT WORKS',
        'This is a digital download. Nothing is shipped. After you buy, Etsy gives you the download right away on the Purchases page. The PDF opens on any phone, tablet or computer. The Word file opens in Microsoft Word, Google Docs or any free word processor.',
        '',
        'GOOD TO KNOW',
        'This blueprint is for education and planning. It does not promise any income or results, and it is not legal, tax or financial advice. Check current rules and costs where you live before you start.',
        'Written by Wayne Thomas for Glamourless Systems, with help from AI writing tools.',
        '',
        'Because this is a digital file, all sales are final. If something is wrong with your download, message us and we will make it right.',
    ]
    return '\n'.join(lines)


def start_here_pdf(path, meta):
    c = canvas.Canvas(path, pagesize=letter)
    W, H = letter
    c.setFillColor(NAVY); c.rect(0, H - 120, W, 120, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont('DVB', 22); c.drawString(54, H - 70, 'Start Here')
    c.setFont('DV', 12); c.drawString(54, H - 95, clean_title(meta['title']))
    y = H - 160
    c.setFillColor('#111111')

    def para(head, body):
        nonlocal y
        c.setFont('DVB', 13); c.drawString(54, y, head); y -= 20
        c.setFont('DV', 11.5)
        for line in textwrap.wrap(body, 88):
            c.drawString(54, y, line); y -= 16
        y -= 12

    para('Thank you for your purchase.', 'Your download has two files: the blueprint as a printable PDF and the same blueprint as an editable Word document. Open the PDF to read it on any device. Open the Word file to type in your own notes and numbers.')
    para('How to use it', 'Read it once from start to finish so you see the whole business. Then go back and work through it chapter by chapter. Keep the Word version as your working copy and update it as you go.')
    para('Your next step', 'This blueprint is one part of a complete system. Glamourless Systems also makes the supporting documents, worksheets, a step-by-step course and calculators that go with it. To see which pieces fit where you are right now, take the free assessment at glamourlesssystems.com. It takes about five minutes.')
    para('Need help?', 'If anything is wrong with your files, send us a message on Etsy and we will fix it.')
    c.setFont('DV', 9); c.setFillColor('#555555')
    c.drawString(54, 54, 'Glamourless Systems | Build Your Profit Scaffold for Your Future.')
    c.save()


def whats_inside_png(path, meta, pages, chapters):
    S = 2000
    im = Image.new('RGB', (S, S), NAVY)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, S, 360], fill=NAVY2)
    fb = ImageFont.truetype(FONTB, 96); fr = ImageFont.truetype(FONT, 52); fs = ImageFont.truetype(FONT, 46); fbs = ImageFont.truetype(FONTB, 60)
    d.text((110, 90), "WHAT'S INSIDE", font=fb, fill=WHITE)
    name = short_name(meta['title'])
    d.text((110, 230), (name[:52] + '...') if len(name) > 55 else name, font=fr, fill=STEEL)
    stats = [(str(pages), 'pages'), (str(len(chapters)), unit(chapters, pages)), ('PDF + Word', 'instant download')]
    x = 110
    for big, small in stats:
        d.text((x, 440), big, font=fbs, fill=ACCENT)
        d.text((x, 520), small, font=fs, fill=STEEL)
        x += 620
    y = 660
    show = chapters[:13]
    for ch in show:
        line = ch if len(ch) <= 62 else ch[:60].rstrip() + '...'
        d.ellipse([110, y + 20, 130, y + 40], fill=ACCENT)
        d.text((160, y), line, font=fs, fill=WHITE)
        y += 82
    if len(chapters) > len(show):
        d.text((160, y), f'plus {len(chapters) - len(show)} more {unit(chapters, pages)}', font=fs, fill=STEEL)
    d.text((110, S - 110), 'GLAMOURLESS SYSTEMS', font=fs, fill=STEEL)
    im.save(path, optimize=True)


def main(skus):
    cat = json.load(open('catalog.json'))
    src = json.load(open('sources.json'))
    os.makedirs(OUT, exist_ok=True)
    mpath = OUT + 'manifest.json'
    manifest = json.load(open(mpath)) if os.path.exists(mpath) else {'items': []}
    have = {i['key']: i for i in manifest['items']}
    for sku in skus:
        s = src[sku]
        pdf_local = STAGE + s['pdf']
        pages, chapters = chapter_list(pdf_local, STAGE + s['docx'] if s.get('docx') else None)
        chapters = [c for i, c in enumerate(chapters) if not (i < 3 and ('blueprint' in c.lower() or c.lower().startswith('solving')))]
        opener = first_paragraph(pdf_local)
        meta = cat.get(sku) or {'sku': sku, 'title': s['title']}
        meta['title'] = s['title'] if not cat.get(sku) else meta['title']
        d = OUT + sku + '/'
        os.makedirs(d, exist_ok=True)
        start = f'{sku} Start Here.pdf'
        inside = f'{sku} Whats Inside.png'
        start_here_pdf(d + start, meta)
        whats_inside_png(d + inside, meta, pages, chapters)
        # copy sources into the package folder so it is self-contained, with clean file names
        nice = safe_file_name(f"{sku} {short_name(clean_title(meta['title']))} Blueprint")
        imgs, files = [], []
        for k in ('cover', 'mockup'):
            if s.get(k):
                fn = os.path.basename(s[k])
                if len(fn) > 70:
                    stem, ext = os.path.splitext(fn)
                    stem = stem.replace(' The ', ' ').replace(' Blueprint', '')
                    fn = (stem[:70 - len(ext)].rstrip() + ext)
                shutil.copyfile(STAGE + s[k], d + fn); imgs.append(sku + '/' + fn)
        for k in ('pdf', 'docx'):
            if s.get(k):
                fn = nice + '.' + k; shutil.copyfile(STAGE + s[k], d + fn); files.append(sku + '/' + fn)
        item = {
            'key': sku + '-blueprint', 'sku': sku, 'kind': 'blueprint',
            'title': etsy_title(meta['title']),
            'description': description(meta, pages, chapters, opener),
            'price': PRICE_BLUEPRINT, 'quantity': 999,
            'tags': tags_for(meta),
            'images': imgs + [sku + '/' + inside],
            'files': files + [sku + '/' + start],
            'pages': pages, 'chapters': len(chapters),
        }
        have[item['key']] = item
        print(sku, pages, 'pages', len(chapters), 'chapters', '|', item['title'])
    manifest['items'] = sorted(have.values(), key=lambda i: i['key'])
    json.dump(manifest, open(mpath, 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1:])
