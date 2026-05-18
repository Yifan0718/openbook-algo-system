#include <bits/stdc++.h>
using namespace std;


int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;cin>>n; vector<double>x(n+1),y(n+1); for(int i=1;i<=n;i++)cin>>x[i]>>y[i]; double dot=0,nx=0,ny=0; for(int i=1;i<=n;i++){dot+=x[i]*y[i];nx+=x[i]*x[i];ny+=y[i]*y[i];} cout<<fixed<<setprecision(6)<<dot/(sqrt(nx)*sqrt(ny))<<"\n";return 0;}
