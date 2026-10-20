import json,os,html,shutil,glob,urllib.parse
D=json.load(open("data/hadiths.json",encoding="utf-8"))
C=json.load(open("data/categories.json",encoding="utf-8"))
G=json.load(open("data/config.json",encoding="utf-8"))
B=G["base_url"].rstrip("/");N=G["site_name"];O="docs"
shutil.rmtree(O,ignore_errors=True);os.makedirs(O+"/h");os.makedirs(O+"/c")
e=html.escape
CSS="""body{font-family:system-ui,'Noto Naskh Arabic',serif;max-width:760px;margin:0 auto;padding:12px;background:#f7f5ef;color:#1d2b24;line-height:1.8}
a{color:#1f6f4a}.card{background:#fff;border:1px solid #ddd8c8;border-radius:12px;padding:10px 14px;margin:10px 0}
.ar{font-size:1.4rem;direction:rtl;text-align:right}.ps{direction:rtl;text-align:right}.ref{color:#6b7a72;font-size:.9rem}
.tag{display:inline-block;border:1px solid #ddd8c8;border-radius:99px;padding:2px 12px;margin:3px;text-decoration:none;background:#fff}
input{width:100%;padding:8px;border:1px solid #ddd8c8;border-radius:10px;font:inherit}
@media(prefers-color-scheme:dark){body{background:#121a16;color:#e8efe9}.card,.tag,input{background:#1b2620;color:#e8efe9;border-color:#2c3b33}a{color:#4fb985}}"""
def page(path,title,desc,body,up=""):
 open(f"{O}/{path}","w",encoding="utf-8").write(f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(desc[:155])}"><link rel="canonical" href="{B}/{path}"><style>{CSS}</style></head><body><h2><a href="{up}index.html" style="text-decoration:none">☪ {e(N)}</a></h2>{body}</body></html>""")
def cname(k):
 c=C.get(k,{});return " · ".join(x for x in (c.get("en",k),c.get("ps"),c.get("ar")) if x)
def ask(h):
 q="Please explain this hadith ("+h.get("ref","")+"): "+h.get("ar","")+" "+h.get("en","")+" . Explain the meaning and mention scholarly sources."
 return "https://claude.ai/new?q="+urllib.parse.quote(q)
def card(h,up=""):
 s=f'<div class="card" data-s="{e(json.dumps(h,ensure_ascii=False).lower())}">'
 if h.get("ar"):s+=f'<div class="ar">{e(h["ar"])}</div>'
 if h.get("ps"):s+=f'<div class="ps">{e(h["ps"])}</div>'
 if h.get("en"):s+=f'<div>{e(h["en"])}</div>'
 s+=f'<div class="ref">📖 {e(h.get("ref",""))} · <a href="{up}h/{e(h["id"])}.html">link</a> · <a href="{up}c/{e(h["category"])}.html">{e(C.get(h["category"],{}).get("en",h["category"]))}</a> · <a href="{ask(h)}" target="_blank" rel="noopener">🤖 Ask AI</a></div></div>'
 return s
urls=[""]
for h in D:
 t=h.get("en") or h.get("ar","")
 page(f"h/{h['id']}.html",f"{t[:60]} - {h.get('ref','')}",t,card(h,"../")+f'<p><a href="../index.html">← All</a></p>',"../");urls.append(f"h/{h['id']}.html")
for k in C:
 hs=[h for h in D if h["category"]==k]
 page(f"c/{k}.html",f"{C[k].get('en',k)} - hadith",f"Hadith about {C[k].get('en',k)}","<h3>"+e(cname(k))+"</h3>"+"".join(card(h,"../") for h in hs),"../");urls.append(f"c/{k}.html")
tags="".join(f'<a class="tag" href="c/{k}.html">{e(cname(k))}</a>' for k in C)
js="<script>document.getElementById('q').oninput=function(){var v=this.value.toLowerCase();document.querySelectorAll('.card').forEach(function(c){c.style.display=c.dataset.s.indexOf(v)<0?'none':''})}</script>"
page("index.html",N,"Hadith of Prophet Muhammad ﷺ in Arabic, Pashto and English with references.",f'<p>Hadith of Prophet Muhammad ﷺ · احادیث شریف · الأحاديث النبوية</p><p>📚 <b>{len(D)}</b> Hadith · حدیث · حديث</p><p class="ref">🤖 AI can make mistakes. For religious rulings, ask a qualified scholar. · د AI ځوابونه ممکن تېروتنه ولري، د شرعي حکمونو لپاره عالم ته مراجعه وکړئ. · قد يخطئ الذكاء الاصطناعي، وللأحكام الشرعية اسأل عالمًا.</p><input id="q" placeholder="Search / لټون / بحث">'+tags+"".join(card(h) for h in D)+js)
open(O+"/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{B}/{u}</loc></url>" for u in urls)+"</urlset>")
open(O+"/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {B}/sitemap.xml\n")
print("built",len(D),"hadiths")
[shutil.copy(f,O) for f in glob.glob("google*.html")] 
