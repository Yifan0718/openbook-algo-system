#include <bits/stdc++.h>
using namespace std;


long long modpow(long long a,long long b,long long mod){long long r=1%mod;for(a%=mod;b;b>>=1,a=a*a%mod)if(b&1)r=r*a%mod;return r;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,q;long long mod;cin>>n>>q>>mod; vector<long long>fac(n+1),inv(n+1);fac[0]=1%mod;for(int i=1;i<=n;i++)fac[i]=fac[i-1]*i%mod;inv[n]=modpow(fac[n],mod-2,mod);for(int i=n;i>=1;i--)inv[i-1]=inv[i]*i%mod;while(q--){int a,b;cin>>a>>b;if(b<0||b>a)cout<<0<<"\n";else cout<<fac[a]*inv[b]%mod*inv[a-b]%mod<<"\n";}return 0;}
