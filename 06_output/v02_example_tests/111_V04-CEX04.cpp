#include <bits/stdc++.h>
using namespace std;


struct DSU{ vector<int> fa,sz; DSU(int n=0){fa.resize(n+1);sz.assign(n+1,1);iota(fa.begin(),fa.end(),0);} int find(int x){while(x!=fa[x]){fa[x]=fa[fa[x]];x=fa[x];}return x;} bool unite(int a,int b){a=find(a);b=find(b);if(a==b)return false;if(sz[a]<sz[b])swap(a,b);fa[b]=a;sz[a]+=sz[b];return true;} };
int main(){ ios::sync_with_stdio(false); cin.tie(nullptr); int n,m; cin>>n>>m; vector<pair<int,int>> e(m+1); for(int i=1;i<=m;i++)cin>>e[i].first>>e[i].second; int q; cin>>q; vector<int> del(q+1),ban(m+1); for(int i=1;i<=q;i++){cin>>del[i];ban[del[i]]=1;} DSU d(n); int comp=n; for(int i=1;i<=m;i++)if(!ban[i]&&d.unite(e[i].first,e[i].second))comp--; vector<int> ans(q+1); for(int i=q;i>=1;i--){ans[i]=comp; if(d.unite(e[del[i]].first,e[del[i]].second))comp--;} for(int i=1;i<=q;i++)cout<<ans[i]<<"\n"; return 0; }
