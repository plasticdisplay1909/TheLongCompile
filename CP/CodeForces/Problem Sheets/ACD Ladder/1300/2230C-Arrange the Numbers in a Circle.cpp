#include <bits/stdc++.h>
using namespace std;

using ll=long long;
using vll=vector<ll>;

#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define all(x) (x).begin(),(x).end()
#define rep(i,a,b) for(int i=a;i<b;i++)

void solve() {
    int n; cin>>n;
    vll a(n); rep(i,0,n) cin>>a[i];
    ll sum=accumulate(all(a),0LL);

    ll one=0,slot=0;
    for (ll i:a) {
        if (i==1) one++;
        else slot+=(i/2-1); 
    }

    if (one == n-1) slot++;
    ll waste=max(one-slot,0LL);

    cout<<(sum-waste<3 ? 0 : sum-waste)<<"\n";
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}