#include <bits/stdc++.h>
using namespace std;


int main(){ios::sync_with_stdio(false);cin.tie(nullptr);long long n;int k;cin>>n>>k;vector<long long>a(k+1);for(int i=1;i<=k;i++)cin>>a[i];long long ans=0;for(int mask=1;mask<(1<<k);mask++){__int128 l=1;int bits=0;for(int i=1;i<=k;i++)if(mask>>(i-1)&1){bits++;l=l/std::gcd((long long)l,a[i])*a[i];if(l>n)break;}if(l>n)continue;long long cnt=n/(long long)l;if(bits&1)ans+=cnt;else ans-=cnt;}cout<<ans<<"\n";return 0;}
