# DS-06：双指针与滑动窗口

模块编号：DS-06

模块名称：双指针、相向指针、快慢指针与滑动窗口

标签：双指针、滑动窗口、相向指针、快慢指针、连续区间、排序数组

一句话用途：把双重循环枚举区间/配对降到线性或 `O(n log n)`，常用于连续子数组、排序数组配对、去重和窗口计数。

题面触发词：

- 连续子数组、连续区间、最长/最短子段。
- 正整数数组，区间和满足条件。
- 排序数组，两数之和、三数之和。
- 不重复字符最长子串。
- 去重、原地压缩数组。
- 快慢指针、链表判环。

什么时候用：

- 左右端点都只会单调移动，不会反复回退。
- 数组全为非负数，区间和随右端扩张不减，随左端右移不增。
- 数组已排序或可以先排序，配对关系有单调性。
- 要维护一个连续窗口里的计数、和、种类数。

不要什么时候用：

- 数组有负数时，区间和不再单调，普通滑窗求“和不超过 S”可能错。
- 查询不是连续区间，而是任意子集。
- 每次移动端点后需要复杂区间最值，可能要接单调队列、树状数组或线段树。
- 排序会破坏原下标且题目需要原顺序时，不能直接排序相向指针。

复杂度：

- 同向双指针/滑动窗口：通常 `O(n)`。
- 相向双指针：排序后 `O(n log n)`，双指针扫描 `O(n)`。
- 三数之和：排序后固定一个数，内层相向指针，`O(n^2)`。

依赖的标准容器：

- 普通数组默认 1-index，上限明确时优先静态数组。
- `string`。
- `array<int, 256>` 或 `vector<int>` 维护字符计数。
- 排序配对常接 `sort`。

输入如何整理：

```cpp
const int MAXN = 200000 + 5;
int n;
cin >> n;
static long long a[MAXN];
for (int i = 1; i <= n; i++) cin >> a[i];
```

字符串窗口：

```cpp
string s;
cin >> s; // 0-index
```

接口：

```text
同向窗口：for r in 1..n expand, while bad shrink l
相向指针：sort(a+1,a+n+1), l=1, r=n, compare sum
快慢指针：slow 记录答案尾部，fast 扫描所有元素
```

输出能力：

- 最长/最短满足条件的连续区间长度。
- 满足条件的配对数量或一组配对。
- 去重后的长度。
- 字符串最长无重复子串。

下游可接：

- PrefixSum：有负数时改前缀和 + 哈希/二分。
- MonotonicQueue：窗口内最大/最小。
- Greedy：排序后相向配对。
- DP：把 `O(n^2)` 枚举前驱优化成窗口。

可拼接模块：

- CPP-003 / CPP-012 排序和二分。
- DS-01 PrefixSum。
- DS-04 MonotonicQueue。
- STR-01 / CPP-011 string。

## 一眼路由

| 题面信号 | 模板 | 前提 |
|---|---|---|
| 正整数数组，最长和不超过 S | 同向滑动窗口 | 元素非负 |
| 正整数数组，最短和至少 S | 同向滑动窗口 | 元素非负 |
| 排序数组两数之和 | 相向指针 | 有序 |
| 三数之和/三元组 | 固定一个 + 相向指针 | 先排序 |
| 删除有序数组重复项 | 快慢指针 | 有序或相邻重复 |
| 最长无重复字符子串 | 窗口 + 计数 | 字符集可计数 |
| 固定长度窗口最值 | 单调队列 | 查 max/min |

## 模板 1：最长连续子数组，和不超过 S

前提：`a[i] >= 0`。

```cpp
int longest_sum_at_most(const vector<long long> &a, long long S) {
    int n = (int)a.size() - 1;
    int ans = 0;
    int l = 1;
    long long sum = 0;

    for (int r = 1; r <= n; r++) {
        sum += a[r];
        while (l <= r && sum > S) {
            sum -= a[l];
            l++;
        }
        ans = max(ans, r - l + 1);
    }
    return ans;
}
```

调用示例：

```cpp
vector<long long> a = {0, 2, 1, 3, 2};
cout << longest_sum_at_most(a, 4) << '\n'; // 2: 1+3 或 3? 2+1
```

## 模板 2：最短连续子数组，和至少 S

前提：`a[i] >= 0`。

```cpp
int shortest_sum_at_least(const vector<long long> &a, long long S) {
    int n = (int)a.size() - 1;
    const int INF = 1000000000;
    int ans = INF;
    int l = 1;
    long long sum = 0;

    for (int r = 1; r <= n; r++) {
        sum += a[r];
        while (l <= r && sum >= S) {
            ans = min(ans, r - l + 1);
            sum -= a[l];
            l++;
        }
    }

    return ans == INF ? -1 : ans;
}
```

## 模板 3：排序数组两数之和是否存在

```cpp
bool two_sum_exists(long long a[], int n, long long target) {
    sort(a + 1, a + n + 1);
    int l = 1;
    int r = n;

    while (l < r) {
        long long sum = a[l] + a[r];
        if (sum == target) return true;
        if (sum < target) l++;
        else r--;
    }
    return false;
}
```

如果要保留原下标：

```cpp
vector<pair<long long, int>> v;
for (int i = 1; i <= n; i++) v.push_back({a[i], i});
sort(v.begin(), v.end());
```

## 模板 4：有序数组原地去重

输入为 1-index 有序数组 `a[1..n]`。

```cpp
int unique_sorted(int a[], int n) {
    if (n == 0) return 0;
    int slow = 1;
    for (int fast = 2; fast <= n; fast++) {
        if (a[fast] != a[slow]) {
            slow++;
            a[slow] = a[fast];
        }
    }
    return slow; // 去重后有效区间为 a[1..slow]
}
```

STL 版本：

```cpp
sort(a + 1, a + n + 1);
n = unique(a + 1, a + n + 1) - (a + 1); // 新长度
```

## 模板 5：最长无重复字符子串

字符串自然 0-index。

```cpp
int longest_unique_substring(const string &s) {
    vector<int> cnt(256, 0);
    int ans = 0;
    int l = 0;

    for (int r = 0; r < (int)s.size(); r++) {
        unsigned char cr = (unsigned char)s[r];
        cnt[cr]++;

        while (cnt[cr] > 1) {
            unsigned char cl = (unsigned char)s[l];
            cnt[cl]--;
            l++;
        }

        ans = max(ans, r - l + 1);
    }
    return ans;
}
```

## 模板 6：三数之和为 0，去重计数/列举

```cpp
vector<array<int, 3>> three_sum_zero(int a[], int n) {
    sort(a + 1, a + n + 1);
    vector<array<int, 3>> ans;

    for (int i = 1; i <= n; i++) {
        if (i > 1 && a[i] == a[i - 1]) continue;

        int l = i + 1;
        int r = n;
        while (l < r) {
            long long sum = (long long)a[i] + a[l] + a[r];
            if (sum == 0) {
                ans.push_back({a[i], a[l], a[r]});
                l++;
                r--;
                while (l < r && a[l] == a[l - 1]) l++;
                while (l < r && a[r] == a[r + 1]) r--;
            } else if (sum < 0) {
                l++;
            } else {
                r--;
            }
        }
    }
    return ans;
}
```

常见坑：

- 有负数数组不能直接用“sum 太大就左端右移”的滑窗逻辑。
- `while` 收缩条件写错，会漏掉刚好满足的窗口。
- 相向指针通常要求数组有序；没排序时移动方向没有意义。
- 排序后原下标丢失，需要提前存 `{value, id}`。
- 字符串窗口用 `char` 当数组下标时，稳妥写 `unsigned char`。
- 三数之和去重需要跳过重复的 `i/l/r`。

暴力/部分分替代：

- 区间题小数据：双重循环枚举 `[l,r]`，每次累计和。
- 两数之和小数据：双重循环枚举 `i,j`。
- 字符串小数据：枚举每个左端，向右用 `set` 检查重复。

升级方向：

- 双重循环区间和 -> 正数数组滑动窗口。
- 双重循环配对 -> 排序 + 相向指针。
- 固定窗口最值 -> 单调队列。
- 有负数的区间和 -> PrefixSum + 哈希/二分/数据结构。

最小测试样例：

```text
最长和不超过 S：
a = [2,1,3,2], S=4 -> 2

最短和至少 S：
a = [2,1,3,2], S=5 -> 2

两数之和：
[1,2,4,7], target=6 -> true

最长无重复子串：
abca -> 3
```
