# STR-02 KMP 与 Z 函数

模块编号：STR-02

模块名称：单模式串匹配：KMP 与 Z 函数

标签：[字符串][KMP][Z函数][模式匹配][0-index]

一句话用途：在线性时间内查找模式串在文本串中的所有出现位置，并处理前后缀匹配问题。

索引约定：

```text
本模块内部全部使用 0-index。
返回的匹配位置是文本串 text 的 0-index 起点。
若题目要求输出 1-index，输出时写 pos + 1。
KMP 的 pi[i] 表示 s[0..i] 的最长真前后缀长度。
Z[i] 表示 s[i..] 与 s[0..] 的最长公共前缀长度。
```

题面触发词：

- 模式串在文本串中出现几次。
- 找所有匹配位置。
- 最长相同前后缀、border。
- 字符串周期、循环节。
- 每个后缀和原串的最长公共前缀。

什么时候用：

- 单个模式串匹配一个或多个文本。
- 需要线性复杂度。
- 前后缀关系明显。
- 需要判断字符串最小周期。

不要什么时候用：

- 多个模式串同时匹配，优先 Trie/AC 自动机。
- 只是一次短字符串匹配，暴力即可。
- 任意两个子串比较，优先 Rolling Hash。

复杂度：

- KMP 前缀函数：`O(n)`。
- KMP 匹配：`O(n+m)`。
- Z 函数：`O(n)`。

数据范围参考：

- `|s|, |text| <= 1e6`：KMP/Z 都可用。
- 多测总长度很大时，按总长度线性处理。

依赖的标准容器：

- `string`。
- `vector<int>`，下标 `0..n-1`。

输入如何整理：

```cpp
string text, pat;
cin >> text >> pat;
```

接口：

```text
prefix_function(s) -> pi 数组
kmp_find_all(text, pat) -> pat 在 text 中所有 0-index 起点
z_function(s) -> z 数组
minimal_period(s) -> 最小周期长度
```

输出能力：

- 模式串出现次数。
- 所有匹配位置。
- 最长 border。
- 最小周期。
- 后缀与整串的 LCP。

下游可接：

- 字符串周期 + gcd/lcm。
- DP 中的自动机状态。
- 题面要求输出 1-index 位置时接索引转换。

可拼接模块：

- STR-01 基础操作。
- STR-03 Rolling Hash。
- MATH-01 gcd/lcm。

模板代码：

```cpp
vector<int> prefix_function(const string &s) {
    int n = (int)s.size();
    vector<int> pi(n, 0);
    for (int i = 1; i < n; i++) {
        int j = pi[i - 1];
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) j++;
        pi[i] = j;
    }
    return pi;
}

vector<int> kmp_find_all(const string &text, const string &pat) {
    vector<int> ans;
    if (pat.empty()) return ans;
    string s = pat + "#" + text;
    vector<int> pi = prefix_function(s);
    int m = (int)pat.size();
    for (int i = m + 1; i < (int)s.size(); i++) {
        if (pi[i] == m) {
            ans.push_back(i - 2 * m); // text 中的 0-index 起点
        }
    }
    return ans;
}

vector<int> z_function(const string &s) {
    int n = (int)s.size();
    vector<int> z(n, 0);
    int l = 0, r = 0;
    for (int i = 1; i < n; i++) {
        if (i <= r) z[i] = min(r - i + 1, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] - 1 > r) {
            l = i;
            r = i + z[i] - 1;
        }
    }
    return z;
}

int minimal_period(const string &s) {
    int n = (int)s.size();
    if (n == 0) return 0;
    vector<int> pi = prefix_function(s);
    int p = n - pi[n - 1];
    if (n % p == 0) return p;
    return n;
}
```

调用示例：

```cpp
string text = "ababa", pat = "aba";
auto pos = kmp_find_all(text, pat);
for (int p : pos) cout << p + 1 << " "; // 题目要 1-index 时输出 1 3

string s = "ababab";
cout << minimal_period(s) << "\n"; // 2
```

常见坑：

- 返回位置是 0-index，输出题面位置通常要 `+1`。
- 拼接 `pat + "#" + text` 时，分隔符 `#` 不能出现在字符集里；若可能出现，换一个不存在的字符。
- `pi[i]` 是长度，不是下标。
- `minimal_period` 要检查 `n % p == 0`。
- 空模式串一般题目不会给，模板里直接返回空结果。

暴力/部分分替代：

- `|text| * |pat| <= 1e7`：枚举起点逐字符比较。
- 周期小数据：枚举周期长度 `p`，检查每个字符是否等于 `s[i%p]`。
- 前后缀小数据：枚举长度后比较 `substr`。

升级方向：

- 多模式匹配 -> AC 自动机。
- 大量子串相等/LCP 查询 -> Rolling Hash 或后缀数组，后缀数组低优先级。
- KMP 自动机 DP -> 在 pi 基础上构建转移。

最小测试样例：

```text
text=ababa, pat=aba
0-index 匹配位置：0 2
1-index 输出位置：1 3

s=ababab
minimal_period=2
```
