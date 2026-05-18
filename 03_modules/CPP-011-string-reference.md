# CPP-011 string 考场速查

模块编号：CPP-011

模块名称：`string` 考场速查与常用代码

标签：[C++17][string][字符处理][子串查找][getline][类型转换]

一句话用途：把 C++ `string` 的构造、访问、修改、查找、比较、转换和字符统计整理成考场可直接抄的可靠片段。

题面触发词：

- 字符串、单词、整行文本、含空格输入。
- 子串、前缀、后缀、查找最后一次出现。
- 字典序最小/最大、按字符串排序。
- 删除、插入、替换、拼接。
- 数字字符串转整数、整数转字符串。
- 判断字符是否为数字/字母、大小写转换、统计字符频次。

什么时候用：

- 只需要 STL 基础字符串操作，不需要 KMP、Hash、Trie。
- 字符串长度和操作次数不大，允许 `insert/erase/replace/substr` 复制或移动字符。
- 题目要求模拟编辑字符串、统计字符、分割单词、做简单查找。

不要什么时候用：

- 长串反复模式匹配，优先 STR-02 KMP/Z。
- 大量任意子串相等判断，优先 STR-03 Rolling Hash。
- 大量在字符串中间插入删除，`string` 会整体移动字符，可能 TLE。

复杂度：

- `size/empty/operator[]`：`O(1)`。
- `push_back/pop_back/back/front`：尾部操作通常 `O(1)`。
- `insert/erase/replace`：最坏 `O(n)`，因为要移动后面的字符。
- `substr(pos,len)`：`O(len)`，会复制新字符串。
- `find/rfind/compare`：和参与比较/查找的字符数相关，频繁大规模查找不要当作线性算法保证。

索引约定：

```text
C++ string 自然 0-index：合法位置是 0..s.size()-1。
题面第 k 个字符若是 1-index，写 k-- 后再访问。
substr(pos, len)：pos 是起点，len 是长度，不是右端点。
题面 1-index 闭区间 [l,r]：s.substr(l - 1, r - l + 1)。
```

依赖的标准容器：

- `string`。
- `vector<string>`。
- 字符计数常用 `vector<int>(256)` 或 `array<int, 26>`。
- 分割整行可用 `stringstream`。

接口速查：

| 需求 | 写法 |
|---|---|
| 构造空串 | `string s;` |
| 构造重复字符 | `string s(n, 'a');` |
| 从 C 风格字符串构造 | `string s = "abc";` |
| 拼接 | `s += t;` 或 `s = a + b;` |
| 长度 | `int n = (int)s.size();` |
| 判空 | `s.empty()` |
| 下标访问 | `s[i]` |
| 首尾字符 | `s.front()`、`s.back()`，先保证非空 |
| 尾部加入 | `s.push_back(c);` 或 `s += c;` |
| 尾部删除 | `s.pop_back();`，先保证非空 |
| 插入 | `s.insert(pos, t);` |
| 删除 | `s.erase(pos, len);` |
| 替换 | `s.replace(pos, len, t);` |
| 截取 | `s.substr(pos, len);` |
| 从左查找 | `s.find(t)` |
| 从右查找 | `s.rfind(t)` |
| 比较 | `s.compare(t)` 或 `s < t` |
| 转整数 | `stoi(s)`、`stoll(s)` |
| 转字符串 | `to_string(x)` |

## 1. 构造、长度、访问

```cpp
string a;              // 空串
string b = "abc";      // "abc"
string c(5, 'x');      // "xxxxx"
string d = b + c;      // 拼接

int n = (int)b.size(); // 推荐转 int，避免无符号坑
if (!b.empty()) {
    char first = b.front();
    char last = b.back();
    if ((int)b.size() > 1) {
        char mid = b[1]; // 0-index，b[1] 是第二个字符
    }
}
```

遍历：

```cpp
string s = "abc";

for (int i = 0; i < (int)s.size(); i++) {
    cout << i << ' ' << s[i] << '\n';
}

for (char c : s) {
    cout << c << '\n';
}
```

## 2. 修改：push_back / pop_back / insert / erase / replace

```cpp
string s = "abc";

s.push_back('d');        // "abcd"
s += 'e';                // "abcde"
s += "fg";               // "abcdefg"

if (!s.empty()) {
    s.pop_back();        // "abcdef"
}

s.insert(3, "XXX");      // 在下标 3 前插入："abcXXXdef"
s.erase(3, 3);           // 从下标 3 开始删 3 个："abcdef"
s.replace(1, 3, "OO");   // 从下标 1 开始替换 3 个："aOOef"
```

安全删除某个字符：

```cpp
string s = "abcde";
int pos = 2; // 删除 'c'
if (0 <= pos && pos < (int)s.size()) {
    s.erase(pos, 1); // "abde"
}
```

删除所有某字符，推荐新建结果串，比反复 `erase` 更稳：

```cpp
string remove_char(const string &s, char bad) {
    string res;
    for (char c : s) {
        if (c != bad) res.push_back(c);
    }
    return res;
}
```

## 3. substr / find / rfind

```cpp
string s = "abracadabra";

string t1 = s.substr(0, 4); // "abra"
string t2 = s.substr(3);    // 从下标 3 到结尾："acadabra"

size_t p = s.find("ra");    // 第一次出现位置：2
if (p != string::npos) {
    cout << "found at " << p << '\n';
}

size_t q = s.rfind("ra");   // 最后一次出现位置：9
if (q != string::npos) {
    cout << "last at " << q << '\n';
}
```

从某个位置开始找：

```cpp
string s = "aaaa";
size_t p = s.find("aa", 1); // 从下标 1 开始找，结果 1
```

统计模式串出现次数，允许重叠：

```cpp
int count_occurrence_overlap(const string &s, const string &pat) {
    if (pat.empty()) return 0;
    int ans = 0;
    size_t pos = s.find(pat);
    while (pos != string::npos) {
        ans++;
        pos = s.find(pat, pos + 1);
    }
    return ans;
}
```

不允许重叠：

```cpp
int count_occurrence_no_overlap(const string &s, const string &pat) {
    if (pat.empty()) return 0;
    int ans = 0;
    size_t pos = s.find(pat);
    while (pos != string::npos) {
        ans++;
        pos = s.find(pat, pos + pat.size());
    }
    return ans;
}
```

## 4. compare 与字典序

`string` 默认按字典序比较，和字典中排序类似：从左到右找第一个不同字符，字符小的字符串更小；若前面都相同，短的更小。

```cpp
string a = "abc";
string b = "abd";
string c = "abcde";

cout << (a < b) << '\n'; // true，因为 'c' < 'd'
cout << (a < c) << '\n'; // true，因为 a 是 c 的前缀且更短

int x = a.compare(b);    // x < 0 表示 a < b
int y = b.compare(a);    // y > 0 表示 b > a
int z = a.compare("abc");// z == 0 表示相等
```

排序字符串：

```cpp
vector<string> v = {"ba", "ab", "aa"};
sort(v.begin(), v.end()); // "aa", "ab", "ba"
```

自定义：先按长度，再按字典序：

```cpp
sort(v.begin(), v.end(), [](const string &x, const string &y) {
    if (x.size() != y.size()) return x.size() < y.size();
    return x < y;
});
```

## 5. getline 混 cin

`cin >> x` 会留下行尾换行；接着 `getline` 会先读到这个空行。解决：在第一次 `getline` 前吃掉换行。

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    for (int i = 0; i < n; i++) {
        string line;
        getline(cin, line);
        cout << line << '\n';
    }

    return 0;
}
```

只读无空格字符串：

```cpp
string s;
cin >> s;
```

读整行，允许空格：

```cpp
string line;
getline(cin, line);
```

## 6. stoi / stoll / to_string

```cpp
string a = "123";
string b = "-9000000000000";

int x = stoi(a);
long long y = stoll(b);

string sx = to_string(x);
string sy = to_string(y);
```

从字符串中扫描整数，考场更常用手扫，避免异常处理：

```cpp
vector<long long> read_ints_from_line(const string &line) {
    vector<long long> nums;
    int n = (int)line.size();
    for (int i = 0; i < n; ) {
        while (i < n && !isdigit((unsigned char)line[i]) && line[i] != '-') i++;
        if (i >= n) break;

        int sign = 1;
        if (line[i] == '-') {
            sign = -1;
            i++;
        }

        long long x = 0;
        bool has_digit = false;
        while (i < n && isdigit((unsigned char)line[i])) {
            has_digit = true;
            x = x * 10 + (line[i] - '0');
            i++;
        }
        if (has_digit) nums.push_back(sign * x);
    }
    return nums;
}
```

提醒：

```text
stoi 超出 int 范围或字符串不是合法数字会抛异常；竞赛中若不想写 try/catch，先保证输入合法。
大整数用 stoll；再大就按字符串处理或高精度。
```

## 7. 字符函数：isdigit / isalpha / tolower / toupper

这些函数来自 `<cctype>`，`bits/stdc++.h` 已包含。为了避免 `char` 为负导致未定义行为，传参时推荐转 `unsigned char`。

```cpp
char c = 'A';

if (isdigit((unsigned char)c)) {
    cout << "digit\n";
}
if (isalpha((unsigned char)c)) {
    cout << "letter\n";
}

char low = (char)tolower((unsigned char)c); // 'a'
char up = (char)toupper((unsigned char)low); // 'A'
```

整串转小写：

```cpp
string to_lower_string(string s) {
    for (char &c : s) {
        c = (char)tolower((unsigned char)c);
    }
    return s;
}
```

只保留字母数字并转小写：

```cpp
string normalize_alnum_lower(const string &s) {
    string res;
    for (char c : s) {
        unsigned char uc = (unsigned char)c;
        if (isalnum(uc)) {
            res.push_back((char)tolower(uc));
        }
    }
    return res;
}
```

## 8. 按字符计数

小写字母计数：

```cpp
array<int, 26> count_lower(const string &s) {
    array<int, 26> cnt{};
    for (char c : s) {
        if ('a' <= c && c <= 'z') {
            cnt[c - 'a']++;
        }
    }
    return cnt;
}
```

ASCII 字符计数：

```cpp
vector<int> count_ascii(const string &s) {
    vector<int> cnt(256, 0);
    for (unsigned char c : s) {
        cnt[c]++;
    }
    return cnt;
}
```

判断两个小写字符串是否为异位词：

```cpp
bool same_lower_multiset(const string &a, const string &b) {
    return count_lower(a) == count_lower(b);
}
```

## 9. split 思路

按空白切单词，最省事用 `stringstream`：

```cpp
vector<string> split_by_space(const string &line) {
    stringstream ss(line);
    vector<string> words;
    string word;
    while (ss >> word) {
        words.push_back(word);
    }
    return words;
}
```

按指定分隔符切，例如逗号：

```cpp
vector<string> split_by_char(const string &s, char sep) {
    vector<string> parts;
    string cur;
    for (char c : s) {
        if (c == sep) {
            parts.push_back(cur);
            cur.clear();
        } else {
            cur.push_back(c);
        }
    }
    parts.push_back(cur);
    return parts;
}
```

调用示例：

```cpp
string line = "alice,bob,,tom";
vector<string> parts = split_by_char(line, ',');
// parts = {"alice", "bob", "", "tom"}
```

## 10. 可抄完整模板

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

string substr_1idx(const string &s, int l, int r) {
    return s.substr(l - 1, r - l + 1);
}

array<int, 26> count_lower(const string &s) {
    array<int, 26> cnt{};
    for (char c : s) {
        if ('a' <= c && c <= 'z') cnt[c - 'a']++;
    }
    return cnt;
}

vector<int> count_ascii(const string &s) {
    vector<int> cnt(256, 0);
    for (unsigned char c : s) cnt[c]++;
    return cnt;
}

string to_lower_string(string s) {
    for (char &c : s) c = (char)tolower((unsigned char)c);
    return s;
}

vector<string> split_by_space(const string &line) {
    stringstream ss(line);
    vector<string> words;
    string word;
    while (ss >> word) words.push_back(word);
    return words;
}

vector<string> split_by_char(const string &s, char sep) {
    vector<string> parts;
    string cur;
    for (char c : s) {
        if (c == sep) {
            parts.push_back(cur);
            cur.clear();
        } else {
            cur.push_back(c);
        }
    }
    parts.push_back(cur);
    return parts;
}

int count_occurrence_overlap(const string &s, const string &pat) {
    if (pat.empty()) return 0;
    int ans = 0;
    size_t pos = s.find(pat);
    while (pos != string::npos) {
        ans++;
        pos = s.find(pat, pos + 1);
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s = "abracadabra";

    s.push_back('!');
    s.pop_back();
    s.insert(3, "X");
    s.erase(3, 1);
    s.replace(0, 4, "ABRA");

    cout << s.substr(0, 4) << '\n';
    cout << count_occurrence_overlap(s, "ra") << '\n';

    vector<string> words = split_by_space("one two three");
    for (string w : words) cout << w << '\n';

    int x = stoi("123");
    long long y = stoll("1234567890123");
    cout << to_string(x + 1) << ' ' << to_string(y) << '\n';

    return 0;
}
```

## 11. 常见坑

- `string` 是 0-index；题面位置常是 1-index，访问前先减一。
- `s[i]` 不检查越界；`s.at(i)` 会检查但较少用。考场访问前确认 `0 <= i < (int)s.size()`。
- 空串不能用 `front/back/pop_back`。
- `substr(pos, len)` 的第二个参数是长度，不是右端点。
- `find/rfind` 找不到返回 `string::npos`，不是 `-1`；用 `if (p != string::npos)` 判断。
- `string::npos` 类型是 `size_t`，不要写 `int p = s.find(t)` 后再和 `-1` 混着判断。
- `size()` 是无符号类型；倒序循环先写 `int n = (int)s.size()`。
- `insert/erase/replace` 都可能 `O(n)`，在循环中反复对长串中间操作会退化到 `O(n^2)`。
- 反复 `s = s + c` 可能复制多次；追加单字符优先 `push_back`。
- `stoi/stoll` 要求字符串合法且范围足够；不确定时手写扫描或用 `stringstream`。
- `isdigit/isalpha/tolower/toupper` 传入 `char` 前推荐转 `unsigned char`。
- `getline` 混 `cin >>` 时，第一次 `getline` 前先 `cin.ignore(...)`。

暴力/部分分替代：

- 查找子串小数据可直接双循环逐字符比较。
- 删除/替换小数据直接 `erase/replace` 模拟。
- 复杂行格式看不懂时，整行 `getline` 后用 `stringstream` 或手扫字符。

升级方向：

- 单模式多次匹配：KMP/Z。
- 多模式匹配：Trie/AC 自动机。
- 子串相等、大量回文判断：Rolling Hash。
- 回文子串统计：中心扩展或 STR-05 Manacher。

最小测试样例：

```text
s = abracadabra
s.substr(0,4) = abra
s.find("ra") = 2
s.rfind("ra") = 9
"abc" < "abd" = true
split_by_char("a,b,,c", ',') = ["a", "b", "", "c"]
```
