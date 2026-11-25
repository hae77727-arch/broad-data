import json, os, urllib.request as u
B="https://iptv-org.github.io/api/"
get=lambda f: json.load(u.urlopen(B+f))
ch={c["id"]:c for c in get("channels.json")
    if not c.get("closed") and not c.get("is_nsfw")}
out={}; allc=[]; seen=set()
for s in get("streams.json"):
    c=ch.get(s["channel"])
    if not c or s["url"] in seen: continue
    seen.add(s["url"])
    cc=c["country"].lower()
    cat=(c.get("categories") or ["general"])[0]
    out.setdefault(cc,[]).append(
      {"n":c["name"],"u":s["url"],"l":c.get("logo"),"c":cat})
    allc.append({"n":c["name"],"u":s["url"],"c":cat,"cc":cc})
os.makedirs("data/tv",exist_ok=True)
w=lambda p,d: json.dump(d,open(p,"w"),separators=(",",":"),ensure_ascii=False)
index=[]
for cc,L in out.items():
    w(f"data/tv/{cc}.json",L)
    index.append({"code":cc,"count":len(L)})
w("data/tv-index.json",index)
w("data/search.json",allc)
w("data/countries.json",[{"code":c["code"],"name":c["name"]} for c in get("countries.json")])
