#!/usr/bin/env python3
"""Build one Etsy draft package per interactive course (kind 'course', key 'CRS-GS-XXXX').
Uses screenshots + info.json made by course_shots.py in crs/<SKU>/.
The course zip (html + Read Me First) is built here.
"""
import glob, json, os, re, sys, zipfile
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/claude/etsy')
import build_docs as bd
import build_kits as bk

SRC = '/mnt/user-data/uploads/Glamourless Systems Main/GS Etsy Courses/'
CRS = '/home/claude/etsy/crs/'
OUT = bd.OUT
NAVY, NAVY2, STEEL, WHITE, ACCENT, PAPER = bd.NAVY, bd.NAVY2, bd.STEEL, bd.WHITE, bd.ACCENT, bd.PAPER
F = bk.F
MIN_WORDS = 1500
SPECIAL = {'GS-0113': 'ShoreHaul 78 Micro Skiff Build', 'GS-0245': 'Helping Hands Career Entry', 'GS-0246': 'Tech Career Entry',
           'GS-0272': 'Skilled Trade Career Entry', 'GS-0273': 'First Career', 'GS-0284': 'Career Pivot'}

def modules(text):
    L = [l.strip() for l in text.split('\n') if l.strip()]
    mods = {}
    for i, l in enumerate(L[:-1]):
        m = re.match(r'^(?:Module|Lesson|Chapter)\s+0?(\d{1,2})\s*(?:of\s+\d+)?\s*[:.\-–—•·]?\s*(.*)$', l)
        if not m: continue
        n = int(m.group(1)); t = m.group(2).strip()
        if not t or re.match(r'^(of\b|Days?\b|Before\b|Week\b|\d)', t): t = L[i + 1]
        if re.match(r'^(Module|Lesson|Chapter|Days?|Before|Week|Start|\d+$)', t) or len(t) < 4 or len(t) > 90: continue
        mods.setdefault(n, t)
    out = [mods[k] for k in sorted(mods) if k > 0]
    return out

def frame_shot(png, w):
    p = Image.open(png).convert('RGB'); s = w / p.width
    return p.resize((w, int(p.height * s)))

def device(im, shot, x, y, w):
    s = frame_shot(shot, w)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x - 18, y - 46, x + w + 18, y + s.height + 18], radius=22, fill='#1F2937')
    for i, c in enumerate(['#EF4444', '#F59E0B', '#22C55E']):
        d.ellipse([x + 6 + i * 34, y - 32, x + 26 + i * 34, y - 12], fill=c)
    im.paste(s, (x, y)); return s.height

def phone(im, shot, x, y, w):
    p = Image.open(shot).convert('RGB'); s = w / p.width
    p = p.resize((w, int(p.height * s)))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x - 22, y - 22, x + w + 22, y + p.height + 22], radius=48, fill='#111827')
    im.paste(p, (x, y))

def img_cover(path, name, nmods, mini, dash, ph):
    W = H = 2000
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    badge = ('MINI COURSE' if mini else 'INTERACTIVE COURSE') + '  ·  OPENS IN ANY BROWSER'
    fb = F(1, 44); bw = d.textlength(badge, font=fb)
    d.rounded_rectangle([110, 100, 110 + bw + 60, 180], radius=18, fill=ACCENT); d.text((140, 114), badge, font=fb, fill=NAVY)
    y = 240; ft = F(1, 100)
    for ln in bd.wrap(d, name, ft, 1780)[:3]:
        d.text((110, y), ln, font=ft, fill=WHITE); y += 120
    d.text((110, y + 10), f'{nmods} modules  ·  step by step  ·  checklists that save your place' if not mini else f'{nmods} short modules  ·  step by step', font=F(0, 50), fill=STEEL)
    top = y + 150
    hh = device(im, dash, 150, top, 1450)
    phone(im, ph, 1560, top + 120, 300)
    bk.footer(d, H, W); im.save(path, quality=88, optimize=True)

def img_module(path, shot):
    W = H = 2000
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 170], fill=NAVY); d.text((100, 55), 'Inside a module: learn it, do it, check it off', font=F(1, 58), fill=WHITE)
    s = frame_shot(shot, 1800)
    if s.height > 1720: s = s.crop((0, 0, 1800, 1720))
    d.rectangle([92, 222, 108 + 1800, 238 + s.height], fill='#C9D2DE'); im.paste(s, (100, 230))
    im.save(path, quality=88, optimize=True)

def img_modules(path, name, mods):
    W = H = 2000
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 300], fill=NAVY2)
    d.text((110, 90), 'What you will work through', font=F(1, 84), fill=WHITE)
    d.text((110, 205), name, font=F(0, 46), fill=STEEL)
    two = len(mods) > 10
    fi = F(0, 42 if two else 50); fn = F(1, 42 if two else 50)
    xs = [110, 1040] if two else [110]; colw = 840 if two else 1700
    per = (len(mods) + 1) // 2 if two else len(mods)
    k = 0
    for ci, x in enumerate(xs):
        y = 380
        for t in mods[ci * per:(ci + 1) * per]:
            k += 1
            d.ellipse([x, y, x + 70, y + 70], fill=ACCENT)
            num = str(k); d.text((x + 35 - d.textlength(num, font=fn) / 2, y + 8), num, font=fn, fill=NAVY)
            lines = bd.wrap(d, t, fi, colw - 110)[:2]
            yy = y + 8
            for ln in lines: d.text((x + 100, yy), ln, font=fi, fill=WHITE); yy += 54
            y = max(y + 90, yy + 30)
            if y > H - 220: break
    bk.footer(d, H, W); im.save(path, quality=88, optimize=True)

def img_howto(path, needs_bundle, bp_head, saves):
    W = H = 2000
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    d.text((110, 120), 'How it works', font=F(1, 92), fill=WHITE)
    steps = [('Download the zip', 'Etsy gives you the file right away on your Purchases page. Nothing is shipped.'),
             ('Unzip and open', 'Double click the course file. It opens in Chrome, Edge, Safari or Firefox. No login, no app, no subscription.'),
             ('Work module by module', 'Each module tells you what to learn, what to do and how to check it is done.' + (' Your progress saves in that browser.' if saves else ''))]
    y = 330
    for i, (h, b) in enumerate(steps, 1):
        d.ellipse([110, y, 210, y + 100], fill=ACCENT)
        d.text((160 - d.textlength(str(i), font=F(1, 60)) / 2, y + 14), str(i), font=F(1, 60), fill=NAVY)
        d.text((260, y), h, font=F(1, 58), fill=WHITE); yy = y + 78
        for ln in bd.wrap(d, b, F(0, 46), 1620)[:3]: d.text((260, yy), ln, font=F(0, 46), fill=STEEL); yy += 58
        y = yy + 60
    msg = (f'Built to be used with the {bp_head} and its toolkit, sold separately. The course tells you which document to open at each step.'
           if needs_bundle else f'Pairs with the {bp_head}, sold separately in our shop.')
    d.rounded_rectangle([110, y + 10, 1890, y + 300], radius=24, outline=ACCENT, width=4); yy = y + 50
    for ln in bd.wrap(d, msg, F(0, 46), 1700)[:4]: d.text((150, yy), ln, font=F(0, 46), fill=WHITE); yy += 58
    bk.footer(d, H, W); im.save(path, quality=88, optimize=True)

def tags_for(short, mini):
    t = []
    def add(x):
        x = x.lower().strip()
        if 3 <= len(x) <= 20 and x not in t: t.append(x)
    w = [x for x in re.sub(r'[^a-z0-9 ]', ' ', short.lower()).split() if x not in ('and', 'the', 'a', 'of', 'for')]
    add(' '.join(w[:2])); add(' '.join(w[:2]) + ' course'); add(' '.join(w[:3]))
    for g in ['online course', 'business course', 'interactive course', 'startup course', 'small business', 'side hustle',
              'business training', 'how to start', 'business plan', 'digital download', 'self paced course', 'entrepreneur']:
        if len(t) >= 13: break
        add(g)
    return t[:13]

def build(sku, bp):
    infos = glob.glob(CRS + sku + '/info.json')
    if not infos: print(sku, 'no shots'); return None
    info = json.load(open(infos[0]))
    src = os.path.join(SRC, info['dir'], info['file']); html = open(src, encoding='utf-8', errors='replace').read()
    import course_parse as cp
    hp = cp.parse(src)
    words = max(hp['words'], len(info['text'].split()), len(info['text2'].split()))
    if words < MIN_WORDS: print(sku, 'SKIP too thin', words); return None
    cands = [modules(info['text']), modules(info['text2']), modules('\n'.join(cp.text_lines(html))), hp['modules']]
    cands = [[m for m in c if not re.match(r'^(Chapter|Module|Part)\s*\d+$', m) and '${' not in m] for c in cands]
    mods = max(cands, key=len)
    mc = re.search(r'of (\d+) modules complete', info['text']) or re.search(r'(?m)^0\s*/\s*(\d+)$', info['text'])
    if mc and 3 <= int(mc.group(1)) < len(mods): mods = mods[:int(mc.group(1))]
    if len(mods) < 3: print(sku, 'SKIP no modules', mods); return None
    head = bk.head_of(bp)
    short = SPECIAL.get(sku) or bk.niche_from(head)
    mini = words < 6000
    name = f'{short} ' + ('Mini Course' if mini else 'Interactive Course')
    if sku not in SPECIAL and not mini: name = f'{short} Business Course'
    if sku not in SPECIAL and mini: name = f'{short} Business Mini Course'
    needs_bundle = bool(re.search(r'(?i)your (blueprint )?bundle|full bundle|in your bundle', html))
    saves = 'localStorage' in html
    key = 'CRS-' + sku; od = os.path.join(OUT, key); os.makedirs(od, exist_ok=True)
    for f in glob.glob(od + '/*'): os.remove(f)
    imgs = []
    def P(n): imgs.append(f'{key}/{key} {n}.jpg'); return os.path.join(od, f'{key} {n}.jpg')
    sd = CRS + sku
    img_cover(P('Cover'), name, len(mods), mini, sd + '/dash.png', sd + '/phone.png')
    img_module(P('Inside a Module'), sd + '/module.png')
    img_modules(P('Modules'), name, mods)
    img_howto(P('How It Works'), needs_bundle, head, saves)
    zname = bd.safe(name) + '.zip'
    readme = '\r\n'.join([name, 'Glamourless Systems', '', 'HOW TO OPEN THE COURSE',
        '1. Unzip this file (double click it on a computer, or tap it in the Files app on a phone).',
        f'2. Double click "{bd.safe(name)}.html". It opens in your web browser: Chrome, Edge, Safari or Firefox.',
        '3. Start with Module 1 and work in order.' + (' Your progress and checklists save in that browser on that device.' if saves else ''),
        '', 'No internet, login or app is needed once it is downloaded. Keep a copy of the file somewhere safe.', ''] +
        ([f'This course is the step by step path for the {head}. At each step it names the working document to open. Those documents come in the blueprint and its toolkit, which are sold separately in our Etsy shop.', ''] if needs_bundle else []) +
        ['This course is for education and planning. It is not legal, tax or financial advice and it does not promise any income.',
         'Questions or a problem with the file? Message us on Etsy and we will make it right.']) + '\r\n'
    with zipfile.ZipFile(os.path.join(od, zname), 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr(bd.safe(name) + '.html', html.encode('utf-8'))
        z.writestr('Read Me First.txt', readme.encode('utf-8'))
    title = None
    for t in (f'{name}, {len(mods)} Module Self Paced Online Course, Step by Step Startup Training, Works Offline in Any Browser',
              f'{name}, {len(mods)} Module Self Paced Course, Step by Step Training',
              f'{name}, Self Paced Course'):
        if len(t) <= 140: title = t; break
    lead = (f'{name} turns the plan into action. It is a self paced course in {len(mods)} modules that walks you through starting and running '
            + (bk.bd.art(short) + ' business' if sku not in SPECIAL else 'this path') + ' one step at a time, with checklists you tick off as you go.')
    D = [lead, '']
    if needs_bundle:
        D += ['PLEASE READ FIRST', f'This course is the implementation companion to the {head}. At each step it tells you which working document to open. Those documents are NOT included in this listing. They come in the blueprint and the business toolkit, sold separately in our shop. If you want everything, get those too.', '']
    D += ['WHAT YOU WILL WORK THROUGH'] + [f'{i}. {m}' for i, m in enumerate(mods, 1)] + ['',
          'WHAT YOU GET', '- The full course as one file that opens in any web browser', '- A Read Me First file with simple opening steps',
          '- Works on a computer, tablet or phone, with no login, app or subscription'] + (['- Checklists and progress that save in your browser'] if saves else []) + ['',
          'HOW IT WORKS', 'This is a digital download. Nothing is shipped. After you buy, Etsy gives you a zip file right away on your Purchases page. Unzip it and double click the course file.', '',
          'GOOD TO KNOW', 'This course is for education and planning. It does not promise any income or results, and it is not legal, tax or financial advice. Check the rules where you live before you start.',
          'Written by Wayne Thomas for Glamourless Systems, with help from AI writing tools.', '',
          'Because this is a digital file, all sales are final. If something is wrong with your download, message us and we will make it right.']
    return {'key': key, 'sku': key, 'kind': 'course', 'parent': sku, 'title': title, 'description': '\n'.join(D),
            'price': 30.00, 'quantity': 999, 'tags': tags_for(short, mini), 'images': imgs,
            'files': [f'{key}/{zname}'], 'modules': len(mods), 'words': words, 'needs_bundle': needs_bundle}

def main(only):
    mpath = os.path.join(OUT, 'manifest.json'); m = json.load(open(mpath))
    bps = {i['sku']: i for i in m['items'] if i['kind'] == 'blueprint'}
    new = []
    for sku in sorted(bps):
        if only and sku not in only: continue
        it = build(sku, bps[sku])
        if it: new.append(it); print(it['key'], it['modules'], it['words'], it['price'], '|', it['title'][:80], flush=True)
    keys = {i['key'] for i in new}
    m['items'] = [i for i in m['items'] if i['key'] not in keys] + new
    json.dump(m, open(mpath, 'w'), indent=1)
    print('manifest items', len(m['items']), 'courses', sum(1 for i in m['items'] if i['kind'] == 'course'))

if __name__ == '__main__':
    main(sys.argv[1:])
