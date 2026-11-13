# Etsy tag cleanup: remove the wasted "digital download" tag (Etsy already labels and filters digital items)
# and fill every listing to all 13 tag slots with topic-specific, buyer-search phrases (each 20 characters or less).
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from niche_tags import NICHE, KEYED
SRC, OUT = sys.argv[1], sys.argv[2]
man = json.load(open(SRC)); items = man['items']
DROP = {'digital download'}
STOP = {'the','and','of','a','an','for','to','your','with','on','in','my','gs','from','that'}
SUFFIX = {
 'kit': [' business', ' forms', ' templates', ' checklist', ' contract', ' pricing', ' tracker', ' startup'],
 'blueprint': [' business', ' business plan', ' startup', ' guide', ' how to start', ' side hustle', ' ebook'],
 'course': [' course', ' training', ' business', ' class', ' how to start', ' startup'],
 'tool': [' app', ' tool', ' software', ' template', ' tracker', ' calculator'],
 'book': [' ebook', ' guide', ' book', ' playbook', ' pdf'],
}
EXTRA = {
 'kit': ['business forms kit', 'editable word forms', 'service contract', 'pricing template', 'client intake form', 'startup checklist'],
 'blueprint': ['how to start', 'business guide pdf', 'startup plan', 'business ideas', 'self employed', 'make money'],
 'course': ['self paced course', 'business class', 'startup training', 'entrepreneur course', 'online class'],
 'tool': ['business app', 'browser app', 'instant use app', 'small business app', 'contractor app', 'service business app'],
 'book': ['small business book', 'business pdf', 'marketing ebook', 'entrepreneur ebook', 'business tips'],
}
def clean(t):
    t = re.sub(r"[^a-z0-9' \-]", ' ', t.lower()); return re.sub(r'\s+', ' ', t).strip()
def topic(it):
    t = it['title']
    if it['kind'] == 'tool': t = t.split('|')[0]
    elif it['kind'] == 'book': t = t.split(',')[0]
    else: t = re.split(r'\s+Business\b|\s+Toolkit\b|\s+Blueprint\b|\s+Course\b|,', t)[0]
    t = re.sub(r'^(The|GS)\s+', '', t.strip(), flags=re.I)
    return clean(t)
GENERIC = {'builder','system','systems','manager','operator','route','desk','studio','service','services','business','app','kit','pack','engine','authority','playbook','guide','network','machine','method','planner','calculator','suite','tool','tools','board','console','platform','utility','packager','generators','blueprint','course','money','pro','hustle','first','career','entry'}
def ok(ws):
    if not ws or ws[0] in STOP or ws[-1] in STOP: return False
    if len(ws) == 1 and (ws[0] in GENERIC or len(ws[0]) < 5): return False
    return True
def cores(tp):
    w = [x for x in tp.split() if x]
    out = []
    for n in range(len(w), 0, -1):          # longest tail first: "custom luxury metal card" -> "luxury metal card" -> "metal card"
        c = ' '.join(w[len(w)-n:])
        if len(c) <= 20 and ok(c.split()): out.append(c)
    for n in range(len(w), 1, -1):          # leading phrases too: "yard cleanup", "piano tuning"
        c = ' '.join(w[:n])
        if len(c) <= 20 and ok(w[:n]) and c not in out: out.append(c)
    return out
log = []
for it in items:
    k = it['kind']; old = list(it['tags'])
    tags = [t for t in old if t not in DROP]
    sku0 = (it.get('parent') or it['sku'])[3:]
    if k in ('kit', 'blueprint', 'course') and sku0 in NICHE:
        # Rebuild the topic part: drop the old auto tags cut from the product name (e.g. "clutter to", "damage to course"),
        # keep the general category tags, and lead with real search phrases for that business.
        tw = set(topic(it).split()) - STOP - GENERIC - {'business', 'route', 'operator'}
        keep = [t for t in tags if not (set(t.split()) & tw)]
        lead = []
        for n in NICHE[sku0]:
            if n not in lead: lead.append(n)
        for n in NICHE[sku0]:
            for sfx in SUFFIX[k][:2]:
                c = clean(n + sfx)
                if len(c) <= 20 and c not in lead and c not in keep: lead.append(c)
        lead = lead[:5]
        tags = (lead + [t for t in keep if t not in lead])[:13]
    have = set(tags)
    def add(t):
        t = clean(t)
        if t and len(t) <= 20 and t not in have and len(tags) < 13 and not t.endswith(tuple(' ' + s for s in STOP)):
            tags.append(t); have.add(t)
    sku = (it.get('parent') or it['sku'])[3:] if k not in ('tool', 'book') else None
    for n in KEYED.get(it['key'], []): add(n)
    if sku in NICHE:
        for n in NICHE[sku]: add(n)
        for n in NICHE[sku]:
            for s in SUFFIX[k]: add(n + s)
        cs = []
    elif k == 'book':
        cs = []
    else:
        cs = cores(topic(it))
    for c in cs[:1]: add(c)
    for c in cs[:3]:
        for s in SUFFIX[k]: add(c + s)
    for c in cs: add(c)
    for e in EXTRA[k]: add(e)
    it['tags'] = tags
    if tags != old: log.append((it['key'], old, tags))
man['tags_version'] = 'tags-20261113b'
man['update_tags'] = [k for k, _, _ in log]
json.dump(man, open(OUT, 'w'), indent=1)
print(len(log), 'listings get new tags')
print('short of 13:', sum(1 for i in items if len(i['tags']) < 13), ' with digital download:', sum('digital download' in i['tags'] for i in items),
      ' over 20 chars:', sum(any(len(t) > 20 for t in i['tags']) for i in items))
import random; random.seed(3)
log = log or [('none', [], [])]
for key, o, n in random.sample(log, 8): print(key, '\n  -', [x for x in o if x not in n], '\n  +', [x for x in n if x not in o])
