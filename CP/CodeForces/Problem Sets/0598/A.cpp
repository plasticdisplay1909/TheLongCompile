#include <bits/stdc++.h>
using namespace std;

using ll=long long;
#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define all(x) (x).begin(),(x).end()

void solve() {
    ll n; cin>>n;
    ll i=1;
    
    ll ans=(n*(n+1))/2;
    while (i<=n) {
        ans-=2*i;
        i*=2;
    }
    cout<<ans<<"\n";
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}