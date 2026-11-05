# Glamourless Systems backup assessments build script (Python 3, needs requests and beautifulsoup4)
# 1. Downloads the four live assessment pages from glamourlesssystems.com
# 2. Pulls the assessment custom code block out of each page (the element whose id ends in __custom-code)
# 3. Applies the same name-field reorder the live head script gs-name-later applies (change and choose)
# 4. Wraps each block in a plain page shell and writes the site files ready for GitHub Pages
# Fix page uses only its own built-in styles (the global stylesheet breaks its hero layout).
import requests, json, os
from bs4 import BeautifulSoup
OUT='site'; os.makedirs(OUT,exist_ok=True)
SYS='https://a2ff-admin.systeme.io/home'
PAGES={'start':('start-assessment','Start Something Assessment'),'change':('change-assessment','Change Something Assessment'),
 'choose':('choose-assessment','Choose Something Assessment'),'fix':('fix-assessment','Fix Something Assessment')}
RULES={'change':[('t=["SL0","SL1"].concat(6===e.Q1?["SL1m"]:[],[','t=["SL1"].concat(6===e.Q1?["SL1m"]:[],["SL0",')],
 'choose':[('var e=["S0","B1","s1",','var e=["B1","s1","S0",')]}
def shell(title,body,css=True):
    link='<link rel="stylesheet" href="gs-global.css">' if css else ''
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
     '<meta name="robots" content="noindex,nofollow"><title>'+title+' | Glamourless Systems</title>'+link+'<script src="payhip-links.js?v=1"></script>'
     '<style>.gs-backup-top{background:#061529;padding:14px 20px}.gs-backup-top a{color:#fff;font-family:Oswald,Arial,sans-serif;font-size:20px;text-decoration:none;letter-spacing:.5px}</style>'
     '</head><body>\n<div class="gs-backup-top"><a href="'+SYS+'">GLAMOURLESS SYSTEMS</a></div>\n'+body+'\n<script src="backup-glue.js?v=4"></script></body></html>\n')
raw_start=None
for k,(slug,title) in PAGES.items():
    raw=requests.get('https://glamourlesssystems.com/'+slug,timeout=30).text
    if k=='start': raw_start=raw
    s=BeautifulSoup(raw,'html.parser')
    block=max(s.select('[id$="__custom-code"]'),key=lambda e:len(e.decode_contents())).decode_contents()
    for o,n in RULES.get(k,[]):
        assert block.count(o)==1; block=block.replace(o,n)
    open(f'{OUT}/{k}.html','w').write(shell(title,block,css=(k!='fix')))
# global stylesheet lives JSON-escaped inside the page data
a=raw_start.find('\\u003Cstyle id=\\"gs-global-css\\">'); b=raw_start.find('\\u003C\\u002Fstyle>',a)
css=json.loads('"'+raw_start[a:b]+'"'); open(f'{OUT}/gs-global.css','w').write(css[css.find('>')+1:])
# index.html, checkout.html, backup-glue.js, payhip-links.js, robots.txt and .nojekyll are hand written (see the repository)
