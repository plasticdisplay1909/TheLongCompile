#include <bits/stdc++.h>
using namespace std;

using ll=long long;
using pll=pair<ll,ll>;
using vpll=vector<pll>;

#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define all(x) (x).begin(),(x).end()
#define rep(i,a,b) for(int i=a;i<b;i++)

void solve() {
    ll n; cin>>n;
    vpll a(n); rep(i,0,n) {cin>>a[i].first; a[i].second=i+1;}

    sort(all(a));

    int ans=0;
    rep(i,0,n) rep(j,i+1,n) {
        ll x=a[i].first,y=a[j].first;
        if (x*y>2*n) break;
        if (x*y==(a[i].second+a[j].second)) ans++;
    }

    cout<<ans<<"\n";
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}