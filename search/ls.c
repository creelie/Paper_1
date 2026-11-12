// randomized greedy for long legal (closed) sequences. stdin: blocks "n target\n" then n lines of adjacency bitstrings. prints best and whether > target.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static uint64_t s=88172645463325252ULL; static inline uint64_t rnd(){s^=s<<13;s^=s>>7;s^=s<<17;return s;}
static int pc(u128 x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
int main(int argc,char**argv){int tries=atoi(argv[1]);int K=atoi(argv[2]),R=atoi(argv[3]);int n,target;char buf[200];int id=0;
 while(scanf("%d %d",&n,&target)==2){u128 nb[128];for(int i=0;i<n;i++){scanf("%s",buf);nb[i]=0;for(int j=0;j<n;j++)if(buf[j]=='1')nb[i]|=(u128)1<<j;nb[i]|=(u128)1<<i;}
  if(id%K!=R){id++;continue;} int best=0;int seqb[128];
  for(int t=0;t<tries&&best<=target;t++){u128 D=0;int L=0;int seq[128];int slack=rnd()%3;
   while(1){int m=1000;int c[128],nc=0;for(int v=0;v<n;v++){int k=pc(nb[v]&~D);if(k&&k<m)m=k;}
    if(m==1000)break;for(int v=0;v<n;v++){int k=pc(nb[v]&~D);if(k&&k<=m+(int)(rnd()%(slack+1)))c[nc++]=v;}
    int v=c[rnd()%nc];seq[L++]=v;D|=nb[v];}
   if(L>best){best=L;for(int i=0;i<L;i++)seqb[i]=seq[i];}}
  printf("%d %d %d %s",id++,best,target,best>target?"FOUND":"no");if(best>target){printf(" seq");for(int i=0;i<best;i++)printf(" %d",seqb[i]);}printf("\n");fflush(stdout);}
 return 0;}
