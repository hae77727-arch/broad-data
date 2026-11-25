import json, os, urllib.request as u
B="https://iptv-org.github.io/api/"
get=lambda f: json.load(u.urlopen(B+f))
ch={c["id"]:c for c in get("channels.json")
    if not c.get("closed") and not c.get("is_nsfw")}
out={}
for s in get("streams.json"):
    c=ch.get(s["channel"])
    if not c: continue
    out.setdefault(c["country"].lower(),[]).append(
      {"n":c["name"],"u":s["url"],"l":c.get("logo"),
       "c":(c.get("categories") or ["general"])[0]})
os.makedirs("data/tv",exist_ok=True)
index=[]
for cc,L in out.items():
    json.dump(L,open(f"data/tv/{cc}.json","w"),
              separators=(",",":"),ensure_ascii=False)
    index.append({"code":cc,"count":len(L)})
json.dump(index,open("data/tv-index.json","w"))
