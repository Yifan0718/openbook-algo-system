# STR-01 string 常用操作

模块编号：STR-01

模块名称：C++ string 常用操作与索引转换

标签：[字符串][string][基础操作][0-index]

一句话用途：统一字符串读入、截取、查找、拼接、排序和 0-index/1-index 转换，减少低级错误。

索引约定：

```text
本模块内部使用 C++ string 自然 0-index：位置 0..n-1。
题面若给第 k 个字符，通常是 1-index：读入后用 k--。
子串 substr(pos, len) 的 pos 是 0-index，len 是长度，不是右端点。
若题面给闭区间 [l,r] 且为 1-index，则 C++ 写 s.substr(l-1, r-l+1)。
```

题面触发词：

- 字符串处理、字符替换、统计字符。
- 子串、前缀、后缀。
- 字典序排序。
- 翻转、拼接、删除、插入。
- 大小写转换。

什么时候用：

- 题目只需要简单字符串操作，不需要 KMP/Hash。
- 字符串长度不大，可以直接用 `substr/find`。
- 需要把题面 1-index 位置转成 C++ 0-index。

不要什么时候用：

- `n,m` 很大且要重复匹配子串，`find/substr` 可能 TLE。
- 需要大量判断任意子串是否相等，优先 Rolling Hash。
- 多模式串匹配，优先 Trie/AC 自动机。

复杂度：

- `s.size()`：`O(1)`。
- `s.substr(pos,len)`：`O(len)`。
- `s.find(t)`：通常可用但最坏不作为算法保证。
- 排序字符串数组：`O(总比较成本 * log n)`。

数据范围参考：

- `|s| <= 1e5`：一次线性扫描没问题。
- 重复 `substr` 复制总长度可能到 `O(n^2)`，要小心。

依赖的标准容器：

- `string`。
- `vector<int>` / `vector<string>`。
- 字符计数常用 `array<int, 26>` 或 `vector<int>(256)`。

输入如何整理：

```cpp
string s;
cin >> s; // 无空格字符串

string line;
getline(cin, line); // 含空格整行，注意先处理上一行换行
```

接口：

```text
to0(pos1) -> 题面 1-index 转 0-index
substr_1idx(s,l,r) -> 题面 1-index 闭区间子串
count_lower(s) -> 统计小写字母
is_prefix(s,t) -> t 是否为 s 的前缀
is_suffix(s,t) -> t 是否为 s 的后缀
```

输出能力：

- 字符频次。
- 子串、前缀、后缀。
- 字典序比较。
- 简单模拟修改后的字符串。

下游可接：

- KMP/Z 函数。
- Trie。
- Rolling Hash。
- STR-05 Manacher。

可拼接模块：

- STR-02 KMP/Z。
- STR-03 Trie/Rolling Hash。
- STR-05 Manacher。
- DP LCS/编辑距离。

模板代码：

```cpp
int to0(int pos1) {
    return pos1 - 1;
}

string substr_1idx(const string &s, int l, int r) {
    if (l < 1 || r < l || r > (int)s.size()) return "";
    return s.substr(l - 1, r - l + 1);
}

array<int, 26> count_lower(const string &s) {
    array<int, 26> cnt{};
    for (char c : s) {
        if ('a' <= c && c <= 'z') cnt[c - 'a']++;
    }
    return cnt;
}

bool is_prefix(const string &s, const string &t) {
    if (t.size() > s.size()) return false;
    for (int i = 0; i < (int)t.size(); i++) {
        if (s[i] != t[i]) return false;
    }
    return true;
}

bool is_suffix(const string &s, const string &t) {
    int n = (int)s.size(), m = (int)t.size();
    if (m > n) return false;
    for (int i = 0; i < m; i++) {
        if (s[n - m + i] != t[i]) return false;
    }
    return true;
}
```

调用示例：

```cpp
string s = "abcdef";
int l = 2, r = 4; // 题面 1-index
cout << substr_1idx(s, l, r) << "\n"; // bcd

auto cnt = count_lower(s);
cout << cnt['a' - 'a'] << "\n";
```

常见坑：

- `s[i]` 是 0-index。
- `substr(pos, len)` 第二个参数是长度，不是右端点。
- `getline` 前如果刚用过 `cin >> x`，要吃掉换行。
- `char` 可能是 signed，做 ASCII 桶建议转 `unsigned char` 或用 `vector<int>(256)`。
- 循环写 `i < s.size() - 1` 时，空串会让无符号减法出事；先转 `int n=s.size()`。

暴力/部分分替代：

- 子串匹配小数据：从每个位置开始逐字符比较。
- 子串相等小数据：直接 `substr` 比较。
- 多次修改小数据：直接改 `string`。

升级方向：

- 单模式匹配大数据 -> KMP/Z。
- 多模式前缀统计 -> Trie。
- 任意子串相等 -> Rolling Hash。
- 回文子串 -> STR-05 Manacher 或中心扩展。

最小测试样例：

```text
s = abcdef
题面 [2,4] -> substr_1idx = bcd
is_prefix(abcdef, abc) = true
is_suffix(abcdef, def) = true
```
