# SIGN-LA-01 线性代数、向量与小矩阵

模块编号：SIGN-LA-01

模块名称：线性代数常识：向量、矩阵、距离、投影和小规模变换

标签：签到题、线性代数、向量、矩阵、距离、点积、叉积、Markov、C++17

一句话用途：遇到向量、矩阵、坐标变换、小规模线性代数或机器学习特征计算时，用本模块快速查公式。

题面触发词：向量、矩阵、点积、叉积、距离、投影、旋转、转移矩阵、特征、线性组合。

什么时候用：

- 坐标、几何、机器学习特征题需要向量计算。
- 题目给小矩阵，要求乘法、转置、行列式、逆矩阵或转移若干步。
- 题目出现 Markov 转移、状态概率、二维旋转。

不要什么时候用：

- 大规模线性方程组求解，优先 `SIM-07` 高斯消元。
- 复杂矩阵快速幂，优先 `MATH-05`。
- 高阶线代证明题，本卷只服务计算和模拟。

复杂度：

- 向量距离/点积：`O(d)`。
- 矩阵乘法：`O(n*m*k)`。
- 2x2 行列式/逆：`O(1)`。

依赖的标准容器：`vector<double>`、静态二维数组、`cmath`、`iomanip`。

输入如何整理：

```text
矩阵 A 的尺寸是 rows x cols。
A*B 能乘的条件：A.cols == B.rows。
向量维度必须一致。
```

接口：

```text
dot(a,b,d) -> 点积。
norm2(a,d) -> 平方范数。
dist2(a,b,d) -> 平方欧氏距离。
cross2(ax,ay,bx,by) -> 二维叉积。
mat_mul(A,B) -> 小矩阵乘法。
```

常见坑：

- 矩阵乘法不满足交换律，`A*B` 和 `B*A` 通常不同。
- 欧氏距离比较大小时可比较平方距离，少开根。
- cosine 相似度分母为 0 要特判。
- 旋转角必须是弧度。

暴力/部分分替代：

- 小矩阵直接三重循环。
- 多步转移次数很小直接重复乘；次数很大再用矩阵快速幂。
- 维度很低时直接展开公式。

## 1. 向量公式

| 名称 | 公式 |
|---|---|
| 点积 | `a dot b = sum ai*bi` |
| 范数 | `||a|| = sqrt(a dot a)` |
| 欧氏距离 | `sqrt(sum((ai-bi)^2))` |
| 曼哈顿距离 | `sum(abs(ai-bi))` |
| cosine 相似度 | `(a dot b)/(||a||*||b||)` |
| 二维叉积 | `ax*by - ay*bx` |
| 三角形有向面积 | `cross(B-A, C-A)/2` |
| 投影长度 | `(a dot b)/||b||` |

```cpp
double dot_product(const double a[], const double b[], int d) {
    double s = 0;
    for (int i = 1; i <= d; i++) s += a[i] * b[i];
    return s;
}

double dist2(const double a[], const double b[], int d) {
    double s = 0;
    for (int i = 1; i <= d; i++) {
        double t = a[i] - b[i];
        s += t * t;
    }
    return s;
}

double cross2(double ax, double ay, double bx, double by) {
    return ax * by - ay * bx;
}
```

## 2. 小矩阵公式

| 名称 | 公式 |
|---|---|
| 2x2 行列式 | `ad-bc` |
| 2x2 逆矩阵 | `1/det * [[d,-b],[-c,a]]` |
| trace | 主对角线和 |
| 对称矩阵 | `A[i][j] == A[j][i]` |
| 单位矩阵 | 对角线 1，其余 0 |
| 转置 | `B[j][i]=A[i][j]` |

```cpp
const int MAXD = 55;
double A[MAXD][MAXD], B[MAXD][MAXD], C[MAXD][MAXD];

void mat_mul(int n, int m, int k) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= k; j++) {
            C[i][j] = 0;
            for (int t = 1; t <= m; t++) {
                C[i][j] += A[i][t] * B[t][j];
            }
        }
    }
}
```

## 3. 机器学习里常见线代

| 场景 | 计算 |
|---|---|
| 线性模型打分 | `score = w dot x + b` |
| 全连接层 | `y[j] = b[j] + sum_i x[i]*W[i][j]` |
| kNN 距离 | 常用欧氏距离或曼哈顿距离 |
| 文本相似度 | cosine 或 Jaccard |
| Markov 一步转移 | `next = cur * P` |
| PCA 低维投影 | `z = x dot direction` |

