# v0.2 例题扩展 Worker B

负责范围：

- 第 1 卷：C++17 / STL / 输入输出。
- 第 9 卷：Python 互补卷。

编写原则：

- 第 1 卷代码全部使用 C++17，`#include <bits/stdc++.h>` 与 `using namespace std;`，数组和顺序数据默认按 1-index 组织。
- 第 9 卷强调 Python 是 C++ 主战之外的补位工具，只有在高精度、哈希状态、标准库枚举、字符串解析等场景明显省事时才建议使用。
- 每题给出完整可运行代码，不使用文件读写。

覆盖矩阵：

| 归属卷 | 例题 | 核心覆盖 |
|---|---|---|
| 第 1 卷 | V01-EX01 | `cin/cout`、`vector`、固定小数 |
| 第 1 卷 | V01-EX02 | `scanf/printf`、补零、格式化输出 |
| 第 1 卷 | V01-EX03 | `getline`、EOF、`string`、`map` |
| 第 1 卷 | V01-EX04 | `unordered_map`、快速查询 |
| 第 1 卷 | V01-EX05 | `priority_queue`、自定义优先级 |
| 第 1 卷 | V01-EX06 | `set`、去重排序 |
| 第 1 卷 | V01-EX07 | `sort`、`lower_bound`、1-index 位置 |
| 第 1 卷 | V01-EX08 | `vector`、`string`、自定义排序 |
| 第 1 卷 | V01-EX09 | `getline` 混合 token 输入、整行统计 |
| 第 1 卷 | V01-EX10 | `sort`、`lower_bound`、`upper_bound`、区间计数 |
| 第 9 卷 | V09-EX01 | Python 大整数 |
| 第 9 卷 | V09-EX02 | `dict` / `Counter`、EOF token 读入 |
| 第 9 卷 | V09-EX03 | `set`、元组判重 |
| 第 9 卷 | V09-EX04 | `heapq` |
| 第 9 卷 | V09-EX05 | `deque`、BFS |
| 第 9 卷 | V09-EX06 | `itertools.permutations` 小数据枚举 |
| 第 9 卷 | V09-EX07 | EOF 按行读入 |
| 第 9 卷 | V09-EX08 | `sys.setrecursionlimit`、递归 DFS |
| 第 9 卷 | V09-EX09 | `functools.lru_cache`、记忆化 |
| 第 9 卷 | V09-EX10 | `deque`、滑动窗口 |

***

## 第 1 卷：C++17 / STL / 输入输出例题

### V01-EX01 班级成绩汇总

- 归属卷：第 1 卷
- 覆盖模块：CPP-001 主骨架与输入输出、CPP-002 vector、CPP-10 格式化输出
- 考场用途：练习 `cin/cout` 快速骨架、1-index `vector` 存数、`fixed << setprecision` 输出平均值。

**题目描述：** 给定一个班级 `n` 名同学的整数成绩，输出总分、平均分和最高分。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数，表示每名同学的成绩。

**输出格式：** 输出三行，分别为 `sum=总分`、`average=平均分`、`max=最高分`。平均分保留两位小数。

**样例输入：**
```text
5
80 90 75 100 95
```

**样例输出：**
```text
sum=440
average=88.00
max=100
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> score(n + 1);
    long long sum = 0;
    int best = 0;
    for (int i = 1; i <= n; i++) {
        cin >> score[i];
        sum += score[i];
        best = max(best, score[i]);
    }

    double avg = 1.0 * sum / n;
    cout << "sum=" << sum << '\n';
    cout << fixed << setprecision(2) << "average=" << avg << '\n';
    cout << "max=" << best << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
3
1 2 3
```
期望输出：
```text
sum=6
average=2.00
max=3
```

2. 输入：
```text
1
99
```
期望输出：
```text
sum=99
average=99.00
max=99
```

### V01-EX02 商品小票打印

- 归属卷：第 1 卷
- 覆盖模块：CPP-10 scanf/printf、格式化输出、补零、小数位
- 考场用途：练习只使用 `scanf/printf` 的传统 IO，避免关闭同步后混用 C 和 C++ 输入输出。

**题目描述：** 给定 `n` 件商品的编号、单价和数量，输出每件商品的小计和总价。商品编号按 4 位补零输出，小计和总价保留两位小数。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行包含整数 `id`、实数 `price`、整数 `count`。

**输出格式：** 前 `n` 行输出 `编号 小计`，最后一行输出 `TOTAL 总价`。

**样例输入：**
```text
3
7 12.5 2
42 3.2 5
105 100 1
```

**样例输出：**
```text
0007 25.00
0042 16.00
0105 100.00
TOTAL 141.00
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Item {
    int id;
    double price;
    int count;
};

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    vector<Item> item(n + 1);
    double total = 0.0;
    for (int i = 1; i <= n; i++) {
        if (scanf("%d%lf%d", &item[i].id, &item[i].price, &item[i].count) != 3) return 0;
    }

    for (int i = 1; i <= n; i++) {
        double subtotal = item[i].price * item[i].count;
        total += subtotal;
        printf("%04d %.2f\n", item[i].id, subtotal);
    }
    printf("TOTAL %.2f\n", total);
    return 0;
}
```

**测试设计：**

1. 输入：
```text
2
1 1.5 3
23 10 2
```
期望输出：
```text
0001 4.50
0023 20.00
TOTAL 24.50
```

2. 输入：
```text
1
9999 0.99 10
```
期望输出：
```text
9999 9.90
TOTAL 9.90
```

### V01-EX03 EOF 单词频率表

- 归属卷：第 1 卷
- 覆盖模块：CPP-001 EOF、CPP-10 getline、CPP-011 string、CPP-005 map
- 考场用途：练习 `getline` 读到 EOF、`stringstream` 拆词、`map` 自动按字典序输出。

**题目描述：** 输入若干行文本，统计每个单词出现次数。单词只按空白分隔，大小写视为不同单词。

**输入格式：** 若干行文本，直到文件结束。

**输出格式：** 按单词字典序输出，每行一个单词和出现次数。

**样例输入：**
```text
apple banana apple
pear banana
```

**样例输出：**
```text
apple 2
banana 2
pear 1
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    map<string, int> cnt;
    string line;
    while (getline(cin, line)) {
        stringstream ss(line);
        string word;
        while (ss >> word) {
            cnt[word]++;
        }
    }

    for (const auto &kv : cnt) {
        cout << kv.first << ' ' << kv.second << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
one
one two
```
期望输出：
```text
one 2
two 1
```

2. 输入：
```text
z y x
```
期望输出：
```text
x 1
y 1
z 1
```

### V01-EX04 通讯录号码查询

- 归属卷：第 1 卷
- 覆盖模块：CPP-005 unordered_map、CPP-011 string、CPP-001 cin/cout
- 考场用途：练习用 `unordered_map` 做姓名到号码的快速查询，并在大量插入前预留空间。

**题目描述：** 给定通讯录中若干人的姓名和号码，再回答若干次查询。若姓名存在，输出号码；否则输出 `NOT FOUND`。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行一个姓名和号码。再输入整数 `q`，接下来 `q` 行每行一个待查询姓名。

**输出格式：** 对每次查询输出一行结果。

**样例输入：**
```text
3
Alice 10086
Bob 10010
Cindy 95588
4
Bob
David
Alice
Cindy
```

**样例输出：**
```text
10010
NOT FOUND
10086
95588
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    unordered_map<string, string> phone;
    phone.reserve(n * 2 + 10);
    phone.max_load_factor(0.7);

    for (int i = 1; i <= n; i++) {
        string name, number;
        cin >> name >> number;
        phone[name] = number;
    }

    int q;
    cin >> q;
    for (int i = 1; i <= q; i++) {
        string name;
        cin >> name;
        auto it = phone.find(name);
        if (it == phone.end()) {
            cout << "NOT FOUND\n";
        } else {
            cout << it->second << '\n';
        }
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
1
Tom 123
3
Tom
Jerry
Tom
```
期望输出：
```text
123
NOT FOUND
123
```

2. 输入：
```text
2
A 1
B 2
2
B
A
```
期望输出：
```text
2
1
```

### V01-EX05 任务优先级调度

- 归属卷：第 1 卷
- 覆盖模块：CPP-004 priority_queue、CPP-002 vector/string、结构体比较
- 考场用途：练习 `priority_queue` 默认最大堆思想：优先级越大越先处理，优先级相同则耗时短者先处理，再按输入顺序稳定打破平局。

**题目描述：** 给定 `n` 个任务，每个任务有名称、优先级和耗时。按规则输出处理顺序：优先级高的先处理；优先级相同，耗时短的先处理；仍相同，先输入的先处理。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行包含任务名 `name`、整数优先级 `priority`、整数耗时 `time`。

**输出格式：** 输出 `n` 行，每行一个任务的名称、优先级和耗时。

**样例输入：**
```text
5
write 2 30
fix 5 10
test 5 5
read 1 1
pack 2 20
```

**样例输出：**
```text
test 5 5
fix 5 10
pack 2 20
write 2 30
read 1 1
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Task {
    string name;
    int priority;
    int time;
    int id;

    bool operator<(const Task &other) const {
        if (priority != other.priority) return priority < other.priority;
        if (time != other.time) return time > other.time;
        return id > other.id;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    priority_queue<Task> pq;
    for (int i = 1; i <= n; i++) {
        Task t;
        cin >> t.name >> t.priority >> t.time;
        t.id = i;
        pq.push(t);
    }

    while (!pq.empty()) {
        Task t = pq.top();
        pq.pop();
        cout << t.name << ' ' << t.priority << ' ' << t.time << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
3
a 1 10
b 3 20
c 2 5
```
期望输出：
```text
b 3 20
c 2 5
a 1 10
```

2. 输入：
```text
3
first 2 8
second 2 8
third 2 3
```
期望输出：
```text
third 2 3
first 2 8
second 2 8
```

### V01-EX06 整数去重排序

- 归属卷：第 1 卷
- 覆盖模块：CPP-005 set、CPP-001 cin/cout
- 考场用途：练习 `set` 自动去重和升序输出，适合数据量中等、需要有序唯一集合的题。

**题目描述：** 给定 `n` 个整数，输出不同整数的个数，并按升序输出所有不同整数。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数。

**输出格式：** 第一行输出 `count=不同整数个数`。第二行按升序输出不同整数，用一个空格分隔。

**样例输入：**
```text
8
5 3 5 2 3 9 2 1
```

**样例输出：**
```text
count=5
1 2 3 5 9
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    set<int> values;
    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        values.insert(x);
    }

    cout << "count=" << values.size() << '\n';
    bool first = true;
    for (int x : values) {
        if (!first) cout << ' ';
        first = false;
        cout << x;
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
5
4 4 4 4 4
```
期望输出：
```text
count=1
4
```

2. 输入：
```text
6
-1 3 -1 0 3 2
```
期望输出：
```text
count=4
-1 0 2 3
```

### V01-EX07 排序后找第一个不小于目标的位置

- 归属卷：第 1 卷
- 覆盖模块：CPP-003 sort/lower_bound、CPP-012 STL 算法、CPP-002 vector
- 考场用途：练习半开区间二分，输出排序后 1-index 位置，避免把迭代器差值当成原数组下标。

**题目描述：** 给定 `n` 个整数和 `q` 次查询。先将数组升序排序。每次查询给定 `x`，找到排序后第一个大于等于 `x` 的数，输出它的位置和值；若不存在，输出 `-1`。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数。第三行一个整数 `q`。接下来 `q` 行每行一个整数 `x`。

**输出格式：** 每次查询输出一行。若找到，输出 `位置 值`；否则输出 `-1`。

**样例输入：**
```text
6
8 1 5 3 5 10
4
0
5
6
11
```

**样例输出：**
```text
1 1
3 5
5 8
-1
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    sort(a.begin() + 1, a.end());

    int q;
    cin >> q;
    for (int i = 1; i <= q; i++) {
        int x;
        cin >> x;
        auto it = lower_bound(a.begin() + 1, a.end(), x);
        if (it == a.end()) {
            cout << -1 << '\n';
        } else {
            int pos = (int)(it - a.begin());
            cout << pos << ' ' << *it << '\n';
        }
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
4
4 2 8 6
3
1
6
9
```
期望输出：
```text
1 2
3 6
-1
```

2. 输入：
```text
5
5 5 5 5 5
2
5
6
```
期望输出：
```text
1 5
-1
```

### V01-EX08 学生成绩排行

- 归属卷：第 1 卷
- 覆盖模块：CPP-002 vector/string、CPP-003 sort 与 lambda、CPP-012 自定义比较
- 考场用途：练习结构体数组的 1-index 存储和多关键字排序：分数降序，姓名升序。

**题目描述：** 给定 `n` 名学生的姓名和成绩，按成绩从高到低排序；成绩相同按姓名字典序升序排序。输出排名、姓名和成绩。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行一个姓名和一个整数成绩。

**输出格式：** 输出 `n` 行，每行 `排名 姓名 成绩`。

**样例输入：**
```text
5
Tom 90
Amy 95
Bob 90
Cindy 100
Dave 95
```

**样例输出：**
```text
1 Cindy 100
2 Amy 95
3 Dave 95
4 Bob 90
5 Tom 90
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Student {
    string name;
    int score;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Student> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i].name >> a[i].score;
    }

    sort(a.begin() + 1, a.end(), [](const Student &lhs, const Student &rhs) {
        if (lhs.score != rhs.score) return lhs.score > rhs.score;
        return lhs.name < rhs.name;
    });

    for (int i = 1; i <= n; i++) {
        cout << i << ' ' << a[i].name << ' ' << a[i].score << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
3
B 80
A 80
C 90
```
期望输出：
```text
1 C 90
2 A 80
3 B 80
```

2. 输入：
```text
2
Li 100
Wang 99
```
期望输出：
```text
1 Li 100
2 Wang 99
```

### V01-EX09 整行记录统计

- 归属卷：第 1 卷
- 覆盖模块：CPP-10 getline、CPP-011 string、CPP-001 token 输入后处理换行
- 考场用途：练习 `cin >> n` 后立刻 `getline` 前必须清掉行尾换行，适合题目含空格字符串的场景。

**题目描述：** 给定 `n` 行记录。对每一行，输出行号、字符长度和单词数量。单词按空白分隔。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行是一条记录，可能包含空格。

**输出格式：** 输出 `n` 行，每行 `行号 长度 单词数量`。

**样例输入：**
```text
3
Hello World
abc 123
A B C
```

**样例输出：**
```text
1 11 2
2 7 2
3 5 3
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    vector<string> line(n + 1);
    for (int i = 1; i <= n; i++) {
        getline(cin, line[i]);
    }

    for (int i = 1; i <= n; i++) {
        stringstream ss(line[i]);
        string word;
        int words = 0;
        while (ss >> word) words++;
        cout << i << ' ' << line[i].size() << ' ' << words << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
2
single
two words
```
期望输出：
```text
1 6 1
2 9 2
```

2. 输入：
```text
1
  lead and tail..
```
期望输出：
```text
1 17 3
```

### V01-EX10 闭区间计数查询

- 归属卷：第 1 卷
- 覆盖模块：CPP-003 lower_bound/upper_bound、CPP-012 sort 与二分、CPP-002 vector
- 考场用途：练习在有序数组上统计 `[L, R]` 中元素个数，避免手写二分边界出错。

**题目描述：** 给定 `n` 个整数和 `q` 个查询。每次查询给出 `L R`，输出数组中落在闭区间 `[L, R]` 内的元素个数。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数。第三行一个整数 `q`。接下来 `q` 行每行两个整数 `L R`。

**输出格式：** 对每个查询输出一行答案。

**样例输入：**
```text
7
1 5 2 2 8 10 5
3
1 2
3 7
6 10
```

**样例输出：**
```text
3
2
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    sort(a.begin() + 1, a.end());

    int q;
    cin >> q;
    for (int i = 1; i <= q; i++) {
        int l, r;
        cin >> l >> r;
        auto left_it = lower_bound(a.begin() + 1, a.end(), l);
        auto right_it = upper_bound(a.begin() + 1, a.end(), r);
        cout << (right_it - left_it) << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
5
1 2 3 4 5
2
2 4
6 9
```
期望输出：
```text
3
0
```

2. 输入：
```text
4
7 7 7 7
2
7 7
1 6
```
期望输出：
```text
4
0
```

***

## 第 9 卷：Python 互补卷例题

### V09-EX01 大整数 Fibonacci

- 归属卷：第 9 卷
- 覆盖模块：PY-00 Python 使用路由、PY-01 输入输出、PY-05 大整数优势
- 考场用途：当答案位数很长而算法本身只是简单递推时，Python `int` 明显省掉 C++ 高精度实现。

**题目描述：** 给定整数 `n`，输出 Fibonacci 数列第 `n` 项。定义 `F(0)=0`，`F(1)=1`。

**输入格式：** 一行一个整数 `n`。

**输出格式：** 输出 `F(n)`。

**样例输入：**
```text
100
```

**样例输出：**
```text
354224848179261915075
```

**完整代码：**
```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    print(a)

if __name__ == "__main__":
    main()
```

**测试设计：**

1. 输入：
```text
0
```
期望输出：
```text
0
```

2. 输入：
```text
50
```
期望输出：
```text
12586269025
```

### V09-EX02 EOF 词频 TopK

- 归属卷：第 9 卷
- 覆盖模块：PY-01 EOF 输入、PY-02 Counter/dict、PY-05 Python 适用边界
- 考场用途：当题目是文本统计、哈希计数和排序时，Python `Counter` 能明显减少样板代码；若数据极大且卡常，再切回 C++。

**题目描述：** 第一项输入为整数 `k`，后面直到 EOF 都是单词。统计每个单词出现次数，输出出现次数最多的前 `k` 个单词。次数相同按单词字典序升序。

**输入格式：** 输入包含若干空白分隔的 token，第一个 token 为 `k`，其余 token 为单词。

**输出格式：** 输出最多 `k` 行，每行一个单词和次数。

**样例输入：**
```text
3
apple banana apple
pear banana apple
orange pear
```

**样例输出：**
```text
apple 3
banana 2
pear 2
```

**完整代码：**
```python
import sys
from collections import Counter

def main():
    tokens = sys.stdin.buffer.read().decode().split()
    if not tokens:
        return
    k = int(tokens[0])
    words = tokens[1:]
    cnt = Counter(words)
    order = sorted(cnt.items(), key=lambda item: (-item[1], item[0]))
    for word, times in order[:k]:
        print(word, times)

if __name__ == "__main__":
    main()
```

**测试设计：**

1. 输入：
```text
2
b a b c a a
```
期望输出：
```text
a 3
b 2
```

2. 输入：
```text
5
solo
```
期望输出：
```text
solo 1
```

### V09-EX03 坐标点判重

- 归属卷：第 9 卷
- 覆盖模块：PY-01 tuple、PY-02 set、PY-00 Python 适用场景
- 考场用途：当状态天然是二元组或字符串时，Python `set` 可直接判重，省掉 C++ 自定义哈希。

**题目描述：** 给定 `n` 个平面整数坐标点，输出不同点的个数，并按 `x` 升序、`y` 升序输出所有不同点。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行两个整数 `x y`。

**输出格式：** 第一行输出不同点个数。接下来按顺序输出所有不同点。

**样例输入：**
```text
6
1 2
1 2
2 1
3 3
2 1
-1 0
```

**样例输出：**
```text
4
-1 0
1 2
2 1
3 3
```

**完整代码：**
```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    points = set()
    for _ in range(n):
        x = int(next(it))
        y = int(next(it))
        points.add((x, y))

    ans = sorted(points)
    print(len(ans))
    for x, y in ans:
        print(x, y)

if __name__ == "__main__":
    main()
```

**测试设计：**

1. 输入：
```text
3
0 0
0 0
0 1
```
期望输出：
```text
2
0 0
0 1
```

2. 输入：
```text
4
2 2
1 3
2 1
1 3
```
期望输出：
```text
3
1 3
2 1
2 2
```

### V09-EX04 合并石子最小代价

- 归属卷：第 9 卷
- 覆盖模块：PY-02 heapq、PY-04 常用算法模板、PY-05 标准库限制
- 考场用途：当只需要标准最小堆且没有删除任意元素、修改 key 等需求时，Python `heapq` 写法短；若需要复杂堆操作，仍优先 C++。

**题目描述：** 有 `n` 堆石子，每次选择两堆合并，代价为两堆石子数量之和。输出把所有石子合成一堆的最小总代价。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数表示每堆石子的数量。

**输出格式：** 输出最小总代价。

**样例输入：**
```text
4
1 2 3 4
```

**样例输出：**
```text
19
```

**完整代码：**
```python
import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    heap = [int(x) for x in data[1:1 + n]]
    heapq.heapify(heap)

    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        s = a + b
        total += s
        heapq.heappush(heap, s)
    print(total)

if __name__ == "__main__":
    main()
```

**测试设计：**

1. 输入：
```text
1
7
```
期望输出：
```text
0
```

2. 输入：
```text
4
5 5 5 5
```
期望输出：
```text
40
```

### V09-EX05 迷宫最短路

- 归属卷：第 9 卷
- 覆盖模块：PY-02 deque、PY-04 BFS、PY-05 Python 适用边界
- 考场用途：中小规模网格 BFS 用 Python `deque` 很省代码；若网格巨大、时间限制紧或图边很多，优先 C++。

**题目描述：** 给定 `n` 行 `m` 列迷宫，`.` 表示空地，`#` 表示墙，`S` 表示起点，`T` 表示终点。每步可上下左右移动一格，求从 `S` 到 `T` 的最短步数，不可达输出 `-1`。

**输入格式：** 第一行两个整数 `n m`。接下来 `n` 行，每行长度为 `m` 的字符串。

**输出格式：** 输出最短步数，若不可达输出 `-1`。

**样例输入：**
```text
3 4
S...
.##.
...T
```

**样例输出：**
```text
5
```

**完整代码：**
```python
import sys
from collections import deque

def main():
    lines = sys.stdin.read().splitlines()
    if not lines:
        return
    n, m = map(int, lines[0].split())
    grid = lines[1:1 + n]

    start = target = None
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "S":
                start = (i, j)
            elif grid[i][j] == "T":
                target = (i, j)

    dist = [[-1] * m for _ in range(n)]
    q = deque()
    si, sj = start
    dist[si][sj] = 0
    q.append((si, sj))

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < n and 0 <= ny < m:
                if grid[nx][ny] != "#" and dist[nx][ny] == -1:
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))

    ti, tj = target
    print(dist[ti][tj])

if __name__ == "__main__":
    main()
```

**测试设计：**

1. 输入：
```text
2 2
ST
..
```
期望输出：
```text
1
```

2. 输入：
```text
2 3
S#T
###
```
期望输出：
```text
-1
```

### V09-EX06 小集合相邻差排列计数

- 归属卷：第 9 卷
- 覆盖模块：PY-02 itertools、PY-00 Python 作为部分分工具、PY-05 枚举规模限制
- 考场用途：`n` 很小且需要快速枚举排列时，Python `itertools.permutations` 明显省事；`n > 10` 的全排列不要硬用。

**题目描述：** 给定 `n` 个互不相同的整数和整数 `k`。统计有多少个排列满足任意相邻两个数的绝对差都不超过 `k`。

**输入格式：** 第一行两个整数 `n k`。第二行 `n` 个互不相同的整数。

**输出格式：** 输出满足条件的排列数量。

**样例输入：**
```text
3 1
1 2 3
```

**样例输出：**
```text
2
```

**完整代码：**
```python
import sys
from itertools import permutations

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    k = int(data[1])
    a = [int(x) for x in data[2:2 + n]]

    ans = 0
    for p in permutations(a):
        ok = True
        for i in range(1, n):
            if abs(p[i] - p[i - 1]) > k:
                ok = False
                break
        if ok:
            ans += 1
    print(ans)

if __name__ == "__main__":
    main()
```

**测试设计：**

1. 输入：
```text
4 1
1 2 3 4
```
期望输出：
```text
2
```

2. 输入：
```text
3 100
10 20 30
```
期望输出：
```text
6
```

### V09-EX07 EOF 每行求和

- 归属卷：第 9 卷
- 覆盖模块：PY-01 EOF 输入、PY-06 基础语法、PY-05 IO 检查
- 考场用途：当行边界有意义时，不要用全局 `split()` 抹掉换行；Python 按行处理 EOF 很直接。

**题目描述：** 输入若干行整数。对每一行，输出该行所有整数之和。空行的和为 `0`。

**输入格式：** 若干行，每行包含零个或多个整数，直到 EOF。

**输出格式：** 对每一行输出一个整数，表示该行的和。

**样例输入：**
```text
1 2 3
10 -5
7
```

**样例输出：**
```text
6
5
7
```

**完整代码：**
```python
import sys

def main():
    out = []
    for line in sys.stdin.buffer:
        nums = [int(x) for x in line.split()]
        out.append(str(sum(nums)))
    sys.stdout.write("\n".join(out))
    if out:
        sys.stdout.write("\n")

if __name__ == "__main__":
    main()
```

**测试设计：**

1. 输入：
```text
5
1 1 1 1
```
期望输出：
```text
5
4
```

2. 输入：
```text

2 -2 3
```
期望输出：
```text
0
3
```

### V09-EX08 树的子树大小

- 归属卷：第 9 卷
- 覆盖模块：PY-03 递归 DFS、PY-05 递归限制、PY-06 sys.setrecursionlimit
- 考场用途：递归深度不大或只是中小数据时，Python DFS 写法短；若树可能是一条 `2e5` 长链，深递归仍建议改迭代或切回 C++。

**题目描述：** 给定一棵 `n` 个节点的无根树，以 1 号点为根，输出每个点的子树大小。

**输入格式：** 第一行一个整数 `n`。接下来 `n-1` 行，每行两个整数 `u v` 表示一条边。

**输出格式：** 输出一行 `n` 个整数，第 `i` 个整数表示节点 `i` 的子树大小。

**样例输入：**
```text
5
1 2
1 3
3 4
3 5
```

**样例输出：**
```text
5 1 3 1 1
```

**完整代码：**
```python
import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(next(it))
        v = int(next(it))
        graph[u].append(v)
        graph[v].append(u)

    sys.setrecursionlimit(max(1000000, n * 2 + 10))
    size = [0] * (n + 1)

    def dfs(u, parent):
        size[u] = 1
        for v in graph[u]:
            if v == parent:
                continue
            dfs(v, u)
            size[u] += size[v]

    dfs(1, 0)
    print(" ".join(str(size[i]) for i in range(1, n + 1)))

if __name__ == "__main__":
    main()
```

**测试设计：**

1. 输入：
```text
3
1 2
2 3
```
期望输出：
```text
3 2 1
```

2. 输入：
```text
4
1 2
1 3
1 4
```
期望输出：
```text
4 1 1 1
```

### V09-EX09 障碍网格路径数

- 归属卷：第 9 卷
- 覆盖模块：PY-03 lru_cache 记忆化、PY-01 字符串输入、PY-05 Python 大整数与递归风险
- 考场用途：状态转移清楚但手写 DP 容易走错边界时，Python 记忆化能快速得到可靠版本；大网格满数据时仍应考虑表格 DP 或 C++。

**题目描述：** 给定 `n` 行 `m` 列网格，`.` 表示可走，`#` 表示障碍。从左上角走到右下角，每步只能向下或向右，求路径条数。若起点或终点为障碍，答案为 0。

**输入格式：** 第一行两个整数 `n m`。接下来 `n` 行，每行一个长度为 `m` 的字符串。

**输出格式：** 输出路径条数。

**样例输入：**
```text
3 3
...
.#.
...
```

**样例输出：**
```text
2
```

**完整代码：**
```python
import sys
from functools import lru_cache

def main():
    lines = sys.stdin.read().splitlines()
    if not lines:
        return
    n, m = map(int, lines[0].split())
    grid = lines[1:1 + n]
    sys.setrecursionlimit(max(1000000, n + m + 10))

    @lru_cache(None)
    def dfs(i, j):
        if i >= n or j >= m:
            return 0
        if grid[i][j] == "#":
            return 0
        if i == n - 1 and j == m - 1:
            return 1
        return dfs(i + 1, j) + dfs(i, j + 1)

    print(dfs(0, 0))

if __name__ == "__main__":
    main()
```

**测试设计：**

1. 输入：
```text
2 2
..
..
```
期望输出：
```text
2
```

2. 输入：
```text
2 2
#.
..
```
期望输出：
```text
0
```

### V09-EX10 滑动窗口最大值

- 归属卷：第 9 卷
- 覆盖模块：PY-02 deque、PY-04 常用算法模板、PY-05 list/deque 复杂度区别
- 考场用途：固定窗口最值用 `deque` 是标准线性做法；不要用 `pop(0)` 或每个窗口排序。

**题目描述：** 给定长度为 `n` 的整数序列和窗口长度 `k`，输出每个连续长度为 `k` 的窗口中的最大值。

**输入格式：** 第一行两个整数 `n k`。第二行 `n` 个整数。

**输出格式：** 输出 `n-k+1` 个整数，表示每个窗口最大值，用空格分隔。

**样例输入：**
```text
8 3
1 3 -1 -3 5 3 6 7
```

**样例输出：**
```text
3 3 5 5 6 7
```

**完整代码：**
```python
import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    k = int(data[1])
    a = [0] + [int(x) for x in data[2:2 + n]]

    q = deque()
    ans = []
    for i in range(1, n + 1):
        while q and q[0] <= i - k:
            q.popleft()
        while q and a[q[-1]] <= a[i]:
            q.pop()
        q.append(i)
        if i >= k:
            ans.append(str(a[q[0]]))

    print(" ".join(ans))

if __name__ == "__main__":
    main()
```

**测试设计：**

1. 输入：
```text
5 1
4 3 2 1 0
```
期望输出：
```text
4 3 2 1 0
```

2. 输入：
```text
5 5
2 9 1 8 3
```
期望输出：
```text
9
```
