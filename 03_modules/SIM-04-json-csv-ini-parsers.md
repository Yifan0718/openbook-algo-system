# SIM-04 JSON / CSV / INI 解析器

模块编号：SIM-04

模块名称：常见数据格式解析器：JSON、CSV、INI

标签：模拟、解析器、JSON、CSV、INI、字符串扫描、配置文件、日志处理、C++17

一句话用途：当模拟题给出结构化文本、配置文件、表格或日志片段时，直接套这个模块解析成树、表或键值表，再接统计/查询逻辑。

题面触发词：

- 给一个 JSON 字符串，查询字段、统计节点、输出某些路径。
- 给一个 CSV 表格，处理逗号、双引号、转义引号。
- 给一个 INI 配置，解析 section、key、value。
- 题目让你“按格式读入一段配置/日志/表格”。
- 输入不是普通空格分隔，而是半结构化文本。

什么时候用：

- 题目重点是格式解析和模拟，而不是算法复杂度。
- 手写 `cin >>` 会丢空格、逗号、引号或换行。
- JSON 需要保留结构，后续可能查询路径或对子树统计。
- CSV 里字段可能包含逗号或引号。
- INI 里有 section 和键值对。

不要什么时候用：

- 输入格式只是普通整数/字符串列表，直接 `cin` 更短。
- JSON 要求严格标准全部边角、浮点高精度或超大嵌套深度时，本模板需要按题意微调。
- CSV 方言很复杂，例如自定义分隔符、多行字段特殊规则，本模板需要微调。
- INI 有复杂转义、继承、数组，本模板只解析 `[section]` 下的 `key=value` 或 `key:value`。

复杂度：

- JSON 解析：`O(len)`。
- CSV 解析：`O(len)`。
- INI 解析：`O(len)`。
- 查询 JSON 路径若每次在线找 key，按对象子节点数线性；查询多时可对对象额外建 `map`。

数据范围参考：

- 文本长度 `<= 2e5`：本模块可直接用。
- JSON 节点池 `MAXJSON` 按文本长度防御性开大，通常 `MAXJSON = 400005`。
- CSV/INI 用 `vector` 存结果，行列特别大时注意内存。

依赖的标准容器：

- `string`：保存原文本、字段、key、value。
- `vector`：保存 CSV 表格、INI 键值、JSON 子节点。
- 静态数组 `json_node[MAXJSON]`：JSON AST 节点池，节点编号 1-index。

输入如何整理：

```cpp
string mode;
getline(cin, mode);

string text, line;
while (getline(cin, line)) {
    text += line;
    text += '\n';
}
```

接口：

```text
JSON:
JsonParser parser(text);
int root = parser.parse();
dump_json_leaves(root, "$", out);

CSV:
vector<vector<string>> rows = parse_csv(text);
rows[i][j] 使用 1-index，rows[0] 和每行 [0] 是占位。

INI:
vector<IniKV> kvs = parse_ini(text);
kvs[i].section, kvs[i].key, kvs[i].value。
```

## 模块选择卡

| 格式 | 典型特征 | 输出结构 |
|---|---|---|
| JSON | `{}`、`[]`、`"key"`、`true/null` | AST 树 |
| CSV | 逗号分隔，字段可用 `"` 包住 | 1-index 表格 |
| INI | `[section]`、`key=value` | 键值列表 |

模板代码：

```cpp
#include <cassert>
#include <cctype>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;

const int MAXJSON = 400005;

enum JsonType {
    JSON_NULL = 0,
    JSON_BOOL = 1,
    JSON_NUMBER = 2,
    JSON_STRING = 3,
    JSON_ARRAY = 4,
    JSON_OBJECT = 5
};

struct JsonNode {
    int type;
    string value;
    vector<int> child;     // 1-index: child[1..]
    vector<string> key;    // object 用，1-index: key[1..]
};

JsonNode json_node[MAXJSON];
int json_cnt = 0;

int new_json_node(int type, const string &value = "") {
    assert(json_cnt + 1 < MAXJSON);
    ++json_cnt;
    json_node[json_cnt].type = type;
    json_node[json_cnt].value = value;
    json_node[json_cnt].child.clear();
    json_node[json_cnt].key.clear();
    json_node[json_cnt].child.push_back(0);
    json_node[json_cnt].key.push_back("");
    return json_cnt;
}

string trim_copy(const string &s) {
    int l = 0;
    int r = (int)s.size() - 1;
    while (l <= r && isspace((unsigned char)s[l])) l++;
    while (r >= l && isspace((unsigned char)s[r])) r--;
    if (l > r) return "";
    return s.substr(l, r - l + 1);
}

string escape_visible(const string &s) {
    string t;
    for (char c : s) {
        if (c == '\\') t += "\\\\";
        else if (c == '"') t += "\\\"";
        else if (c == '\n') t += "\\n";
        else if (c == '\r') t += "\\r";
        else if (c == '\t') t += "\\t";
        else t.push_back(c);
    }
    return t;
}

string escape_cell_visible(const string &s) {
    string t;
    for (char c : s) {
        if (c == '\n') t += "\\n";
        else if (c == '\r') t += "\\r";
        else if (c == '\t') t += "\\t";
        else t.push_back(c);
    }
    return t;
}

struct JsonParser {
    string s;
    int pos;

    JsonParser(const string &text) {
        s = text;
        pos = 0;
    }

    void skip_spaces() {
        while (pos < (int)s.size() && isspace((unsigned char)s[pos])) pos++;
    }

    bool starts_with(const string &pat) {
        return s.compare(pos, pat.size(), pat) == 0;
    }

    int hex_value(char c) {
        if ('0' <= c && c <= '9') return c - '0';
        if ('a' <= c && c <= 'f') return c - 'a' + 10;
        if ('A' <= c && c <= 'F') return c - 'A' + 10;
        throw runtime_error("bad hex digit");
    }

    int parse_hex4() {
        int code = 0;
        for (int i = 1; i <= 4; i++) {
            if (pos >= (int)s.size() || !isxdigit((unsigned char)s[pos])) {
                throw runtime_error("bad unicode escape");
            }
            code = code * 16 + hex_value(s[pos]);
            pos++;
        }
        return code;
    }

    void append_utf8(string &res, int code) {
        if (code < 0 || code > 0x10FFFF) {
            throw runtime_error("bad unicode codepoint");
        }
        if (code <= 0x7F) {
            res.push_back((char)code);
        } else if (code <= 0x7FF) {
            res.push_back((char)(0xC0 | (code >> 6)));
            res.push_back((char)(0x80 | (code & 0x3F)));
        } else if (code <= 0xFFFF) {
            res.push_back((char)(0xE0 | (code >> 12)));
            res.push_back((char)(0x80 | ((code >> 6) & 0x3F)));
            res.push_back((char)(0x80 | (code & 0x3F)));
        } else {
            res.push_back((char)(0xF0 | (code >> 18)));
            res.push_back((char)(0x80 | ((code >> 12) & 0x3F)));
            res.push_back((char)(0x80 | ((code >> 6) & 0x3F)));
            res.push_back((char)(0x80 | (code & 0x3F)));
        }
    }

    int parse() {
        int root = parse_value();
        skip_spaces();
        if (pos != (int)s.size()) {
            throw runtime_error("extra json characters");
        }
        return root;
    }

    int parse_value() {
        skip_spaces();
        if (pos >= (int)s.size()) throw runtime_error("empty json value");
        char c = s[pos];
        if (c == '{') return parse_object();
        if (c == '[') return parse_array();
        if (c == '"') return new_json_node(JSON_STRING, parse_string());
        if (c == '-' || isdigit((unsigned char)c)) return parse_number();
        if (starts_with("true")) {
            pos += 4;
            return new_json_node(JSON_BOOL, "true");
        }
        if (starts_with("false")) {
            pos += 5;
            return new_json_node(JSON_BOOL, "false");
        }
        if (starts_with("null")) {
            pos += 4;
            return new_json_node(JSON_NULL, "null");
        }
        throw runtime_error("bad json value");
    }

    string parse_string() {
        if (pos >= (int)s.size() || s[pos] != '"') {
            throw runtime_error("missing string quote");
        }
        pos++;
        string res;
        while (pos < (int)s.size()) {
            char c = s[pos++];
            if (c == '"') return res;
            if (c != '\\') {
                if ((unsigned char)c < 0x20) {
                    throw runtime_error("unescaped control character in string");
                }
                res.push_back(c);
                continue;
            }
            if (pos >= (int)s.size()) throw runtime_error("bad escape");
            char e = s[pos++];
            if (e == '"' || e == '\\' || e == '/') res.push_back(e);
            else if (e == 'b') res.push_back('\b');
            else if (e == 'f') res.push_back('\f');
            else if (e == 'n') res.push_back('\n');
            else if (e == 'r') res.push_back('\r');
            else if (e == 't') res.push_back('\t');
            else if (e == 'u') {
                int code = parse_hex4();
                if (0xD800 <= code && code <= 0xDBFF) {
                    if (pos + 1 >= (int)s.size() || s[pos] != '\\' || s[pos + 1] != 'u') {
                        throw runtime_error("missing low surrogate");
                    }
                    pos += 2;
                    int low = parse_hex4();
                    if (low < 0xDC00 || low > 0xDFFF) {
                        throw runtime_error("bad low surrogate");
                    }
                    code = 0x10000 + (code - 0xD800) * 0x400 + (low - 0xDC00);
                } else if (0xDC00 <= code && code <= 0xDFFF) {
                    throw runtime_error("lone low surrogate");
                }
                append_utf8(res, code);
            } else {
                throw runtime_error("unknown escape");
            }
        }
        throw runtime_error("unterminated string");
    }

    int parse_number() {
        int start = pos;
        if (s[pos] == '-') pos++;
        if (pos >= (int)s.size() || !isdigit((unsigned char)s[pos])) {
            throw runtime_error("bad number");
        }
        if (s[pos] == '0') {
            pos++;
        } else {
            while (pos < (int)s.size() && isdigit((unsigned char)s[pos])) pos++;
        }
        if (pos < (int)s.size() && s[pos] == '.') {
            pos++;
            int digit_start = pos;
            while (pos < (int)s.size() && isdigit((unsigned char)s[pos])) pos++;
            if (pos == digit_start) throw runtime_error("bad decimal number");
        }
        if (pos < (int)s.size() && (s[pos] == 'e' || s[pos] == 'E')) {
            pos++;
            if (pos < (int)s.size() && (s[pos] == '+' || s[pos] == '-')) pos++;
            int digit_start = pos;
            while (pos < (int)s.size() && isdigit((unsigned char)s[pos])) pos++;
            if (pos == digit_start) throw runtime_error("bad exponent number");
        }
        return new_json_node(JSON_NUMBER, s.substr(start, pos - start));
    }

    int parse_array() {
        pos++;
        int u = new_json_node(JSON_ARRAY);
        skip_spaces();
        if (pos < (int)s.size() && s[pos] == ']') {
            pos++;
            return u;
        }
        while (true) {
            int v = parse_value();
            json_node[u].child.push_back(v);
            skip_spaces();
            if (pos < (int)s.size() && s[pos] == ',') {
                pos++;
                continue;
            }
            if (pos < (int)s.size() && s[pos] == ']') {
                pos++;
                break;
            }
            throw runtime_error("bad array");
        }
        return u;
    }

    int parse_object() {
        pos++;
        int u = new_json_node(JSON_OBJECT);
        skip_spaces();
        if (pos < (int)s.size() && s[pos] == '}') {
            pos++;
            return u;
        }
        while (true) {
            skip_spaces();
            string k = parse_string();
            skip_spaces();
            if (pos >= (int)s.size() || s[pos] != ':') {
                throw runtime_error("missing colon");
            }
            pos++;
            int v = parse_value();
            json_node[u].key.push_back(k);
            json_node[u].child.push_back(v);
            skip_spaces();
            if (pos < (int)s.size() && s[pos] == ',') {
                pos++;
                continue;
            }
            if (pos < (int)s.size() && s[pos] == '}') {
                pos++;
                break;
            }
            throw runtime_error("bad object");
        }
        return u;
    }
};

string json_value_repr(int u) {
    int type = json_node[u].type;
    if (type == JSON_NULL) return "null";
    if (type == JSON_BOOL) return json_node[u].value;
    if (type == JSON_NUMBER) return json_node[u].value;
    if (type == JSON_STRING) return "\"" + escape_visible(json_node[u].value) + "\"";
    if (type == JSON_ARRAY) return "[array]";
    return "{object}";
}

void dump_json_leaves(int u, const string &path, vector<pair<string, string>> &out) {
    int type = json_node[u].type;
    if (type != JSON_ARRAY && type != JSON_OBJECT) {
        out.push_back({path, json_value_repr(u)});
        return;
    }
    if (type == JSON_ARRAY) {
        for (int i = 1; i < (int)json_node[u].child.size(); i++) {
            dump_json_leaves(json_node[u].child[i], path + "[" + to_string(i) + "]", out);
        }
        return;
    }
    for (int i = 1; i < (int)json_node[u].child.size(); i++) {
        dump_json_leaves(json_node[u].child[i], path + "." + json_node[u].key[i], out);
    }
}

vector<vector<string>> parse_csv(const string &text) {
    vector<vector<string>> rows(1);
    vector<string> row(1);
    string cell;
    bool in_quote = false;
    bool just_closed_quote = false;
    bool row_has_anything = false;

    for (int i = 0; i < (int)text.size(); i++) {
        char c = text[i];
        if (c == '\r') continue;
        row_has_anything = true;

        if (in_quote) {
            if (c == '"') {
                if (i + 1 < (int)text.size() && text[i + 1] == '"') {
                    cell.push_back('"');
                    i++;
                } else {
                    in_quote = false;
                    just_closed_quote = true;
                }
            } else {
                cell.push_back(c);
            }
            continue;
        }

        if (c == '"' && cell.empty() && !just_closed_quote) {
            in_quote = true;
        } else if (c == ',') {
            row.push_back(cell);
            cell.clear();
            just_closed_quote = false;
        } else if (c == '\n') {
            row.push_back(cell);
            rows.push_back(row);
            row.assign(1, "");
            cell.clear();
            just_closed_quote = false;
            row_has_anything = false;
        } else if (just_closed_quote && (c == ' ' || c == '\t')) {
            continue;
        } else if (just_closed_quote) {
            throw runtime_error("bad csv after quote");
        } else {
            cell.push_back(c);
            just_closed_quote = false;
        }
    }

    if (in_quote) throw runtime_error("unterminated csv quote");
    if (row_has_anything || !cell.empty() || row.size() > 1) {
        row.push_back(cell);
        rows.push_back(row);
    }
    return rows;
}

struct IniKV {
    string section;
    string key;
    string value;
};

vector<IniKV> parse_ini(const string &text) {
    vector<IniKV> res(1);
    string section = "global";
    string line;

    for (int i = 0; i <= (int)text.size(); i++) {
        if (i < (int)text.size() && text[i] != '\n') {
            if (text[i] != '\r') line.push_back(text[i]);
            continue;
        }

        string cur = trim_copy(line);
        line.clear();
        if (cur.empty()) continue;
        if (cur[0] == '#' || cur[0] == ';') continue;

        if (cur.front() == '[' && cur.back() == ']') {
            section = trim_copy(cur.substr(1, (int)cur.size() - 2));
            if (section.empty()) section = "global";
            continue;
        }

        int pos = -1;
        for (int j = 0; j < (int)cur.size(); j++) {
            if (cur[j] == '=' || cur[j] == ':') {
                pos = j;
                break;
            }
        }
        if (pos == -1) continue;

        IniKV item;
        item.section = section;
        item.key = trim_copy(cur.substr(0, pos));
        item.value = trim_copy(cur.substr(pos + 1));
        res.push_back(item);
    }

    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string mode;
    if (!getline(cin, mode)) return 0;
    mode = trim_copy(mode);

    string text, line;
    while (getline(cin, line)) {
        text += line;
        text.push_back('\n');
    }

    try {
        if (mode == "json") {
            json_cnt = 0;
            JsonParser parser(text);
            int root = parser.parse();
            vector<pair<string, string>> out;
            dump_json_leaves(root, "$", out);
            cout << json_cnt << ' ' << out.size() << '\n';
            for (auto &item : out) {
                cout << item.first << "=" << item.second << '\n';
            }
        } else if (mode == "csv") {
            vector<vector<string>> rows = parse_csv(text);
            cout << (int)rows.size() - 1 << '\n';
            for (int i = 1; i < (int)rows.size(); i++) {
                cout << "row " << i << " cols " << (int)rows[i].size() - 1 << '\n';
                for (int j = 1; j < (int)rows[i].size(); j++) {
                    cout << "[" << i << "," << j << "]=" << escape_cell_visible(rows[i][j]) << '\n';
                }
            }
        } else if (mode == "ini") {
            vector<IniKV> kvs = parse_ini(text);
            cout << (int)kvs.size() - 1 << '\n';
            for (int i = 1; i < (int)kvs.size(); i++) {
                cout << kvs[i].section << "." << kvs[i].key << "=" << kvs[i].value << '\n';
            }
        } else {
            cout << "ERROR\n";
        }
    } catch (const exception &e) {
        cout << "ERROR\n";
    }

    return 0;
}
```

调用示例：

```cpp
JsonParser parser(text);
int root = parser.parse();
vector<pair<string, string>> leaves;
dump_json_leaves(root, "$", leaves);

vector<vector<string>> table = parse_csv(csv_text);
vector<IniKV> kvs = parse_ini(ini_text);
```

常见坑：

- JSON 字符串必须用 `getline` 或整段读入，不能直接 `cin >> text`。
- JSON 数字这里按字符串保存，避免溢出；需要算数时再转 `long long` 或接 `SIM-02`。
- JSON 的 `\uXXXX` 会转成 UTF-8；代理对例如 `\uD83D\uDE00` 也会合并后输出。
- CSV 引号内的逗号不是分隔符，`"a,b"` 是一个字段。
- CSV 中 `""` 表示一个真实的双引号。
- INI 行首 `#` 和 `;` 当注释，行内注释本模板不自动裁掉。
- 普通数组和 CSV 行列都用 1-index；字符串扫描下标仍是局部 0-index。

暴力/部分分替代：

- JSON 不会写完整树时，先用字符串扫描查固定字段，拿小数据分。
- CSV 如果题目保证没有引号，先用 `stringstream + getline(ss, cell, ',')`。
- INI 如果没有 section，直接按 `key=value` 切分。
- 若格式只出现一两种固定模式，手写特判比完整解析器更快。

最小测试样例：

```text
输入
json
{"b":[true,null,"x"],"a":{"n":-12,"s":"hi\n"}}

输出
8 5
$.b[1]=true
$.b[2]=null
$.b[3]="x"
$.a.n=-12
$.a.s="hi\n"
```

补充自测 1：

```text
输入
csv
name,score,note
Alice,10,"hello,world"
Bob,20,"a ""quote"""

输出
3
row 1 cols 3
[1,1]=name
[1,2]=score
[1,3]=note
row 2 cols 3
[2,1]=Alice
[2,2]=10
[2,3]=hello,world
row 3 cols 3
[3,1]=Bob
[3,2]=20
[3,3]=a "quote"
```

补充自测 2：

```text
输入
ini
# comment
name = root
[db]
host=localhost
port : 3306
[feature]
enabled=true

输出
4
global.name=root
db.host=localhost
db.port=3306
feature.enabled=true
```
