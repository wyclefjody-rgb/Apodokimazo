import sys as _sys
for _s in (_sys.stdout, _sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
import os, json, numpy as np
from collections import Counter
from load import load, GROUP
from analysis_helpers import freq_matrix, delta
from scipy.spatial.distance import cdist
rng=np.random.default_rng(1)
bk=load("book")
big=[b for b,t in bk.items() if len(t)>=4000]
out={"books":big,"curve":[]}
for S in [150,250,400,500,750,1000,1500,2000]:
    acc=[]
    for rep in range(40):
        refs={}; tests={}
        for b in big:
            t=bk[b]; h=len(t)//2
            # alternate which half is reference to avoid position effects
            ref,rest=(t[:h],t[h:]) if rep%2==0 else (t[h:],t[:h])
            refs[b]=ref
            o=rng.integers(0,len(rest)-S+1); tests[b]=rest[o:o+S]
        allt={**{("R",k):v for k,v in refs.items()},**{("T",k):v for k,v in tests.items()}}
        lab,X,_=freq_matrix({i:v for i,v in enumerate(allt.values())},100)
        import os
        Z=np.sqrt(X) if os.environ.get("DIST","simple")=="simple" else (X-X.mean(0))/(X.std(0)+1e-12)
        n=len(big); Zr,Zt=Z[:n],Z[n:]
        D=cdist(Zt,Zr,"cityblock")
        acc.append(np.mean(D.argmin(1)==np.arange(n)))
    out["curve"].append({"size":S,"acc":float(np.mean(acc)),"sd":float(np.std(acc))})
out["chance"]=1/len(big)
ch=load("chapter")
from analysis_helpers import cluster
from scipy.cluster.hierarchy import fcluster
la2={l:v for l,v in ch.items() if l.split()[0] in ("Lk","Ac")}
lb,Db,Lb=cluster(la2); cb=fcluster(Lb,2,"maxclust")
out["luke_with_acts"]=[l for l,c in zip(lb,cb) if l.startswith("Lk") and c==cb[lb.index("Ac 1")]]
json.dump(out,open(f"chunk_{os.environ.get('DIST','simple')}.json","w",encoding="utf8"),indent=1); print(json.dumps(out,indent=1))
