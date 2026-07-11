#include <bits/stdc++.h>
using namespace std;

using vi=vector<int>;

#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define rep(i,a,b) for(int i=a;i<b;i++)

void solve() {
    int n; cin>>n;
    vi a(n); rep(i,0,n) cin>>a[i];

    if (a[0]==1) {
        cout<<n+1<<' ';
        rep(i,1,n+1) cout<<i<<' ';
        cout<<"\n"; return;
    } else if (a[n-1]==0) {
        rep(i,1,n+2) cout<<i<<' '; cout<<"\n"; return;
    } else{
        int pos=-1;
        rep(i,0,n-1) if (a[i]==0 and a[i+1]==1) {pos=i; break;}

        if (pos==-1) {cout<<-1<<"\n"; return;}
        else {
            rep(i,1,pos+2) cout<<i<<' ';
            cout<<n+1<<' ';
            rep(i,pos+2,n+1) cout<<i<<' ';
            cout<<"\n";
        }
    }
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}