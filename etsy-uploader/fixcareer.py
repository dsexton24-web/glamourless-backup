# Career guides are not business plans. Run after build_packages.py to correct their listing text.
import json,re
P='out/GS Etsy Upload Packages/manifest.json'
m=json.load(open(P))
C={
'GS-0245':('Helping Hands Career Entry Guide, Step by Step Plan to Start a Care Career, Printable PDF and Editable Word Guide','A plain career entry guide for people who want to start work in helping and care roles. Pay and licensing figures change and vary by state, so verify current numbers with the Bureau of Labor Statistics and your state before you decide.',['care career','caregiver career','helping careers']),
'GS-0246':('Tech Career Entry Playbook, Step by Step Plan to Break Into Tech, Printable PDF and Editable Word Guide','A plain career entry playbook for getting started in technology work. Pay and certification prices change, so verify with current job postings, the vendor and the Bureau of Labor Statistics before you budget.',['tech career','break into tech','it career guide']),
'GS-0272':('Trade Entry Playbook, Step by Step Plan to Start a Skilled Trade Career, Printable PDF and Editable Word Guide','A plain playbook for entering the skilled trades. Licensing rules, program terms and requirements differ by place and change over time, so check your local rules before you commit.',['skilled trades','trade career','apprenticeship']),
'GS-0273':('First Career Playbook, Step by Step Plan to Choose and Start a First Career, Printable PDF and Editable Word Guide','A plain playbook for people choosing and starting their first career, from how entry level hiring works to a twelve month get hired and get promoted plan.',['first career','first job guide','graduation gift']),
'GS-0284':('Career Pivot Playbook, Step by Step Plan to Change Careers, Printable PDF and Editable Word Guide','A plain playbook for moving from one career to another. It is a project plan, not a pep talk. Work it in order: the audit and the lanes come before the resume, the resume before the search, the search before the negotiation.',['career change','career pivot','change careers']),
}
WHO={'GS-0245':'Built for people who want paid work helping others and need a clear way in, with or without a degree.','GS-0246':'Built for beginners and career changers who want a first job in tech without wasting money on the wrong course.','GS-0272':'Built for people who want to earn while they learn in a skilled trade instead of taking on college debt.','GS-0273':'Built for young adults, recent graduates and the parents helping them pick a first career and get hired.','GS-0284':'Built for working adults who want to move into a different career without starting from zero.'}
COMMON=['career guide','career planning','job search guide','career playbook','resume help','interview prep','career workbook','printable guide','editable word doc','digital download']
for it in m['items']:
    c=C.get(it.get('sku'))
    if not c or it.get('kind','blueprint')!='blueprint': continue
    t,lead,tg=c
    assert len(t)<=140,(it['sku'],len(t))
    it['title']=t
    d=it['description']; rest=d.split('\n\n',1)[1]
    rest=rest.replace('is a complete written business plan you can follow step by step','is a complete written career plan you can follow step by step').replace('from the first decision to steady customers','from the first decision to the job offer')
    rest=re.sub(r'WHO IT IS FOR\n.*?\n\n','WHO IT IS FOR\n'+WHO[it['sku']]+'\n\n',rest,flags=re.S)
    rest=rest.replace('How Hiring Actually Works at 18 to\n','How Hiring Actually Works at 18 to 22\n')
    it['description']=lead+'\n\n'+rest
    tags=[x for x in tg+COMMON if len(x)<=20][:13]; assert len(tags)==13
    it['tags']=tags
    print(it['sku'],len(t),'business' in it['description'].lower(), 'customer' in it['description'].lower())

import build_packages as bp
D='out/GS Etsy Upload Packages/'
by={i['sku']:i for i in m['items'] if i.get('kind','blueprint')!='tool'}
# career guides: Start Here page should not talk about a business
for sku in C:
    bp.start_here_pdf(D+sku+'/'+sku+' Start Here.pdf',{'title':by[sku]['title'].split(',')[0]},whole='plan',thing='guide')
# GS-0113 is a boat builder's manual, not a business plan
it=by['GS-0113']
it['title']='ShoreHaul 78 Micro Skiff Concept Manual, Ultralight Stitch and Glue Boat Build Guide, Printable PDF and Editable Word'
d=it['description']
d=d.replace('ShoreHaul 78 Concept Manual is a complete written business plan you can follow step by step.','The ShoreHaul 78 Concept Manual is a complete written build guide you can follow step by step.').replace(', from the first decision to steady customers.',', from tools and materials through the build.')
d=d.replace('- The full blueprint as a printable PDF','- The full manual as a printable PDF').replace('- The same blueprint as an editable Word document, so you can make it your own','- The same manual as an editable Word document, so you can add your own notes')
d=d.replace('This blueprint is for education and planning. It does not promise any income or results, and it is not legal, tax or financial advice. Check current rules and costs where you live before you start.','This is a concept manual for education and planning. Boat building and boating carry real risk. You are responsible for your own build, materials, testing and safety on the water, and for following the boating rules where you live. Check current material prices before you budget.')
it['description']=d
it['tags']=['micro skiff','boat building','stitch and glue','diy boat','small boat','skiff build','boat build guide','epoxy fiberglass','woodworking project','diy project','shorehaul 78','printable guide','digital download']
bp.start_here_pdf(D+'GS-0113/GS-0113 Start Here.pdf',{'title':'ShoreHaul 78 Concept Manual'},whole='build',thing='manual')
# GS-0089: make the platonic scope obvious in the title
it=by['GS-0089']
it['title']='Platonic Companionship Service Business Blueprint, Step by Step Startup Plan, Printable PDF and Editable Word Guide'
it['tags']=(['companion service','platonic companion']+[t for t in it['tags'] if t not in('companion service','platonic companion')])[:13]
for s in ('GS-0113','GS-0089'):
    assert len(by[s]['title'])<=140 and len(by[s]['tags'])==13 and all(len(t)<=20 for t in by[s]['tags']),s
    print(s,len(by[s]['title']),by[s]['title'])
json.dump(m,open(P,'w'),indent=1)
