# DIVIDE-00 分治与倍增

模块编号：DIVIDE-00

模块名称：Divide and Conquer、MergeSort 与 Binary Lifting

标签：[分治][归并排序][逆序对][倍增][二进制拆分]

一句话用途：把大问题拆成左右两半递归解决，再合并答案；把重复跳转/操作按 `2^k` 预处理，快速处理大步数。

题面触发词：

- 分治、递归处理区间。
- 归并排序、逆序对。
- 每次分成左右两半。
- 跳 `k` 步、祖先、倍增。
- 操作次数很大，按二进制拆分。

什么时候用：

- 区间问题可以拆成 `[l,mid]` 和 `[mid+1,r]`。
- 左右答案能在线性或 `O(log n)` 代价合并。
- 反复执行同一种“跳转”或“转移”，可以预处理 `2^k` 次效果。

不要什么时候用：

- 左右两边强依赖，合并代价接近 `O(n^2)` 且无法优化。
- 数据量很小，直接暴力更快写。
- 倍增的下一步不确定，不能提前得到 `up[0][x]`。

复杂度：

- 标准分治：若每层合并 `O(n)`，总复杂度 `O(n log n)`。
- 归并排序：`O(n log n)`。
- 逆序对：`O(n log n)`。
- 倍增预处理：`O(n log K)`，单次跳转 `O(log K)`。

数据范围参考：

- `n <= 2e5`：归并排序/逆序对标准可过。
- 逆序对数量最大约 `n*(n-1)/2`，答案用 `long long`。
- `k <= 1e18`：倍增 `LOG = 60` 足够；为了防御性覆盖更大的 `long long` 正数步数，可直接用 `LOG = 63`。

依赖的标准容器：

- 1-index 数组。
- `vector<long long>`。
- 倍增表 `up[LOG][N]` 或 `vector<vector<int>>`。

输入如何整理：

```cpp
cin >> n;
for (int i = 1; i <= n; i++) cin >> a[i];
```

接口：

```text
solve(l,r) -> 分治递归框架
merge_sort(l,r) -> 排序并返回逆序对数
build_up(n) -> 预处理倍增表
jump(x,k) -> 从 x 跳 k 步
```

输出能力：

- 排序后的数组。
- 逆序对数量。
- 第 `k` 个后继、`k` 级祖先、函数图跳转结果。

下游可接：

- CDQ 分治，低优先级。
- 树上倍增 LCA。
- 快速幂、矩阵快速幂。
- SparseTable。

可拼接模块：

- `DIVIDE-00 + DS-02 树状数组`：逆序对也可用树状数组。
- `DIVIDE-00 + GRAPH-09 LCA`：倍增父亲。
- `DIVIDE-00 + MATH-02 FastPower`：二进制拆分思想一致。

分治递归模板：

```cpp
void solve(int l, int r) {
    if (l >= r) {
        // 处理单个元素
        return;
    }

    int mid = (l + r) / 2;
    solve(l, mid);
    solve(mid + 1, r);

    // 合并左右两边的答案
}
```

归并排序与逆序对模板：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const int N = 200000 + 5;

int n;
ll a[N], tmp[N];

ll merge_sort(int l, int r) {
    if (l >= r) return 0;
    int mid = (l + r) / 2;
    ll ans = 0;
    ans += merge_sort(l, mid);
    ans += merge_sort(mid + 1, r);

    int i = l, j = mid + 1, k = l;
    while (i <= mid && j <= r) {
        if (a[i] <= a[j]) {
            tmp[k++] = a[i++];
        } else {
            tmp[k++] = a[j++];
            ans += mid - i + 1;
        }
    }
    while (i <= mid) tmp[k++] = a[i++];
    while (j <= r) tmp[k++] = a[j++];
    for (int p = l; p <= r; p++) a[p] = tmp[p];
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];

    cout << merge_sort(1, n) << '\n';
    return 0;
}
```

倍增跳转模板：

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 200000 + 5;
const int LOG = 63;

int n;
int up[LOG][N];

void build_up() {
    // up[0][x] 必须在 0..n 内，0 表示无后继/无父亲。
    for (int k = 1; k < LOG; k++) {
        for (int x = 1; x <= n; x++) {
            int y = up[k - 1][x];
            up[k][x] = (y == 0 ? 0 : up[k - 1][y]);
        }
    }
}

int jump(int x, long long step) {
    for (int k = 0; k < LOG; k++) {
        if ((step >> k) & 1LL) {
            x = up[k][x];
            if (x == 0) break;
        }
    }
    return x;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> n >> q;
    for (int x = 1; x <= n; x++) cin >> up[0][x];
    build_up();

    while (q--) {
        int x;
        long long k;
        cin >> x >> k;
        cout << jump(x, k) << '\n';
    }
    return 0;
}
```

倍增思想简表：

| 场景 | `up[k][x]` 表示 | 查询方式 |
| --- | --- | --- |
| 函数图跳转 | 从 `x` 走 `2^k` 步到哪里 | 把 `k` 拆成二进制 |
| LCA | `x` 的 `2^k` 级祖先 | 先拉平深度，再同时上跳 |
| SparseTable | 从 `i` 开始长度 `2^k` 的区间答案 | 两段覆盖查询区间 |
| 快速幂 | 当前底数的 `2^k` 次方 | 指数二进制位为 1 就乘 |
| 矩阵快速幂 | 转移矩阵执行 `2^k` 次 | 同快速幂 |

调用示例：

```cpp
ll inv_count = merge_sort(1, n);

up[0][x] = parent[x];
build_up();
int ancestor = jump(x, k);
```

常见坑：

- 逆序对答案必须用 `long long`。
- 归并时用 `a[i] <= a[j]`，相等不算逆序对。
- `mid = (l + r) / 2` 在普通竞赛范围够用；超大坐标用 `l + (r-l)/2`。
- 分治递归别漏 `l >= r` 边界。
- 倍增表的 `up[k][0]` 保持为 `0`，作为跳出树的哨兵。
- `LOG` 要覆盖最大步数，不只是覆盖 `n`；`1e18` 用 `60` 足够，懒得细算时用 `63` 更稳。

暴力/部分分替代：

- 逆序对 `n <= 5000`：双重循环计数。
- 排序题：直接 `sort(a + 1, a + n + 1)`，不写归并。
- 跳 `k` 步且 `k <= 1e5`：循环跳。
- 单次祖先查询：一直爬父亲。

升级方向：

- 归并排序 -> CDQ 分治处理三维偏序。
- 普通倍增 -> LCA 倍增。
- 静态区间最值 -> SparseTable。
- 重复线性转移 -> 矩阵快速幂。

最小测试样例：

```text
逆序对输入：
5
5 4 2 3 1

输出：
9

倍增跳转：
1 -> 2 -> 3 -> 3
jump(1,2)=3
```
