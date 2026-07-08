#include <bits/stdc++.h>
using namespace std;

using ll=long long;
using pll=pair<ll,ll>;
using umll=unordered_map<ll,ll>;
using vpll=vector<pll>;

#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define all(x) (x).begin(),(x).end()
#define rep(i,a,b) for(int i=a;i<b;i++)


void solve() {
    ll a,b,k; cin>>a>>b>>k;
    vpll x(k);
    rep(i,0,k) cin>>x[i].first;
    rep(i,0,k) cin>>x[i].second;

    umll boy,girl;
    rep(i,0,k) boy[x[i].first]++,girl[x[i].second]++;

    ll ans=0;
    rep(i,0,k) {
        boy[x[i].first]--,girl[x[i].second]--;

        ans+=max(0LL,k-i-1-boy[x[i].first]-girl[x[i].second]);
    }

    cout<<ans<<"\n";
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}