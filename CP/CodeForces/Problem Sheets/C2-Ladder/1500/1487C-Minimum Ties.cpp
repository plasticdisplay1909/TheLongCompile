#include <bits/stdc++.h>
using namespace std;
#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);

void solve() {
    int n; cin>>n;
    for (int i=1;i<=n;i++) {
        for (int j=i+1;j<=n;j++) {
            int d=j-i;

            // Odd number of matches
            // n/2 wins 1 draw
            if (n%2==0) {
                if (d<n/2) cout<<1<<" ";
                else if (d==n/2) cout<<0<<" ";
                else cout<<-1<<" ";
            } else  {
                if (d<=n/2) cout<<1<<" ";
                else cout<<-1<<" ";
            }
        }
    }

    cout<<"\n";
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}