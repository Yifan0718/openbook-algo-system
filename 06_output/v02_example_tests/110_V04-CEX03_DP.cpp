#include <bits/stdc++.h>
using namespace std;


int main(){ ios::sync_with_stdio(false); cin.tie(nullptr); int n,k; long long C; cin>>n>>k>>C; vector<long long>a(n+1),dp(n+1); for(int i=1;i<=n;i++)cin>>a[i]; deque<int> dq; dq.push_back(0); for(int i=1;i<=n;i++){ while(!dq.empty()&&dq.front()<i-k)dq.pop_front(); dp[i]=dp[dq.front()]+a[i]-C; while(!dq.empty()&&dp[dq.back()]<=dp[i])dq.pop_back(); dq.push_back(i);} cout<<*max_element(dp.begin()+1,dp.end())<<"\n"; return 0; }
