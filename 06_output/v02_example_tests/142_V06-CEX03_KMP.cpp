#include <bits/stdc++.h>
using namespace std;


vector<int> prefix_function(const string&s){int n=s.size();vector<int>pi(n);for(int i=1;i<n;i++){int j=pi[i-1];while(j&&s[i]!=s[j])j=pi[j-1];if(s[i]==s[j])j++;pi[i]=j;}return pi;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);string p,t;cin>>p>>t;string s=p+"#"+t;auto pi=prefix_function(s);int ans=0;for(int x:pi)if(x==(int)p.size())ans++;cout<<ans<<"\n";return 0;}
