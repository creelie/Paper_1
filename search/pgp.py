import itertools, sys, numpy as np, time
sys.setrecursionlimit(100000)
def pgprime(p):
    pts=[]
    for v in itertools.product(range(p),repeat=3):
        if v==(0,0,0): continue
        i=next(j for j in range(3) if v[j]); inv=pow(v[i],-1,p)
        w=tuple(inv*c%p for c in v)
        if w not in pts: pts.append(w)
    return [[1 if sum(a*b for a,b in zip(P,L))%p==0 else 0 for L in pts] for P in pts]
def rankp(M,p):
    M=[r[:] for r in M]; r=0
    for c in range(len(M[0])):
        piv=next((i for i in range(r,len(M)) if M[i][c]%p),None)
        if piv is None: continue
        M[r],M[piv]=M[piv],M[r]; inv=pow(M[r][c],-1,p)
        M[r]=[x*inv%p for x in M[r]]
        for i in range(len(M)):
            if i!=r and M[i][c]%p:
                f=M[i][c]; M[i]=[(a-f*b)%p for a,b in zip(M[i],M[r])]
        r+=1
    return r
def gcov(rows,limit=5e7):
    memo={}
    def f(D):
        if D in memo: return memo[D]
        b=0
        for r in rows:
            if r&~D:
                x=1+f(D|r)
                if x>b:b=x
        memo[D]=b
        if len(memo)>limit: raise Exception('limit')
        return b
    return f(0),len(memo)
if __name__=="__main__":
 for p in [3,5]:
    N=pgprime(p); k=len(N); rows=[sum(1<<j for j in range(k) if N[i][j]) for i in range(k)]
    t=time.time(); print(p,k,'p-rank',rankp(N,p),'gcov',gcov(rows),round(time.time()-t,1),flush=True)
    