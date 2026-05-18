# SIM-03 表达式求值与 AST 语法树

模块编号：SIM-03

模块名称：表达式求值、递归下降解析与 AST 语法树

标签：表达式求值、AST、递归下降、语法树、模拟、字符串扫描、C++17

一句话用途：当题目要求计算表达式、处理括号和优先级，或者需要对表达式结构做二次处理时，用递归下降先把表达式建成 1-index AST，再递归求值或做树上 DP。

题面触发词：

- 给一个算术表达式，求它的值。
- 表达式包含括号、多位数、空格、一元负号。
- 有变量，需要先赋值再计算。
- 要输出表达式树、前缀/后缀表达式。
- 要对表达式做替换、化简、检查、统计子表达式。
- 要多次修改变量并重复求值。

什么时候用：

- 题目不是单纯 `a+b`，而是有优先级和括号。
- 双栈求值容易被一元负号、变量或后续扩展搞乱。
- 你需要保留表达式结构，而不只是得到一个数。
- 后续要在表达式树上做 DFS、DP、哈希、比较或替换。

不要什么时候用：

- 表达式只含 `+ - * /` 且只求一次值，双栈求值更短。
- 表达式长度极大且递归深度可能接近长度，递归下降可能栈深。
- 有浮点、小数、函数调用、数组下标、逻辑短路等复杂语法，本模板需要扩展。
- 除法/取模涉及负数时，要确认题目规则是否和 C++ 一致。

复杂度：

- 建树：`O(len)`。
- 单次求值：`O(节点数)`。
- 输出前缀/后缀表达式：`O(节点数)`。
- 如果多次变量赋值并重复求值，每次仍是 `O(节点数)`；可按题目做子树缓存。

数据范围参考：

- 表达式长度 `<= 2e5`：静态节点池开 `MAXNODE = 2 * len + 5` 更稳。
- 普通算术表达式中节点数不超过数字/变量/运算符数量总和。
- 本模板用 `long long` 求值，结果可能超出时改接 `SIM-02 BigInteger`。

依赖的标准容器：

- `string`：读表达式和变量名。字符串内部按 C++ 自然 0-index。
- `map<string,long long>`：变量赋值表，变量少时最稳；变量很多可改 `unordered_map`。
- 静态数组 `node[MAXNODE]`：AST 节点池，节点编号 1-index。

输入如何整理：

```cpp
int k;
cin >> k;
for (int i = 1; i <= k; i++) {
    string name;
    long long value;
    cin >> name >> value;
    vars[name] = value;
}

string expr;
getline(cin, expr); // 吃掉上一行换行
getline(cin, expr); // 真正表达式
```

接口：

```text
Parser parser(expr);
int root = parser.parse();
long long ans = eval(root, vars);
emit_prefix(root, out);
emit_postfix(root, out);
```

AST 节点约定：

| 字段 | 含义 |
|---|---|
| `type = 0` | 数字节点，使用 `value` |
| `type = 1` | 变量节点，使用 `name` |
| `type = 2` | 一元运算节点，使用 `op` 和 `left_child` |
| `type = 3` | 二元运算节点，使用 `op, left_child, right_child` |

## 为什么 AST 比直接求值更通用

直接求值只得到一个答案；AST 会保留结构：

```text
表达式：-(a + 3) * b

        *
      /   \
    neg    b
     |
     +
   /   \
  a     3
```

保留结构之后可以继续做：

- 前缀/后缀表达式输出。
- 变量替换后重复求值。
- 统计每个子表达式的值。
- 判断两个表达式结构是否相同。
- 在表达式树上做 DP，例如最小修改代价、布尔表达式翻转代价。

模板代码：

```cpp
#include <cassert>
#include <cctype>
#include <climits>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;

const int MAXNODE = 400005;

struct AstNode {
    int type; // 0 number, 1 variable, 2 unary, 3 binary
    long long value;
    string name;
    char op;
    int left_child;
    int right_child;
};

AstNode node[MAXNODE];
int node_cnt = 0;

int new_number(long long value) {
    assert(node_cnt + 1 < MAXNODE);
    ++node_cnt;
    node[node_cnt].type = 0;
    node[node_cnt].value = value;
    node[node_cnt].name.clear();
    node[node_cnt].op = 0;
    node[node_cnt].left_child = 0;
    node[node_cnt].right_child = 0;
    return node_cnt;
}

int new_variable(const string &name) {
    assert(node_cnt + 1 < MAXNODE);
    ++node_cnt;
    node[node_cnt].type = 1;
    node[node_cnt].value = 0;
    node[node_cnt].name = name;
    node[node_cnt].op = 0;
    node[node_cnt].left_child = 0;
    node[node_cnt].right_child = 0;
    return node_cnt;
}

int new_unary(char op, int child) {
    assert(node_cnt + 1 < MAXNODE);
    ++node_cnt;
    node[node_cnt].type = 2;
    node[node_cnt].value = 0;
    node[node_cnt].name.clear();
    node[node_cnt].op = op;
    node[node_cnt].left_child = child;
    node[node_cnt].right_child = 0;
    return node_cnt;
}

int new_binary(char op, int left_child, int right_child) {
    assert(node_cnt + 1 < MAXNODE);
    ++node_cnt;
    node[node_cnt].type = 3;
    node[node_cnt].value = 0;
    node[node_cnt].name.clear();
    node[node_cnt].op = op;
    node[node_cnt].left_child = left_child;
    node[node_cnt].right_child = right_child;
    return node_cnt;
}

struct Parser {
    string s;
    int pos;

    Parser(const string &expr) {
        s = expr;
        pos = 0;
    }

    void skip_spaces() {
        while (pos < (int)s.size() && isspace((unsigned char)s[pos])) pos++;
    }

    bool match(char c) {
        skip_spaces();
        if (pos < (int)s.size() && s[pos] == c) {
            pos++;
            return true;
        }
        return false;
    }

    int parse() {
        int root = parse_add_sub();
        skip_spaces();
        if (pos != (int)s.size()) {
            throw runtime_error("unexpected character");
        }
        return root;
    }

    int parse_add_sub() {
        int u = parse_mul_div_mod();
        while (true) {
            skip_spaces();
            if (pos >= (int)s.size() || (s[pos] != '+' && s[pos] != '-')) break;
            char op = s[pos++];
            int v = parse_mul_div_mod();
            u = new_binary(op, u, v);
        }
        return u;
    }

    int parse_mul_div_mod() {
        int u = parse_unary();
        while (true) {
            skip_spaces();
            if (pos >= (int)s.size() || (s[pos] != '*' && s[pos] != '/' && s[pos] != '%')) break;
            char op = s[pos++];
            int v = parse_unary();
            u = new_binary(op, u, v);
        }
        return u;
    }

    int parse_unary() {
        skip_spaces();
        if (match('+')) return parse_unary();
        if (match('-')) return new_unary('-', parse_unary());
        return parse_primary();
    }

    int parse_primary() {
        skip_spaces();
        if (match('(')) {
            int u = parse_add_sub();
            if (!match(')')) {
                throw runtime_error("missing right parenthesis");
            }
            return u;
        }

        if (pos < (int)s.size() && isdigit((unsigned char)s[pos])) {
            __int128 value = 0;
            while (pos < (int)s.size() && isdigit((unsigned char)s[pos])) {
                value = value * 10 + (s[pos] - '0');
                if (value > LLONG_MAX) {
                    throw runtime_error("integer literal overflow");
                }
                pos++;
            }
            return new_number((long long)value);
        }

        if (pos < (int)s.size() && (isalpha((unsigned char)s[pos]) || s[pos] == '_')) {
            string name;
            while (pos < (int)s.size()) {
                unsigned char ch = (unsigned char)s[pos];
                if (!isalnum(ch) && s[pos] != '_') break;
                name.push_back(s[pos]);
                pos++;
            }
            return new_variable(name);
        }

        throw runtime_error("bad primary expression");
    }
};

long long checked_ll(__int128 x) {
    if (x < (__int128)LLONG_MIN || x > (__int128)LLONG_MAX) {
        throw runtime_error("integer overflow");
    }
    return (long long)x;
}

long long eval_ast(int u, const map<string, long long> &vars) {
    if (node[u].type == 0) return node[u].value;
    if (node[u].type == 1) {
        auto it = vars.find(node[u].name);
        if (it == vars.end()) {
            throw runtime_error("undefined variable");
        }
        return it->second;
    }
    if (node[u].type == 2) {
        long long x = eval_ast(node[u].left_child, vars);
        if (node[u].op == '-' && x == LLONG_MIN) {
            throw runtime_error("integer overflow");
        }
        if (node[u].op == '-') return -x;
        return x;
    }

    long long a = eval_ast(node[u].left_child, vars);
    long long b = eval_ast(node[u].right_child, vars);
    if (node[u].op == '+') return checked_ll((__int128)a + b);
    if (node[u].op == '-') return checked_ll((__int128)a - b);
    if (node[u].op == '*') return checked_ll((__int128)a * b);
    if (node[u].op == '/') {
        if (b == 0) throw runtime_error("division by zero");
        if (a == LLONG_MIN && b == -1) throw runtime_error("integer overflow");
        return a / b;
    }
    if (node[u].op == '%') {
        if (b == 0) throw runtime_error("modulo by zero");
        if (a == LLONG_MIN && b == -1) throw runtime_error("integer overflow");
        return a % b;
    }
    throw runtime_error("bad operator");
}

void emit_prefix(int u, vector<string> &out) {
    if (node[u].type == 0) {
        out.push_back(to_string(node[u].value));
        return;
    }
    if (node[u].type == 1) {
        out.push_back(node[u].name);
        return;
    }
    if (node[u].type == 2) {
        out.push_back("neg");
        emit_prefix(node[u].left_child, out);
        return;
    }
    out.push_back(string(1, node[u].op));
    emit_prefix(node[u].left_child, out);
    emit_prefix(node[u].right_child, out);
}

void emit_postfix(int u, vector<string> &out) {
    if (node[u].type == 0) {
        out.push_back(to_string(node[u].value));
        return;
    }
    if (node[u].type == 1) {
        out.push_back(node[u].name);
        return;
    }
    if (node[u].type == 2) {
        emit_postfix(node[u].left_child, out);
        out.push_back("neg");
        return;
    }
    emit_postfix(node[u].left_child, out);
    emit_postfix(node[u].right_child, out);
    out.push_back(string(1, node[u].op));
}

void write_tokens(const vector<string> &tokens) {
    for (int i = 0; i < (int)tokens.size(); i++) {
        if (i) cout << ' ';
        cout << tokens[i];
    }
    cout << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int k;
    if (!(cin >> k)) return 0;

    map<string, long long> vars;
    for (int i = 1; i <= k; i++) {
        string name;
        long long value;
        cin >> name >> value;
        vars[name] = value;
    }

    string expr;
    getline(cin, expr);
    string line;
    while (getline(cin, line)) {
        if (!expr.empty()) expr.push_back(' ');
        expr += line;
    }

    try {
        Parser parser(expr);
        int root = parser.parse();
        cout << eval_ast(root, vars) << '\n';
        cout << node_cnt << '\n';

        vector<string> prefix;
        emit_prefix(root, prefix);
        write_tokens(prefix);

        vector<string> postfix;
        emit_postfix(root, postfix);
        write_tokens(postfix);
    } catch (const exception &e) {
        cout << "ERROR\n";
    }

    return 0;
}
```

调用示例：

```cpp
map<string, long long> vars;
vars["a"] = 10;
vars["b"] = 4;

Parser parser("-(a + 3) * b");
int root = parser.parse();
cout << eval_ast(root, vars) << '\n';
```

常见坑：

- 字符串扫描天然 0-index，这是局部例外；AST 节点编号仍是 1-index。
- 一元负号和二元减号必须分开处理：`-3` 是 unary，`a-b` 是 binary。
- `parse_unary()` 要放在乘除模下面、括号/数字/变量上面。
- C++ 整数除法向 0 取整，负数 `/` 和 `%` 规则要和题面核对。
- `long long` 可能溢出；表达式结果很大时把 `eval_ast` 的返回值改成 `BigInteger`。
- `MAXNODE` 要按表达式长度防御性开大，普通表达式可开 `2 * len + 5`。
- 如果表达式有 `^`，要单独加一层优先级，且通常是右结合。
- 如果题目有函数调用如 `max(a,b)`，需要在 `parse_primary()` 里扩展。

暴力/部分分替代：

- 只含数字、`+ - * /`、括号且只求值：可以先写双栈直接求值。
- 没有括号且只有 `+ -`：直接从左到右扫描。
- 只有单字符变量：变量名可用数组 `val[256]`，不用 `map`。
- 需要多次换变量求值：AST 建一次，之后每次只更新 `vars` 并 DFS 求值。
- 不会写完整 AST 时，先支持无变量、无一元负号的版本拿部分分。

最小测试样例：

```text
输入
2
a 10
b 4
-(a + 3) * b + 20 / 3

输出
-46
10
+ * neg + a 3 b / 20 3
a 3 + neg b * 20 3 / +
```

补充自测：

```text
输入
3
x -7
y 3
z 10
x / y + x % y + z * (2 + 3)

输出
47
13
+ + / x y % x y * z + 2 3
x y / x y % + z 2 3 + * +
```
