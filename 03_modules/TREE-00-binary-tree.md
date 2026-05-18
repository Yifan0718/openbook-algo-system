# TREE-00 二叉树基础

模块编号：TREE-00

模块名称：BinaryTree 数组建树、遍历与重建

标签：[树][二叉树][遍历][递归][栈][重建]

一句话用途：用 `lc[u] / rc[u]` 表示左右儿子，快速完成二叉树建树、前中后序遍历和由前序+中序重建。

题面触发词：

- 二叉树、左儿子、右儿子。
- 前序遍历、中序遍历、后序遍历。
- 给出每个点的左右孩子。
- 给出前序和中序，求后序或还原树。
- 完全二叉树、堆式编号。

什么时候用：

- 节点编号是 `1..n`，空儿子用 `0` 或 `-1` 表示。
- 题目明确是二叉树，不需要一般图建边。
- 只需要遍历顺序、父亲、深度、子树大小等基础信息。

不要什么时候用：

- 输入是普通无向树，每个点儿子数不固定，应使用邻接表 DFS。
- 二叉搜索树插入/删除要按 BST 性质单独处理。
- 节点值不唯一时，不能直接用“前序+中序”唯一重建。

复杂度：

- 建树：`O(n)`。
- 递归/迭代遍历：`O(n)`。
- 前序+中序重建：`O(n)`，需要值唯一并建立位置表。

数据范围参考：

- `n <= 2e5`：数组开 `N = 200000 + 5`。
- 深链递归可能爆栈，`n` 很大时遍历优先用迭代版。
- 完全二叉树编号：左儿子 `2*u`，右儿子 `2*u+1`。

依赖的标准容器：

- 1-index 数组：`lc[u]`、`rc[u]`、`fa[u]`。
- `vector<int>` 存遍历结果。
- `stack<int>` 做迭代遍历。

输入如何整理：

```cpp
// 常见输入：第 i 行给 i 的左儿子、右儿子，0 表示空。
cin >> n;
for (int i = 1; i <= n; i++) {
    cin >> lc[i] >> rc[i];
}
```

接口：

```text
find_root() -> 根据入度找根
build_complete(n) -> 按完全二叉树编号补左右儿子
preorder_dfs(root), inorder_dfs(root), postorder_dfs(root)
preorder_iter(root), inorder_iter(root), postorder_iter(root)
build(preL, preR, inL, inR) -> 前序+中序重建
```

输出能力：

- 前序、中序、后序遍历序列。
- 每个点父亲。
- 完全二叉树左右儿子。
- 由前序+中序得到左右儿子或后序。

下游可接：

- 树形 DP。
- DFS 序。
- 二叉树表达式求值。
- 二叉搜索树判断。

可拼接模块：

- `TREE-00 + DP-14 TreeDP`。
- `TREE-00 + Stack`。
- `TREE-00 + GRAPH-09 LCA`，仅当二叉树转成普通树后需要路径查询。

模板代码：数组建二叉树与遍历

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 200000 + 5;

int n, root;
int lc[N], rc[N], fa[N];

void clear_tree(int n) {
    for (int i = 0; i <= n; i++) {
        lc[i] = rc[i] = fa[i] = 0;
    }
}

int find_root() {
    vector<int> indeg(n + 1, 0);
    for (int u = 1; u <= n; u++) {
        if (lc[u]) {
            indeg[lc[u]]++;
            fa[lc[u]] = u;
        }
        if (rc[u]) {
            indeg[rc[u]]++;
            fa[rc[u]] = u;
        }
    }
    for (int i = 1; i <= n; i++) {
        if (indeg[i] == 0) return i;
    }
    return 0;
}

void read_left_right_tree() {
    cin >> n;
    clear_tree(n);
    for (int i = 1; i <= n; i++) {
        cin >> lc[i] >> rc[i];
        if (lc[i] < 0) lc[i] = 0;
        if (rc[i] < 0) rc[i] = 0;
    }
    root = find_root();
}

void build_complete(int n_) {
    n = n_;
    clear_tree(n);
    for (int u = 1; u <= n; u++) {
        if (2 * u <= n) {
            lc[u] = 2 * u;
            fa[2 * u] = u;
        }
        if (2 * u + 1 <= n) {
            rc[u] = 2 * u + 1;
            fa[2 * u + 1] = u;
        }
    }
    root = (n == 0 ? 0 : 1);
}

vector<int> pre_rec, in_rec, post_rec;

void preorder_dfs(int u) {
    if (u == 0) return;
    pre_rec.push_back(u);
    preorder_dfs(lc[u]);
    preorder_dfs(rc[u]);
}

void inorder_dfs(int u) {
    if (u == 0) return;
    inorder_dfs(lc[u]);
    in_rec.push_back(u);
    inorder_dfs(rc[u]);
}

void postorder_dfs(int u) {
    if (u == 0) return;
    postorder_dfs(lc[u]);
    postorder_dfs(rc[u]);
    post_rec.push_back(u);
}

vector<int> preorder_iter(int root) {
    vector<int> res;
    if (root == 0) return res;
    stack<int> st;
    st.push(root);
    while (!st.empty()) {
        int u = st.top();
        st.pop();
        res.push_back(u);
        if (rc[u]) st.push(rc[u]);
        if (lc[u]) st.push(lc[u]);
    }
    return res;
}

vector<int> inorder_iter(int root) {
    vector<int> res;
    stack<int> st;
    int u = root;
    while (u || !st.empty()) {
        while (u) {
            st.push(u);
            u = lc[u];
        }
        u = st.top();
        st.pop();
        res.push_back(u);
        u = rc[u];
    }
    return res;
}

vector<int> postorder_iter(int root) {
    vector<int> res;
    if (root == 0) return res;
    stack<pair<int, int>> st;
    st.push({root, 0});
    while (!st.empty()) {
        auto [u, visited] = st.top();
        st.pop();
        if (u == 0) continue;
        if (visited) {
            res.push_back(u);
        } else {
            st.push({u, 1});
            st.push({rc[u], 0});
            st.push({lc[u], 0});
        }
    }
    return res;
}

void print_vector(const vector<int> &v) {
    for (int i = 0; i < (int)v.size(); i++) {
        if (i) cout << ' ';
        cout << v[i];
    }
    cout << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    read_left_right_tree();

    print_vector(preorder_iter(root));
    print_vector(inorder_iter(root));
    print_vector(postorder_iter(root));
    return 0;
}
```

模板代码：由前序 + 中序重建

拼接提醒：下面是一个独立完整模板，所以重新声明了 `N/n/lc/rc`。如果已经复制了上面的二叉树基础模板，合并时复用同一套 `N/n/lc/rc`，只额外加入 `pre/inord/pos/build/print_postorder` 即可。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 200000 + 5;

int n;
int pre[N], inord[N], pos[N];
int lc[N], rc[N];

int build(int pl, int pr, int il, int ir) {
    if (pl > pr) return 0;
    int u = pre[pl];
    int k = pos[u];
    int left_cnt = k - il;

    lc[u] = build(pl + 1, pl + left_cnt, il, k - 1);
    rc[u] = build(pl + left_cnt + 1, pr, k + 1, ir);
    return u;
}

void print_postorder(int u) {
    if (u == 0) return;
    print_postorder(lc[u]);
    print_postorder(rc[u]);
    cout << u << ' ';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    for (int i = 1; i <= n; i++) cin >> pre[i];
    for (int i = 1; i <= n; i++) {
        cin >> inord[i];
        pos[inord[i]] = i;
    }

    int root = build(1, n, 1, n);
    print_postorder(root);
    cout << '\n';
    return 0;
}
```

调用示例：

```cpp
root = find_root();
vector<int> a = preorder_iter(root);
vector<int> b = inorder_iter(root);
vector<int> c = postorder_iter(root);
```

常见坑：

- 空儿子统一转成 `0`，不要一会儿用 `-1` 一会儿用 `0`。
- 前序+中序重建要求节点值唯一；值重复时不能唯一确定。
- 如果节点值不是 `1..n`，`pos[value]` 数组要改成 `unordered_map<int,int>`。
- 递归遍历遇到链状树可能爆栈，`n >= 2e5` 时优先用迭代遍历。
- 找根时检查入度，不能默认 `1` 一定是根。
- 完全二叉树编号只适用于题目明确按堆式编号存树。

暴力/部分分替代：

- `n <= 2000`：递归遍历最省事，先拿基础分。
- 只问一次遍历：不必建复杂结构，读完 `lc/rc` 后直接 DFS。
- 前序+中序不会重建：可以递归切区间直接输出后序，不一定显式存树。

升级方向：

- 二叉树基础遍历 -> 树形 DP。
- 二叉树转普通树 -> LCA/树上距离。
- 多次子树查询 -> DFS 序 + 树状数组/SegmentTree。

最小测试样例：

```text
输入左右儿子：
5
2 3
4 5
0 0
0 0
0 0

前序：1 2 4 5 3
中序：4 2 5 1 3
后序：4 5 2 3 1
```
