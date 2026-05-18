#include <bits/stdc++.h>
using namespace std;


int main(){ios::sync_with_stdio(false);cin.tie(nullptr);double x,w,b,target,lr;cin>>x>>w>>b>>target>>lr;double y=w*x+b;double loss=(y-target)*(y-target);double gw=2*(y-target)*x;double gb=2*(y-target);w-=lr*gw;b-=lr*gb;cout<<fixed<<setprecision(4)<<loss<<" "<<w<<" "<<b<<"\n";return 0;}
