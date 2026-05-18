#include <bits/stdc++.h>
using namespace std;


int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,m;cin>>n>>m; vector<vector<int>>g(n+1); vector<int>ind(n+1); for(int i=1;i<=m;i++){int u,v;cin>>u>>v;g[u].push_back(v);ind[v]++;} queue<int>q; vector<int>sem(n+1,1); for(int i=1;i<=n;i++)if(!ind[i])q.push(i); int seen=0,ans=1; while(!q.empty()){int u=q.front();q.pop();seen++;ans=max(ans,sem[u]); for(int v:g[u]){sem[v]=max(sem[v],sem[u]+1); if(--ind[v]==0)q.push(v);}} if(seen<n)cout<<"CYCLE\n"; else cout<<ans<<"\n"; return 0;}
