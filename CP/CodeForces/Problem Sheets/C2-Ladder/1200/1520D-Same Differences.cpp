#include <bits/stdc++.h>
using namespace std;

using ll=long long;
using vi=vector<int>;
#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define rep(i,a,b) for(int i=a;i<b;i++)

void solve() {
    int n; cin>>n;
    unordered_map<int,ll> x;
    vi a(n); rep(i,0,n) {cin>>a[i];x[a[i]-i]++;}

    ll ans=0;
    for (auto p:x) {
        ll b=p.second;
        ans+=(b*(b-1))/2;
    }
    cout<<ans<<"\n";
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}