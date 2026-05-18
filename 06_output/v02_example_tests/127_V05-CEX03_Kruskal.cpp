#include <bits/stdc++.h>
using namespace std;


struct DSU{vector<int>f;DSU(int n){f.resize(n+1);iota(f.begin(),f.end(),0);}int find(int x){return x==f[x]?x:f[x]=find(f[x]);}bool unite(int a,int b){a=find(a);b=find(b);if(a==b)return false;f[b]=a;return true;}};
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,m;cin>>n>>m; struct E{int u,v,w;}; vector<E>e(m); for(auto &x:e)cin>>x.u>>x.v>>x.w; sort(e.begin(),e.end(),[](E a,E b){return a.w<b.w;}); DSU d(n); long long ans=0;int cnt=0,last=0; for(auto x:e)if(d.unite(x.u,x.v)){ans+=x.w;cnt++;last=x.w;} if(cnt<n-1)cout<<"orz\n"; else cout<<ans<<" "<<last<<"\n"; return 0;}
