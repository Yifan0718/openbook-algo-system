#include <bits/stdc++.h>
using namespace std;


struct Mat{long long a[2][2];};
Mat mul(Mat x,Mat y,long long mod){Mat z{{{0,0},{0,0}}};for(int i=0;i<2;i++)for(int k=0;k<2;k++)for(int j=0;j<2;j++)z.a[i][j]=(z.a[i][j]+x.a[i][k]*y.a[k][j])%mod;return z;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);long long n,mod;cin>>n>>mod;if(n==0){cout<<0<<"\n";return 0;}Mat r{{{1,0},{0,1}}},b{{{1,1},{1,0}}};long long e=n-1;while(e){if(e&1)r=mul(r,b,mod);b=mul(b,b,mod);e>>=1;}cout<<r.a[0][0]%mod<<"\n";return 0;}
