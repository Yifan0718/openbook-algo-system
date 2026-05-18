#include <bits/stdc++.h>
using namespace std;


bool leap(int y){return y%400==0||(y%4==0&&y%100!=0);}
int mdays(int y,int m){int d[]={0,31,28,31,30,31,30,31,31,30,31,30,31};return m==2?d[m]+leap(y):d[m];}
long long days(int y,int m,int d){long long ans=0;for(int yy=1;yy<y;yy++)ans+=365+leap(yy);for(int mm=1;mm<m;mm++)ans+=mdays(y,mm);return ans+d;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int y1,m1,d1,y2,m2,d2;cin>>y1>>m1>>d1>>y2>>m2>>d2;cout<<llabs(days(y2,m2,d2)-days(y1,m1,d1))<<"\n";return 0;}
