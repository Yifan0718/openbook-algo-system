# SIM-02 手写高精度 BigInteger 类

模块编号：SIM-02

模块名称：带符号高精度整数 BigInteger 类

标签：高精度、大整数、BigInteger、运算符重载、加减乘除模、C++17、考场备用

一句话用途：当题目要求整数位数超过 `long long`，且需要把高精度整数当普通整数一样做 `+ - * / %`、比较、输入输出时，直接抄这个类。

题面触发词：

- 高精度整数、大整数、任意长度整数。
- 不能使用 Java BigInteger / Python int。
- 结果可能有几百位、几千位。
- 需要高精度加、减、乘、除、取模、比较。
- 需要负数。

什么时候用：

- 题目需要完整整数运算，而不是只做加法或乘小整数。
- 大整数可能为负。
- 需要多次复用同一套运算，手写字符串函数容易乱。
- 数据范围位数中等，`O(n^2)` 乘法和长除法可以接受。

不要什么时候用：

- 只需要非负加减或乘小整数时，`SIM-01` 更短、更快、更好抄。
- 位数达到 `1e5` 且需要大量乘法/除法时，本类太慢，可能要 FFT/NTT 或专门算法。
- 只需要取模一个普通 `long long mod`，边读边取模更短。
- 题目只比较大小，不要抄完整类，`strip0 + cmp_big` 就够。

复杂度：

- 比较、取相反数、绝对值：`O(n)` 或 `O(1)`。
- 加法/减法：`O(n)`。
- 乘法：`O(n*m)`。
- 除法/取模：十进制长除法，约 `O(n^2)`，常数小但不适合超大位数密集除法。
- 这里 `n,m` 指十进制位数。

数据范围参考：

- 几百位、几千位：本类通常可用。
- 上万位：加减可用，乘除要谨慎。
- 只做一次或少量乘除：可先用本类拿分。

依赖的标准容器：

- `vector<int>`：低位在前，每个元素一位十进制数字。
- `string`：输入输出。
- `iostream`：流输入输出。
- `algorithm`：反转和比较辅助。
- `cassert`：除数为 0 时防御。

输入如何整理：

```cpp
BigInteger a, b;
cin >> a >> b;
```

支持：

```text
普通十进制整数
+123
-123
00000123
-00000123
0
-0  // 会规范成 0
```

接口：

```text
BigInteger x;
BigInteger x(long long);
BigInteger x(string);

x.to_string()
x.is_zero()
x.abs()

比较：== != < > <= >=
一元：+x, -x
四则：+ - * / %
复合：+= -= *= /= %=
自增自减：++x, x++, --x, x--
输入输出：cin >> x, cout << x
```

输出能力：

- 输出带符号十进制整数。
- 除法向 0 取整，和 C++ 整数除法一致。
- 取模符号跟被除数一致，和 C++ 整数 `%` 一致。

下游可接：

- 模拟题、递推题、计数题的大整数输出。
- 字符串扫描。
- 暴力/部分分中需要精确大整数的场景。

可拼接模块：

- `SIM-01`：轻量非负高精度。
- `MATH-02`：如果只需要模普通整数，用快速幂/取模。
- `DP-20`：方案数超出 `long long` 且题目不取模时，`dp` 值可改成 `BigInteger`。

## 模型选择卡

| 需求 | 优先用 |
|---|---|
| 非负加减、乘小整数 | `SIM-01` |
| 带符号、比较、完整 `+ - * / %` | `SIM-02 BigInteger` |
| 只要 `x mod m` | 边读边取模 |
| 大量乘大整数 | 低优先级，可能要 FFT/NTT |

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

struct BigInteger {
    // 十进制逐位存储，d[0] 是个位。sign: -1, 0, 1。
    vector<int> d;
    int sign;

    BigInteger(long long x = 0) {
        *this = x;
    }

    BigInteger(const string &s) {
        this->read(s);
    }

    BigInteger& operator=(long long x) {
        d.clear();
        if (x == 0) {
            sign = 0;
            return *this;
        }
        sign = 1;
        unsigned long long y;
        if (x < 0) {
            sign = -1;
            y = 0ULL - (unsigned long long)x;
        } else {
            y = (unsigned long long)x;
        }
        while (y > 0) {
            d.push_back((int)(y % 10));
            y /= 10;
        }
        return *this;
    }

    void read(const string &s) {
        d.clear();
        sign = 1;

        int i = 0;
        while (i < (int)s.size() && isspace((unsigned char)s[i])) i++;
        if (i < (int)s.size() && (s[i] == '+' || s[i] == '-')) {
            if (s[i] == '-') sign = -1;
            i++;
        }
        while (i < (int)s.size() && s[i] == '0') i++;

        for (int j = (int)s.size() - 1; j >= i; j--) {
            if (!isdigit((unsigned char)s[j])) {
                throw runtime_error("bad integer literal");
            }
            d.push_back(s[j] - '0');
        }
        trim();
    }

    string to_string() const {
        if (sign == 0) return "0";
        string s;
        if (sign < 0) s.push_back('-');
        for (int i = (int)d.size() - 1; i >= 0; i--) {
            s.push_back(char('0' + d[i]));
        }
        return s;
    }

    bool is_zero() const {
        return sign == 0;
    }

    BigInteger abs() const {
        BigInteger res = *this;
        if (res.sign < 0) res.sign = 1;
        return res;
    }

    void trim() {
        while (!d.empty() && d.back() == 0) d.pop_back();
        if (d.empty()) sign = 0;
    }

    static int abs_cmp(const BigInteger &a, const BigInteger &b) {
        if (a.d.size() != b.d.size()) {
            return a.d.size() < b.d.size() ? -1 : 1;
        }
        for (int i = (int)a.d.size() - 1; i >= 0; i--) {
            if (a.d[i] != b.d[i]) return a.d[i] < b.d[i] ? -1 : 1;
        }
        return 0;
    }

    void abs_add(const BigInteger &b) {
        int n = max(d.size(), b.d.size());
        d.resize(n, 0);
        int carry = 0;
        for (int i = 0; i < n; i++) {
            int cur = d[i] + carry;
            if (i < (int)b.d.size()) cur += b.d[i];
            d[i] = cur % 10;
            carry = cur / 10;
        }
        if (carry) d.push_back(carry);
        if (!d.empty() && sign == 0) sign = 1;
    }

    // 要求 |*this| >= |b|，只改绝对值，不改 sign。
    void abs_sub(const BigInteger &b) {
        int borrow = 0;
        for (int i = 0; i < (int)d.size(); i++) {
            int cur = d[i] - borrow - (i < (int)b.d.size() ? b.d[i] : 0);
            if (cur < 0) {
                cur += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }
            d[i] = cur;
        }
        trim();
    }

    BigInteger operator+() const {
        return *this;
    }

    BigInteger operator-() const {
        BigInteger res = *this;
        res.sign = -res.sign;
        return res;
    }

    BigInteger& operator+=(const BigInteger &b) {
        if (b.sign == 0) return *this;
        if (sign == 0) {
            *this = b;
            return *this;
        }
        if (sign == b.sign) {
            abs_add(b);
            return *this;
        }

        int cmp = abs_cmp(*this, b);
        if (cmp == 0) {
            d.clear();
            sign = 0;
        } else if (cmp > 0) {
            abs_sub(b);
        } else {
            BigInteger tmp = b;
            tmp.abs_sub(*this);
            *this = tmp;
        }
        return *this;
    }

    BigInteger& operator-=(const BigInteger &b) {
        *this += -b;
        return *this;
    }

    BigInteger& operator*=(const BigInteger &b) {
        if (is_zero() || b.is_zero()) {
            d.clear();
            sign = 0;
            return *this;
        }

        vector<int> res(d.size() + b.d.size() + 1, 0);
        for (int i = 0; i < (int)d.size(); i++) {
            int carry = 0;
            for (int j = 0; j < (int)b.d.size() || carry; j++) {
                int cur = res[i + j] + carry;
                if (j < (int)b.d.size()) cur += d[i] * b.d[j];
                res[i + j] = cur % 10;
                carry = cur / 10;
            }
        }

        d = res;
        sign *= b.sign;
        trim();
        return *this;
    }

    void shift10_add(int digit) {
        assert(0 <= digit && digit <= 9);
        if (sign == 0) {
            if (digit == 0) return;
            d.push_back(digit);
            sign = 1;
            return;
        }
        d.insert(d.begin(), digit);
        trim();
    }

    static pair<BigInteger, BigInteger> divmod(BigInteger a, BigInteger b) {
        if (b.is_zero()) {
            throw runtime_error("BigInteger division by zero");
        }
        if (a.is_zero()) return {BigInteger(0), BigInteger(0)};

        int qsign = a.sign * b.sign;
        int rsign = a.sign;
        a.sign = 1;
        b.sign = 1;

        if (abs_cmp(a, b) < 0) {
            a.sign = rsign;
            a.trim();
            return {BigInteger(0), a};
        }

        BigInteger q, cur;
        q.sign = 1;
        q.d.assign(a.d.size(), 0);

        for (int i = (int)a.d.size() - 1; i >= 0; i--) {
            cur.shift10_add(a.d[i]);
            int x = 0;
            while (abs_cmp(cur, b) >= 0) {
                cur.abs_sub(b);
                x++;
            }
            q.d[i] = x;
        }

        q.sign = qsign;
        q.trim();
        cur.sign = cur.d.empty() ? 0 : rsign;
        cur.trim();
        return {q, cur};
    }

    BigInteger& operator/=(const BigInteger &b) {
        *this = divmod(*this, b).first;
        return *this;
    }

    BigInteger& operator%=(const BigInteger &b) {
        *this = divmod(*this, b).second;
        return *this;
    }

    BigInteger& operator++() {
        *this += 1;
        return *this;
    }

    BigInteger operator++(int) {
        BigInteger old = *this;
        ++(*this);
        return old;
    }

    BigInteger& operator--() {
        *this -= 1;
        return *this;
    }

    BigInteger operator--(int) {
        BigInteger old = *this;
        --(*this);
        return old;
    }

    friend bool operator<(const BigInteger &a, const BigInteger &b) {
        if (a.sign != b.sign) return a.sign < b.sign;
        if (a.sign == 0) return false;
        int cmp = abs_cmp(a, b);
        return a.sign > 0 ? cmp < 0 : cmp > 0;
    }

    friend bool operator==(const BigInteger &a, const BigInteger &b) {
        return a.sign == b.sign && a.d == b.d;
    }

    friend bool operator!=(const BigInteger &a, const BigInteger &b) {
        return !(a == b);
    }

    friend bool operator>(const BigInteger &a, const BigInteger &b) {
        return b < a;
    }

    friend bool operator<=(const BigInteger &a, const BigInteger &b) {
        return !(b < a);
    }

    friend bool operator>=(const BigInteger &a, const BigInteger &b) {
        return !(a < b);
    }

    friend BigInteger operator+(BigInteger a, const BigInteger &b) {
        a += b;
        return a;
    }

    friend BigInteger operator-(BigInteger a, const BigInteger &b) {
        a -= b;
        return a;
    }

    friend BigInteger operator*(BigInteger a, const BigInteger &b) {
        a *= b;
        return a;
    }

    friend BigInteger operator/(BigInteger a, const BigInteger &b) {
        a /= b;
        return a;
    }

    friend BigInteger operator%(BigInteger a, const BigInteger &b) {
        a %= b;
        return a;
    }

    friend ostream& operator<<(ostream &out, const BigInteger &x) {
        return out << x.to_string();
    }

    friend istream& operator>>(istream &in, BigInteger &x) {
        string s;
        in >> s;
        x.read(s);
        return in;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    while (q--) {
        string op;
        cin >> op;
        if (op == "inc") {
            BigInteger a;
            cin >> a;
            cout << ++a << '\n';
        } else if (op == "dec") {
            BigInteger a;
            cin >> a;
            cout << --a << '\n';
        } else if (op == "abs") {
            BigInteger a;
            cin >> a;
            cout << a.abs() << '\n';
        } else {
            BigInteger a, b;
            cin >> a >> b;
            if (op == "+") cout << a + b << '\n';
            else if (op == "-") cout << a - b << '\n';
            else if (op == "*") cout << a * b << '\n';
            else if (op == "/") cout << a / b << '\n';
            else if (op == "%") cout << a % b << '\n';
            else if (op == "<") cout << (a < b) << '\n';
            else if (op == ">") cout << (a > b) << '\n';
            else if (op == "==") cout << (a == b) << '\n';
            else if (op == "!=") cout << (a != b) << '\n';
        }
    }

    return 0;
}
```

调用示例：

```cpp
BigInteger a = "999999999999999999999999999";
BigInteger b = "-123456789";

cout << a + b << '\n';
cout << a * b << '\n';
cout << a / 7 << '\n';
cout << a % 7 << '\n';

if (a > b) {
    cout << "a bigger\n";
}
```

常见坑：

- 除数不能为 0；模板中会抛出 `runtime_error`，不要依赖 `assert` 防御运行时输入。
- 本模板除法向 0 取整，`-1000 / 7 = -142`。
- 本模板取模符号跟被除数一致，`-1000 % 7 = -6`。
- 十进制逐位存储很容易看懂，但乘除不适合超大位数密集计算。
- `read()` 会忽略前导零，`-0000` 会规范成 `0`。
- 如果只做非负加减乘小数，不要抄完整类，`SIM-01` 更短。
- 如果要和普通整数混算，`BigInteger(long long)` 构造函数会自动接上，例如 `a + 1`、`a / 7`。

暴力/部分分替代：

- 小位数子任务先用 `long long`。
- 只需要比较大小时，只写字符串比较。
- 只需要 `% mod` 时，边读边取模。
- 乘法不会写时，乘小整数可用 `SIM-01 mul_small`。
- 除法不会写时，小数据可重复减法先拿分。

升级方向：

```text
long long -> SIM-01 非负字符串函数 -> SIM-02 BigInteger 类
O(nm) 乘法 -> Karatsuba / FFT / NTT
十进制慢除法 -> 高基数长除法
只对普通 mod 取模 -> 边读边取模
```

最小测试样例：

```text
输入
5
+ 999 1
- 1 1000
* -123 45
/ 1000 7
% -1000 7

输出
1000
-999
-5535
142
-6
```

补充自测：

```text
输入
9
/ -1000 7
% 1000 -7
< -5 3
> 00010 9
== -0000 0
!= 123 0123
inc -1
dec 0
abs -12345

输出
-142
6
1
1
1
0
0
-1
12345
```
