# AI-15 计算图与反向模式自动求梯度

模块编号：AI-15

模块名称：表达式计算图的自动微分模板

标签：AI、自动求导、计算图、反向模式、梯度、链式法则、C++17

一句话用途：当题目给一串计算图节点，要求输出表达式值和各变量梯度时，用本模块按拓扑顺序前向算值、逆序反向传梯度。

题面触发词：

- computational graph、autograd、automatic differentiation。
- 变量、常量、节点、边、操作符。
- 求偏导、gradient、backward。
- 链式法则、反向传播。

什么时候用：

- 计算图是有向无环图，节点编号按依赖顺序给出。
- 需要对一个输出节点求所有输入变量梯度。
- 操作只有 `+ - * / sin cos exp log relu` 等常见函数。

不要什么时候用：

- 图中有环时不能直接用本模板。
- 多输出函数要看题面，是对哪个输出反传，还是多个输出梯度相加。
- `log(x)` 要求 `x > 0`，除法要求分母非 0。

复杂度：

- 前向计算：`O(节点数)`。
- 反向传播：`O(节点数)`。

依赖的标准容器：

- `vector<Node>`：1-index 存节点。
- `vector<int>`：变量节点编号。

输入如何整理：

```cpp
int n;
cin >> n;
// 第 i 行描述第 i 个节点，依赖编号必须小于 i。
```

接口：

```text
支持节点:
var value
const value
add a b
sub a b
mul a b
div a b
sin a
cos a
exp a
log a
relu a

默认输出节点是 n。
输出: value_of_node_n，然后按变量出现顺序输出梯度。
```

## 也可以封装成 AD 类

如果题面不是逐行给计算图，而是要求你在代码里动态拼公式，可以把每个操作封装成函数：

```text
int x = var(2.0)
int y = var(3.0)
int z = add(mul(x, y), sin_node(x))
backward(z)
grad(x), grad(y)
```

类封装和下面的逐行解析模板本质相同：每创建一个新节点，就把操作类型、左右儿子、当前值存进数组；最后从 root 逆序累加梯度。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Node {
    string op;
    int l = 0, r = 0;
    double val = 0;
    double grad = 0;
    bool is_var = false;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Node> a(n + 1);
    vector<int> vars;
    auto check_child = [&](int id, int cur) {
        if (id <= 0 || id >= cur) throw runtime_error("bad node reference");
    };

    for (int i = 1; i <= n; i++) {
        cin >> a[i].op;
        if (a[i].op == "var" || a[i].op == "const") {
            cin >> a[i].val;
            if (a[i].op == "var") {
                a[i].is_var = true;
                vars.push_back(i);
            }
        } else if (a[i].op == "add" || a[i].op == "sub" ||
                   a[i].op == "mul" || a[i].op == "div") {
            cin >> a[i].l >> a[i].r;
            int l = a[i].l, r = a[i].r;
            check_child(l, i);
            check_child(r, i);
            if (a[i].op == "add") a[i].val = a[l].val + a[r].val;
            if (a[i].op == "sub") a[i].val = a[l].val - a[r].val;
            if (a[i].op == "mul") a[i].val = a[l].val * a[r].val;
            if (a[i].op == "div") {
                if (fabs(a[r].val) < 1e-15) throw runtime_error("division by zero");
                a[i].val = a[l].val / a[r].val;
            }
        } else if (a[i].op == "sin" || a[i].op == "cos" ||
                   a[i].op == "exp" || a[i].op == "log" ||
                   a[i].op == "relu") {
            cin >> a[i].l;
            int l = a[i].l;
            check_child(l, i);
            if (a[i].op == "sin") a[i].val = sin(a[l].val);
            if (a[i].op == "cos") a[i].val = cos(a[l].val);
            if (a[i].op == "exp") a[i].val = exp(a[l].val);
            if (a[i].op == "log") {
                if (a[l].val <= 0) throw runtime_error("log domain error");
                a[i].val = log(a[l].val);
            }
            if (a[i].op == "relu") a[i].val = max(0.0, a[l].val);
        } else {
            throw runtime_error("unknown op");
        }
    }

    a[n].grad = 1.0;
    for (int i = n; i >= 1; i--) {
        double g = a[i].grad;
        if (a[i].op == "add") {
            a[a[i].l].grad += g;
            a[a[i].r].grad += g;
        } else if (a[i].op == "sub") {
            a[a[i].l].grad += g;
            a[a[i].r].grad -= g;
        } else if (a[i].op == "mul") {
            int l = a[i].l, r = a[i].r;
            a[l].grad += g * a[r].val;
            a[r].grad += g * a[l].val;
        } else if (a[i].op == "div") {
            int l = a[i].l, r = a[i].r;
            a[l].grad += g / a[r].val;
            a[r].grad -= g * a[l].val / (a[r].val * a[r].val);
        } else if (a[i].op == "sin") {
            int l = a[i].l;
            a[l].grad += g * cos(a[l].val);
        } else if (a[i].op == "cos") {
            int l = a[i].l;
            a[l].grad -= g * sin(a[l].val);
        } else if (a[i].op == "exp") {
            int l = a[i].l;
            a[l].grad += g * a[i].val;
        } else if (a[i].op == "log") {
            int l = a[i].l;
            a[l].grad += g / a[l].val;
        } else if (a[i].op == "relu") {
            int l = a[i].l;
            if (a[l].val > 0) a[l].grad += g;
        }
    }

    cout << fixed << setprecision(6);
    cout << a[n].val << '\n';
    for (int i = 0; i < (int)vars.size(); i++) {
        if (i > 0) cout << ' ';
        cout << a[vars[i]].grad;
    }
    cout << '\n';

    return 0;
}
```

调用示例：

```cpp
// f(x,y)=x*y+sin(x)，节点 n 是最终输出，反向传播后 var 节点上就是偏导。
```

常见坑：

- 反向模式是从输出往输入传梯度，输出节点初始梯度为 1。
- 同一个节点可能被多个后续节点使用，梯度要累加。
- 所有依赖必须已经前向算好，所以输入节点顺序要是拓扑序。
- ReLU 在 0 处不可导，本模板按 0 处理。
- 浮点答案一般输出 6 到 10 位小数。

暴力/部分分替代：

- 不会自动求导：对小数据用数值差分 `f(x+eps)-f(x-eps)`，但精度较差。
- 只支持四则运算也能拿部分分。
- 若题目给表达式字符串，先用 `SIM-03` 建 AST，再把 AST 转成计算图。

最小测试样例：

```text
输入
5
var 2
var 3
mul 1 2
sin 1
add 3 4

输出
6.909297
2.583853 2.000000
```
