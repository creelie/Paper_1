// Exact Grundy domination (closed, mode 'c') or Grundy total domination (open, mode 't').
// Input: n m mode, then m edges (0-based). Output: value and a witness sequence.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int n; static u128 nb[128];
#define HB 26
static u128 *keys; static signed char *vals; static uint64_t hmask, used=0;
static uint64_t hsh(u128 x){uint64_t a=(uint64_t)x,b=(uint64_t)(x>>64);a^=b*0x9E3779B97F4A7C15ULL;a^=a>>29;a*=0xBF58476D1CE4E5B9ULL;a^=a>>32;return a;}
static int look(u128 k){uint64_t h=hsh(k)&hmask;while(vals[h]>=0){if(keys[h]==k)return vals[h];h=(h+1)&hmask;}return -1;}
static void put(u128 k,int v){uint64_t h=hsh(k)&hmask;while(vals[h]>=0){if(keys[h]==k){vals[h]=v;return;}h=(h+1)&hmask;}keys[h]=k;vals[h]=v;used++;
 if(used*2>hmask){fprintf(stderr,"table full\n");exit(2);}}
static int f(u128 D){
  int r=look(D); if(r>=0) return r;
  int best=0;
  // pruning: upper bound = number of undominated vertices
  for(int v=0;v<n;v++){ u128 nw=nb[v]&~D; if(nw){ int x=1+f(D|nw); if(x>best)best=x; } }
  put(D,best); return best;
}
int main(int argc,char**argv){
  int m; char mode; if(scanf("%d %d %c",&n,&m,&mode)!=3)return 1;
  for(int i=0;i<n;i++) nb[i]= (mode=='c')? ((u128)1<<i):0;
  for(int i=0;i<m;i++){int a,b;scanf("%d %d",&a,&b);nb[a]|=(u128)1<<b;nb[b]|=(u128)1<<a;}
  int hb=HB; if(argc>1) hb=atoi(argv[1]);
  hmask=((uint64_t)1<<hb)-1; keys=malloc(sizeof(u128)<<hb); vals=malloc((size_t)1<<hb); memset(vals,-1,(size_t)1<<hb);
  int val=f(0); printf("%d",val);
  // witness
  u128 D=0; printf(" seq:");
  while(1){int bv=-1;for(int v=0;v<n;v++){u128 nw=nb[v]&~D;if(nw&&1+f(D|nw)==f(D)){bv=v;break;}} if(bv<0)break; printf(" %d",bv); D|=nb[bv]&~D; D|=nb[bv];}
  printf(" states:%llu\n",(unsigned long long)used); return 0;}
