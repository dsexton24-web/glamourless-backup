# Builds the GS Long Dwell Media page: page.html, longdwellmedia.js (HighLevel loader), index.html (preview), hl-block.html
import json, html
esc=html.escape
ADS=[("Main Street Pizza","$5 OFF","Any large pizza","#d62b2b"),("Corner Auto Care","$10 OFF","Any oil change","#1e3f8f"),("Smile Bright Dental","$79","New patient exam and cleaning","#2f7bf5"),("Classic Cuts Barber","$5 OFF","Any haircut","#d62b2b"),("Fresh Market Grocery","$10 OFF","A $50 purchase","#2e9a46"),
("Glow Salon & Spa","$10 OFF","Any service of $50+","#c2337a"),("Keep Safe Storage","50% OFF","First month","#1e3f8f"),
("Fix It Phone Repair","$15 OFF","Any phone repair","#1e3f8f"),("Easy Move Hauling","$25 OFF","Any local move","#d62b2b"),
("Happy Tails Pet Supply","$5 OFF","A $25 purchase","#2e9a46"),("Open Door Gym","3 DAYS","Free trial pass","#2e9a46"),("Sunrise Diner","10% OFF","Any meal","#d62b2b"),("Sparkle Home Cleaning","$25 OFF","Your first cleaning","#1e3f8f"),("Neighborhood Pharmacy","$5 OFF","Prescription transfer","#2e9a46")]
def mat():
    S=40; W,H=24*S,18*S; M=12; ox,oy=40,30; vw,vh=W+80,H+110
    cw=(W-2*M)/5; ch=(H-2*M)/4; g=6
    # positions: row0 cols0-4, rows1-2 cols0 & 4, row3 cols0-4
    pos=[(0,c) for c in range(5)]+[(1,0),(1,4),(2,0),(2,4)]+[(3,c) for c in range(5)]
    o=[f'<svg viewBox="0 0 {vw} {vh}" role="img" aria-label="18 by 24 inch folding-table mat with 14 equal ad spots around the edge and a laundromat promotion in the center" xmlns="http://www.w3.org/2000/svg">']
    o.append(f'<rect x="{ox}" y="{oy}" width="{W}" height="{H}" rx="14" fill="#123a7a"/>')
    for k,(r,c) in enumerate(pos):
        n,off,cond,col=ADS[k]; x=ox+M+c*cw+g/2; y=oy+M+r*ch+g/2; w=cw-g; h=ch-g
        o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="9" fill="#fff"/>')
        fs=15 if len(n)<17 else 13
        o.append(f'<text x="{x+w/2:.1f}" y="{y+28:.1f}" text-anchor="middle" font-family="Arial" font-weight="800" font-size="{fs}" fill="#0e2a52">{esc(n)}</text>')
        o.append(f'<rect x="{x+10:.1f}" y="{y+44:.1f}" width="{w-82:.1f}" height="44" rx="6" fill="{col}"/>')
        o.append(f'<text x="{x+10+(w-82)/2:.1f}" y="{y+74:.1f}" text-anchor="middle" font-family="Arial" font-weight="800" font-size="19" fill="#fff">{esc(off)}</text>')
        o.append(f'<text x="{x+12:.1f}" y="{y+108:.1f}" font-family="Arial" font-size="11.5" fill="#101c36">{esc(cond)}</text>')
        o.append(f'<text x="{x+w/2:.1f}" y="{y+h-14:.1f}" text-anchor="middle" font-family="Arial" font-weight="700" font-size="13" fill="#101c36">(810) 555-01{10+k}</text>')
        qx=x+w-64; qy=y+42
        o.append(f'<rect x="{qx:.1f}" y="{qy:.1f}" width="54" height="54" fill="#fff" stroke="#101c36" stroke-width="2"/>')
        for a,b in ((4,4),(36,4),(4,36)): o.append(f'<rect x="{qx+a:.1f}" y="{qy+b:.1f}" width="14" height="14" fill="#101c36"/>')
        o.append(f'<rect x="{qx+24:.1f}" y="{qy+24:.1f}" width="7" height="7" fill="#101c36"/><rect x="{qx+36:.1f}" y="{qy+38:.1f}" width="12" height="7" fill="#101c36"/>')
    # center host
    x=ox+M+cw+g/2; y=oy+M+ch+g/2; w=3*cw-g; h=2*ch-g
    o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" fill="#dff0ff"/>')
    o.append(f'<circle cx="{x+90:.1f}" cy="{y+h/2-20:.1f}" r="48" fill="#fff" stroke="#0e2a52" stroke-width="6"/><circle cx="{x+90:.1f}" cy="{y+h/2-20:.1f}" r="28" fill="#5aa2ff"/>')
    o.append(f'<text x="{x+(170+w-30)/2:.1f}" y="{y+70:.1f}" text-anchor="middle" font-family="Arial" font-weight="900" font-size="36" fill="#0e2a52">YOUR LAUNDROMAT</text>')
    o.append(f'<text x="{x+(170+w-30)/2:.1f}" y="{y+108:.1f}" text-anchor="middle" font-family="Arial" font-weight="700" font-size="20" fill="#1e3f8f">Host promotion space</text>')
    o.append(f'<rect x="{x+170:.1f}" y="{y+140:.1f}" width="{w-290:.1f}" height="70" rx="12" fill="#0e2a52"/><text x="{x+170+(w-290)/2:.1f}" y="{y+182:.1f}" text-anchor="middle" font-family="Arial" font-weight="800" font-size="18" fill="#fff">Join our loyalty program</text>')
    o.append(f'<rect x="{x+w-100:.1f}" y="{y+140:.1f}" width="70" height="70" fill="#fff" stroke="#101c36" stroke-width="2"/>')
    for a,b in ((5,5),(47,5),(5,47)): o.append(f'<rect x="{x+w-100+a:.1f}" y="{y+140+b:.1f}" width="18" height="18" fill="#101c36"/>')
    o.append(f'<text x="{x+w/2:.1f}" y="{y+h-24:.1f}" text-anchor="middle" font-family="Arial" font-size="15" fill="#53607a">Loyalty program, app or the laundromat\'s own offer</text>')
    by=oy+H+30
    o.append(f'<line x1="{ox}" y1="{by}" x2="{ox+W}" y2="{by}" stroke="#53607a" stroke-width="2"/><line x1="{ox}" y1="{by-8}" x2="{ox}" y2="{by+8}" stroke="#53607a" stroke-width="2"/><line x1="{ox+W}" y1="{by-8}" x2="{ox+W}" y2="{by+8}" stroke="#53607a" stroke-width="2"/>')
    o.append(f'<text x="{ox+W/2}" y="{by+30}" text-anchor="middle" font-family="Arial" font-weight="700" font-size="22" fill="#0e2a52">Mat 24 in wide x 18 in tall</text>')
    o.append('</svg>'); return "".join(o)

CATS="Restaurant|Auto care|Dental|Barber or salon|Grocery|Storage|Phone repair|Moving|Pet supply|Fitness|Cleaning|Pharmacy|Other".split("|")
FAQ=[("Where do the mats go?","On the folding tables inside participating laundromats, at least 10 mats per location, with the owner's permission."),
("Why laundromats?","People spend real time there. While they fold, the mat sits right in front of them, so your offer gets more than a quick glance."),
("How do customers use my offer?","They scan your QR code, enter their name and mobile number, and get your coupon by text. They can also call your phone number on the mat."),
("What do I get back?","Counts of scans, claimed coupons and delivered coupons, plus redemptions when they can be verified. A scan is not a sale, and we report them separately."),
("Is there an AI receptionist?","No. This product is the mat, your QR coupon page and text delivery. Calls go straight to your own number."),
("When does my coupon expire?","Every coupon on the mat expires on the same fixed campaign end date, printed on your ad and shown on your coupon page."),
("Is $299 a monthly fee?","No. It is $299 total for one 60-day campaign."),
("I own a laundromat. What is in it for me?","The center of every mat promotes your loyalty program, app or offer at no cost to you. Host compensation is worked out with each owner."),
("Do you guarantee customers or sales?","No. We track responses honestly and share what can be verified.")]
CSS=open('style.css').read(); FORMJS=open('form.js').read()
opts="".join(f'<option>{esc(c)}</option>' for c in CATS)
faq="".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in FAQ)
page=f'''<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
<div id="gsld">
<div class="stage">Staging preview. Not live. Not linked from the GS website. Do not share yet.</div>

<section class="hero"><div class="w hg">
 <div>
  <span class="kick">GS Long Dwell Media</span>
  <h1>Your offer, in front of them <span>for the whole fold.</span></h1>
  <p class="lead">Full-color ad mats on laundromat folding tables. Local shoppers see your offer the entire time they fold, then scan to get your coupon by text.</p>
  <div class="cta2"><a class="btn" href="#ask">Ask About an Ad Spot</a><a class="btn ghost" href="#how">See How It Works</a></div>
  <ul class="chips"><li>14 spots per mat</li><li>$299 for 60 days</li><li>Your own QR coupon</li></ul>
 </div>
 <figure class="hfig">{mat()}<figcaption>Concept mockup drawn to scale. Sample businesses are fictional.</figcaption></figure>
</div></section>

<section class="s" id="how"><div class="w">
 <div class="sh"><h2>How it works</h2><p>A laundry visit is long. Your ad stays put the whole time.</p></div>
 <div class="steps">
  <div class="step"><b>1</b><h3>You send your offer</h3><p>A real, specific offer, your logo and your phone number. You approve the ad before print.</p></div>
  <div class="step"><b>2</b><h3>We print the mats</h3><p>Fourteen local businesses share each mat, with the laundromat's own promotion in the center.</p></div>
  <div class="step"><b>3</b><h3>Shoppers scan</h3><p>Your QR code opens your offer page. They enter their name and mobile number to claim it.</p></div>
  <div class="step"><b>4</b><h3>The coupon arrives by text</h3><p>Their coupon comes by text. We count scans, claims and verified redemptions for you.</p></div>
 </div>
</div></section>

<section class="s alt" id="mat"><div class="w">
 <div class="sh"><h2>The mat</h2><p>18 x 24 inches, landscape, single-sided. Built to be waterproof, wipeable and tear-resistant, and to lie flat on the table without adhesive.</p></div>
 <figure class="matfig">{mat()}<figcaption>Fourteen equal ad spots around the edge. The center belongs to the host laundromat.</figcaption></figure>
 <div class="specs">
  <div><span>Mat size</span><b>18 x 24 in</b></div>
  <div><span>Ad spots</span><b>14 per mat</b></div>
  <div><span>Mats per location</span><b>10 or more</b></div>
  <div><span>Campaign</span><b>60 days</b></div>
 </div>
 <p class="note">Each ad shows your business name and logo, a real offer, your phone number and your own QR code. Before any mat goes out, we print a full-size test and check that every QR code scans from a normal standing distance and that the mat survives cleaning and daily use.</p>
</div></section>

<section class="s"><div class="w">
 <div class="sh"><h2>Who it is for</h2></div>
 <div class="who">
  <div class="get"><h3>Local businesses</h3><p>Reach neighbors who are close by and have time to read.</p><ul><li>Your offer, logo, phone number and QR code</li><li>Text coupon delivery, with marketing opt-in asked separately</li><li>Scan, claim and redemption counts kept separate</li></ul></div>
  <div class="get"><h3>Laundromat owners</h3><p>Turn your folding tables into something that works for you.</p><ul><li>Center space on every mat for your loyalty program, app or offer</li><li>Durable mats that protect your tables</li><li>Host compensation worked out with each location</li></ul></div>
 </div>
</div></section>

<section class="s alt" id="price"><div class="w">
 <div class="sh"><h2>Pricing</h2><p>One price for the whole campaign. No monthly fees.</p></div>
 <div class="prices">
  <div class="price"><span class="pt">One ad spot</span><div class="amt">$299</div><p>Total for one 60-day campaign at a participating location.</p></div>
 </div>
 <ul class="terms"><li>14 ad spots per mat.</li><li>All coupons expire on the same printed campaign end date.</li><li>A location goes live only after the owner approves and the test mat passes.</li></ul>
</div></section>

<section class="s" id="ask"><div class="w">
 <div class="sh"><h2>Request details</h2><p>Advertisers and laundromat owners can both start here. We will reach out with open spots, participating locations and next steps.</p></div>
 <form class="rf" id="ldf" novalidate>
  <div class="fld full"><label>I am a</label><div class="rad"><label><input type="radio" name="l-role" value="Advertiser" checked> Business that wants to advertise</label><label><input type="radio" name="l-role" value="Laundromat owner"> Laundromat owner</label></div></div>
  <div class="fld"><label for="l-biz">Business name</label><input id="l-biz" autocomplete="organization"></div>
  <div class="fld"><label for="l-name">Your name</label><input id="l-name" autocomplete="name"></div>
  <div class="fld"><label for="l-email">Work email</label><input id="l-email" type="email" autocomplete="email"></div>
  <div class="fld"><label for="l-phone">Phone</label><input id="l-phone" type="tel" autocomplete="tel"></div>
  <div class="fld"><label for="l-city">City or area</label><input id="l-city" autocomplete="address-level2"></div>
  <div class="fld"><label for="l-cat">Category (advertisers)</label><select id="l-cat"><option value="">Choose one</option>{opts}</select></div>
  <div class="fld full"><label for="l-offer">Offer you have in mind, or tell us about your laundromat</label><textarea id="l-offer" placeholder="Example: $10 off any service of $50 or more"></textarea></div>
  <div class="fld full"><label>Best way to reach you</label><div class="rad"><label><input type="radio" name="l-pref" value="Phone" checked> Phone</label><label><input type="radio" name="l-pref" value="Email"> Email</label><label><input type="radio" name="l-pref" value="Text"> Text</label></div></div>
  <input type="text" id="l-hp" name="company_website" tabindex="-1" autocomplete="off" aria-hidden="true" class="hp">
  <div class="fld full"><label class="chk"><input type="checkbox" id="l-ok"><span>Glamourless Systems may contact me about Long Dwell Media by phone, email or text. Message and data rates may apply. Reply STOP to opt out of texts.</span></label></div>
  <div class="msg" id="ldf-msg" role="status" aria-live="polite"></div>
  <div class="fld full"><button class="btn" type="submit">Request Details</button></div>
 </form>
</div></section>

<section class="s alt" id="faq"><div class="w nar">
 <div class="sh"><h2>Questions</h2></div>
 {faq}
</div></section>

<footer><div class="w"><span>Glamourless Systems | 1614 23rd St., Port Huron, MI 48060</span><span><a href="mailto:admin@glamourlesssystems.com">admin@glamourlesssystems.com</a></span></div></footer>
</div>
'''
open('page.html','w').write(page)
js=('/* GS Long Dwell Media page loader. Source of truth: Drive folder GS Long Dwell Media Source Code. */\n(function(){\n'
"var root=document.getElementById('gsld-mount');if(!root){root=document.createElement('div');root.id='gsld-mount';var anchor=[].slice.call(document.querySelectorAll('script')).filter(function(x){return !x.src&&x.textContent.indexOf('longdwellmedia.js')>=0})[0];if(anchor&&anchor.parentNode){anchor.parentNode.insertBefore(root,anchor)}else{document.body.appendChild(root)}}\n"
f"root.innerHTML={json.dumps(page)};\n{FORMJS}\n"
"var g=document.getElementById('gsld');var p=root.parentElement;for(var i=0;i<8&&p&&p!==document.body;i++){if(/c-section|c-row|c-column|inner|custom-code/.test(p.className||'')){p.style.paddingTop='0';p.style.paddingBottom='0';p.style.marginTop='0';p.style.marginBottom='0';p.style.maxWidth='none'}p=p.parentElement}\n"
"try{document.documentElement.style.overflowX='hidden';document.body.style.overflowX='hidden'}catch(e){}\n"
"function fit(){g.style.marginLeft='0';var r=root.getBoundingClientRect();g.style.width=document.documentElement.clientWidth+'px';g.style.marginLeft=(-r.left)+'px'}\n"
"fit();window.addEventListener('resize',fit);window.addEventListener('load',fit);setTimeout(fit,800);\n})();\n")
open('longdwellmedia.js','w').write(js)
open('index.html','w').write('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Long Dwell Media | Glamourless Systems (staging)</title><style>body{margin:0}</style></head><body><script>var s=document.createElement("script");s.src="longdwellmedia.js?v=1";document.body.appendChild(s);</script></body></html>\n')
open('hl-block.html','w').write('<script>var s=document.createElement("script");s.src="https://dsexton24-web.github.io/glamourless-backup/longdwellmedia/longdwellmedia.js?v=1";document.body.appendChild(s);</script>\n')
