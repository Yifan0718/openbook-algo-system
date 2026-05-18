#include <bits/stdc++.h>
using namespace std;


struct Var{double val,grad;};
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);double x,y;cin>>x>>y;Var a{x,0},b{y,0};double c=a.val*b.val;double d=c+a.val;double e=d*d;double ge=1;double gd=ge*2*d;double gc=gd; a.grad+=gd; a.grad+=gc*b.val; b.grad+=gc*a.val;cout<<fixed<<setprecision(4)<<e<<" "<<a.grad<<" "<<b.grad<<"\n";return 0;}
