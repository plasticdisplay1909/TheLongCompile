#include <bits/stdc++.h>
using namespace std;


#define meow ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr);
#define all(x) (x).begin(),(x).end()
#define rep(i,a,b) for(int i=a;i<b;i++)

void solve() {
    string a,s; cin>>a>>s;
    int i=a.size()-1,j=s.size()-1;

    string b="";
    while (i>=0 and j>=0) {
        if (a[i]<=s[j]) {b+=char('0'+ (s[j]-a[i])); i--;j--;}
        else {
            int x=a[i]-'0';
            int y=s[j]-'0';

            if (j>=1) y+=10*(s[j-1]-'0');
            else {cout<<"-1\n"; return;}

            if (y<10 or y>18) {cout<<"-1\n"; return;}
            if (y-x<0 or y-x>=10) {cout<<"-1\n"; return;}

            b+=char('0'+ (y-x));

            j-=2;i--;
        }
    }

    if (i>=0) {cout<<"-1\n"; return;}
    while (j>=0) {b+=s[j]; j--;}
    
    reverse(all(b));
    int pos=0;
    while (pos+1 < (int)b.size() and b[pos]=='0') pos++;
    cout<<b.substr(pos)<<"\n";
}

int main() {
    meow
    int t; cin>>t;
    while (t--) solve();
    return 0;
}