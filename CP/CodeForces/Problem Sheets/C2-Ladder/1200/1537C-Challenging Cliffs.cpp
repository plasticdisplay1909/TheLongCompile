#include <bits/stdc++.h>
using namespace std;

using vi=vector<int>;
#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define all(x) (x).begin(),(x).end()
#define rep(i,a,b) for(int i=a;i<b;i++)


void solve() {
    int n; cin>>n;
    vi a(n); rep(i,0,n) cin>>a[i];

    sort(all(a));
    if (n==2) {
        cout<<a[0]<<' '<<a[1]<<"\n";
        return;
    }

    int mx=1e9,idx=0;
    rep(i,1,n) if (mx>abs(a[i]-a[i-1])) {mx=abs(a[i]-a[i-1]); idx=i;}

    rep(i,idx,n) cout<<a[i]<<' ';
    rep(i,0,idx) cout<<a[i]<<' ';
    cout<<"\n";
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}