#include <bits/stdc++.h>
using namespace std;


int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;cin>>n; vector<int>is(n+1,1),pr; if(n>=0)is[0]=0;if(n>=1)is[1]=0; for(int i=2;i<=n;i++){if(is[i])pr.push_back(i); for(int p:pr){if(1LL*i*p>n)break;is[i*p]=0;if(i%p==0)break;}} cout<<pr.size()<<"\n"; for(int p:pr) if(n-p>=2&&is[n-p]){cout<<p<<" "<<n-p<<"\n"; return 0;} cout<<"NONE\n";return 0;}
