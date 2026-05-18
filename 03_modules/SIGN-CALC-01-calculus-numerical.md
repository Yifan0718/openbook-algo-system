# SIGN-CALC-01 高等数学、微积分与数值方法

模块编号：SIGN-CALC-01

模块名称：微积分、导数积分、梯度和数值近似速查

标签：签到题、高等数学、微积分、导数、积分、梯度、牛顿法、数值积分、C++17

一句话用途：当题目把微积分概念包装成公式模拟题时，用本模块查导数、积分、梯度、数值近似和迭代规则。

题面触发词：导数、偏导、梯度、极值、凸函数、积分、面积、牛顿迭代、梯度下降、差分近似。

什么时候用：

- 题目给出明确函数和公式，要求按若干步迭代。
- 题目要求用导数判断单调、极值或用数值积分近似面积。
- 机器学习题里出现损失函数、梯度、学习率。

不要什么时候用：

- 方程求根已经给出一般一元函数，优先 `SIM-07` 的二分/牛顿模板。
- 题目要求严格符号推导，本卷只提供常见公式和数值模拟。
- 多变量优化规模大，不要自己写复杂优化器，按题面规则模拟。

复杂度：

- 单点导数公式：`O(1)`。
- 数值积分：`O(n)`。
- 迭代法：`O(iter * eval)`。

依赖的标准容器：`vector<double>`、`cmath`、`iomanip`。

输入如何整理：

```text
把函数参数和迭代次数读清楚。
若题目给学习率 lr，每次更新通常是 x -= lr * grad。
若题目给误差 eps，循环要有最大迭代次数防死循环。
```

接口：

```text
finite_diff(f,x) -> 中心差分近似导数。
trapezoid(f,l,r,n) -> 梯形积分。
simpson(f,l,r,n_even) -> Simpson 积分。
gradient_descent_step(x,grad,lr) -> 一步梯度下降。
```

常见坑：

- 三角函数 `sin/cos/tan` 参数是弧度。
- 数值积分的 `n` 越大越准，但太大可能超时。
- 牛顿法遇到导数接近 0 要停止或切换二分。
- 梯度下降是减梯度，梯度上升才是加梯度。

暴力/部分分替代：

- 不会解析求导时，用中心差分近似。
- 不会积分公式时，用梯形积分。
- 不会最优解闭式公式时，按题面迭代固定次数。

## 1. 常见导数表

| 函数 | 导数 |
|---|---|
| `C` | `0` |
| `x^n` | `n*x^(n-1)` |
| `1/x` | `-1/x^2` |
| `sqrt(x)` | `1/(2*sqrt(x))` |
| `e^x` | `e^x` |
| `a^x` | `a^x ln a` |
| `ln x` | `1/x` |
| `log_a x` | `1/(x ln a)` |
| `sin x` | `cos x` |
| `cos x` | `-sin x` |
| `tan x` | `1/cos^2 x` |
| `sigmoid(x)` | `s*(1-s)` |

## 2. 求导规则

```text
(f+g)' = f' + g'
(f*g)' = f'g + fg'
(f/g)' = (f'g - fg') / g^2
f(g(x))' = f'(g(x)) * g'(x)
```

偏导和梯度：

```text
f(x,y)=x^2+3xy+y
df/dx = 2x+3y
df/dy = 3x+1
gradient = (df/dx, df/dy)
```

## 3. 数值方法短代码

```cpp
double finite_diff(double (*f)(double), double x) {
    const double h = 1e-6;
    return (f(x + h) - f(x - h)) / (2.0 * h);
}

double trapezoid(double (*f)(double), double l, double r, int n) {
    double h = (r - l) / n;
    double ans = (f(l) + f(r)) * 0.5;
    for (int i = 1; i < n; i++) ans += f(l + h * i);
    return ans * h;
}

double simpson(double (*f)(double), double l, double r, int n) {
    if (n % 2) n++;
    double h = (r - l) / n;
    double ans = f(l) + f(r);
    for (int i = 1; i < n; i++) {
        ans += f(l + h * i) * (i % 2 ? 4.0 : 2.0);
    }
    return ans * h / 3.0;
}
```

## 4. 常见原函数和积分

| 函数 | 一个原函数 |
|---|---|
| `x^n` | `x^(n+1)/(n+1)`，`n!=-1` |
| `1/x` | `ln|x|` |
| `e^x` | `e^x` |
| `sin x` | `-cos x` |
| `cos x` | `sin x` |
| `1/(1+x^2)` | `atan x` |

## 5. 优化和机器学习常见式

| 场景 | 公式 |
|---|---|
| 平方损失 | `L=(pred-y)^2` |
| MSE | `sum((pred-y)^2)/n` |
| 一维梯度下降 | `x = x - lr * grad(x)` |
| 线性回归预测 | `pred = w*x + b` |
| logistic | `sigmoid(z)=1/(1+exp(-z))` |
| 二分类交叉熵 | `-y ln p - (1-y) ln(1-p)` |

