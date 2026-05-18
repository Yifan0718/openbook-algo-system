# SIM-01 模拟、字符串扫描与高精度

模块编号：SIM-01

模块名称：模拟、字符串扫描与高精度

标签：模拟、字符串、高精度、大整数、非负整数、考场模板

一句话用途：题面让你“按规则一步一步做”或整数超过 `long long` 时，用字符串和稳定循环先拿分。

题面触发词：

- 模拟过程、按顺序执行操作、每一轮变化。
- 字符串表示的数字、位数很大、结果很大。
- 高精度加法、高精度减法、高精度乘小整数。
- 不能使用内置大整数。

什么时候用：

- 规则直接，按题面顺序执行即可。
- 数字长度可能超过 18 位，`long long` 会溢出。
- 只涉及非负大整数的加、减、比较、乘小整数。
- 需要把字符逐个扫描，统计、替换、进位或借位。

不要什么时候用：

- 大整数需要乘大整数、除法、取模很多次，本模块只提供基础版本。
- 题目本质是 DP、图论、贪心，模拟只是读入或输出辅助。
- 数字长度很小且保证在 `long long` 内，直接整数更快更短。

复杂度：

- 字符串扫描：`O(n)`。
- 大整数比较：`O(len)`。
- 大整数加法：`O(len)`。
- 大整数减法：`O(len)`，要求 `a >= b`。
- 大整数乘小整数：`O(len * 位运算常数)`，通常记 `O(len)`。

数据范围参考：

- 位数 `<= 1e5`：字符串高精度可用。
- 操作次数很多时，总复杂度按“总位数扫描次数”估算。
- 乘数 `k` 用 `long long` 存，题面保证是小整数时使用。

依赖的标准容器：

- `string`：存非负大整数。
- `vector<int>`：存操作、方向或状态，数组默认 1-index。

输入如何整理：

```cpp
string a, b;
cin >> a >> b;
a = strip0(a);
b = strip0(b);

int n;
cin >> n;
vector<int> op(n + 1);
for (int i = 1; i <= n; i++) cin >> op[i];
```

模拟整理顺序：

1. 把题面状态写成变量或数组。
2. 把每一步操作写成一个循环。
3. 把边界判断写成 `inside/check` 函数。
4. 字符串数字先 `strip0`，再比较或计算。

接口：

```text
strip0(s) -> 去掉前导零，空结果返回 "0"。
cmp_big(a,b) -> 比较非负大整数，返回 -1/0/1。
add_big(a,b) -> 非负大整数加法。
sub_big(a,b) -> 非负大整数减法，要求 a >= b。
mul_small(a,k) -> 非负大整数乘 long long 小整数 k，k 可为负。
inside(x,y,n,m) -> 网格模拟边界判断。
```

输出能力：

- 输出模拟后的状态。
- 输出大整数计算结果。
- 输出比较结果。

下游可接：

- STR-01 基础字符串操作。
- BASIC-00 控制结构。
- BRUTE 部分分模拟。
- MATH 快速幂或取模模块。

可拼接模块：

- 大整数输入接 `strip0`。
- 高精度加减接模拟计数。
- 字符串扫描接 KMP/Hash 前的预处理。
- 小数据模拟接暴力部分分。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

string strip0(string s) {
    int i = 0;
    while (i + 1 < (int)s.size() && s[i] == '0') {
        i++;
    }
    s = s.substr(i);
    if (s.empty()) return "0";
    return s;
}

int cmp_big(string a, string b) {
    a = strip0(a);
    b = strip0(b);
    if (a.size() != b.size()) {
        return a.size() < b.size() ? -1 : 1;
    }
    if (a == b) return 0;
    return a < b ? -1 : 1;
}

string add_big(string a, string b) {
    a = strip0(a);
    b = strip0(b);
    int i = (int)a.size() - 1;
    int j = (int)b.size() - 1;
    int carry = 0;
    string res;

    while (i >= 0 || j >= 0 || carry) {
        int x = carry;
        if (i >= 0) x += a[i--] - '0';
        if (j >= 0) x += b[j--] - '0';
        res.push_back(char('0' + x % 10));
        carry = x / 10;
    }

    reverse(res.begin(), res.end());
    return strip0(res);
}

string sub_big(string a, string b) {
    a = strip0(a);
    b = strip0(b);
    int i = (int)a.size() - 1;
    int j = (int)b.size() - 1;
    int borrow = 0;
    string res;

    while (i >= 0) {
        int x = (a[i] - '0') - borrow;
        int y = (j >= 0 ? b[j] - '0' : 0);
        if (x < y) {
            x += 10;
            borrow = 1;
        } else {
            borrow = 0;
        }
        res.push_back(char('0' + (x - y)));
        i--;
        j--;
    }

    reverse(res.begin(), res.end());
    return strip0(res);
}

string mul_small(string a, ll k) {
    a = strip0(a);
    if (a == "0" || k == 0) return "0";

    __int128 mag = k;
    bool neg = false;
    if (mag < 0) {
        neg = true;
        mag = -mag;
    }

    __int128 carry = 0;
    string res;
    for (int i = (int)a.size() - 1; i >= 0; i--) {
        __int128 cur = (__int128)(a[i] - '0') * mag + carry;
        res.push_back(char('0' + cur % 10));
        carry = cur / 10;
    }
    while (carry > 0) {
        res.push_back(char('0' + carry % 10));
        carry /= 10;
    }

    reverse(res.begin(), res.end());
    string ans = strip0(res);
    return neg ? "-" + ans : ans;
}

bool inside(int x, int y, int n, int m) {
    return 1 <= x && x <= n && 1 <= y && y <= m;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string op;
    cin >> op;

    if (op == "add") {
        string a, b;
        cin >> a >> b;
        cout << add_big(a, b) << '\n';
    } else if (op == "sub") {
        string a, b;
        cin >> a >> b;
        if (cmp_big(a, b) < 0) {
            cout << '-' << sub_big(b, a) << '\n';
        } else {
            cout << sub_big(a, b) << '\n';
        }
    } else if (op == "mul") {
        string a;
        ll k;
        cin >> a >> k;
        cout << mul_small(a, k) << '\n';
    } else if (op == "cmp") {
        string a, b;
        cin >> a >> b;
        cout << cmp_big(a, b) << '\n';
    }

    return 0;
}
```

调用示例：

```cpp
string a = "000999";
string b = "1";

cout << strip0(a) << '\n';          // 999
cout << add_big(a, b) << '\n';      // 1000
cout << sub_big("1000", "1") << '\n'; // 999
cout << mul_small("123", 45) << '\n'; // 5535
cout << cmp_big("0010", "9") << '\n'; // 1

// 按字符模拟进位或统计。
string s;
cin >> s;
int cnt = 0;
for (int i = 0; i < (int)s.size(); i++) {
    if (isdigit((unsigned char)s[i])) cnt++;
}
```

常见坑：

- 高精度数字必须当字符串读，不能先读进 `long long`。
- 减法模板要求 `a >= b`；如果题目可能为负，要先比较并输出负号。
- `strip0("0000")` 必须返回 `"0"`。
- 字符转数字用 `c - '0'`，数字转字符用 `char('0' + x)`。
- 乘小整数时 `k` 的绝对值和进位用 `__int128`，避免 `LLONG_MIN` 取负和中间乘法溢出。
- 字符串下标是 0-index，普通数组按本书约定优先 1-index。
- `isdigit` 传入非 ASCII 字符时建议转 `unsigned char`。
- 多次模拟操作时，每组数据要重置状态和答案。

暴力/部分分替代：

- 位数 `<= 18` 的子任务可先用 `long long`。
- 乘小整数很小，可用重复加法拿小数据。
- 复杂模拟不会优化时，先按题面逐步执行，拿小范围分。
- 大整数只需要比较大小时，不要写完整加减，先写 `strip0 + cmp_big`。

升级方向：

```text
long long 溢出 -> string 高精度
重复加法乘小数 -> mul_small
大量取模 -> 边读边取模
大整数乘大整数 -> 另写 O(nm) 乘法或 FFT，低优先级
```

最小测试样例：

```text
输入
add
999
1

输出
1000
```

补充自测：

```text
cmp 0010 9 -> 1
sub 1000 1 -> 999
mul 123 45 -> 5535
add 0000 000 -> 0
```
