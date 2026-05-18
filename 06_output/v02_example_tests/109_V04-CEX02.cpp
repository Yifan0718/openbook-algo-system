#include <bits/stdc++.h>
using namespace std;


const int MAXN=200005;
long long tree[MAXN*4], lazyv[MAXN*4];
void push(int p,int l,int r){ if(!lazyv[p])return; int m=(l+r)/2; long long v=lazyv[p]; tree[p*2]+=v*(m-l+1); tree[p*2+1]+=v*(r-m); lazyv[p*2]+=v; lazyv[p*2+1]+=v; lazyv[p]=0; }
void add(int p,int l,int r,int ql,int qr,long long v){ if(ql<=l&&r<=qr){tree[p]+=v*(r-l+1); lazyv[p]+=v; return;} push(p,l,r); int m=(l+r)/2; if(ql<=m)add(p*2,l,m,ql,qr,v); if(qr>m)add(p*2+1,m+1,r,ql,qr,v); tree[p]=tree[p*2]+tree[p*2+1]; }
long long query(int p,int l,int r,int ql,int qr){ if(ql<=l&&r<=qr)return tree[p]; push(p,l,r); int m=(l+r)/2; long long ans=0; if(ql<=m)ans+=query(p*2,l,m,ql,qr); if(qr>m)ans+=query(p*2+1,m+1,r,ql,qr); return ans; }
int main(){ ios::sync_with_stdio(false); cin.tie(nullptr); int n,q; cin>>n>>q; while(q--){int op,l,r; long long v; cin>>op>>l>>r; if(op==1){cin>>v; add(1,1,n,l,r,v);} else cout<<query(1,1,n,l,r)<<"\n";} return 0; }
