import json,sys
# usage: addsrc.py "SKU|dir|pdf|docx|cover|mockup" ...
B='Glamourless Systems Blueprints and Bundles/'
src=json.load(open('sources.json'))
for a in sys.argv[1:]:
    sku,d,pdf,docx,cv,mk=a.split('|')
    title=d.split(' ',1)[1]
    src[sku]=dict(title=title,pdf=B+d+'/Blueprint/'+pdf,docx=B+d+'/Blueprint/'+docx,cover=B+d+'/'+cv if cv!='-' else '',mockup=B+d+'/'+mk if mk!='-' else '')
json.dump(src,open('sources.json','w'),indent=1)
print(len(src))
