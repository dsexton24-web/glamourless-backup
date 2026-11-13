// GS Etsy Uploader: Cloudflare Worker
// Holds the Etsy key as secrets, connects to Doug's Etsy shop once with OAuth (PKCE),
// and turns upload packages (picked from Doug's computer in the browser) into Etsy listings.
//
// Bindings required:
//   KV namespace binding:  STORE
//   Secrets:               ETSY_KEYSTRING, ETSY_SHARED_SECRET
// Optional variable:       ALLOWED_USER_ID (locks the tool to one Etsy user; set automatically on first connect if empty)

const ETSY_API = 'https://api.etsy.com/v3';
const SCOPES = 'listings_r listings_w shops_r';

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    try {
      if (url.pathname === '/') return html(PAGE);
      if (url.pathname === '/connect') return connect(url, env);
      if (url.pathname === '/callback') return callback(url, env);
      if (url.pathname.startsWith('/api/')) {
        const sess = await session(req, env);
        if (!sess) return json({ error: 'not_connected' }, 401);
        if (url.pathname === '/api/status') return json({ ok: true, shop_id: sess.shop_id, shop_name: sess.shop_name });
        if (url.pathname === '/api/taxonomy') return taxonomy(url, env);
        if (url.pathname === '/api/listing' && req.method === 'POST') return createListing(req, env, sess);
        if (url.pathname === '/api/replace-files' && req.method === 'POST') return replaceFiles(req, env, sess);
        if (url.pathname === '/api/update-tags' && req.method === 'POST') return updateTags(req, env, sess);
        if (url.pathname === '/api/disconnect' && req.method === 'POST') {
          await env.STORE.delete('tok');
          return json({ ok: true }, 200, { 'Set-Cookie': 'gs_etsy=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax' });
        }
      }
      return new Response('Not found', { status: 404 });
    } catch (e) {
      return json({ error: 'server_error', detail: String(e && e.message || e) }, 500);
    }
  }
};

// ---------- OAuth ----------
function b64url(bytes) {
  let s = btoa(String.fromCharCode(...new Uint8Array(bytes)));
  return s.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
function randomString(n = 48) {
  return b64url(crypto.getRandomValues(new Uint8Array(n)));
}
async function connect(url, env) {
  const verifier = randomString(48);
  const challenge = b64url(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(verifier)));
  const state = randomString(16);
  await env.STORE.put('pkce:' + state, verifier, { expirationTtl: 900 });
  const redirect = url.origin + '/callback';
  const q = new URLSearchParams({
    response_type: 'code', client_id: env.ETSY_KEYSTRING, redirect_uri: redirect,
    scope: SCOPES, state, code_challenge: challenge, code_challenge_method: 'S256'
  });
  return Response.redirect('https://www.etsy.com/oauth/connect?' + q.toString(), 302);
}
async function callback(url, env) {
  const state = url.searchParams.get('state') || '';
  const code = url.searchParams.get('code');
  const verifier = await env.STORE.get('pkce:' + state);
  if (!code || !verifier) return html(msgPage('Connection did not finish. Go back and click Connect to Etsy again.'), 400);
  await env.STORE.delete('pkce:' + state);
  const r = await fetch(ETSY_API + '/public/oauth/token', {
    method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ grant_type: 'authorization_code', client_id: env.ETSY_KEYSTRING,
      redirect_uri: url.origin + '/callback', code, code_verifier: verifier })
  });
  const t = await r.json();
  if (!r.ok) return html(msgPage('Etsy said no: ' + escapeHtml(JSON.stringify(t))), 400);
  const userId = String(t.access_token).split('.')[0];
  const owner = env.ALLOWED_USER_ID || await env.STORE.get('owner');
  if (owner && owner !== userId) return html(msgPage('This uploader is locked to a different Etsy account.'), 403);
  if (!owner) await env.STORE.put('owner', userId);
  // Find the shop for this user
  const shops = await etsyFetch(env, t.access_token, '/application/users/' + userId + '/shops');
  const shop = await shops.json();
  if (!shops.ok || !shop.shop_id) return html(msgPage('Connected, but no Etsy shop was found on this account.'), 400);
  const sid = randomString(32);
  await env.STORE.put('tok', JSON.stringify({
    access: t.access_token, refresh: t.refresh_token, exp: Date.now() + (t.expires_in - 120) * 1000,
    user_id: userId, shop_id: shop.shop_id, shop_name: shop.shop_name, sid
  }));
  return new Response(null, { status: 302, headers: {
    Location: '/', 'Set-Cookie': `gs_etsy=${sid}; Path=/; Max-Age=2592000; HttpOnly; Secure; SameSite=Lax` } });
}
async function session(req, env) {
  const cookie = req.headers.get('Cookie') || '';
  const m = cookie.match(/gs_etsy=([A-Za-z0-9_-]+)/);
  if (!m) return null;
  const raw = await env.STORE.get('tok');
  if (!raw) return null;
  const tok = JSON.parse(raw);
  if (tok.sid !== m[1]) return null;
  if (Date.now() > tok.exp) {
    const r = await fetch(ETSY_API + '/public/oauth/token', {
      method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ grant_type: 'refresh_token', client_id: env.ETSY_KEYSTRING, refresh_token: tok.refresh })
    });
    const t = await r.json();
    if (!r.ok) { await env.STORE.delete('tok'); return null; }
    tok.access = t.access_token; tok.refresh = t.refresh_token || tok.refresh;
    tok.exp = Date.now() + (t.expires_in - 120) * 1000;
    await env.STORE.put('tok', JSON.stringify(tok));
  }
  return tok;
}
// Waits and retries when Etsy says "too many requests per second", so a step never stops halfway.
async function etsyFetch(env, access, path, init = {}) {
  const headers = Object.assign({ 'x-api-key': env.ETSY_KEYSTRING + ':' + env.ETSY_SHARED_SECRET }, init.headers || {});
  if (access) headers['Authorization'] = 'Bearer ' + access;
  let r;
  for (let a = 0; a < 6; a++) {
    r = await fetch(ETSY_API + path, Object.assign({}, init, { headers }));
    if (r.status !== 429) return r;
    await new Promise(res => setTimeout(res, 1200 * (a + 1)));
  }
  return r;
}

// ---------- Taxonomy search ----------
let TAX_CACHE = null;
async function taxonomy(url, env) {
  if (!TAX_CACHE) {
    const r = await etsyFetch(env, null, '/application/seller-taxonomy/nodes');
    const d = await r.json();
    const flat = [];
    (function walk(nodes, path) {
      for (const n of nodes || []) {
        const p = path.concat(n.name);
        flat.push({ id: n.id, path: p.join(' > ') });
        walk(n.children, p);
      }
    })(d.results, []);
    TAX_CACHE = flat;
  }
  const q = (url.searchParams.get('q') || '').toLowerCase();
  return json({ results: TAX_CACHE.filter(n => n.path.toLowerCase().includes(q)).slice(0, 60) });
}

// ---------- Create one listing ----------
// multipart form: meta (JSON), image0..image9 (files), file0..file4 (files)
async function createListing(req, env, sess) {
  const form = await req.formData();
  const meta = JSON.parse(form.get('meta'));
  const shop = sess.shop_id;
  const steps = [];

  // 1. Draft listing
  const body = new URLSearchParams();
  body.set('quantity', String(meta.quantity || 999));
  body.set('title', meta.title);
  body.set('description', meta.description);
  body.set('price', Number(meta.price).toFixed(2));
  body.set('who_made', 'i_did');
  body.set('when_made', meta.when_made || '2020_2026');
  body.set('is_supply', 'false');
  body.set('taxonomy_id', String(meta.taxonomy_id));
  body.set('type', 'download');
  body.set('should_auto_renew', 'false');
  body.set('is_taxable', 'true');
  (meta.tags || []).slice(0, 13).forEach(t => body.append('tags[]', t));
  if (meta.shop_section_id) body.set('shop_section_id', String(meta.shop_section_id));
  let r = await etsyFetch(env, sess.access, `/application/shops/${shop}/listings`, {
    method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body });
  let d = await r.json();
  if (!r.ok) return json({ ok: false, step: 'create', status: r.status, error: d }, 400);
  const listingId = d.listing_id;
  steps.push('draft ' + listingId);

  // 2. Images
  for (let i = 0; i < 10; i++) {
    const img = form.get('image' + i);
    if (!img) continue;
    const fd = new FormData();
    fd.append('image', img, img.name);
    fd.append('rank', String(i + 1));
    r = await etsyFetch(env, sess.access, `/application/shops/${shop}/listings/${listingId}/images`, { method: 'POST', body: fd });
    if (!r.ok) return json({ ok: false, listing_id: listingId, step: 'image' + i, status: r.status, error: await r.text() }, 400);
    steps.push('image ' + (i + 1));
  }

  // 3. Digital files
  for (let i = 0; i < 5; i++) {
    const f = form.get('file' + i);
    if (!f) continue;
    const fd = new FormData();
    fd.append('file', f, f.name);
    fd.append('name', f.name);
    fd.append('rank', String(i + 1));
    r = await etsyFetch(env, sess.access, `/application/shops/${shop}/listings/${listingId}/files`, { method: 'POST', body: fd });
    if (!r.ok) return json({ ok: false, listing_id: listingId, step: 'file' + i, status: r.status, error: await r.text() }, 400);
    steps.push('file ' + (i + 1));
  }

  // 4. Make sure it is a download listing, auto-renew off, and publish if asked
  const upd = new URLSearchParams({ type: 'download', should_auto_renew: 'false' });
  if (meta.publish) upd.set('state', 'active');
  r = await etsyFetch(env, sess.access, `/application/shops/${shop}/listings/${listingId}`, {
    method: 'PATCH', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: upd });
  if (!r.ok) return json({ ok: false, listing_id: listingId, step: 'update', status: r.status, error: await r.text() }, 400);
  steps.push(meta.publish ? 'published' : 'left as draft');
  return json({ ok: true, listing_id: listingId, sku: meta.sku, steps });
}

// Replace the digital files on an EXISTING listing (draft or active). Never changes state, price, text or photos.
// Order: read current files, delete them, upload the new ones (Etsy allows 5 files, so delete comes first).
async function replaceFiles(req, env, sess) {
  const form = await req.formData();
  const listingId = String(form.get('listing_id') || '').replace(/[^0-9]/g, '');
  if (!listingId) return json({ ok: false, step: 'input', error: 'listing_id missing' }, 400);
  const shop = sess.shop_id;
  const steps = [];
  const news = [];
  for (let i = 0; i < 5; i++) { const f = form.get('file' + i); if (f) news.push(f); }
  if (!news.length) return json({ ok: false, step: 'input', error: 'no files sent' }, 400);
  let r = await etsyFetch(env, sess.access, `/application/listings/${listingId}`);
  let d = await r.json();
  if (!r.ok) return json({ ok: false, listing_id: listingId, step: 'read', status: r.status, error: d }, 400);
  if (String(d.shop_id) !== String(shop)) return json({ ok: false, listing_id: listingId, step: 'read', error: 'listing is not in this shop' }, 400);
  steps.push('state ' + d.state);
  r = await etsyFetch(env, sess.access, `/application/shops/${shop}/listings/${listingId}/files`);
  d = await r.json();
  if (!r.ok) return json({ ok: false, listing_id: listingId, step: 'list', status: r.status, error: d }, 400);
  for (const old of (d.results || [])) {
    r = await etsyFetch(env, sess.access, `/application/shops/${shop}/listings/${listingId}/files/${old.listing_file_id}`, { method: 'DELETE' });
    if (!r.ok && r.status !== 404) return json({ ok: false, listing_id: listingId, step: 'delete ' + old.filename, status: r.status, error: await r.text() }, 400);
    steps.push('removed ' + old.filename);
  }
  for (let i = 0; i < news.length; i++) {
    const f = news[i];
    const fd = new FormData();
    fd.append('file', f, f.name);
    fd.append('name', f.name);
    fd.append('rank', String(i + 1));
    r = await etsyFetch(env, sess.access, `/application/shops/${shop}/listings/${listingId}/files`, { method: 'POST', body: fd });
    if (!r.ok) return json({ ok: false, listing_id: listingId, step: 'upload ' + f.name, status: r.status, error: await r.text() }, 400);
    steps.push('added ' + f.name);
  }
  return json({ ok: true, listing_id: listingId, steps });
}

// Change ONLY the tags on an EXISTING listing. Never creates a listing, never changes state, price, text, photos or files.
async function updateTags(req, env, sess) {
  const body = await req.json();
  const listingId = String(body.listing_id || '').replace(/[^0-9]/g, '');
  const tags = (body.tags || []).map(t => String(t).trim().toLowerCase()).filter(Boolean);
  if (!listingId) return json({ ok: false, step: 'input', error: 'listing_id missing' }, 400);
  if (!tags.length || tags.length > 13 || tags.some(t => t.length > 20)) return json({ ok: false, step: 'input', error: 'need 1 to 13 tags, 20 characters max each' }, 400);
  const shop = sess.shop_id;
  let r = await etsyFetch(env, sess.access, `/application/listings/${listingId}`);
  let d = await r.json();
  if (!r.ok) return json({ ok: false, listing_id: listingId, step: 'read', status: r.status, error: d }, 400);
  if (String(d.shop_id) !== String(shop)) return json({ ok: false, listing_id: listingId, step: 'read', error: 'listing is not in this shop' }, 400);
  const before = d.tags || [];
  r = await etsyFetch(env, sess.access, `/application/shops/${shop}/listings/${listingId}`, {
    method: 'PATCH', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams({ tags: tags.join(',') }) });
  d = await r.json();
  if (!r.ok) return json({ ok: false, listing_id: listingId, step: 'update', status: r.status, error: d }, 400);
  return json({ ok: true, listing_id: listingId, state: d.state, before, after: d.tags });
}

// ---------- helpers ----------
function json(o, status = 200, extra = {}) {
  return new Response(JSON.stringify(o), { status, headers: Object.assign({ 'Content-Type': 'application/json' }, extra) });
}
function html(s, status = 200) {
  return new Response(s, { status, headers: { 'Content-Type': 'text/html; charset=utf-8' } });
}
function escapeHtml(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }
function msgPage(m) { return `<!doctype html><meta name=viewport content="width=device-width,initial-scale=1"><body style="font:17px system-ui;padding:30px;max-width:640px;margin:auto"><h2>GS Etsy Uploader</h2><p>${m}</p><p><a href="/">Back</a></p></body>`; }

const PAGE = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GS Etsy Uploader</title>
<style>
:root{--bg:#0d1326;--panel:#151d38;--line:#2a3663;--text:#e8ecf8;--muted:#9aa6c8;--accent:#8fb4ff;--ok:#3ddc97;--bad:#ff7a7a}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif}
.w{max-width:820px;margin:0 auto;padding:24px 16px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px;margin:14px 0}
h1{font-size:1.5rem;margin:0 0 4px} h2{font-size:1.1rem;margin:0 0 8px}
.muted{color:var(--muted)} .btn{display:inline-block;background:linear-gradient(135deg,#8fb4ff,#b79cff);color:#0d1326;border:0;border-radius:10px;padding:11px 18px;font-weight:700;cursor:pointer;text-decoration:none}
.btn.ghost{background:#1b2546;color:var(--text);border:1px solid var(--line)} .btn:disabled{opacity:.5;cursor:default}
input[type=text]{width:100%;box-sizing:border-box;background:#0d1326;color:var(--text);border:1px solid var(--line);border-radius:8px;padding:9px}
label{display:block;margin:10px 0 4px;font-weight:600}
#log{background:#0a0f1f;border:1px solid var(--line);border-radius:10px;padding:10px;max-height:340px;overflow:auto;font:13px/1.45 ui-monospace,Consolas,monospace;white-space:pre-wrap}
.ok{color:var(--ok)} .bad{color:var(--bad)} .row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
</style></head><body><div class="w">
<h1>GS Etsy Uploader</h1><p class="muted">Turns Glamourless Systems upload packages into Etsy listings. Auto-renew is always off.</p>
<div class="card" id="conn"><h2>Step 1. Connect your Etsy shop</h2><p id="connText" class="muted">Checking...</p>
<a class="btn" id="connectBtn" href="/connect" style="display:none">Connect to Etsy</a></div>
<div class="card"><h2>Step 2. Pick the upload folder</h2>
<p class="muted">Click the button. Go to the G: drive, open My Drive, and open Glamourless Systems Main, and choose the folder named <b>GS Etsy Upload Packages</b> (not the whole Glamourless Systems Main folder, which is far too big). Then click Upload when the browser asks. Nothing is sent until you press an upload button below.</p>
<input type="file" id="folder" webkitdirectory directory multiple style="display:none">
<button class="btn ghost" id="pick">Choose folder</button> <span id="picked" class="muted"></span></div>
<div class="card"><h2>Step 3. Upload</h2>
<label>Etsy category ID</label><input type="text" id="tax" placeholder="Filled in by Claude">
<div class="row" style="margin-top:12px">
<button class="btn" id="test" disabled>Test: first 3 as drafts</button>
<button class="btn ghost" id="all" disabled>Upload all as drafts</button>
<button class="btn ghost" id="pub" disabled>Upload all and publish</button></div>
<p class="muted" style="margin-top:10px">Already-uploaded items are skipped automatically, so you can stop and start again safely.</p></div>
<div class="card"><h2>Step 4. Replace fixed files</h2>
<p class="muted">Swaps in corrected files on listings that were already uploaded. It only changes the download files. Prices, titles, photos and draft or live status stay exactly as they are.</p>
<button class="btn ghost" id="repl" disabled>Replace fixed files</button> <span id="replInfo" class="muted"></span></div>
<div class="card"><h2>Step 5. Update tags</h2>
<p class="muted">Changes only the 13 search tags on listings that already exist. It never creates a listing, so no duplicates.</p>
<button class="btn ghost" id="tagb" disabled>Update tags</button> <span id="tagInfo" class="muted"></span></div>
<div class="card"><h2>Progress</h2><div id="log">Nothing yet.</div>
<div class="row" style="margin-top:10px"><button class="btn ghost" id="save">Save results file</button></div></div>
</div>
<script>
var files=[],manifest=null,results=[],logEl=document.getElementById('log');
function log(t,c){if(logEl.textContent==='Nothing yet.')logEl.textContent='';var s=document.createElement('div');if(c)s.className=c;s.textContent=t;logEl.appendChild(s);logEl.scrollTop=1e9}
var done={};try{done=JSON.parse(localStorage.getItem('gs_etsy_done')||'{}')}catch(e){}
try{var tx=localStorage.getItem('gs_etsy_tax');if(tx)document.getElementById('tax').value=tx}catch(e){}
fetch('/api/status').then(r=>r.json()).then(s=>{var t=document.getElementById('connText');if(s.ok){t.innerHTML='Connected to <b>'+s.shop_name+'</b>.';t.className='ok'}else{t.textContent='Not connected yet.';document.getElementById('connectBtn').style.display='inline-block'}});
document.getElementById('pick').onclick=()=>document.getElementById('folder').click();
document.getElementById('folder').onchange=async e=>{files=[...e.target.files];var m=files.find(f=>/GS Etsy Upload Packages\\/manifest\\.json$/i.test((f.webkitRelativePath||'').replace(/\\\\/g,'/')));if(!m){document.getElementById('picked').textContent='No manifest.json in that folder.';return}
manifest=JSON.parse(await m.text());document.getElementById('picked').textContent=manifest.items.length+' listings found ('+Object.keys(done).length+' already uploaded)';
if(manifest.taxonomy_id&&!document.getElementById('tax').value)document.getElementById('tax').value=manifest.taxonomy_id;
['test','all','pub'].forEach(id=>document.getElementById(id).disabled=false);
var rl=manifest.replace_files||[],rv=manifest.replace_version||'';var todo=rl.filter(k=>replaced[k]!==rv);
document.getElementById('replInfo').textContent=rl.length?(todo.length+' of '+rl.length+' listings need new files'):'Nothing to replace';
document.getElementById('repl').disabled=!todo.length;
var tl=manifest.update_tags||[],tv=manifest.tags_version||'';var tt=tl.filter(k=>tagged[k]!==tv);
document.getElementById('tagInfo').textContent=tl.length?(tt.length+' of '+tl.length+' listings need new tags'):'No tag changes';
document.getElementById('tagb').disabled=!tt.length};
var replaced={};try{replaced=JSON.parse(localStorage.getItem('gs_etsy_replaced')||'{}')}catch(e){}
async function replaceRun(){var rl=manifest.replace_files||[],rv=manifest.replace_version||'';document.getElementById('repl').disabled=true;
for(const key of rl){if(replaced[key]===rv)continue;var it=manifest.items.find(x=>x.key===key);var lid=done[key];
if(!it){log('Replace '+key+': not in manifest. Skipped.','bad');continue}
if(!lid){log('Replace '+key+': never uploaded, so nothing to replace. Skipped.','bad');continue}
log('Replacing files on '+key+' (listing '+lid+') ...');var fd=new FormData();fd.append('listing_id',String(lid));var missing=null;
(it.files||[]).forEach((p,i)=>{var f=fileFor(p);if(f)fd.append('file'+i,f,f.name);else missing=p});
if(missing){log('  Missing file: '+missing+'. Skipped.','bad');continue}
try{var r=await fetch('/api/replace-files',{method:'POST',body:fd});var d=await r.json();results.push(Object.assign({key:key,replace:true},d));
if(d.ok){replaced[key]=rv;try{localStorage.setItem('gs_etsy_replaced',JSON.stringify(replaced))}catch(e){};log('  Done ('+d.steps.join(', ')+')','ok')}
else{log('  Problem at '+d.step+': '+JSON.stringify(d.error).slice(0,300),'bad');if(r.status===401){log('Connection expired. Click Connect to Etsy again.','bad');break}}}
catch(e){log('  Network problem: '+e.message,'bad')}}
log('Finished replacing files.');document.getElementById('repl').disabled=false}
document.getElementById('repl').onclick=()=>replaceRun();
var tagged={};try{tagged=JSON.parse(localStorage.getItem('gs_etsy_tagged')||'{}')}catch(e){}
async function tagRun(){var tl=manifest.update_tags||[],tv=manifest.tags_version||'';document.getElementById('tagb').disabled=true;var n=0;
for(const key of tl){if(tagged[key]===tv)continue;var it=manifest.items.find(x=>x.key===key);var lid=done[key];
if(!it||!lid){log('Tags '+key+': no existing listing. Skipped (nothing is created).','bad');continue}
try{var r=await fetch('/api/update-tags',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({listing_id:lid,tags:it.tags})});var d=await r.json();results.push(Object.assign({key:key,tags:true},d));
if(d.ok){tagged[key]=tv;n++;try{localStorage.setItem('gs_etsy_tagged',JSON.stringify(tagged))}catch(e){};if(n%25===0)log('  '+n+' listings retagged ...','ok')}
else{log('Tags '+key+': problem at '+d.step+': '+JSON.stringify(d.error).slice(0,200),'bad');if(r.status===401){log('Connection expired. Click Connect to Etsy again.','bad');break}}}
catch(e){log('Tags '+key+': network problem: '+e.message,'bad')}}
log('Finished updating tags: '+n+' listings.');document.getElementById('tagb').disabled=false}
document.getElementById('tagb').onclick=()=>tagRun();
function fileFor(rel){return files.find(f=>(f.webkitRelativePath||f.name).replace(/\\\\/g,'/').endsWith('/'+rel))}
async function run(limit,publish){var tax=document.getElementById('tax').value.trim();if(!tax){alert('Category ID is empty.');return}try{localStorage.setItem('gs_etsy_tax',tax)}catch(e){}
['test','all','pub'].forEach(id=>document.getElementById(id).disabled=true);var n=0;
for(const it of manifest.items){if(done[it.key])continue;if(limit&&n>=limit)break;n++;
log('Uploading '+it.key+' '+it.title.slice(0,60)+' ...');var fd=new FormData();
fd.append('meta',JSON.stringify(Object.assign({},it,{taxonomy_id:+tax,publish:!!publish})));
var missing=null;(it.images||[]).forEach((p,i)=>{var f=fileFor(p);if(f)fd.append('image'+i,f,f.name);else missing=p});
(it.files||[]).forEach((p,i)=>{var f=fileFor(p);if(f)fd.append('file'+i,f,f.name);else missing=p});
if(missing){log('  Missing file: '+missing+'. Skipped.','bad');results.push({key:it.key,ok:false,error:'missing '+missing});continue}
try{var r=await fetch('/api/listing',{method:'POST',body:fd});var d=await r.json();results.push(Object.assign({key:it.key},d));
if(d.ok){done[it.key]=d.listing_id;try{localStorage.setItem('gs_etsy_done',JSON.stringify(done))}catch(e){};log('  Done: listing '+d.listing_id+' ('+d.steps.join(', ')+')','ok')}
else{log('  Problem at '+d.step+': '+JSON.stringify(d.error).slice(0,300),'bad');if(r.status===401){log('Connection expired. Click Connect to Etsy again.','bad');break}}}
catch(e){log('  Network problem: '+e.message,'bad');results.push({key:it.key,ok:false,error:e.message})}}
log('Finished this run.');['test','all','pub'].forEach(id=>document.getElementById(id).disabled=false)}
document.getElementById('test').onclick=()=>run(3,false);
document.getElementById('all').onclick=()=>run(0,false);
document.getElementById('pub').onclick=()=>{if(confirm('Publish every remaining listing live on Etsy? Each one costs 20 cents.'))run(0,true)};
document.getElementById('save').onclick=()=>{var b=new Blob([JSON.stringify({done,results},null,2)],{type:'application/json'});var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='GS Etsy Upload Results.json';a.click()};
</script></body></html>`;
