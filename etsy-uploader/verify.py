import json,re,os,sys
O='/home/claude/etsy/out/GS Etsy Upload Packages/'
m=json.load(open(O+'manifest.json'));lo,hi=sys.argv[1],sys.argv[2]
for i in m['items']:
    if i['kind']!='blueprint' or not (lo<=i['sku']<=hi): continue
    bad=[f for f in i['images']+i['files'] if not os.path.exists(O+f) or not re.fullmatch(r'[A-Za-z0-9 ._-]{3,70}',f.split('/')[1])]
    flag='BAD' if bad or len(i['title'])>140 or 'Business Business' in i['title'] or any(len(t)>20 for t in i['tags']) or i['chapters']<6 else 'ok'
    print(i['sku'],i['pages'],i['chapters'],len(i['images']),flag,bad,i['title'][:70])
