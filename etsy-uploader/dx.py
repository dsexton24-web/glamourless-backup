import docx
def set_text(par, new):
    runs = par.runs
    if not runs: par.add_run(new); return
    runs[0].text = new
    for r in runs[1:]: r.text = ''
def all_pars(d):
    for p in d.paragraphs: yield p
    for t in d.tables:
        for row in t.rows:
            for c in row.cells:
                for p in c.paragraphs: yield p
def replace(d, old, new, must=True):
    n = 0
    for p in all_pars(d):
        if old in p.text:
            done=False
            for r in p.runs:
                if old in r.text:
                    r.text=r.text.replace(old,new); done=True
            if not done: set_text(p, p.text.replace(old, new))
            n += 1
    if must and n == 0: raise SystemExit('NOT FOUND: ' + old[:80])
    return n
def text(d): return '\n'.join(p.text for p in all_pars(d))
