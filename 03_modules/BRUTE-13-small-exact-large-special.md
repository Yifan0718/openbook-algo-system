# BRUTE-13：小数据精确 + 大数据特判

模块编号：BRUTE-13

模块名称：小数据精确 + 大数据特判

标签：部分分、特判、小数据暴力、大数据兜底

一句话用途：对小范围输入写精确算法，对大范围输入写合法输出或明显特判，最大化部分分。

题面触发词：

- 子任务按数据范围给分。
- `n <= 20` 一档，`n <= 2e5` 一档。
- 有特殊性质：全相等、链、树、无边、已排序。
- 大数据正解不会。

适用场景：

- 题目有明显分档。
- 小数据能暴力或 memo 精确解决。
- 大数据至少能处理几种简单结构。

什么时候用：

- 不确定满分算法。
- 可以用 `if` 分流不同范围。
- 特殊性质容易检测。

不要什么时候用：

- 特判会破坏正确的小数据逻辑。
- 大数据兜底输出不合法。
- 分流条件和题目子任务条件不一致。

复杂度：

- 小数据：按所选精确算法，例如 `O(2^n)`。
- 大数据特判：通常 `O(n)` 或 `O(n log n)`。

数据范围参考：

- `n <= 20`：子集 / DFS / 状压。
- `n <= 40`：折半。
- 大数据：检测全相等、单调、无边、树链等特殊形态。

依赖的标准容器：

- `vector`
- `algorithm`

输入如何整理：

- 先完整读入。
- 写几个布尔函数检测特殊性质：`all_equal()`、`is_sorted()`、`is_small()`。
- 按“最确定正确”的分支优先返回。

接口：

```cpp
long long solve_small_exact();
long long solve_large_special();
```

输出能力：

- 小数据精确答案。
- 大数据特殊情况精确答案。
- 其他情况合法兜底。

下游可接：

- BRUTE-02 合法兜底输出。
- BRUTE-14 提交版本路线。

可拼接模块：

- BRUTE-04 组合 DFS。
- BRUTE-05 子集枚举。
- BRUTE-12 折半枚举。

模板代码：

注意：本完整程序是“分流策略演示”，不是最大子集和通解。`n <= 20` 精确，`n > 20` 只处理全非负等特殊情况，其余输出合法兜底；真实题目必须按题意替换兜底分支。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int n;
vector<ll> a;

bool all_non_negative() {
    for (int i = 1; i <= n; i++) {
        if (a[i] < 0) return false;
    }
    return true;
}

ll solve_small_exact() {
    ll best = 0;
    int total = 1 << n;
    for (int mask = 0; mask < total; mask++) {
        ll sum = 0;
        for (int i = 1; i <= n; i++) {
            if (mask & (1 << (i - 1))) sum += a[i];
        }
        best = max(best, sum);
    }
    return best;
}

ll solve_large_special() {
    if (all_non_negative()) {
        ll sum = 0;
        for (int i = 1; i <= n; i++) sum += a[i];
        return sum;
    }
    // 兜底：空集合法时答案至少为 0。实际题目要按题意修改。
    return 0;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    a.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];

    if (n <= 20) cout << solve_small_exact() << '\n';
    else cout << solve_large_special() << '\n';
    return 0;
}
```

调用示例：

```cpp
if (n <= 20) {
    cout << solve_small_exact() << '\n';
} else if (all_non_negative()) {
    cout << solve_large_special() << '\n';
} else {
    cout << 0 << '\n';
}
```

常见坑：

- 小数据用 `1 << n`，但 `n` 可能超过 30，必须先判断。
- 特判条件不充分，输出了错误答案。
- 兜底答案不合法。
- 分支里忘记多测清空变量。
- 特殊性质检测本身复杂度太高。

暴力/部分分替代：

- 先只写 `n <= 20` 精确。
- 再加 `n <= 40` 折半。
- 再加全相等、全非负、全非正、已排序、无边等特判。

升级方向：

```text
小数据 DFS -> 小数据 memo -> 折半 -> 大数据特殊性质 -> 正式算法
```

最小测试样例：

```text
输入：
3
-1 5 2

输出：
7
```
