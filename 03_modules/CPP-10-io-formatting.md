# CPP-10：输入输出与格式化

模块编号：CPP-10

模块名称：输入输出与格式化

标签：[C++17][输入输出][格式化][快读快写][小数][对齐]

一句话用途：把 `cin/cout`、`scanf/printf`、快读快写和常见输出格式统一成考场可抄片段，避免格式错误丢分。

题面触发词：

- 多组数据、读到 EOF。
- 保留小数、四舍五入、允许误差。
- 右对齐、左对齐、补零、表格输出。
- 输入含空格字符串、整行、字符网格。
- 输入里有括号、逗号、冒号等固定标点。

什么时候用：

- 每道题开写前确认输入输出形态。
- 样例输出有固定小数位、列宽、补零或特殊标点。
- 数据量很大，普通 `cin/cout` 可能偏慢。
- 需要读整行或混合读数字和字符串。

不要什么时候用：

- 已经使用关闭同步的 `cin/cout` 时，不要再混用 `scanf/printf`。
- 普通数据量题不要先写复杂快读，`cin/cout` 关闭同步更稳。
- 字符串中包含空格时，不要用 `cin >> s` 期待读整行。

复杂度：

- 输入输出本身按字符数线性。
- 快读快写常数更小，但代码更长。

依赖的标准容器：

- `string`、`stringstream`、`vector`。
- 格式化输出使用 `<iomanip>`，`bits/stdc++.h` 已包含。

接口：

```text
cin/cout: ios::sync_with_stdio(false); cin.tie(nullptr)
scanf/printf: %d, %lld, %lf, %.2f, %04d
readInt(x): 快读整数，读到 EOF 返回 false
writeInt(x, end): 快写整数
getline(cin, line): 读整行
```

常见坑：

- `endl` 会刷新，普通换行用 `'\n'`。
- `fixed << setprecision(2)` 是小数点后 2 位，单独 `setprecision(2)` 是总有效数字。
- `setw` 只影响下一个输出项，`setfill/left/right` 会持续生效。
- `scanf` 读 `double` 用 `%lf`，`printf` 输出 `double` 用 `%f`。
- `getline` 前如果刚用过 `cin >> x`，要先 `ignore` 掉行尾换行。

暴力/部分分替代：

- 复杂格式看不懂时，先整行 `getline`，再用 `stringstream` 或手动扫描。
- 输出格式不确定时，优先照样例保持空格和换行，避免额外调试输出。

## 考场目标

输入输出的目标不是优雅，是稳定拿分：

```text
选一套 IO。
多组和 EOF 判断写对。
小数位数按题面。
空格、换行、补零、对齐按样例。
不要 freopen，不要文件 IO，不要 #pragma。
```

本模块默认 C++17、ACM/机考标准输入输出，允许 `using namespace std`。

## 1. 先选 IO 套路

| 场景 | 推荐 |
|---|---|
| 普通题、字符串多 | `cin/cout` + 关闭同步 |
| 传统格式化多、全是基础类型 | `scanf/printf` |
| 极大整数输入输出 | 自写快读快写 |
| 要读整行、含空格字符串 | `getline` |
| 复杂标点格式 | `char` 吃掉标点，或整行后 `stringstream` |

口令：

```text
不要把关闭同步后的 cin/cout 和 scanf/printf 混用。
endl 会刷新，普通换行用 '\n'。
setw 只影响下一个输出项，setfill/left/right 会持续生效。
```

## 1A. 分隔方式总表

最重要的判断：题目输入到底是“token 流”，还是“每一行有特殊含义”。

| 输入形态 | C++ 推荐 | 说明 |
|---|---|---|
| 整数/单词由空格、换行、Tab 任意分隔 | `cin >> x` | `>>` 会自动跳过所有空白，空格和换行等价 |
| 固定个数数组，但可能跨多行 | `for (...) cin >> a[i]` | 不要按行读，直接按 token 读最稳 |
| 第一行一个句子，含空格 | `getline(cin, line)` | `cin >> s` 只能读到第一个空格 |
| 前面读过数字，后面马上读整行 | `cin.ignore(..., '\n'); getline(cin,line)` | 吃掉上一行末尾换行 |
| 允许跳过空行和前导空白后读一行 | `getline(cin >> ws, line)` | 会丢掉行首空格；题目要保留行首空格时不要用 |
| 一行里有不定个整数 | `getline` + `stringstream` | 行边界有意义时用 |
| 逗号/冒号/括号固定格式 | `char` 接标点，或整行扫描 | 如 `(12,34)`、`key: value` |
| CSV/JSON/脚本等半结构化文本 | 整段 `getline`/读全文 | 翻 `SIM-03/04/05` |

口令：

```text
只要题面说“若干整数/字符串”，且没说每行含义不同，就用 cin >>。
只有行本身有意义，或字符串可能含空格，才用 getline。
```

### 空格和换行等价的例子

下面两份输入对 `cin >> n >> a[1] >> a[2] >> a[3]` 完全一样：

```text
3
10 20 30
```

```text
3 10
20
30
```

代码：

```cpp
int n;
cin >> n;
static int a[100005];
for (int i = 1; i <= n; i++) cin >> a[i];
```

### 行边界有意义的例子

每一行一个表达式、日志、名字、句子时，不能只用 `cin >>`。

```cpp
int n;
cin >> n;
cin.ignore(numeric_limits<streamsize>::max(), '\n');

for (int i = 1; i <= n; i++) {
    string line;
    getline(cin, line); // line 可以包含空格，也可以是空行
    // process line
}
```

## 2. cin/cout 常用片段

### 快速 cin/cout 骨架

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    ll sum = 0;
    for (int i = 1; i <= n; i++) {
        ll x;
        cin >> x;
        sum += x;
    }

    cout << sum << '\n';
    return 0;
}
```

### 多组数据

题面给 `T`：

```cpp
int T;
cin >> T;
while (T--) {
    solve();
}
```

题面没给 `T`，读到 EOF：

```cpp
int n, m;
while (cin >> n >> m) {
    // write one case here
}
```

### EOF 读到输入末尾就停止

EOF 题的口令：

```text
不要先判断 cin.eof()。
直接尝试读取；读成功就处理，读失败就停止。
```

读未知个整数，直到输入结束：

```cpp
long long x;
while (cin >> x) {
    // use x
}
```

每组两个数，直到输入结束：

```cpp
int n, m;
while (cin >> n >> m) {
    cout << (n + m) << '\n';
}
```

每组结构复杂时，写 `read_case()`：

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100000 + 5;
const int MAXM = 200000 + 5;

int n, m;
int a[MAXN], u[MAXM], v[MAXM];

bool read_case() {
    if (!(cin >> n >> m)) return false;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i <= m; i++) cin >> u[i] >> v[i];
    return true;
}

void solve_one_case() {
    long long sum = 0;
    for (int i = 1; i <= n; i++) sum += a[i];
    cout << sum << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    while (read_case()) {
        solve_one_case();
    }
    return 0;
}
```

注意：`read_case()` 里用到的 `n/m/a/u/v` 可以是全局变量，也可以改成传引用。关键是第一句先判断这一组是否真的存在。

如果题面给的是“第一行 T”，不要写 EOF 循环；如果题面没给 T，不要强读 T。

### 小数保留位数

```cpp
double x;
cin >> x;

cout << fixed << setprecision(2) << x << '\n'; // 保留 2 位小数
```

提醒：

```text
fixed + setprecision(2)：小数点后 2 位。
只有 setprecision(2)：总有效数字 2 位。
```

### 右对齐、左对齐、补零

```cpp
int x = 7;
string name = "Tom";

cout << setw(5) << x << '\n';                 // 默认右对齐：    7
cout << right << setw(5) << x << '\n';        // 右对齐
cout << left << setw(10) << name << "!" << '\n'; // 左对齐

cout << right << setfill('0') << setw(4) << x << '\n'; // 0007
cout << setfill(' ');                                  // 记得恢复空格填充
```

表格输出：

```cpp
cout << left << setw(12) << "name"
     << right << setw(5) << "score" << '\n';

cout << left << setw(12) << name
     << right << setw(5) << 98 << '\n';
```

## 3. scanf/printf 常用片段

### 基础骨架

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    ll sum = 0;
    for (int i = 1; i <= n; i++) {
        ll x;
        if (scanf("%lld", &x) != 1) return 0;
        sum += x;
    }

    printf("%lld\n", sum);
    return 0;
}
```

### 常用格式符

| 类型 | scanf | printf |
|---|---|---|
| `int` | `%d` | `%d` |
| `long long` | `%lld` | `%lld` |
| `double` | `%lf` | `%f` |
| `char` | `%c` | `%c` |
| C 字符串 `char[]` | `%100s` | `%s` |

`scanf` 读 `char[]` 时要给宽度，例如 `char s[105]; scanf("%100s", s);`。裸 `%s` 在输入过长时可能越界；考场更推荐 `string s; cin >> s;`。

### 小数、宽度、补零

```cpp
double x = 3.14159;
int a = 7;

printf("%.2f\n", x); // 3.14
printf("%5d\n", a);  // 宽度 5，右对齐：    7
printf("%04d\n", a); // 宽度 4，前面补 0：0007
```

多组数据：

```cpp
int T;
scanf("%d", &T);
while (T--) {
    solve();
}
```

直到 EOF：

```cpp
int n, m;
while (scanf("%d%d", &n, &m) == 2) {
    // write one case here
}
```

## 4. 自写快读快写

只在输入输出量特别大、且主要是整数时使用。用了它就全程用它，不要再混 `cin`。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

template <class T>
bool readInt(T &x) {
    int c = getchar();
    if (c == EOF) return false;

    while (c != '-' && (c < '0' || c > '9')) {
        c = getchar();
        if (c == EOF) return false;
    }

    int neg = 0;
    if (c == '-') {
        neg = 1;
        c = getchar();
    }

    using U = make_unsigned_t<T>;
    U y = 0;
    while (c >= '0' && c <= '9') {
        y = y * 10 + (U)(c - '0');
        c = getchar();
    }

    if (neg) x = (T)(U(0) - y);
    else x = (T)y;
    return true;
}

template <class T>
void writeInt(T x, char end = '\n') {
    if (x == 0) {
        putchar('0');
        putchar(end);
        return;
    }

    using U = make_unsigned_t<T>;
    U y;
    if (x < 0) {
        putchar('-');
        y = U(0) - (U)x; // 避免 LLONG_MIN 取负溢出
    } else {
        y = (U)x;
    }

    char s[50]; // long long 足够；__int128 请用 CPP-008 的专门打印模板
    int top = 0;
    while (y > 0) {
        s[top++] = char('0' + y % 10);
        y /= 10;
    }
    while (top--) putchar(s[top]);
    putchar(end);
}

int main() {
    int n;
    if (!readInt(n)) return 0;

    ll sum = 0;
    for (int i = 1; i <= n; i++) {
        ll x = 0;
        if (!readInt(x)) return 0;
        sum += x;
    }

    writeInt(sum);
    return 0;
}
```

EOF 多组：

```cpp
int n, m;
while (readInt(n) && readInt(m)) {
    // write one case here
}
```

`scanf` 版 EOF：

```cpp
int n, m;
while (scanf("%d%d", &n, &m) == 2) {
    printf("%d\n", n + m);
}
```

`scanf` 返回成功读到的变量个数；读两个整数就检查是否等于 2。不要只写 `!= EOF`，因为输入残缺时可能只读到 1 个。

## 5. 字符、整行与换行处理

### 读一个非空白字符

`cin >> c` 会跳过空格和换行：

```cpp
char c;
cin >> c;
```

`scanf(" %c", &c)` 前面的空格会跳过所有空白：

```cpp
char c;
scanf(" %c", &c);
```

### 读下一个原始字符

需要读空格或换行本身：

```cpp
char c;
cin.get(c);
```

```cpp
char c;
scanf("%c", &c);
```

### 读整行

```cpp
string line;
getline(cin, line);
```

如果前面刚用过 `cin >> n`，要先吃掉本行剩余换行：

```cpp
int n;
cin >> n;
cin.ignore(numeric_limits<streamsize>::max(), '\n');

string line;
getline(cin, line);
```

读到 EOF 的整行：

```cpp
string line;
while (getline(cin, line)) {
    // process line
}
```

空行不是 EOF。`getline` 读到空行时 `line == ""` 但循环仍然成立；只有真的没有下一行时循环才结束。

读完整剩余输入，包括换行和空格：

```cpp
string text((istreambuf_iterator<char>(cin)), istreambuf_iterator<char>());
```

如果前面刚读过一个模式名，还要读后面整段文本：

```cpp
string mode;
cin >> mode;
cin.ignore(numeric_limits<streamsize>::max(), '\n');

string text((istreambuf_iterator<char>(cin)), istreambuf_iterator<char>());
```

## 6. 复杂格式处理

### 标点固定：用 char 接住

输入形如 `(12,34)`：

```cpp
char l, comma, r;
int x, y;
cin >> l >> x >> comma >> y >> r;
```

或者：

```cpp
int x, y;
scanf(" (%d,%d)", &x, &y);
```

### 一行里有不定个整数

```cpp
string line;
while (getline(cin, line)) {
    stringstream ss(line);
    int x;
    while (ss >> x) {
        // use x
    }
}
```

### 简单逗号分隔

只适用于题目保证没有引号包裹、字段中不含逗号的简单格式。真正 CSV 翻 `SIM-04`。

```cpp
string line;
getline(cin, line);

stringstream ss(line);
string cell;
vector<string> cells(1); // 1-index
while (getline(ss, cell, ',')) {
    cells.push_back(cell);
}
```

### key=value 或 key: value

```cpp
string line;
getline(cin, line);

int p = line.find('=');
if (p != (int)string::npos) {
    string key = line.substr(0, p);
    string value = line.substr(p + 1);
}
```

冒号同理把 `'='` 改成 `':'`。若要去掉两侧空格，翻 `STR-01` 或手写 `trim`。

### 读带空格的名字和值

输入每行形如 `Tom Hanks 98`，最后一个是分数：

```cpp
string line;
getline(cin, line);

stringstream ss(line);
vector<string> parts;
string word;
while (ss >> word) parts.push_back(word);
if (!parts.empty()) {
    int score = stoi(parts.back());
    parts.pop_back();

    string name;
    for (int i = 0; i < (int)parts.size(); i++) {
        if (i) name += ' ';
        name += parts[i];
    }
}
```

### 网格读入

无空格字符网格：

```cpp
int n, m;
cin >> n >> m;
vector<string> g(n + 1);
for (int i = 1; i <= n; i++) {
    string row;
    cin >> row;
    g[i] = " " + row; // 之后访问 g[i][j]，i=1..n, j=1..m
}
```

有空格分隔的字符网格：

```cpp
const int MAXN = 1000 + 5;
const int MAXM = 1000 + 5;
static char g[MAXN][MAXM];

for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        cin >> g[i][j];
    }
}
```

## 7. 提交前格式检查

```text
题面有没有 T？没有就别强读 T。
EOF 题 while 条件是否判断了读入成功？
小数是保留几位，还是允许误差？
每个答案后有没有换行？
多个数之间是空格还是换行？
printf 的 long long 是否用 %lld？
scanf 读 double 是否用 %lf？
getline 前是否处理了上一次 cin 留下的换行？
setfill('0') 后是否恢复 setfill(' ')？
有没有 endl、调试输出、freopen、文件 IO、#pragma？
```
