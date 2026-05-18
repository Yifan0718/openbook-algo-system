# MATHREF-06 计算几何、数值误差与数学建模路由

本文件定位：整理基础公式和路由，不追求完整计算几何库。考试中几何题先画图，再确认整数/浮点/精度要求。

调用示例：点/向量题先抄 `Point` 运算；直线方向用叉积；整数除法边界用安全 `floor_div/ceil_div`。

最小测试样例：`cross((1,0),(0,1))=1`，`floor_div(-3,2)=-2`，`ceil_div(-3,2)=-1`。

模块编号：MATHREF-06

模块名称：计算几何、数值误差与数学建模路由参考

什么时候用：题目出现点线面、距离、面积、方向、浮点误差、取整、数学建模或找规律。

不要什么时候用：没有几何或浮点要求时不要翻；复杂计算几何不是本资料主攻方向，优先拿基础分。

复杂度：基础公式多为 `O(1)`；枚举点对/线段常见 `O(n^2)`；二分答案多乘 `log 精度`。

依赖的标准容器：点集可用 `vector<Point>`；浮点使用 `double`，整数叉积使用 `long long` 或 `__int128`。

接口：点结构、叉积、点积、距离平方、两倍面积、EPS 比较、取整公式和建模路由。

## 1. 基础计算几何公式

题面触发词：

- 点、线段、直线、多边形。
- 距离、面积、方向、叉积。
- 判断点在线段上。
- 多边形面积、三角形面积。

使用条件：

- 坐标是整数时，方向判断优先用整数叉积。
- 面积可能是 `.5`，可用两倍面积避免浮点。
- 涉及圆、角度、距离时通常用 `double`。

公式/结论：

```text
向量 AB = B-A
点积 dot(a,b)=ax*bx+ay*by
叉积 cross(a,b)=ax*by-ay*bx

cross(B-A, C-A) > 0：C 在 AB 左侧
cross(B-A, C-A) < 0：C 在 AB 右侧
cross(B-A, C-A) = 0：A,B,C 共线

三角形两倍有向面积：
cross(B-A, C-A)

多边形两倍有向面积：
sum cross(P[i], P[i+1])
```

C++17模板或计算方式：

```cpp
using ll = long long;

struct Point {
    ll x, y;
};

Point operator-(Point a, Point b) {
    return {a.x - b.x, a.y - b.y};
}

ll dot(Point a, Point b) {
    return a.x * b.x + a.y * b.y;
}

ll cross(Point a, Point b) {
    return a.x * b.y - a.y * b.x;
}

ll cross(Point a, Point b, Point c) {
    return cross(b - a, c - a);
}

bool on_segment(Point a, Point b, Point p) {
    return cross(a, b, p) == 0 &&
           min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x) &&
           min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y);
}

__int128 polygon_area2(const vector<Point> &p) {
    int n = (int)p.size();
    __int128 s = 0;
    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n;
        s += cross(p[i], p[j]);
    }
    return s >= 0 ? s : -s;
}
```

常见坑：

- 叉积正负和点的顺序有关。
- 多边形面积公式要首尾相接。
- 坐标可达 `1e9` 时叉积可达 `1e18`，用 `long long`；更大用 `__int128`。
- 判断线段相交还要处理共线和端点。

暴力/部分分替代：

- 小坐标格点题可枚举网格点。
- 面积不会推时，把多边形拆成三角形。
- 只判断矩形/水平垂直线段时，写特判。

最小验错：

```text
A=(0,0), B=(2,0), C=(0,2)
cross(A,B,C)=4，三角形面积=2
正方形 (0,0)(1,0)(1,1)(0,1) 的 area2=2，面积=1
```

## 2. 浮点误差与取整

题面触发词：

- 实数、误差不超过 `1e-6`。
- 开方、三角函数、圆。
- 向上取整、向下取整。
- 二分答案输出小数。

使用条件：

- 浮点比较用 `eps`。
- 能用整数就不用浮点。
- 除法取整要分清正负和方向。

公式/结论：

```text
abs(a-b) <= eps 认为相等。
a < b - eps 认为 a 明显小于 b。

正整数 b 下：
floor(a/b) 对非负 a 是 a/b。
ceil(a/b) 对非负 a 是 (a+b-1)/b。
```

C++17模板或计算方式：

```cpp
const double EPS = 1e-9;

int sgn(double x) {
    if (x > EPS) return 1;
    if (x < -EPS) return -1;
    return 0;
}

long long floor_div(long long a, long long b) {
    assert(b != 0);
    __int128 aa = a, bb = b;
    __int128 q = aa / bb;
    __int128 r = aa % bb;
    if (r != 0 && ((r > 0) != (bb > 0))) q--;
    assert((__int128)LLONG_MIN <= q && q <= (__int128)LLONG_MAX);
    return (long long)q;
}

long long ceil_div(long long a, long long b) {
    assert(b != 0);
    __int128 aa = a, bb = b;
    __int128 q = aa / bb;
    __int128 r = aa % bb;
    if (r != 0 && ((r > 0) == (bb > 0))) q++;
    assert((__int128)LLONG_MIN <= q && q <= (__int128)LLONG_MAX);
    return (long long)q;
}
```

常见坑：

- 不要用 `double == double` 判断几何相等。
- `sqrt` 后再转整数可能因为误差少 1 或多 1，要回查修正。
- `ceil((double)a/b)` 对大整数可能精度丢失。
- C++ 整数除法对负数是向 0 截断，不是向下取整。

暴力/部分分替代：

- 小范围答案可以整数枚举，不用浮点二分。
- 几何距离小数据可暴力比较平方距离，避免开方。

最小验错：

```text
sgn(1e-10)=0
ceil_div(5,2)=3
floor_div(-3,2)=-2
ceil_div(-3,2)=-1
```

## 3. 常见数学建模路由

题面触发词：

- 看起来不是裸算法，而是“规律、公式、证明、构造”。
- 数据范围很大，普通模拟/DP 不可能。
- 出现周期、余数、整除、组合、期望、必胜。
- 让求第 `n` 项、方案数、最少/最多次数。

使用条件：

- 先根据数据范围判断是否必须找数学规律。
- 把题面关键词映射到本卷模块。
- 如果正解推不出，先写暴力/部分分并保留输入整理。

公式/结论：

```text
路由口诀：
余数/周期 -> 同余、gcd/lcm、CRT
除法取模 -> 先问 mod 是否质数，再选逆元
质数/因子 -> 筛法、分解、phi/mu
选法/路径 -> 组合数、二项式、Catalan、容斥
至少/没有/并集 -> 容斥
必然存在 -> 抽屉
第 n 项且 n 巨大 -> 递推、矩阵快速幂
随机平均 -> 概率期望
两人轮流 -> 博弈论
点线面 -> 叉积、点积、面积
小数答案 -> EPS、二分、取整
```

C++17模板或计算方式：

```text
建模时先写四行：
1. 变量是什么？
2. 目标是什么？
3. 限制是什么？
4. 数据范围允许什么复杂度？

再决定：
能模拟吗？
能 DP 吗？
是否有周期/组合/同余/递推公式？
```

常见坑：

- 没看数据范围，写了会超时的模拟。
- 看到“取模”就默认模数是质数。
- 把题面 1-index/0-index、闭区间/开区间混淆。
- 公式只在互质、质数、独立等条件下成立，却忘记检查。

暴力/部分分替代：

- 小数据枚举所有对象，记录结果找规律。
- 写 `solve_bruteforce()` 保底，正解推出来后替换主函数。
- 若只有大数据难，做特殊情况：全相等、全 0、树退化成链、模数为质数等。

最小验错：

```text
题面：n<=1e18，求 Fibonacci 第 n 项 mod 1e9+7
路由：第 n 项 + n 巨大 + 固定线性递推 -> 矩阵快速幂

题面：很多条件中至少满足一个
路由：至少一个/并集 -> 容斥

题面：两人轮流取石子，不能取者输
路由：博弈论 win/lose 或 SG
```
