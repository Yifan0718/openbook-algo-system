from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULES = ROOT / "03_modules"
OUT = ROOT / "04_generated_drafts" / "volume_1_cpp_stl.md"

ORDER = [
    "CPP-001-main-io.md",
    "CPP-10-io-formatting.md",
    "CPP-002-basic-containers.md",
    "CPP-011-string-reference.md",
    "STR-01-basic-operations.md",
    "CPP-013-stl-containers-reference.md",
    "CPP-012-stl-algorithms-reference.md",
    "CPP-003-sort-bounds.md",
    "CPP-004-queues-stacks-heaps.md",
    "CPP-005-associative-containers.md",
    "CPP-006-bitset-bit-operations.md",
    "CPP-007-coordinate-compression.md",
    "CPP-008-integers-overflow.md",
    "CPP-009-common-re-wa-pitfalls.md",
]


def main() -> None:
    parts = [
        "# 第 1 卷：C++17 / STL 快查作战卷",
        "",
        "这一卷解决语言和 STL 层面的稳定性：输入输出、字符串、容器、算法函数、排序二分、队列堆、映射、位运算、压缩、整数和常见 RE/WA。",
        "",
        "核心口令：",
        "",
        "```text",
        "允许 using namespace std。",
        "数组默认 1-index。",
        "字符串保持 0-index。",
        "答案和距离用 long long。",
        "容器访问前查 empty。",
        "排序二分必须同一顺序。",
        "```",
        "",
        "## 头文件安全包",
        "",
        "默认用 GNU g++ 时可以写 `#include <bits/stdc++.h>`。如果现场环境不支持，直接翻 `CPP-001`，把第一行替换成“标准头文件安全包”；不要现场凭记忆一个个补头文件。",
        "",
        "## 输入输出索引表",
        "",
        "| 需求 | 优先查 | 常用写法 | 坑点 |",
        "|---|---|---|---|",
        "| 普通读写 | CPP-001 / CPP-10 | `ios::sync_with_stdio(false); cin.tie(nullptr);` | 关闭同步后不要混用 `scanf/printf` |",
        "| 传统格式化 | CPP-10 | `scanf/printf`、`%.2f`、`%04d` | `double` 用 `%lf` 读、`%f` 输出 |",
        "| 读整行/含空格 | CPP-10 / CPP-011 | `getline(cin, line)` | 前面用过 `cin >> x` 要 `ignore` 换行 |",
        "| 快读快写 | CPP-10 | `readInt(x)`、`writeInt(x)` | 只在数据极大时使用，注意 EOF |",
        "| 小数/对齐/补零 | CPP-10 | `fixed << setprecision(2)`、`setw` | `setw` 只影响下一个输出项 |",
        "",
        "## STL 函数索引表",
        "",
        "| 需求 | 优先查 | 常用写法 | 坑点 |",
        "|---|---|---|---|",
        "| 字符串成员函数 | CPP-011 = string API；STR-01 = 字符串题路由 | `substr/find/rfind/insert/erase/replace` | `npos`、0-index、`erase` 是 O(n) |",
        "| 顺序容器 | CPP-013 | `vector/deque/list/array` | `reserve` 不改变 size，`list` 不能下标 |",
        "| 优先队列 | CPP-013 / CPP-004 | `priority_queue<T, vector<T>, greater<T>>` | 默认最大堆，小根堆写法较长 |",
        "| 哈希表 | CPP-013 / CPP-005 | `unordered_map`、`unordered_set` | 大量插入前 `max_load_factor + reserve` |",
        "| 排序与比较 | CPP-012 / CPP-003 | `sort(v.begin(), v.end(), cmp)` | `cmp` 不能写 `<=` |",
        "| 去重 | CPP-012 | `sort` + `erase(unique(...))` | `unique` 不会真的删尾部 |",
        "| 删除指定值 | CPP-012 / CPP-013 | `erase(remove(...), end)` | 只适合顺序容器 |",
        "| 二分查找 | CPP-012 / CPP-003 | `lower_bound/upper_bound/binary_search` | 目标区间必须已排序 |",
        "| 全排列 | CPP-012 / BRUTE-03 | `next_permutation` | 初始序列先排序 |",
        "| 数值工具 | CPP-012 / MATH-01 | `iota/accumulate/partial_sum/gcd/lcm` | `accumulate` 初值写 `0LL` |",
        "| 位集合 | CPP-006 | `bitset<N>` | `N` 必须编译期常量 |",
        "",
        "## 模块目录",
        "",
        "| 模块 | 内容 |",
        "|---|---|",
    ]

    for name in ORDER:
        path = MODULES / name
        if not path.exists():
            raise FileNotFoundError(f"missing module: {name}")
        title = path.read_text(encoding="utf-8", errors="replace").splitlines()[0].lstrip("# ").strip()
        parts.append(f"| `{name}` | {title} |")

    for name in ORDER:
        path = MODULES / name
        if not path.exists():
            continue
        parts.append("\n\n---\n\n")
        parts.append(f"<!-- source: 03_modules/{name} -->")
        parts.append(path.read_text(encoding="utf-8", errors="replace").rstrip())

    OUT.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Included {sum((MODULES / name).exists() for name in ORDER)} modules")


if __name__ == "__main__":
    main()
