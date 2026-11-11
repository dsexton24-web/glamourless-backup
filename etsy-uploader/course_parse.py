import re, html, os, glob
SRC='/mnt/user-data/uploads/Glamourless Systems Main/GS Etsy Courses/'
def text_lines(s):
    t=re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>','',s)
    t=re.sub(r'(?s)<[^>]+>','\n',t); t=html.unescape(t)
    return [l.strip() for l in t.split('\n') if l.strip()]
def parse(path):
    s=open(path,encoding='utf-8',errors='replace').read()
    title=html.unescape((re.findall(r'(?is)<title>(.*?)</title>',s) or [''])[0]).split('|')[0].strip()
    L=text_lines(s); mods={}
    for i,l in enumerate(L[:-1]):
        m=re.match(r'^(?:Module|Lesson|Step|Week)\s+(\d{1,2})\s*[:.\-–—]?\s*(.*)$',l)
        if m:
            n=int(m.group(1)); t=m.group(2).strip() or L[i+1]
            if re.match(r'^(Module|Lesson|Days?|Before|Week)\b',t) or len(t)<4: continue
            if n not in mods and len(t)<90: mods[n]=t
    mods=[mods[k] for k in sorted(mods)]
    if len(mods)<3:
        hs=[html.unescape(re.sub(r'<[^>]+>','',h)).strip() for h in re.findall(r'(?is)<h2[^>]*>(.*?)</h2>',s)]
        mods=[h for h in hs if 3<len(h)<90][:20]
    quiz=bool(re.search(r'(?i)quiz|knowledge check',s)); tools=len(re.findall(r'(?i)calculator',s))>0
    return dict(title=title,modules=mods,quiz=quiz,calc=tools,words=len(' '.join(L).split()),size=len(s))
if __name__=='__main__':
    for d in sorted(os.listdir(SRC)):
        f=[x for x in glob.glob(SRC+d+'/*.html')]
        if not f: continue
        p=parse(f[0]); print(d[:7],p['size']//1000,'KB',p['words'],'w',len(p['modules']),'mods|',p['title'][:50],'|',p['modules'][:3])
