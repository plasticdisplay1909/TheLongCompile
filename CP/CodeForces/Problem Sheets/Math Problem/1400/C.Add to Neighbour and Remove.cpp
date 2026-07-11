#include <bits/stdc++.h>
using namespace std;

using ll=long long;
using vll=vector<ll>;

#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define all(x) (x).begin(),(x).end()
#define rall(x) x.rbegin(),x.rend()
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

    ll sum=accumulate(all(a),0ll);
    vll f=get_factor(sum);
    sort(rall(f));

    for (ll x:f) {
        ll tar=sum/x;
        ll curr=0;
        bool cond=true;

        int block=0;
        rep(i,0,n) {
            curr+=a[i];
            if (curr>tar) {cond=false;break;block=0;}
            if (curr==tar) {curr=0;block++;}
        }

        if (cond) {
            cout<<n-block<<"\n";
            return;
        }
    }
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}