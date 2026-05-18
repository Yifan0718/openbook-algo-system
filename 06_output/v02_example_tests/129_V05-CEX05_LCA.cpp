#include <bits/stdc++.h>
using namespace std;


const int LOG=20;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,q;cin>>n>>q; vector<vector<pair<int,int>>>g(n+1); for(int i=1;i<n;i++){int u,v,w;cin>>u>>v>>w;g[u].push_back({v,w});g[v].push_back({u,w});} vector<array<int,LOG>>up(n+1),mn(n+1); vector<int>dep(n+1); function<void(int,int)>dfs=[&](int u,int p){up[u][0]=p; for(int k=1;k<LOG;k++){up[u][k]=up[up[u][k-1]][k-1];mn[u][k]=min(mn[u][k-1],mn[up[u][k-1]][k-1]);} for(auto [v,w]:g[u])if(v!=p){dep[v]=dep[u]+1;mn[v][0]=w;dfs(v,u);}}; for(int k=0;k<LOG;k++)mn[1][k]=1e9; dfs(1,1); while(q--){int a,b;cin>>a>>b;int ans=1e9;if(dep[a]<dep[b])swap(a,b);int diff=dep[a]-dep[b];for(int k=0;k<LOG;k++)if(diff>>k&1){ans=min(ans,mn[a][k]);a=up[a][k];} if(a!=b){for(int k=LOG-1;k>=0;k--)if(up[a][k]!=up[b][k]){ans=min(ans,mn[a][k]);ans=min(ans,mn[b][k]);a=up[a][k];b=up[b][k];} ans=min(ans,mn[a][0]);ans=min(ans,mn[b][0]);} cout<<ans<<"\n";} return 0;}
