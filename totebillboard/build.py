# Builds the GS Tote Billboard page: page.html (content), totebillboard.js (HighLevel loader), index.html (preview shell)
import json, html
FRONT=[("Thumb Coast Roofing","$250 OFF","Any new roof installation",101,"roof"),
("Port Huron Family Dental","$99","New patient exam, X-rays, cleaning",102,"tooth"),
("River City Lawn & Landscape","10% OFF","Any lawn service",103,"tree"),
("Riverfront Auto Detailing","$50 OFF","Any full detail package",104,"car"),
("Lakeside Pizza & Grill","$5 OFF","Any $25 order",105,"pizza"),
("Lakeview Home Improvements","10% OFF","Any remodel project",106,"roof")]
BACK=[("Huron Pet Care","$25 OFF","First grooming service",107,"paw"),
("St. Clair Heating & Cooling","$25 OFF","Any HVAC service",108,"snow"),
("Brightcoat Painting","$50 OFF","Any painting project",109,"roller"),
("Blue Water Plumbing & Drain","$50 OFF","Any repair of $200+",110,"drop"),
("Greenway Tree Service","$100 OFF","Tree service of $500+",111,"tree"),
("Sparkle Bright Cleaning","$50 OFF","Your first cleaning",112,"star")]
COL={"roof":"#e8632b","tooth":"#2f7bf5","tree":"#2e9a46","car":"#1e3f8f","pizza":"#f2b632","paw":"#0e2a52","snow":"#2f9be0","roller":"#2f7bf5","drop":"#2f9be0","star":"#2f7bf5"}
def esc(s): return html.escape(s)
def bag(ads,label,dims=True):
    S=24 # units per inch
    W,H=19*S,14*S; IW,IH=10*S,8*S
    ox,oy=60,90  # bag origin inside viewBox
    vw,vh=W+120,H+150
    ix=ox+(W-IW)/2; iy=oy+(H-IH)/2
    o=[f'<svg viewBox="0 0 {vw} {vh}" role="img" aria-label="{esc(label)}: 19 by 14 inch tote with a centered 10 by 8 inch print area holding six ads" xmlns="http://www.w3.org/2000/svg">']
    # handles
    for hx in (ox+W*0.27,ox+W*0.73):
        o.append(f'<path d="M{hx-34} {oy+4} C{hx-34} {oy-80},{hx+34} {oy-80},{hx+34} {oy+4}" fill="none" stroke="#0e2a52" stroke-width="13" stroke-linecap="round"/>')
    o.append(f'<rect x="{ox}" y="{oy}" width="{W}" height="{H}" rx="6" fill="#f6f3ec" stroke="#0e2a52" stroke-width="3"/>')
    o.append(f'<rect x="{ox}" y="{oy}" width="12" height="{H}" fill="#0e2a52"/><rect x="{ox+W-12}" y="{oy}" width="12" height="{H}" fill="#0e2a52"/><rect x="{ox}" y="{oy}" width="{W}" height="10" fill="#0e2a52"/>')
    # imprint zone
    o.append(f'<rect x="{ix-3}" y="{iy-3}" width="{IW+6}" height="{IH+6}" fill="none" stroke="#f2b632" stroke-width="2" stroke-dasharray="6 4"/>')
    g=4; cw=(IW-g)/2; ch=(IH-2*g)/3
    for k,(n,off,cond,ext,ic) in enumerate(ads):
        r,c=divmod(k,2); x=ix+c*(cw+g); y=iy+r*(ch+g)
        o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" rx="5" fill="#fff" stroke="#1e3f8f" stroke-width="1.2"/>')
        o.append(f'<circle cx="{x+12:.1f}" cy="{y+13:.1f}" r="7" fill="{COL[ic]}"/>')
        o.append(f'<text x="{x+23:.1f}" y="{y+12:.1f}" font-family="Arial" font-weight="700" font-size="{6.4 if len(n)<22 else 5.2}" fill="#0e2a52">{esc(n)}</text>')
        o.append(f'<rect x="{x+6:.1f}" y="{y+22:.1f}" width="48" height="13" rx="2" fill="#d62b2b"/><text x="{x+30:.1f}" y="{y+31.5:.1f}" text-anchor="middle" font-family="Arial" font-weight="800" font-size="8" fill="#fff">{esc(off)}</text>')
        o.append(f'<text x="{x+6:.1f}" y="{y+44:.1f}" font-family="Arial" font-size="5" fill="#101c36">{esc(cond)}</text>')
        o.append(f'<text x="{x+6:.1f}" y="{y+56:.1f}" font-family="Arial" font-weight="700" font-size="5" fill="#101c36">Campaign line, Ext. {ext}</text>')
        qx=x+cw-30; qy=y+16
        o.append(f'<rect x="{qx:.1f}" y="{qy:.1f}" width="24" height="24" fill="#fff" stroke="#101c36" stroke-width="1"/>')
        for a,b in ((2,2),(16,2),(2,16)): o.append(f'<rect x="{qx+a:.1f}" y="{qy+b:.1f}" width="6" height="6" fill="#101c36"/>')
        o.append(f'<rect x="{qx+11:.1f}" y="{qy+11:.1f}" width="3" height="3" fill="#101c36"/><rect x="{qx+16:.1f}" y="{qy+16:.1f}" width="5" height="3" fill="#101c36"/>')
        o.append(f'<rect x="{qx-3:.1f}" y="{qy+27:.1f}" width="30" height="13" rx="2" fill="#1e3f8f"/><text x="{qx+12:.1f}" y="{qy+32.5:.1f}" text-anchor="middle" font-family="Arial" font-weight="700" font-size="3.6" fill="#fff">Scan to</text><text x="{qx+12:.1f}" y="{qy+37:.1f}" text-anchor="middle" font-family="Arial" font-weight="700" font-size="3.6" fill="#fff">Learn More</text>')
    if dims:
        by=oy+H+26
        o.append(f'<line x1="{ox}" y1="{by}" x2="{ox+W}" y2="{by}" stroke="#53607a" stroke-width="1.5"/><line x1="{ox}" y1="{by-6}" x2="{ox}" y2="{by+6}" stroke="#53607a" stroke-width="1.5"/><line x1="{ox+W}" y1="{by-6}" x2="{ox+W}" y2="{by+6}" stroke="#53607a" stroke-width="1.5"/>')
        o.append(f'<text x="{ox+W/2}" y="{by+20}" text-anchor="middle" font-family="Arial" font-weight="700" font-size="14" fill="#0e2a52">Bag 19 in wide</text>')
        rx=ox+W+22
        o.append(f'<line x1="{rx}" y1="{oy}" x2="{rx}" y2="{oy+H}" stroke="#53607a" stroke-width="1.5"/><text x="{rx+8}" y="{oy+H/2}" font-family="Arial" font-weight="700" font-size="14" fill="#0e2a52" transform="rotate(90 {rx+8} {oy+H/2})" text-anchor="middle">14 in tall</text>')
        o.append(f'<text x="{ix+IW/2}" y="{iy-10}" text-anchor="middle" font-family="Arial" font-weight="700" font-size="12" fill="#b07f00">Print area 10 in x 8 in</text>')
    o.append('</svg>'); return "".join(o)

CATS="Roofing|Dental|Lawn and landscape|Auto detailing|Restaurant|Home improvement|Pet care|Heating and cooling|Painting|Plumbing|Tree service|Cleaning|Other".split("|")
FAQ=[("Where are the bags handed out?","Through a participating local retailer. Exact locations and quantities are shared for each confirmed edition before you pay."),
("How long does the AI answer calls and scans?","For the agreed campaign service period, not forever. The period is spelled out in your advertiser agreement."),
("Do you guarantee appointments or sales?","No. We track responses and confirmed outcomes when they can be verified, and we report them to you honestly."),
("Can I choose my offer?","Yes. We review it to make sure it is a real, specific value, truthful, clear about who qualifies, and easy to redeem."),
("What happens when a shopper calls?","They call one campaign number and enter your three-digit extension, or say your business name. The AI answers as your business."),
("What if an appointment lands after the offer expires?","If the customer claims or books before the expiration date, and your terms allow it, the service can happen later."),
("Can my competitor be on the same bag?","No. Each edition is category exclusive, one business per category."),
("How is my QR traffic tracked?","Each advertiser gets its own QR link and campaign ID, so your scans are counted separately from everyone else's."),
("Is the $650 a monthly fee?","No. It is a one-time price per placement for one campaign. There is no subscription.")]
opts="".join(f'<option>{esc(c)}</option>' for c in CATS)
faq="".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in FAQ)

CSS=open('style.css').read()
page=f'''<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
<div id="gstb">

<section class="hero"><div class="w hg">
 <div>
  <span class="kick">GS Tote Billboard System</span>
  <h1>Put your local offer in <span>shoppers' hands.</span></h1>
  <p class="lead">Your business appears on a reusable neighborhood grocery tote, with an AI-powered response system to answer questions and help customers take the next step.</p>
  <div class="cta2"><a class="btn" href="#ask">Ask About an Advertising Spot</a><a class="btn ghost" href="#how">See How It Works</a></div>
  <ul class="chips"><li>12 spots per edition</li><li>One business per category</li><li>Your own QR code and extension</li></ul>
 </div>
 <figure class="hfig">{bag(FRONT,"Front of tote",dims=False)}<figcaption>Concept mockup. Sample businesses are fictional.</figcaption></figure>
</div></section>

<section class="s" id="how"><div class="w">
 <div class="sh"><h2>How it works</h2><p>Advertising people carry home and use again every week.</p></div>
 <div class="steps">
  <div class="step"><b>1</b><h3>You send your offer</h3><p>You give us a real, specific offer, your logo and your terms. You approve everything before print.</p></div>
  <div class="step"><b>2</b><h3>We build the edition</h3><p>We lay out a 12-advertiser, two-sided tote and arrange printing and hand-out through a participating local retailer.</p></div>
  <div class="step"><b>3</b><h3>Shoppers respond</h3><p>They scan your QR code or call the campaign number and your extension.</p></div>
  <div class="step"><b>4</b><h3>The AI follows up</h3><p>It explains your approved offer and books or reserves it when you allow that. You get a report of what happened.</p></div>
 </div>
</div></section>

<section class="s alt"><div class="w">
 <div class="sh"><h2>What you get</h2></div>
 <div class="gets">
  <div class="get"><h3>Category exclusive spot</h3><p>One placement per edition, and no competitor in your category on the same bag.</p></div>
  <div class="get"><h3>Your printed ad</h3><p>Your logo, a specific offer, clear terms, a unique QR code and your own extension on the shared campaign number.</p></div>
  <div class="get"><h3>AI receptionist for the campaign</h3><p>Answers calls and QR chats about your offer. It books only into time slots you approve, with at least 48 hours of lead time.</p></div>
  <div class="get"><h3>Campaign reporting</h3><p>Calls, scans, conversations, confirmed appointments and, when you share them, sales.</p></div>
  <div class="get"><h3>Design and production handled</h3><p>We coordinate your ad design, printing and hand-out once the vendor and retail partner are confirmed.</p></div>
 </div>
</div></section>

<section class="s" id="bag"><div class="w">
 <div class="sh"><h2>The bag</h2><p>A 19 x 14 x 4 inch reusable tote. Each side has one 10 x 8 inch print area in the center, with six ads in three rows of two. Twelve different businesses across both sides.</p></div>
 <div class="two">
  <figure>{bag(FRONT,"Front side")}<figcaption><b>Front:</b> extensions 101 to 106</figcaption></figure>
  <figure>{bag(BACK,"Back side")}<figcaption><b>Back:</b> extensions 107 to 112</figcaption></figure>
 </div>
 <div class="specs">
  <div><span>Bag size</span><b>19 x 14 x 4 in</b></div>
  <div><span>Print area per side</span><b>10 x 8 in</b></div>
  <div><span>Each ad</span><b>About 5 x 2.6 in</b></div>
  <div><span>Advertisers</span><b>6 per side, 12 total</b></div>
 </div>
 <p class="note">Drawings are to scale and show fictional sample businesses. Each ad is small, so before print we check a full-size proof to make sure your offer, terms and QR code read and scan clearly. Final bag material and size depend on the supplier.</p>
</div></section>

<section class="s alt" id="price"><div class="w">
 <div class="sh"><h2>Pricing</h2><p>One price per placement, per campaign. No monthly fees.</p></div>
 <div class="prices">
  <div class="price"><span class="pt">Founding advertiser</span><div class="amt">$650</div><p>Per placement for your first campaign.</p></div>
  <div class="price"><span class="pt">Later campaigns</span><div class="amt">$750</div><p>Per placement for campaigns after your first.</p></div>
 </div>
 <ul class="terms"><li>12 placements per edition, one business per category.</li><li>The AI receptionist is included for the campaign service period.</li><li>An edition moves forward only after the retail partner and production are confirmed.</li></ul>
</div></section>

<section class="s" id="ask"><div class="w">
 <div class="sh"><h2>Request tote advertising details</h2><p>Tell us about your business. We will contact you with open categories, planned distribution details and next steps.</p></div>
 <form class="rf" id="tbf" novalidate>
  <div class="fld"><label for="t-biz">Business name</label><input id="t-biz" autocomplete="organization"></div>
  <div class="fld"><label for="t-name">Your name</label><input id="t-name" autocomplete="name"></div>
  <div class="fld"><label for="t-email">Work email</label><input id="t-email" type="email" autocomplete="email"></div>
  <div class="fld"><label for="t-phone">Phone</label><input id="t-phone" type="tel" autocomplete="tel"></div>
  <div class="fld"><label for="t-city">City or area</label><input id="t-city" autocomplete="address-level2"></div>
  <div class="fld"><label for="t-cat">Category</label><select id="t-cat"><option value="">Choose one</option>{opts}</select></div>
  <div class="fld full"><label for="t-offer">Offer you have in mind</label><textarea id="t-offer" placeholder="Example: $50 off any repair of $200 or more, new customers only"></textarea></div>
  <div class="fld full"><label>Best way to reach you</label><div class="rad"><label><input type="radio" name="t-pref" value="Phone" checked> Phone</label><label><input type="radio" name="t-pref" value="Email"> Email</label><label><input type="radio" name="t-pref" value="Text"> Text</label></div></div>
  <input type="text" id="t-hp" name="company_website" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">
  <div class="fld full"><label class="chk"><input type="checkbox" id="t-ok"><span>Glamourless Systems may contact me about tote advertising by phone, email or text. Message and data rates may apply. Reply STOP to opt out of texts.</span></label></div>
  <div class="msg" id="tbf-msg" role="status" aria-live="polite"></div>
  <div class="fld full"><button class="btn" type="submit">Request Tote Advertising Details</button></div>
 </form>
</div></section>

<section class="s alt" id="faq"><div class="w nar">
 <div class="sh"><h2>Questions</h2></div>
 {faq}
</div></section>

</div>
'''
FORMJS=open('form.js').read()
open('page.html','w').write(page)
js=('/* GS Tote Billboard page loader. Source of truth: Drive folder GS Tote Billboard Source Code. */\n(function(){\n'
"var root=document.getElementById('gstb-mount');if(!root){root=document.createElement('div');root.id='gstb-mount';var anchor=[].slice.call(document.querySelectorAll('script')).filter(function(x){return !x.src&&x.textContent.indexOf('totebillboard.js')>=0})[0];if(anchor&&anchor.parentNode){anchor.parentNode.insertBefore(root,anchor)}else{document.body.appendChild(root)}}\n"
f"root.innerHTML={json.dumps(page)};\n{FORMJS}\n"
"var g=document.getElementById('gstb');var p=root.parentElement;for(var i=0;i<8&&p&&p!==document.body;i++){if(/c-section|c-row|c-column|inner|custom-code/.test(p.className||'')){p.style.paddingTop='0';p.style.paddingBottom='0';p.style.marginTop='0';p.style.marginBottom='0';p.style.maxWidth='none'}p=p.parentElement}\n"
"try{if(!document.title||/^https?:/.test(document.title))document.title=\"Tote Billboard System | Glamourless Systems\"}catch(e){}\n"
"try{document.documentElement.style.overflowX='hidden';document.body.style.overflowX='hidden'}catch(e){}\n"
"function fit(){g.style.marginLeft='0';var r=root.getBoundingClientRect();g.style.width=document.documentElement.clientWidth+'px';g.style.marginLeft=(-r.left)+'px'}\n"
"fit();window.addEventListener('resize',fit);window.addEventListener('load',fit);setTimeout(fit,800);\n})();\n")
open('totebillboard.js','w').write(js)
open('index.html','w').write('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Tote Billboard System | Glamourless Systems</title><style>body{margin:0}</style></head><body><script>var s=document.createElement("script");s.src="totebillboard.js?v=2";document.body.appendChild(s);</script></body></html>\n')
open('hl-block.html','w').write('<script>var s=document.createElement("script");s.src="https://dsexton24-web.github.io/glamourless-backup/totebillboard/totebillboard.js?v=2";document.body.appendChild(s);</script>\n')
