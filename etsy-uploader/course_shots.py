import json, os, re, sys, glob, asyncio
from playwright.async_api import async_playwright
SRC='/mnt/user-data/uploads/Glamourless Systems Main/GS Etsy Courses/'
OUT='/home/claude/etsy/crs/'
async def one(browser, d):
    f=glob.glob(SRC+d+'/*.html')[0]; sku=d[:7]; od=OUT+sku; os.makedirs(od,exist_ok=True)
    url='file://'+f
    ctx=await browser.new_context(viewport={'width':1440,'height':900})
    p=await ctx.new_page()
    await p.goto(url); await p.wait_for_timeout(700)
    await p.screenshot(path=od+'/dash.png')
    txt=await p.evaluate('document.body.innerText')
    clicked=False
    for pat in [r'Start Module 1', r'Begin Module 1', r'Start (the )?course', r'^Start', r'Begin', r'Module 1\b']:
        loc=p.get_by_text(re.compile(pat,re.I)).first
        try:
            if await loc.count() and await loc.is_visible():
                await loc.click(timeout=1500); clicked=True; break
        except Exception: pass
    await p.wait_for_timeout(600)
    await p.evaluate('window.scrollTo(0,0)')
    await p.screenshot(path=od+'/module.png')
    txt2=await p.evaluate('document.body.innerText')
    await ctx.close()
    ctx=await browser.new_context(viewport={'width':390,'height':844},device_scale_factor=2)
    p=await ctx.new_page(); await p.goto(url); await p.wait_for_timeout(600)
    await p.screenshot(path=od+'/phone.png'); await ctx.close()
    json.dump({'dir':d,'file':os.path.basename(f),'text':txt,'text2':txt2,'clicked':clicked},open(od+'/info.json','w'))
    return sku, clicked
async def main(only):
    dirs=sorted(x for x in os.listdir(SRC) if os.path.isdir(SRC+x) and glob.glob(SRC+x+'/*.html'))
    if only: dirs=[x for x in dirs if x[:7] in only]
    dirs=[x for x in dirs if not os.path.exists(OUT+x[:7]+'/info.json')]
    async with async_playwright() as pw:
        b=await pw.chromium.launch()
        for d in dirs:
            try: print(await one(b,d),flush=True)
            except Exception as e: print(d[:7],'ERR',e,flush=True)
        await b.close()
asyncio.run(main(sys.argv[1:]))
