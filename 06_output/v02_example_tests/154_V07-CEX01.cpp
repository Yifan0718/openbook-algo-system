#include <bits/stdc++.h>
using namespace std;


long long slow(vector<int>a){long long ans=0;for(int i=0;i<(int)a.size();i++)for(int j=i+1;j<(int)a.size();j++)if(a[i]>a[j])ans++;return ans;}
long long fast(vector<int>a){int n=a.size();vector<int>xs=a;sort(xs.begin(),xs.end());xs.erase(unique(xs.begin(),xs.end()),xs.end());vector<int>bit(xs.size()+2);auto add=[&](int x){for(;x<(int)bit.size();x+=x&-x)bit[x]++;};auto sum=[&](int x){int r=0;for(;x>0;x-=x&-x)r+=bit[x];return r;};long long ans=0;for(int i=n-1;i>=0;i--){int id=lower_bound(xs.begin(),xs.end(),a[i])-xs.begin()+1;ans+=sum(id-1);add(id);}return ans;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;cin>>n;vector<int>a(n);for(int&i:a)cin>>i;cout<<(slow(a)==fast(a)?"OK":"BAD")<<" "<<fast(a)<<"\n";return 0;}
