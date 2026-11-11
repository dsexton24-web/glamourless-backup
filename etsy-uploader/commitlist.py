import json,os,sys,shutil
lo,hi=sys.argv[1],sys.argv[2]
OUT='out/GS Etsy Upload Packages/'; ST='/mnt/user-data/outputs/GS Etsy Upload Packages/'
D='G:\\My Drive\\Glamourless Systems Main\\GS Etsy Upload Packages\\'
items=[]
for sku in sorted(os.listdir(OUT)):
    if lo<=sku<=hi and os.path.isdir(OUT+sku):
        os.makedirs(ST+sku,exist_ok=True)
        for f in sorted(os.listdir(OUT+sku)):
            shutil.copyfile(OUT+sku+'/'+f, ST+sku+'/'+f)
            items.append({'stagedPath':ST+sku+'/'+f,'devicePath':D+sku+'\\'+f})
shutil.copyfile(OUT+'manifest.json',ST+'manifest.json')
items.append({'stagedPath':ST+'manifest.json','devicePath':D+'manifest.json'})
for n in range(0,len(items),50):
    json.dump(items[n:n+50],open(f'/tmp/claude-0/c{n//50}.json','w'))
print(len(items))
