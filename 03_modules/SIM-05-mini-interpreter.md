# SIM-05 手写编译器 / 解释器骨架

模块编号：SIM-05

模块名称：小语言解释器：Tokenizer、表达式 AST、语句 AST 与执行环境

标签：模拟、解释器、编译器、AST、Tokenizer、Parser、变量环境、if、while、print、C++17

一句话用途：当题目设计了一个“小语言”或“脚本规则”，要求你解释执行赋值、输出、条件、循环时，用 tokenizer + AST + 环境表拆成三层写，避免把所有逻辑塞进字符串扫描。

题面触发词：

- 给一段程序/脚本，要求输出执行结果。
- 有变量、赋值、表达式、`print`。
- 有 `if/else`、`while`、块 `{}`。
- 要模拟一个简单编译器、解释器、虚拟机、规则引擎。
- 需要解析语句，而不只是单个表达式。

什么时候用：

- 输入已经像一门小语言，而不是普通数据。
- 语句之间有状态，例如变量会被赋值和更新。
- 需要区分词法、语法、执行，题面规则较多。
- `SIM-03` 只能处理表达式，不够处理语句流。

不要什么时候用：

- 题面只是普通表达式求值，优先 `SIM-03`。
- 题目给的是汇编式指令，例如 `ADD x y`，直接逐行模拟更短。
- 语言包含函数、递归、数组、字符串变量、作用域闭包等，本模板需要扩展。
- 循环可能无限执行，必须按题目要求设置步数上限或检测循环。

复杂度：

- Tokenizer：`O(len)`。
- Parser 建 AST：`O(token数)`。
- 执行：约等于实际执行语句次数；`while` 可能远大于源码长度。
- 表达式求值：每次按表达式子树大小。

数据范围参考：

- 源码长度 `<= 2e5`：节点池按 `2 * token数` 防御性开。
- 变量数量不大时用 `map<string,long long>` 最稳；变量很多可改 `unordered_map`。
- 本模板设置 `EXEC_LIMIT = 1000000` 防止死循环；正式题按题面调整。

依赖的标准容器：

- `string`：源码和 token 文本。字符串扫描局部使用 0-index。
- `vector<Token>`：token 序列，手动放哨兵后按 1-index 访问。
- 静态数组：表达式节点、语句节点均为 1-index。
- `map<string,long long>`：变量环境。

输入如何整理：

```cpp
string code((istreambuf_iterator<char>(cin)), istreambuf_iterator<char>());
```

接口：

```text
vector<Token> tokens = tokenize(code);
Parser parser(tokens);
int root = parser.parse_program();
exec_stmt(root);
```

## 三层结构

| 层 | 做什么 | 不做什么 |
|---|---|---|
| Tokenizer | 把字符流切成数字、标识符、运算符、括号、分号 | 不判断语句是否合法 |
| Parser | 按语法建表达式 AST 和语句 AST | 不执行变量赋值 |
| Executor | 根据 AST 修改变量环境并输出 | 不再扫描原始字符串 |

## 本模板支持的语法

```text
program     := statement*
statement   := name = expr ;
            | print expr ;
            | if (expr) statement else statement
            | while (expr) statement
            | { statement* }
            | ;

expr        := comparison
comparison  := add ( (==|!=|<|<=|>|>=) add )*
add         := mul ( (+|-) mul )*
mul         := unary ( (*|/|%) unary )*
unary       := (+|-|!) unary | primary
primary     := number | name | (expr)
```

模板代码：

```cpp
#include <cassert>
#include <cctype>
#include <climits>
#include <iostream>
#include <iterator>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;

using ll = long long;

const int MAXEXPR = 400005;
const int MAXSTMT = 200005;
const ll EXEC_LIMIT = 1000000;

struct Token {
    int type; // 0 end, 1 number, 2 identifier, 3 symbol/operator
    string text;
    ll value;
};

vector<Token> tokenize(const string &s) {
    vector<Token> tok(1);
    int i = 0;
    while (i < (int)s.size()) {
        unsigned char ch = (unsigned char)s[i];
        if (isspace(ch)) {
            i++;
            continue;
        }

        if (isdigit(ch)) {
            __int128 value = 0;
            int start = i;
            while (i < (int)s.size() && isdigit((unsigned char)s[i])) {
                value = value * 10 + (s[i] - '0');
                if (value > LLONG_MAX) {
                    throw runtime_error("integer literal overflow");
                }
                i++;
            }
            tok.push_back({1, s.substr(start, i - start), (ll)value});
            continue;
        }

        if (isalpha(ch) || s[i] == '_') {
            int start = i;
            while (i < (int)s.size()) {
                unsigned char c = (unsigned char)s[i];
                if (!isalnum(c) && s[i] != '_') break;
                i++;
            }
            tok.push_back({2, s.substr(start, i - start), 0});
            continue;
        }

        if (i + 1 < (int)s.size()) {
            string two = s.substr(i, 2);
            if (two == "==" || two == "!=" || two == "<=" || two == ">=") {
                tok.push_back({3, two, 0});
                i += 2;
                continue;
            }
        }

        string one_chars = "+-*/%(){};=<>!";
        if (one_chars.find(s[i]) != string::npos) {
            tok.push_back({3, string(1, s[i]), 0});
            i++;
            continue;
        }

        throw runtime_error("bad character");
    }
    tok.push_back({0, "END", 0});
    return tok;
}

struct ExprNode {
    int type; // 0 number, 1 variable, 2 unary, 3 binary
    ll value;
    string name;
    string op;
    int left_child;
    int right_child;
};

struct StmtNode {
    int type; // 0 block, 1 assign, 2 print, 3 if, 4 while
    string name;
    int expr;
    int first_child;
    int second_child;
    vector<int> body;
};

ExprNode expr_node[MAXEXPR];
StmtNode stmt_node[MAXSTMT];
int expr_cnt = 0;
int stmt_cnt = 0;

int new_expr_number(ll value) {
    assert(expr_cnt + 1 < MAXEXPR);
    ++expr_cnt;
    expr_node[expr_cnt] = {0, value, "", "", 0, 0};
    return expr_cnt;
}

int new_expr_variable(const string &name) {
    assert(expr_cnt + 1 < MAXEXPR);
    ++expr_cnt;
    expr_node[expr_cnt] = {1, 0, name, "", 0, 0};
    return expr_cnt;
}

int new_expr_unary(const string &op, int child) {
    assert(expr_cnt + 1 < MAXEXPR);
    ++expr_cnt;
    expr_node[expr_cnt] = {2, 0, "", op, child, 0};
    return expr_cnt;
}

int new_expr_binary(const string &op, int left_child, int right_child) {
    assert(expr_cnt + 1 < MAXEXPR);
    ++expr_cnt;
    expr_node[expr_cnt] = {3, 0, "", op, left_child, right_child};
    return expr_cnt;
}

int new_stmt(int type) {
    assert(stmt_cnt + 1 < MAXSTMT);
    ++stmt_cnt;
    stmt_node[stmt_cnt].type = type;
    stmt_node[stmt_cnt].name.clear();
    stmt_node[stmt_cnt].expr = 0;
    stmt_node[stmt_cnt].first_child = 0;
    stmt_node[stmt_cnt].second_child = 0;
    stmt_node[stmt_cnt].body.clear();
    return stmt_cnt;
}

bool is_cmp_op(const string &op) {
    return op == "==" || op == "!=" || op == "<" || op == "<=" || op == ">" || op == ">=";
}

struct Parser {
    vector<Token> tok;
    int pos;

    Parser(const vector<Token> &tokens) {
        tok = tokens;
        pos = 1;
    }

    Token cur() const {
        return tok[pos];
    }

    bool match(const string &text) {
        if (cur().text == text) {
            pos++;
            return true;
        }
        return false;
    }

    void expect(const string &text) {
        if (!match(text)) throw runtime_error("unexpected token");
    }

    int parse_program() {
        int u = new_stmt(0);
        while (cur().type != 0) {
            stmt_node[u].body.push_back(parse_statement());
        }
        return u;
    }

    int parse_statement() {
        if (match(";")) {
            return new_stmt(0);
        }

        if (match("{")) {
            int u = new_stmt(0);
            while (!match("}")) {
                if (cur().type == 0) throw runtime_error("missing block end");
                stmt_node[u].body.push_back(parse_statement());
            }
            return u;
        }

        if (cur().text == "print") {
            pos++;
            int u = new_stmt(2);
            stmt_node[u].expr = parse_expr();
            expect(";");
            return u;
        }

        if (cur().text == "if") {
            pos++;
            expect("(");
            int cond = parse_expr();
            expect(")");
            int then_stmt = parse_statement();
            int else_stmt = 0;
            if (cur().text == "else") {
                pos++;
                else_stmt = parse_statement();
            }
            int u = new_stmt(3);
            stmt_node[u].expr = cond;
            stmt_node[u].first_child = then_stmt;
            stmt_node[u].second_child = else_stmt;
            return u;
        }

        if (cur().text == "while") {
            pos++;
            expect("(");
            int cond = parse_expr();
            expect(")");
            int body_stmt = parse_statement();
            int u = new_stmt(4);
            stmt_node[u].expr = cond;
            stmt_node[u].first_child = body_stmt;
            return u;
        }

        if (cur().type == 2) {
            string name = cur().text;
            pos++;
            expect("=");
            int e = parse_expr();
            expect(";");
            int u = new_stmt(1);
            stmt_node[u].name = name;
            stmt_node[u].expr = e;
            return u;
        }

        throw runtime_error("bad statement");
    }

    int parse_expr() {
        return parse_compare();
    }

    int parse_compare() {
        int u = parse_add_sub();
        while (is_cmp_op(cur().text)) {
            string op = cur().text;
            pos++;
            int v = parse_add_sub();
            u = new_expr_binary(op, u, v);
        }
        return u;
    }

    int parse_add_sub() {
        int u = parse_mul_div_mod();
        while (cur().text == "+" || cur().text == "-") {
            string op = cur().text;
            pos++;
            int v = parse_mul_div_mod();
            u = new_expr_binary(op, u, v);
        }
        return u;
    }

    int parse_mul_div_mod() {
        int u = parse_unary();
        while (cur().text == "*" || cur().text == "/" || cur().text == "%") {
            string op = cur().text;
            pos++;
            int v = parse_unary();
            u = new_expr_binary(op, u, v);
        }
        return u;
    }

    int parse_unary() {
        if (cur().text == "+" || cur().text == "-" || cur().text == "!") {
            string op = cur().text;
            pos++;
            return new_expr_unary(op, parse_unary());
        }
        return parse_primary();
    }

    int parse_primary() {
        if (cur().type == 1) {
            ll value = cur().value;
            pos++;
            return new_expr_number(value);
        }
        if (cur().type == 2) {
            string name = cur().text;
            pos++;
            return new_expr_variable(name);
        }
        if (match("(")) {
            int u = parse_expr();
            expect(")");
            return u;
        }
        throw runtime_error("bad expression");
    }
};

map<string, ll> env;
vector<ll> output_values;
ll exec_steps = 0;

void tick() {
    ++exec_steps;
    if (exec_steps > EXEC_LIMIT) throw runtime_error("execution limit exceeded");
}

ll get_var(const string &name) {
    auto it = env.find(name);
    if (it == env.end()) return 0;
    return it->second;
}

ll checked_ll(__int128 x) {
    if (x < (__int128)LLONG_MIN || x > (__int128)LLONG_MAX) {
        throw runtime_error("integer overflow");
    }
    return (ll)x;
}

ll eval_expr(int u) {
    ExprNode &e = expr_node[u];
    if (e.type == 0) return e.value;
    if (e.type == 1) return get_var(e.name);
    if (e.type == 2) {
        ll x = eval_expr(e.left_child);
        if (e.op == "+") return x;
        if (e.op == "-") {
            if (x == LLONG_MIN) throw runtime_error("integer overflow");
            return -x;
        }
        if (e.op == "!") return x == 0;
    }

    ll a = eval_expr(e.left_child);
    ll b = eval_expr(e.right_child);
    if (e.op == "+") return checked_ll((__int128)a + b);
    if (e.op == "-") return checked_ll((__int128)a - b);
    if (e.op == "*") return checked_ll((__int128)a * b);
    if (e.op == "/") {
        if (b == 0) throw runtime_error("division by zero");
        if (a == LLONG_MIN && b == -1) throw runtime_error("integer overflow");
        return a / b;
    }
    if (e.op == "%") {
        if (b == 0) throw runtime_error("modulo by zero");
        if (a == LLONG_MIN && b == -1) throw runtime_error("integer overflow");
        return a % b;
    }
    if (e.op == "==") return a == b;
    if (e.op == "!=") return a != b;
    if (e.op == "<") return a < b;
    if (e.op == "<=") return a <= b;
    if (e.op == ">") return a > b;
    if (e.op == ">=") return a >= b;
    throw runtime_error("bad operator");
}

void exec_stmt(int u) {
    if (u == 0) return;
    tick();
    StmtNode &st = stmt_node[u];

    if (st.type == 0) {
        for (int v : st.body) exec_stmt(v);
    } else if (st.type == 1) {
        env[st.name] = eval_expr(st.expr);
    } else if (st.type == 2) {
        output_values.push_back(eval_expr(st.expr));
    } else if (st.type == 3) {
        if (eval_expr(st.expr) != 0) exec_stmt(st.first_child);
        else exec_stmt(st.second_child);
    } else if (st.type == 4) {
        while (eval_expr(st.expr) != 0) {
            tick();
            exec_stmt(st.first_child);
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string code((istreambuf_iterator<char>(cin)), istreambuf_iterator<char>());
    if (code.empty()) return 0;

    try {
        vector<Token> tokens = tokenize(code);
        Parser parser(tokens);
        int root = parser.parse_program();
        exec_stmt(root);
        for (ll x : output_values) {
            cout << x << '\n';
        }
    } catch (const exception &e) {
        cout << "ERROR\n";
    }

    return 0;
}
```

调用示例：

```text
x = 0;
sum = 0;
while (x < 5) {
    x = x + 1;
    sum = sum + x;
}
print sum;
```

常见坑：

- 解释器题一定要先分层：字符 -> token -> AST -> 执行，不要边扫描边执行复杂语句。
- `if/while` 的条件表达式统一用非 0 为真，0 为假。
- 未定义变量本模板默认值为 0；如果题目要求报错，就在 `get_var()` 改成 throw。
- `while` 可能死循环，要按题目要求设置 `EXEC_LIMIT` 或检测状态。
- 这里没有局部作用域，所有变量都是全局变量；函数和局部变量要额外加环境栈。
- C++ 除法和取模按向 0 取整，负数规则要和题目核对。
- 关键字 `print/if/else/while` 不应再当普通变量名。
- 语句 AST 节点和表达式 AST 节点都是 1-index；token vector 也从 1 开始放有效 token。

暴力/部分分替代：

- 如果只有逐行指令，例如 `SET x 1`、`ADD x 2`，直接按行模拟，不必建 AST。
- 如果没有 `if/while`，只写赋值和 `print`。
- 如果表达式只含数字和变量，不含括号优先级，先用从左到右扫描拿部分分。
- 如果循环次数很小，甚至可以不建语句 AST，边解析边执行；但遇到 `while` 需要回跳时 AST 更稳。
- 函数/作用域不会写时，先把所有变量当全局，拿无函数子任务分。

升级方向：

```text
表达式 AST -> 语句 AST -> 全局环境
全局环境 -> 环境栈/局部作用域
解释执行 -> 生成三地址码/字节码
while 执行 -> 状态检测/步数限制
long long 值 -> BigInteger / string / bool / array
```

最小测试样例：

```text
输入
x = 0;
sum = 0;
while (x < 5) {
    x = x + 1;
    sum = sum + x;
}
print sum;

输出
15
```

补充自测：

```text
输入
a = 3;
b = 4;
print -(a + b) * 2;
if (a * b == 12) {
    print 1;
} else {
    print 0;
}
print a / 2;

输出
-14
1
1
```

补充自测 2：

```text
输入
i = 3;
while (i != 0) {
    print i;
    i = i - 1;
}
if (!i) print 99; else print 0;

输出
3
2
1
99
```
