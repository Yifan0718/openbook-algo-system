# SIGN-SIM-01 生活化签到模拟题模板

模块编号：SIGN-SIM-01

模块名称：生活化模拟题：日期、BMI、排名、Excel 列号、格式和小工具

标签：签到题、生活模拟、日期、BMI、排名、Excel列号、格式化、C++17

一句话用途：把最常见的生活化签到题做成可抄模板，重点保证输入输出合法、边界不丢分。

题面触发词：BMI、成绩等级、GPA、排名、同分、Excel 列号、日期差、星期、单位换算、括号匹配、状态机。

什么时候用：

- 题目是现实规则模拟，算法不难但规则细。
- 输出格式要求固定小数、补零、对齐或分类文字。
- 需要把字符串编号转换成数字，或把数字转编号。

不要什么时候用：

- 日期题涉及历史儒略历/格里高利历切换、夏令时数据库，优先 `SIM-06`。
- 表达式、JSON、脚本等复杂解析，优先 `SIM-03/04/05`。
- 方程求解优先 `SIM-07`。

复杂度：多数 `O(1)`；字符串扫描 `O(len)`；排名排序 `O(n log n)`。

依赖的标准容器：`string`、`vector`、`algorithm`、`stack`、`iomanip`。

输入如何整理：

```text
先读规则，再把每条规则写成 if/else 或小函数。
有多组数据时每组清空状态。
涉及格式输出时统一放到最后输出。
```

接口：

```text
bmi(weight,height) -> BMI。
excel_col_to_num(s) -> A1 风格列号转数字。
excel_num_to_col(x) -> 数字转列号。
days_from_civil(y,m,d) -> 日期转序号。
rank_with_ties(score) -> 同分排名。
```

常见坑：

- 身高若输入厘米，BMI 要除以 100 转米。
- Excel 列号是 1-index：A=1，Z=26，AA=27。
- 排名有 dense ranking 和 competition ranking，按题面。
- 日期差是否包含起止当天，要看题面样例。

暴力/部分分替代：

- 日期公式忘记时，小范围逐日加。
- 排名规则复杂时，先排序输出普通名次。
- 状态机不会抽象时，用 `if/else` 按字符扫描。

## 1. 高频短规则

| 模型 | 规则 |
|---|---|
| BMI | `weight_kg / height_m^2` |
| 成绩等级 | 从高到低写 `if`，避免区间重叠 |
| GPA | 加权平均：`sum(score*credit)/sum(credit)` |
| 同分排名 | 比自己分高的人数 + 1 |
| Excel 列号 | 26 进制但没有 0 |
| 括号匹配 | 栈 |
| 自动机 | `state = trans[state][input]` |

## 2. 完整可运行小工具

这个程序故意覆盖多个签到常识：BMP 大小、三角形面积、日期差、二分类指标、进制转换、BMI、Excel 列号。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const double PI = acos(-1.0);

bool triangle_ok(double a, double b, double c) {
    return a + b > c && a + c > b && b + c > a;
}

double triangle_area(double a, double b, double c) {
    if (!triangle_ok(a, b, c)) return -1.0;
    double s = (a + b + c) / 2.0;
    return sqrt(max(0.0, s * (s - a) * (s - b) * (s - c)));
}

ll bmp_pixel_bytes(ll w, ll h, int bpp) {
    ll row_bits = w * bpp;
    ll row_bytes = ((row_bits + 31) / 32) * 4;
    return row_bytes * h;
}

ll days_from_civil(int y, int m, int d) {
    y -= m <= 2;
    const int era = (y >= 0 ? y : y - 399) / 400;
    const unsigned yoe = (unsigned)(y - era * 400);
    const unsigned doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
    const unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return era * 146097LL + (ll)doe - 719468LL;
}

int hex_value(char c) {
    if ('0' <= c && c <= '9') return c - '0';
    if ('a' <= c && c <= 'f') return c - 'a' + 10;
    if ('A' <= c && c <= 'F') return c - 'A' + 10;
    return -1;
}

ll to_decimal(const string &s, int base) {
    ll ans = 0;
    for (char c : s) ans = ans * base + hex_value(c);
    return ans;
}

ll excel_col_to_num(const string &s) {
    ll ans = 0;
    for (char c : s) ans = ans * 26 + (c - 'A' + 1);
    return ans;
}

string excel_num_to_col(ll x) {
    string s;
    while (x > 0) {
        x--;
        s.push_back(char('A' + x % 26));
        x /= 26;
    }
    reverse(s.begin(), s.end());
    return s;
}

void solve_metrics() {
    int n;
    cin >> n;
    int tp = 0, fp = 0, fn = 0, tn = 0;
    for (int i = 1; i <= n; i++) {
        int y, p;
        cin >> y >> p;
        if (y == 1 && p == 1) tp++;
        else if (y == 0 && p == 1) fp++;
        else if (y == 1 && p == 0) fn++;
        else tn++;
    }
    double acc = (double)(tp + tn) / max(1, n);
    double precision = (tp + fp == 0 ? 0 : (double)tp / (tp + fp));
    double recall = (tp + fn == 0 ? 0 : (double)tp / (tp + fn));
    double f1 = (precision + recall == 0 ? 0 : 2 * precision * recall / (precision + recall));
    cout << fixed << setprecision(6) << acc << ' ' << precision << ' ' << recall << ' ' << f1 << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string mode;
    cin >> mode;
    cout << fixed << setprecision(6);

    if (mode == "triangle") {
        double a, b, c;
        cin >> a >> b >> c;
        double area = triangle_area(a, b, c);
        if (area < 0) cout << "INVALID\n";
        else cout << area << "\n";
    } else if (mode == "bmp") {
        ll w, h;
        int bpp;
        cin >> w >> h >> bpp;
        cout << bmp_pixel_bytes(w, h, bpp) << "\n";
    } else if (mode == "datediff") {
        int y1, m1, d1, y2, m2, d2;
        cin >> y1 >> m1 >> d1 >> y2 >> m2 >> d2;
        cout << llabs(days_from_civil(y1, m1, d1) - days_from_civil(y2, m2, d2)) << "\n";
    } else if (mode == "metrics") {
        solve_metrics();
    } else if (mode == "base") {
        string s;
        int b;
        cin >> s >> b;
        cout.unsetf(ios::floatfield);
        cout << to_decimal(s, b) << "\n";
    } else if (mode == "bmi") {
        double kg, cm;
        cin >> kg >> cm;
        double h = cm / 100.0;
        cout << kg / (h * h) << "\n";
    } else if (mode == "excel_to_num") {
        string s;
        cin >> s;
        cout.unsetf(ios::floatfield);
        cout << excel_col_to_num(s) << "\n";
    } else if (mode == "excel_to_col") {
        ll x;
        cin >> x;
        cout << excel_num_to_col(x) << "\n";
    }
    return 0;
}
```

## 3. 最小测试样例

```text
triangle
3 4 5
=> 6.000000

bmp
3 2 24
=> 24

datediff
2024 2 28 2024 3 1
=> 2

excel_to_num
AA
=> 27
```

