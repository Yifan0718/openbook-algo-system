#include <bits/stdc++.h>
using namespace std;


double sigmoid(double z){return 1.0/(1.0+exp(-z));}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;double lr;cin>>n>>lr;double w=0,b=0; for(int i=1;i<=n;i++){double x,y;cin>>x>>y;double p=sigmoid(w*x+b);double e=p-y;w-=lr*e*x;b-=lr*e;}cout<<fixed<<setprecision(6)<<w<<" "<<b<<"\n";return 0;}
