#include <bits/stdc++.h>
using namespace std;

#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define rep(i,a,b) for(int i=a;i<b;i++)

void solve() {
    int n; cin>>n;
    
    int x=1e9,y=1e9;
    int ans=0;

    rep(i,0,n) {
        int v; cin>>v;
        if (v<=x) x=v;
        else if (y<v) {ans++; x=v;}
        else y=v;

        if (x>y) swap(x,y);
    }

    cout<<ans<<"\n";
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}