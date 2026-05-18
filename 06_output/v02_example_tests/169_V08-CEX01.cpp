#include <bits/stdc++.h>
using namespace std;


long long exgcd(long long a,long long b,long long&x,long long&y){if(!b){x=1;y=0;return a;}long long x1,y1,g=exgcd(b,a%b,x1,y1);x=y1;y=x1-a/b*y1;return g;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);long long a,b,c;cin>>a>>b>>c;long long x,y,g=exgcd(abs(a),abs(b),x,y);if(c%g){cout<<"NO\n";return 0;}x*=c/g;y*=c/g;if(a<0)x=-x;if(b<0)y=-y;cout<<x<<" "<<y<<"\n";return 0;}
