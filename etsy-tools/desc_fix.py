# Replaces the broken opening paragraph of 46 blueprint listings with a plain, search-friendly summary.
# Only the first paragraph changes; everything after it stays exactly as it was.
import json, sys
OPEN = {
'GS-0014':"Plan your path to becoming a commercial pilot: training routes, certificates, flight hours, real costs, financing, and how to land your first paying flying job. A career plan, not a promise of a job.",
'GS-0038':"Plan a step-by-step exit from your job or current business into income you control online: what to build first, how to test it, and when it is safe to make the jump.",
'GS-0067':"Build a lead intelligence business that researches, verifies, and packages local business leads for contractors and service companies who need reliable prospects, not junk lists.",
'GS-0101':"Career guide to working as a remote mining operations controller: what the job involves, the skills and training employers look for, how to get hired, and what the shifts are really like.",
'GS-0105':"Build revenue from a local service route: choose the right route service, price stops, group customers tightly, and grow recurring accounts you can run on a set schedule.",
'GS-0113':"The complete builder's manual for the ShoreHaul 78, an ultralight shore-launch micro skiff one person can launch and retrieve without a trailer, plus a plan for building and selling them.",
'GS-0120':"Start a personalized wood products business: choose products people order as gifts, price for profit, take custom orders, and sell locally and online from a home workshop.",
'GS-0124':"Start a UGC content studio that makes user-generated-style video ads for brands: find clients, price packages, script and film content, and deliver work brands come back for.",
'GS-0144':"Start a specialty business installing hidden emergency escape ladders in homes: find customers, quote and install safely, and partner with builders, realtors, and safety-minded homeowners.",
'GS-0162':"Build a business around lost and hidden places: tours, content, and guides that turn local history and forgotten locations into paid experiences, done legally and with permission.",
'GS-0182':"Start a professional house sitting and pet sitting business: set your services and prices, screen clients, handle keys and emergencies, and build repeat customers and referrals.",
'GS-0185':"Start a piano tuning and service route: learn what the trade involves, plan training, price tunings, and build recurring clients with schools, churches, teachers, and homeowners.",
'GS-0186':"Start a senior home modification business that helps older adults stay safe and independent at home: assessments, grab bars, ramps, and safety upgrades, with clear scope and referral rules.",
'GS-0187':"Evaluate and start a drone exterior cleaning business for commercial buildings: equipment choices, FAA rules, site safety, pricing, and how to land recurring cleaning contracts.",
'GS-0191':"Start a mobile mattress sanitizing business: equipment, cleaning process, pricing, and selling to homeowners, rentals, hotels, and care facilities. A companion to the Mattress Money Machine blueprint.",
'GS-0195':"Build a niche directory website: pick a profitable niche, gather and verify listings, get found in search, and earn from featured listings, ads, and leads.",
'GS-0196':"Start a contextual collectible vending route: place compact vending machines selling themed collectibles in the right host locations, then stock, service, and grow the route.",
'GS-0234':"Start a referral pipeline agency that designs, recruits, and tracks referral-partner programs for local businesses, so your clients get steady customer introductions.",
'GS-0235':"Plan, launch, and grow a podcast: pick your show format, record and edit, book guests, promote episodes, and measure what is working.",
'GS-0241':"Design, price, sell, and run premium workshop days for businesses and groups, with a clear plan for content, facilitation, and follow-up that brings repeat bookings.",
'GS-0247':"Start a live shopping business that sells products through live video: choose a platform, source inventory, run shows that convert, and handle shipping and returns.",
'GS-0248':"Start a decorative gravel stabilization and resin-bound surface business for driveways, paths, and patios: materials, installation, pricing, and finding customers.",
'GS-0249':"Start an artificial skylight installation business: LED sky panels for basements, offices, and windowless rooms, with product selection, installation, pricing, and sales.",
'GS-0250':"Start an automotive laser button restoration service that restores worn, faded buttons and controls on car interiors for owners, detailers, and dealers.",
'GS-0251':"Start a custom 3D chocolate printing business for events, gifts, and brands: choose a printer, design products, price orders, and sell to party planners and companies.",
'GS-0252':"Run stick-catching reaction games at fairs, festivals, and live events: equipment, staffing, safety, pricing per play, and booking events.",
'GS-0253':"Start a single-serve honey packaging and distribution business: sourcing honey, packaging formats, food rules, pricing, and selling to cafes, gyms, hotels, and gift shops.",
'GS-0255':"Start a cemetery memorial vending route: place machines near cemeteries and memorial sites selling flowers, candles, and remembrance items, with host agreements and restocking.",
'GS-0256':"Build an advertising network on laundromat screens and surfaces: sign host locations, sell ad space to local businesses, and run campaigns customers actually see.",
'GS-0258':"Source specialty equipment from local marketplaces, auctions, and liquidations and resell it on eBay: what to buy, how to verify it, price it, ship it, and grow.",
'GS-0267':"Start an outdoor lighting business that designs and installs landscape and permanent lighting for homes and businesses, with pricing, installation, and sales steps.",
'GS-0268':"Start a self-portrait studio where customers take their own professional-looking photos with a fixed camera, studio lighting, and a remote shutter, booked by the session.",
'GS-0271':"Work as a fractional operator who runs operations for several small businesses part time: package your services, find clients, set pricing, and deliver results.",
'GS-0276':"Find, evaluate, and buy an existing small business: where to look, how to check the numbers, financing options, due diligence, and taking over without losing customers.",
'GS-0277':"Run an online store as an operator: product selection, store setup, listings, ads, fulfillment, customer service, and the numbers that keep it profitable.",
'GS-0278':"Operate rental property like a business: buying criteria, real numbers, tenant screening, maintenance, turnover, and keeping cash flow positive.",
'GS-0279':"Build a career as a licensed sales professional: choose your field, get licensed, find leads, run appointments, and build a steady book of clients.",
'GS-0289':"Start an interior LED cove lighting service that installs hidden ceiling and wall lighting in homes and businesses, with product choices, installation, and pricing.",
'GS-0290':"Start an equipment rental business with little money: pick equipment people rent, set rates and deposits, protect your gear, and grow a rental fleet.",
'GS-0291':"Start an event rental business: tables, chairs, tents, and party gear, with a plan to start small, price rentals, handle delivery, and scale up.",
'GS-0292':"Start a mobile permanent jewelry business: welded bracelets and chains at parties, pop-up markets, and events, with equipment, pricing, and booking steps.",
'GS-0293':"Start a screen protector installation business: local demand, supplies, pricing, kiosk and mobile setups, and selling to phone owners and businesses.",
'GS-0294':"Start a day-of event coordination business for weddings and events: services, pricing, vendor coordination, timelines, and how it differs from full planning.",
'GS-0295':"Start a public domain publishing business: find public domain works, add real value, format and publish on Amazon KDP and other stores, and follow the rules.",
'GS-0296':"Start a ceiling texture modernization business that removes or covers popcorn ceilings and updates textured ceilings, with strict safety screening before any work.",
'GS-0299':"Start a custom luxury metal card business: metal business cards and VIP cards, with suppliers, design, pricing, and selling to professionals and brands.",
}
m = json.load(open(sys.argv[1])); n = 0
for i in m['items']:
    if i['kind'] == 'blueprint' and i['sku'] in OPEN:
        parts = i['description'].split('\n\n', 1)
        i['description'] = OPEN[i['sku']] + '\n\n' + parts[1]; n += 1
m['update_text'] = [i['sku'] + '-blueprint' for i in m['items'] if i['kind'] == 'blueprint' and i['sku'] in OPEN]
m['text_version'] = 'desc-20261113'
json.dump(m, open(sys.argv[2], 'w'), indent=1)
print(n, 'descriptions fixed')
