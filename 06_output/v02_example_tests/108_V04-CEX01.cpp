#include <bits/stdc++.h>
using namespace std;


struct BIT {
    int n; vector<long long> t;
    BIT(int n=0): n(n), t(n+1,0) {}
    void add(int x,long long v){ for(;x<=n;x+=x&-x)t[x]+=v; }
    long long sum(int x){ long long r=0; for(;x>0;x-=x&-x)r+=t[x]; return r; }
};
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; cin>>n; vector<int>a(n+1),xs;
    for(int i=1;i<=n;i++){cin>>a[i]; xs.push_back(a[i]);}
    sort(xs.begin(),xs.end()); xs.erase(unique(xs.begin(),xs.end()),xs.end());
    BIT bit(xs.size()); long long inv=0;
    for(int i=n;i>=1;i--){ int id=lower_bound(xs.begin(),xs.end(),a[i])-xs.begin()+1; inv+=bit.sum(id-1); bit.add(id,1); }
    cout<<inv<<"\n"; return 0;
}
