#include <bits/stdc++.h>
using namespace std;


struct P{double x,y;};
double cross(P a,P b,P c){return (b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x);}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;cin>>n;vector<P>p(n+1);for(int i=1;i<=n;i++)cin>>p[i].x>>p[i].y;double area=0;for(int i=1;i<=n;i++){int j=i==n?1:i+1;area+=p[i].x*p[j].y-p[i].y*p[j].x;}cout<<fixed<<setprecision(1)<<fabs(area)/2<<"\n";return 0;}
