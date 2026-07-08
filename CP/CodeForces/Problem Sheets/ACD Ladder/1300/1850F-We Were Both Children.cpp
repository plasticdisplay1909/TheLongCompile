#include <bits/stdc++.h>
using namespace std;

using vi=vector<int>;
#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define all(x) (x).begin(),(x).end()
#define rep(i,a,b) for(int i=a;i<b;i++)

void solve() {
    int n; cin>>n;
    vi a(n+1,0),b(n+1,0);

    rep(i,0,n) {
        int x; cin>>x;
        if (x<=n) a[x]++;
    }

    rep(i,1,n+1) for (int j=i;j<=n;j+=i) b[j]+=a[i];

    cout<<*max_element(all(b))<<"\n";
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}