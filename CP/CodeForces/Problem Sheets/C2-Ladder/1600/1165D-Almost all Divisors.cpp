#include <bits/stdc++.h>
using namespace std;

using ll=long long;
using vll=vector<ll>;

#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define all(x) (x).begin(),(x).end()
#define rep(i,a,b) for(int i=a;i<b;i++)


vll get_factor(ll n) {
    vll d;
    for (ll i=1;i*i<=n;i++) {
        if (n%i==0) {
            d.push_back(i);
            if (i*i!=n) d.push_back(n/i);
        }
    }
    return d;
}

void solve() {
    int n; cin>>n;
    vll a(n); rep(i,0,n) cin>>a[i];
    sort(all(a));

    ll x=a[0]*a[n-1];
    
    vll d=get_factor(x);
    sort(all(d));
    d.pop_back(); d.erase(d.begin());
    cout<<(a==d ? x : -1)<<"\n";
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}