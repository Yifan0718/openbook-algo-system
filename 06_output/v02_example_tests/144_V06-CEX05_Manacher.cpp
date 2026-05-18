#include <bits/stdc++.h>
using namespace std;


int main(){ios::sync_with_stdio(false);cin.tie(nullptr);string s;cin>>s;string t="@";for(char c:s){t+="#";t+=c;}t+="#$";int n=t.size();vector<int>p(n);int c=0,r=0,ans=0;for(int i=1;i<n-1;i++){int mir=2*c-i;if(i<r)p[i]=min(r-i,p[mir]);while(t[i+1+p[i]]==t[i-1-p[i]])p[i]++;if(i+p[i]>r){c=i;r=i+p[i];}ans=max(ans,p[i]);}cout<<ans<<"\n";return 0;}
