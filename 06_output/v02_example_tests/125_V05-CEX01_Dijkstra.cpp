#include <bits/stdc++.h>
using namespace std;


int main(){ ios::sync_with_stdio(false); cin.tie(nullptr); int n,m,s,t;cin>>n>>m>>s>>t; vector<vector<pair<int,int>>> g(n+1); for(int i=1;i<=m;i++){int u,v,w;cin>>u>>v>>w;g[u].push_back({v,w});g[v].push_back({u,w});} const long long INF=4e18; vector<long long>d(n+1,INF),cnt(n+1); priority_queue<pair<long long,int>,vector<pair<long long,int>>,greater<pair<long long,int>>>pq; d[s]=0;cnt[s]=1;pq.push({0,s}); while(!pq.empty()){auto [du,u]=pq.top();pq.pop(); if(du!=d[u])continue; for(auto [v,w]:g[u]){ if(d[v]>du+w){d[v]=du+w;cnt[v]=cnt[u];pq.push({d[v],v});} else if(d[v]==du+w)cnt[v]+=cnt[u]; }} cout<<(d[t]==INF?-1:d[t])<<" "<<(d[t]==INF?0:cnt[t])<<"\n"; return 0; }
