# Held SKU repairs, 2026-11-12, Claude APP. Re-runnable record of every text change.
# Usage: python3 repair_all.py <canonical Blueprints and Bundles folder> <output folder>
import sys, os, copy, docx
sys.path.insert(0, os.path.dirname(__file__)); import dx

R, O = sys.argv[1], sys.argv[2]
P296 = R + '/GS-0296 Ceiling Texture Modernization Blueprint'
P298 = R + '/GS-0298 Mobile Basketball Trailer Blueprint'
P250 = R + '/GS-0250 Automotive Laser Button Restoration Blueprint'
P297 = R + '/GS-0297 Custom Vendor Signage Blueprint'

DOCX = {
 P296 + '/Supporting Documents/SD-GS-0296-06 Pre-Disturbance Screening Checklist.docx': [
  ('decide whether testing is required, and stop the job cold', 'confirm a documented negative lab result for every material before it is disturbed, and stop the job cold'),
  ('PROCEED, no test required', 'PROCEED, documented negative lab result'),
  ('Material identity is documented and the substrate is verified eligible under your written criteria.', "A qualified lab has tested a sample of every material you will disturb in this room, and the written result is negative. Build year, appearance, old paperwork or the owner's word are never enough on their own."),
  ('File the basis for the decision on this sheet. Proceed to containment setup.', 'Attach the lab report for every material to this sheet. Then proceed to containment setup.'),
  ('All rooms cleared to proceed under documented criteria', 'All rooms cleared to proceed, documented negative lab result attached for every material to be disturbed')],
 P296 + '/Supporting Documents/SD-GS-0296-01 Asbestos Stop-Work and Referral SOP.docx': [
  ('Resume work only when the file shows a documented basis to proceed, a test result, or a completed referral.', 'Resume work only when the file holds a documented negative lab result for every material to be disturbed. A completed referral closes the removal work for this company; it never reopens it.')],
 P296 + '/Blueprint/GS-0296 Ceiling Texture Modernization Blueprint.docx': [
  ('Eligible: you have documented basis, such as reliable records or a documented negative test result for the material to be disturbed, and no other stop condition applies.', 'Eligible: you hold a documented negative lab result for every material to be disturbed, and no other stop condition applies. Records, build year and appearance can raise a flag, but they never replace the lab result.')],
 P298 + '/Supporting Documents/SD-GS-0298-07 Safety Inspection Checklist.docx': [
  ('Only the operator or a designated helper retrieves balls from inside the zone during play.', 'No one enters a shooting lane while shooting is live. Balls return to a collection point, or the operator or a designated helper goes in for them only after shooting is stopped. Waiting players never chase balls.'),
  ('If something on this sheet fails, the trailer does not open until it is fixed or the affected part stays closed.', 'If something on this sheet fails, the trailer does not open until it is fixed and re-inspected, or the affected hoop or area stays closed for the whole event.'),
  ('Result (circle one):   OPEN   /   OPEN WITH NOTED FIXES   /   DO NOT OPEN', 'Result (circle one):   OPEN   /   DO NOT OPEN'),
  ('Fixes required before opening, if any: ', 'Failed items (each must be fixed and re-inspected, or that hoop or area stays closed, before you circle OPEN): ')],
 P250 + '/Blueprint/GS-0250 Automotive Laser Button Restoration.docx': [
  ('When the material is unknown, you test on a hidden area or a sacrificial coupon, or you decline.', 'When the material is unknown or not on your verified acceptable-materials list, you stop and decline the part. A test coupon never tells you what a material is. It only checks process quality on material you have already identified and approved.'),
  ('Unknown means test or decline.', 'Unknown means stop and decline.'),
  ('A common effective setup is multi-stage filtration: a pre-filter for larger particles, a HEPA filter for fine particulates, and activated carbon for gases and volatile organics. If you vent outdoors, check local air quality and building rules first. If you recirculate indoors, the filtration must actually be rated for the contaminants, and filters must be changed on schedule, not when you remember.', "Which extraction and filtration setup is right, and whether you must vent outdoors or may recirculate indoors, depends on your machine, your materials and your site. Use the extraction your laser manufacturer specifies for the materials you will process, check local air quality and building rules, and change filters on the manufacturer's schedule, not when you remember."),
  ('never laser a part with unknown coatings, adhesives, or residues without identifying them or testing on a sacrificial area with full extraction running.', 'never laser a part with unknown coatings, adhesives, or residues. Identify them from manufacturer or supplier documentation first. If you cannot, decline the part.'),
  ('If your ventilation is ever compromised, or during filter changes and machine cleaning where accumulated dust is disturbed, use appropriate respiratory protection. Do not use dust masks as a substitute for ventilation.', "If your extraction is ever weak, failed or in doubt, stop the laser. A respirator is never a way to keep working without extraction. Fix the extraction and re-verify airflow before the next job. For filter changes and machine cleaning, follow the manufacturer's procedure. Where a respirator is required, use it under a proper respiratory protection program, and never use a dust mask in place of ventilation."),
  ('Connect the exhaust port to a fume extraction unit with pre-filter, HEPA, and activated carbon stages, ducted to vent outside through a wall penetration that complies with your local building rules, or recirculating through the filtration unit if outdoor venting is not permitted.', 'Connect the exhaust port to the fume extraction your laser manufacturer specifies for your materials, installed to meet your local building and air rules.'),
  ('Designate yourself laser safety officer in writing, with the dated responsibility statement.', 'Name in writing who is responsible for laser safety, and only after that person has finished the training above. A title on paper is not training.'),
  ('plus your written SOP and your written designation as laser safety officer.', 'plus your written SOP and a written record of who is responsible for laser safety, backed by that training.'),
  ('and the interlock stop test is logged.', "and your interlock checks are logged, done only the way the manufacturer's manual directs, never by opening the door on a live job."),
  ('plus the logged interlock stop test', "plus logged interlock checks done only by the manufacturer's procedure"),
  ('Unknown means coupon-test on sacrificial material with full extraction, or decline.', 'Unknown means decline. A coupon is only for material already on your verified list.'),
  ('Chapter 03. Laser classes, enclosure, fumes, training and PPE . . . 19', 'Chapter 03. Laser classes, enclosure, fumes, training and PPE . . . 20')],
 P250 + '/Supporting Documents/SD-GS-0250-03 Laser Safety and Ventilation Preflight.docx': [
  ('door-open test stops emission', "any further interlock check only as the manufacturer's manual directs; never open the door on a live job")],
 P250 + '/Supporting Documents/SD-GS-0250-05 Part Eligibility and Exclusion Matrix.docx': [
  ('Test on coupon or decline.', 'Decline. A coupon does not identify a material.')],
 P250 + '/Supporting Documents/SD-GS-0250-08 Test Coupon and Settings Record.docx': [
  ('so the tenth panel matches the first.', 'so the tenth panel matches the first. Coupons are run only on material already on your verified acceptable-materials list, with extraction verified. A coupon never identifies an unknown material.')],
}

HTML = {
 P296 + '/IC-0296/IC-GS-0296 Ceiling Texture Modernization Blueprint.html': [
  ('<label>Where required, has a qualified professional assessed / tested it?</label><select name="tested"><option value="yes">Yes, documented</option><option value="no">No</option><option value="na">Not required for this documented material</option></select>',
   '<label>Is there a documented lab result for every material you will disturb?</label><select name="tested"><option value="no">No / not yet / verbal only</option><option value="yes">Yes, negative, written lab report on file</option><option value="positive">Yes, and asbestos was detected</option></select>'),
  ("if(v(f,'tested')==='no'){return '⛔ HOLD: Material is identified, but required qualified assessment / testing is not documented. No start until it is. Documented screening is Step Zero.'}",
   "if(v(f,'tested')==='positive'){return '⛔ STOP AND REFER: Asbestos was detected. This is regulated work, outside this service. Do not disturb it. Refer the customer to qualified abatement professionals and document the referral.'}if(v(f,'tested')!=='yes'){return '⛔ HOLD: No documented negative lab result for every material you will disturb. No start until there is one. Age, appearance, old paperwork or an owner statement never replace a lab result. Documented screening is Step Zero.'}"),
  ('required assessment/testing documented,', 'a documented negative lab result for every material to be disturbed,')],
 P298 + '/IC-0298/IC-GS-0298 Mobile Basketball Trailer Blueprint.html': [
  ('keep balls retrieved safely', 'keep everyone out of live shooting lanes (balls come back by collection point, or staff retrieve them only after shooting stops)')],
}

# GS-0297: two new sections (text in Held SKU Repair log); inserted before these headings,
# cloning the style of 'Procedure Five: Damage and Rework Management' and its body paragraph.
GS0297_INSERTS = [
 ('The Decision Process: When Quality Slips', 'The Job File: One Folder Per Order'),
 ('Checklist: Channels and Acquisition', 'Tracking Where Every Order Came From'),
]

os.makedirs(O, exist_ok=True)
for f, reps in DOCX.items():
    d = docx.Document(f)
    for a, b in reps: dx.replace(d, a, b)
    d.save(os.path.join(O, os.path.basename(f)))
for f, reps in HTML.items():
    s = open(f, encoding='utf-8').read()
    for a, b in reps:
        assert s.count(a) == 1, a[:60]; s = s.replace(a, b)
    open(os.path.join(O, os.path.basename(f)), 'w', encoding='utf-8').write(s)
# PDFs regenerated with: soffice --headless --convert-to pdf <docx>
# Buyer zips and website kit zips: members replaced by name, all other members copied byte for byte.
