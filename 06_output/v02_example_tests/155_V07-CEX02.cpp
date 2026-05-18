#include <bits/stdc++.h>
using namespace std;


int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;cin>>n;vector<long long>a(n+1);for(int i=1;i<=n;i++)cin>>a[i];bool ok=true;for(int i=1;i<=n;i++){if(a[i]<-1000000000LL||a[i]>1000000000LL)ok=false;}cout<<(ok?"INPUT_OK":"INPUT_OUT_OF_RANGE")<<"\n";return 0;}
