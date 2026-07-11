#include <bits/stdc++.h>
using namespace std;

using ll=long long;
using vll=vector<ll>;

#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define all(x) (x).begin(),(x).end()
#define rep(i,a,b) for(int i=a;i<b;i++)

void solve() {
    int n,k; cin>>n>>k;
    vll a(n); rep(i,0,n) cin>>a[i];

    if (k>=3) {cout<<0<<"\n"; return;}
    sort(all(a));

    ll d=a[0];
    rep(i,1,n) d=min(d,a[i]-a[i-1]);

    if (k==1) {cout<<d<<"\n"; return;}

    rep(i,0,n) rep(j,0,i) {
        ll v=a[i]-a[j];
        ll p=lower_bound(all(a),v)-a.begin();

        if (p<n) d=min(d,a[p]-v);
        if (p>0) d=min(d,v-a[p-1]);
    }

    cout<<d<<"\n";
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}