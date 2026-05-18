#include <bits/stdc++.h>
using namespace std;


struct Node{int nxt[26];int cnt;Node(){memset(nxt,0,sizeof(nxt));cnt=0;}};
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,q;cin>>n>>q;vector<Node>tr(1); for(int i=1;i<=n;i++){string s;cin>>s;int u=0;for(char c:s){int x=c-'a';if(!tr[u].nxt[x]){tr[u].nxt[x]=tr.size();tr.push_back(Node());}u=tr[u].nxt[x];tr[u].cnt++;}} while(q--){string s;cin>>s;int u=0,ok=1;for(char c:s){int x=c-'a';if(!tr[u].nxt[x]){ok=0;break;}u=tr[u].nxt[x];}cout<<(ok?tr[u].cnt:0)<<"\n";}return 0;}
