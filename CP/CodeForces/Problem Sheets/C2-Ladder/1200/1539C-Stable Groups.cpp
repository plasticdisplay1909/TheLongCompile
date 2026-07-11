#include <bits/stdc++.h>
using namespace std;

using ll=long long;
using vll=vector<ll>;

#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define all(x) (x).begin(),(x).end()
#define rep(i,a,b) for(int i=a;i<b;i++)


void solve() {
    ll n,k,x; cin>>n>>k>>x;
    vll a(n); rep(i,0,n) cin>>a[i];
    sort(all(a));

    vll diff; ll block=1;
    rep(i,1,n) {
        if (a[i]-a[i-1]>x) {
            block++;
            ll m=(a[i]-a[i-1]-1)/x;
            diff.push_back(m);
        }
    }
    sort(all(diff));

    int l=diff.size();
    
    for (ll i:diff) {
        if (k-i>=0) {k-=i; block--;}
        else break;
    }

    cout<<block<<"\n";
}

int main() {
    meow
    solve();
    return 0;
}