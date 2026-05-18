#include <bits/stdc++.h>
using namespace std;


int main(){ios::sync_with_stdio(false);cin.tie(nullptr);long long a,b,limit;cin>>a>>b>>limit;__int128 prod=(__int128)a*b;cout<<(prod>limit?"OVER":"OK")<<"\n";return 0;}
