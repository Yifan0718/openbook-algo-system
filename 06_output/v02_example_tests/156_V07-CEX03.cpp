#include <bits/stdc++.h>
using namespace std;


int main(){ios::sync_with_stdio(false);cin.tie(nullptr);long long l=1,r=100,ans=-1,target;cin>>target;while(l<=r){long long mid=(l+r)/2;if(mid*mid>=target){ans=mid;r=mid-1;}else l=mid+1;}cout<<ans<<"\n";return 0;}
