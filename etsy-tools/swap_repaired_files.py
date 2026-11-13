# Rebuild Etsy package files for SKUs with Instinct's Nov 13 repaired-file notice.
# Blueprint docx/pdf: canonical bytes under the package filename. Kit/course zips: repaired members swapped by name, all others copied byte for byte.
import json, os, zipfile, hashlib, shutil
U = '/mnt/user-data/uploads/Glamourless Systems Main/'
CAN = U + 'Glamourless Systems Blueprints and Bundles/'
PKG_LOCAL = '/home/claude/etsy/out/GS Etsy Upload Packages/'
PKG_KIT = U + 'GS Etsy Upload Packages/'
OUT = '/mnt/user-data/outputs/Etsy Repaired Swap/'
M = json.load(open('/home/claude/repairs/swapmap.json'))
man = {i['key']: i for i in json.load(open(PKG_LOCAL + 'manifest.json'))['items']}
sha = lambda b: hashlib.sha256(b).hexdigest()[:12]
log = []
def put(rel, data):
    p = OUT + rel; os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'wb').write(data)
def rezip(src, rel, repl):
    zi = zipfile.ZipFile(src); out = OUT + rel; os.makedirs(os.path.dirname(out), exist_ok=True)
    hit = set()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zo:
        for info in zi.infolist():
            data = zi.read(info.filename)
            if info.filename in repl:
                new = repl[info.filename]; hit.add(info.filename)
                log.append(f'{rel} :: {info.filename}  {len(data)} -> {len(new)} bytes  {"CHANGED" if new != data else "SAME"}')
                data = new
            zo.writestr(info.filename, data)
    miss = set(repl) - hit
    assert not miss, (rel, miss)
for s, b in M['BP'].items():
    it = man[s + '-blueprint']
    for f in it['files']:
        if 'Start Here' in f: continue
        ext = f.rsplit('.', 1)[1]
        new = open(CAN + M['F'][s] + '/Blueprint/' + b + '.' + ext, 'rb').read()
        old = open(PKG_LOCAL + f, 'rb').read()
        log.append(f'{f}  {len(old)} -> {len(new)}  {"CHANGED" if new != old else "SAME"}'); put(f, new)
for s, ic in M['IC'].items():
    f = man['CRS-' + s]['files'][0]
    new = open(CAN + M['F'][s] + '/' + ic.replace('\\', '/'), 'rb').read()
    zi = zipfile.ZipFile(PKG_LOCAL + f); h = [n for n in zi.namelist() if n.endswith('.html')][0]
    rezip(PKG_LOCAL + f, f, {h: new})
for s, sds in M['SD'].items():
    f = man['KIT-' + s]['files'][0]
    repl = {n: open(CAN + M['F'][s] + '/Supporting Documents/' + n, 'rb').read() for n in sds}
    rezip(PKG_KIT + f, f, repl)
open(OUT + 'swap log.txt', 'w').write('\n'.join(log) + '\n')
print('\n'.join(log)); print(sum('SAME' in l for l in log), 'same,', sum('CHANGED' in l for l in log), 'changed')
