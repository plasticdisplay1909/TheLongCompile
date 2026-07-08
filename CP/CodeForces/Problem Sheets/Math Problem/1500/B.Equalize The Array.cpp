#include <bits/stdc++.h>
using namespace std;

using ll=long long;
using vll=vector<ll>;

#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define all(x) (x).begin(),(x).end()
#define rep(i,a,b) for(int i=a;i<b;i++)


void solve() {
    int n; cin>>n;
    map<int,ll> x;

    rep(i,0,n) {
        int k; cin>>k;
        x[k]++;
    }

    vll f;
    for(auto p:x) f.push_back(p.second);

    sort(all(f));
    int m=f.size();

    vll pre(m+1,0);
    rep(i,0,m) pre[i+1]=pre[i]+f[i];
    ll ans=n;

    rep(i,0,m) {
        ll left=pre[i], right=(pre[m]-pre[i+1]) -1LL*(m-i-1)*f[i];
        ans=min(ans,left+right);
    }

    cout<<ans<<"\n";
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}