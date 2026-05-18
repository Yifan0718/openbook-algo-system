#include <bits/stdc++.h>
using namespace std;

vector<string> tokenize(const string &s) {
    vector<string> words;
    string cur;
    for (unsigned char c : s) {
        if (isalnum(c)) cur.push_back((char)tolower(c));
        else if (!cur.empty()) {
            words.push_back(cur);
            cur.clear();
        }
    }
    if (!cur.empty()) words.push_back(cur);
    return words;
}

map<string, int> count_words(const vector<string> &v) {
    map<string, int> c;
    for (auto &w : v) c[w]++;
    return c;
}

double cosine(const map<string, int> &a, const map<string, int> &b, const map<string, int> &df, int n) {
    map<string, double> va, vb;
    for (auto [w, c] : a) {
        int dfi = df.count(w) ? df.at(w) : 0;
        va[w] = c * (log((double)(n + 1) / (dfi + 1)) + 1.0);
    }
    for (auto [w, c] : b) {
        int dfi = df.count(w) ? df.at(w) : 0;
        vb[w] = c * (log((double)(n + 1) / (dfi + 1)) + 1.0);
    }
    double dot = 0, na = 0, nb = 0;
    for (auto [w, x] : va) {
        na += x * x;
        if (vb.count(w)) dot += x * vb[w];
    }
    for (auto [w, y] : vb) nb += y * y;
    if (na == 0 || nb == 0) return 0;
    return dot / sqrt(na * nb);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    string line;
    getline(cin, line);
    vector<map<string, int>> docs(n + 1);
    map<string, int> df;
    for (int i = 1; i <= n; i++) {
        getline(cin, line);
        docs[i] = count_words(tokenize(line));
        for (auto [w, c] : docs[i]) df[w]++;
    }
    getline(cin, line);
    auto query = count_words(tokenize(line));
    int best = 1;
    double score = -1;
    for (int i = 1; i <= n; i++) {
        double cur = cosine(docs[i], query, df, n);
        if (cur > score + 1e-12) {
            score = cur;
            best = i;
        }
    }
    cout << fixed << setprecision(6) << best << ' ' << score << '\n';
    return 0;
}
