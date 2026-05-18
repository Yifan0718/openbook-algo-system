#include <bits/stdc++.h>
using namespace std;

struct Trie {
    struct Node {
        int nxt[26]{};
        int pass = 0;
    };
    vector<Node> tr;

    Trie() {
        tr.push_back(Node());
    }

    void insert(const string &s) {
        int u = 0;
        tr[u].pass++;
        for (char c : s) {
            int x = c - 'a';
            if (!tr[u].nxt[x]) {
                tr[u].nxt[x] = (int)tr.size();
                tr.push_back(Node());
            }
            u = tr[u].nxt[x];
            tr[u].pass++;
        }
    }

    int query(const string &s) const {
        int u = 0;
        for (char c : s) {
            int x = c - 'a';
            if (x < 0 || x >= 26 || !tr[u].nxt[x]) return 0;
            u = tr[u].nxt[x];
        }
        return tr[u].pass;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    Trie trie;
    while (q--) {
        string op, s;
        cin >> op >> s;
        if (op == "add") trie.insert(s);
        else cout << trie.query(s) << '\n';
    }
    return 0;
}
