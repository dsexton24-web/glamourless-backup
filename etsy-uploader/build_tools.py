#!/usr/bin/env python3
"""Build Etsy draft packages for the central GS HTML tools.

For each tool in tools.json:
  HT <Name>/HT <Name> Cover.png        branded cover with a framed screenshot
  HT <Name>/HT <Name> Screen One.png   real screenshot of the tool
  HT <Name>/HT <Name> Screen Two.png   second screenshot (when the page is tall enough)
  HT <Name>/HT <Name> Features.png     what's inside + how it works card
  HT <Name>/<Name>.zip                 the tool html + Read Me First.txt
Adds one manifest item per tool (key 'HT-<slug>', kind 'tool') to the shared manifest.json.
"""
import json, os, re, shutil, zipfile
from PIL import Image, ImageDraw, ImageFont

SRC = '/mnt/user-data/uploads/Glamourless Systems Main/Glamourless Systems Engines/Gs-HTML Tools/'
OUT = '/home/claude/etsy/out/GS Etsy Upload Packages/'
SHOTS = '/home/claude/etsy/toolshots/'
FONT = '/usr/share/fonts/opentype/inter/Inter-Regular.otf'
FONTB = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
NAVY, NAVY2, STEEL, WHITE, ACCENT = '#061529', '#0E2A52', '#9DB4CF', '#FFFFFF', '#5B9BFF'
PRICE_CALC, PRICE_SYSTEM = 13.00, 13.00

INTRO = {
 'Asset Label Barcode and QR System': 'Track every tool, machine and asset you own, then design and print barcode and QR labels for them.',
 'Audit and Inspection Field App': 'Run inspections from templates, record findings, assign corrective actions and produce clean reports.',
 'Before and After Job Documentation System': 'Pair before and after photos by job and turn them into a customer-ready report.',
 'Build My Service Offer Wizard': 'A guided wizard that turns what you do into a clear service offer, with an internal sheet and a customer sheet.',
 'Business Document Builder': 'Build business documents from guided templates using your saved business profile.',
 'Business Performance Dashboard': 'See revenue, pipeline, job margin and route performance in one dashboard built from your own numbers.',
 'Business Scenario Simulator': 'Model your business, then test scenarios side by side to see what changes the outcome most.',
 'Business Tracker Suite': 'Nine trackers in one app: leads, mileage, job profit, equipment, recurring customers, inspections, referrals, sales activity and launch progress.',
 'Cash Flow Planner': 'Forecast cash in and out, set reserve rules and run what-if scenarios before a shortfall happens.',
 'Client Intake and Job Scope Builder': 'Collect customer details and build a clear job scope from reusable intake templates.',
 'Commission and Compensation Manager': 'Set up pay plans, log transactions and calculate commissions and payouts with statements.',
 'Contractor Price Book System': 'Build a price book of services, assemblies, labor, materials and equipment with your own pricing rules.',
 'Customer Service Configurator and Estimate Builder': 'Let customers configure a service and see an estimate, with an operator setup side for your pricing.',
 'Data Migration and Format Conversion Utility': 'Map, transform and validate data from one format to another before you move it into a new system.',
 'Deterministic Business Document Generators': 'Generate business documents from facts you enter and fixed templates. It never invents pricing, legal or customer details.',
 'Dispatch and Capacity Manager': 'Schedule jobs to workers, crews and vehicles and catch capacity conflicts before they happen.',
 'Evidence and Audit Packet Builder': 'Organize evidence, findings and corrective actions into a complete audit packet.',
 'GS Campaign Challenge and Lead Experience Builder': 'Build interactive challenge campaigns that capture leads, then review the lead records and results.',
 'GS Community Challenge and League Platform': 'Run seasons, challenges, score entry and leaderboards for a community, club or league.',
 'GS Daily Challenge Publisher': 'Plan a bank of daily challenges, schedule them on a calendar and track scores.',
 'GS Game and Simulation Economy Balancer': 'Model resources, progression and upgrades in a game economy and run simulations to balance it.',
 'GS Interactive Experience Analytics Console': 'Import event data from interactive experiences and explore funnels, distributions and data quality.',
 'GS Interactive Localization and Content Pack Manager': 'Manage strings, translations and content packs for an interactive project and export a bundle.',
 'GS Interactive Product Finder and Merchandising Game Builder': 'Build a product finder quiz from your catalog that recommends products and captures leads.',
 'GS Multi Portal Web Game Adapter Kit': 'Plan and validate builds of a web game for multiple game portals from one project.',
 'GS Playable Promotion and Branded Mini Game Builder': 'Configure a branded mini game promotion with prize entry, testing and closeout.',
 'GS Realistic Job Preview Builder': 'Build a realistic job preview so candidates see the real work before they apply.',
 'GS Scenario Content Authoring Studio': 'Author branching scenarios with nodes, choices and variables, then playtest and export them.',
 'GS White Label Interactive Experience Packager': 'Package interactive tools for clients with branding, licensing, hosting plans and handoff checklists.',
 'GS-0169 Vehicle Inspection Field App': 'Run vehicle inspections from templates, record findings and produce inspection reports.',
 'Interactive Assessments and Certifications': 'Run lessons, practice scenarios and a final assessment, with completion records per learner.',
 'Interactive Sales Presentation Builder': 'Run guided sales presentations with discovery questions, packages, comparisons and objection answers.',
 'Interactive Workbooks': 'A step by step business launch workbook: foundation, customer, offer, startup costs, pricing and break-even.',
 'Inventory and Equipment Managers': 'Track equipment, supplies, stock movements, maintenance and replacement in one place.',
 'Job and Project Kanban Board': 'Move jobs through a kanban board with tasks, checklists and due dates.',
 'Local CSV Data Cleanup and Reconciliation Utility': 'Import a CSV, find missing values and duplicates, standardize fields, reconcile and export clean data.',
 'Offline Digital Catalog Builder': 'Build a searchable visual catalog of your services, packages and products.',
 'Offline Field Manual and Knowledge Base': 'Load your procedures and reference material into a searchable offline field manual.',
 'Photo Documentation System': 'Organize job photos by customer, job and location and build documentation reports.',
 'Punch List and Closeout System': 'Track punch list items through verification and evidence to a documented closeout.',
 'Quote and Proposal Builder': 'Build quotes and proposals from your service catalog and track them as pipeline.',
 'Route and Territory Manager': 'Manage customers, stops, routes, territories and recurring service in one place.',
 'Solo Operator Business OS': 'Run a one-person business: customers, pipeline, estimates, jobs, invoices, payments, expenses and tasks.',
 'Solo Operator CRM': 'Track contacts, pipeline, follow-ups, tasks and revenue without a monthly CRM bill.',
 'SOP Execution System': 'Build SOPs, run them as live workflows and catch QA exceptions as work happens.',
 'Visual Damage and Site Inspection Mapper': 'Mark damage and findings on images and site plans, then build a findings schedule and report.',
 'Warranty and Claims Manager': 'Track warranty and claim cases with evidence, deadlines, follow-ups and case packets.',
 'Work Order Manager': 'Create, schedule and track work orders with labor, materials and equipment.',
 'Batch Document Factory': 'Turn a list of records and one template into many individual documents or labels at once.',
 'Business Troubleshooter and Decision Tree Engine': 'Walk through guided troubleshooters like "Why am I not profitable?" and build your own decision trees.',
}

def cut(s, n):
    if len(s) <= n: return s
    return s[:n].rsplit(' ', 1)[0].rstrip()

def clean_name(n):
    n = re.sub(r'^GS-\d+\s+', '', n)
    n = re.sub(r'^GS\s+', '', n)
    return n

def slug(n):
    return re.sub(r'[^A-Za-z0-9]+', '-', clean_name(n)).strip('-')

def is_calc(n, nav):
    return nav == ['Inputs'] or nav[:1] == ['Inputs'] or re.search(r'Calculator|Planner|Reality Check|Fit Finder|Diagnostic|Quote Builder|Bid', n) is not None

def wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def cover(path, name, shot, calc):
    W, H = 2000, 1600
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    fb = ImageFont.truetype(FONTB, 88); fs = ImageFont.truetype(FONT, 46); ft = ImageFont.truetype(FONTB, 40)
    lines = wrap(d, name, fb, 1780)[:2]
    y = 90
    for ln in lines:
        d.text((110, y), ln, font=fb, fill=WHITE); y += 108
    d.text((110, y + 20), ('Interactive calculator' if calc else 'Offline business app') + '  ·  Runs in your browser  ·  No subscription', font=fs, fill=STEEL)
    top = y + 120
    s = Image.open(shot).convert('RGB')
    bw = 1780; bh = H - top - 150
    s = s.resize((bw, int(s.height * bw / s.width)))
    s = s.crop((0, 0, bw, min(bh, s.height)))
    d.rectangle([104, top - 6, 110 + s.width + 6, top + s.height + 6], fill=ACCENT)
    im.paste(s, (110, top))
    d.text((110, H - 100), 'GLAMOURLESS SYSTEMS', font=ft, fill=STEEL)
    d.text((W - 110 - d.textlength('INSTANT DOWNLOAD', font=ft), H - 100), 'INSTANT DOWNLOAD', font=ft, fill=ACCENT)
    im.save(path, optimize=True)

def features(path, name, nav, intro):
    W, H = 2000, 1600
    im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 300], fill=NAVY2)
    fb = ImageFont.truetype(FONTB, 84); fr = ImageFont.truetype(FONT, 46); fs = ImageFont.truetype(FONT, 42); fh = ImageFont.truetype(FONTB, 50)
    d.text((110, 70), "WHAT'S INSIDE", font=fb, fill=WHITE)
    nm = clean_name(name); nm = nm if len(nm) <= 60 else nm[:58] + '...'
    d.text((110, 190), nm, font=fr, fill=STEEL)
    items = [n for n in nav if n.lower() not in ('help', 'help / about')][:12] if len(nav) > 1 else []
    y = 370
    if items:
        col = 0
        for i, it in enumerate(items):
            x = 110 if i < 6 else 1000
            yy = 370 + (i % 6) * 84
            d.ellipse([x, yy + 18, x + 20, yy + 38], fill=ACCENT)
            t = it if len(it) <= 30 else it[:28] + '...'
            d.text((x + 45, yy), t, font=fs, fill=WHITE)
        y = 370 + 6 * 84 + 30
    else:
        for ln in wrap(d, intro, fs, 1780)[:5]:
            d.text((110, y), ln, font=fs, fill=WHITE); y += 62
        y += 40
    d.text((110, y), 'HOW IT WORKS', font=fh, fill=ACCENT); y += 90
    for step in ['Download the zip and unzip it', 'Double-click the file to open it in your browser',
                 'Your data saves on your own device, no account needed', 'Use Backup to export your data any time']:
        d.ellipse([110, y + 16, 130, y + 36], fill=ACCENT)
        d.text((160, y), step, font=fs, fill=WHITE); y += 76
    d.text((110, H - 100), 'GLAMOURLESS SYSTEMS', font=ImageFont.truetype(FONTB, 40), fill=STEEL)
    im.save(path, optimize=True)

README = """{name}
Glamourless Systems

HOW TO OPEN IT
1. Unzip this download (on Windows, right-click the zip and choose Extract All).
2. Double-click "{file}". It opens in your web browser (Chrome, Edge, Firefox or Safari).
3. That's it. No install, no account, no subscription, no internet needed after download.

WHERE YOUR DATA GOES
Everything you enter is saved in your browser on this device only. Nothing is sent anywhere.
Clearing your browser's site data will erase it, so use the Backup or Export option regularly
and keep the backup file somewhere safe. Use the same browser each time.

TIPS
- Bookmark the file after you open it so it's one click away.
- Works best on a computer. You can copy the file to another device and restore your backup there.
- Print / Save as PDF uses your browser's print window.

LICENSE
For use in your own business. Please do not resell or redistribute the file.

Questions: reply to your Etsy order message and we'll help.
"""

def description(name, nav, intro, calc):
    nm = clean_name(name)
    parts = [f"{nm}: {intro}", '',
             'This is a self-contained app that runs in your web browser. No install, no account, no monthly fee, and it works offline. Your data stays on your own device.', '']
    items = [n.replace('\n', ' ') for n in nav if n.lower() not in ('help', 'help / about')]
    if len(items) > 1:
        parts.append("WHAT'S INSIDE")
        parts += ['- ' + re.sub(r'\s+\d+%$', '', i) for i in items[:16]]
        parts.append('')
    parts += ['WHAT YOU GET',
              f'- {nm} (one HTML file, inside a zip)',
              '- Read Me First guide with simple setup steps', '',
              'HOW IT WORKS',
              '1. Download and unzip the file.',
              '2. Double-click it. It opens in Chrome, Edge, Firefox or Safari.',
              '3. Start entering your numbers. Everything saves on your device.',
              '4. Use Backup / Export to keep a copy of your data.', '',
              'GOOD TO KNOW',
              '- Digital download only. Nothing is shipped.',
              '- Works best on a laptop or desktop computer.',
              '- Built for small business owners, solo operators and service businesses.',
              '- For use in your own business. Not for resale.', '',
              'Made by Glamourless Systems. We build practical tools that help ordinary people run a business they control.']
    return '\n'.join(parts)

GENERIC = ['small business tool', 'offline app', 'business template', 'digital download', 'service business',
           'html app', 'solo business', 'no subscription', 'contractor tools', 'business planner', 'side hustle']

def tags_for(name, calc):
    nm = clean_name(name).lower().replace('&', 'and')
    t = []
    words = [w for w in re.findall(r'[a-z0-9]+', nm) if w not in ('and', 'the', 'my', 'do', 'i', 'to', 'this', 'of')]
    if len(nm) <= 20: t.append(nm)
    for i in range(len(words) - 1):
        p = words[i] + ' ' + words[i + 1]
        if len(p) <= 20 and p not in t: t.append(p)
    if calc: t += [x for x in ['business calculator', 'pricing calculator'] if x not in t]
    for g in GENERIC:
        if len(t) >= 13: break
        if g not in t: t.append(g)
    return [x for x in t if 3 <= len(x) <= 20][:13]

def etsy_title(name, calc):
    nm = clean_name(name)
    tail = ' | Business Calculator, Offline Browser App, No Subscription, Instant Download' if calc else ' | Small Business App, Works Offline in Your Browser, No Subscription, Instant Download'
    t = nm + tail
    return t if len(t) <= 140 else (nm + ' | Offline Browser App, No Subscription, Instant Download')[:140]

def main():
    names = json.load(open('/home/claude/etsy/tools.json'))
    info = json.load(open('/home/claude/etsy/toolinfo.json'))
    shots = {}
    for l in open('/home/claude/etsy/shots.jsonl'):
        try: d = json.loads(l); shots[d['n']] = d
        except Exception: pass
    mpath = OUT + 'manifest.json'
    manifest = json.load(open(mpath))
    have = {i['key']: i for i in manifest['items']}
    for n in names:
        nm = clean_name(n)
        nav = [x.replace('\n', ' ') for x in info[n]['nav']]
        intro = INTRO.get(n) or (info[n]['ps'][0] if info[n]['ps'] else f'A practical {nm.lower()} for small business owners.')
        calc = is_calc(n, info[n]['nav'])
        folder = 'HT ' + nm
        folder = folder if len(folder) <= 60 else folder[:60].rstrip()
        d = OUT + folder + '/'; os.makedirs(d, exist_ok=True)
        short = cut(nm, 50)
        imgs = []
        f1 = f'HT {short} Cover.png'; cover(d + f1, nm, SHOTS + n + ' A.png', calc); imgs.append(f1)
        f2 = f'HT {short} Screen One.png'; shutil.copyfile(SHOTS + n + ' A.png', d + f2); imgs.append(f2)
        if shots.get(n, {}).get('h', 0) > 1000:
            f3 = f'HT {short} Screen Two.png'; shutil.copyfile(SHOTS + n + ' B.png', d + f3); imgs.append(f3)
        f4 = f'HT {short} Features.png'; features(d + f4, n, nav, intro); imgs.append(f4)
        zname = cut(nm, 66) + '.zip'
        htmlname = nm + '.html'
        with zipfile.ZipFile(d + zname, 'w', zipfile.ZIP_DEFLATED) as z:
            z.write(SRC + n + '.html', htmlname)
            z.writestr('Read Me First.txt', README.format(name=nm, file=htmlname))
        item = {'key': 'HT-' + slug(n), 'sku': 'HT-' + slug(n), 'kind': 'tool',
                'title': etsy_title(n, calc), 'description': description(n, nav, intro, calc),
                'price': PRICE_CALC if calc else PRICE_SYSTEM, 'quantity': 999,
                'tags': tags_for(n, calc),
                'images': [folder + '/' + i for i in imgs], 'files': [folder + '/' + zname]}
        have[item['key']] = item
        print(item['key'], item['price'], len(item['title']), len(item['tags']), len(imgs))
    manifest['items'] = sorted(have.values(), key=lambda i: i['key'])
    json.dump(manifest, open(mpath, 'w'), indent=1)

if __name__ == '__main__':
    main()
