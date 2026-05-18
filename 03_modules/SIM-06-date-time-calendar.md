# SIM-06 日期、时间、时区与历法

模块编号：SIM-06

模块名称：日期转序号、天数差、星期、时区、夏令时与儒略/格里高利历

标签：模拟、日期、时间、历法、时区、夏令时、儒略历、格里高利历、C++17

一句话用途：遇到给定日期求相差天数、星期几、加减天、跨时区时间转换、夏令时规则或历史历法切换时，统一把日期转成整数 day number，再做加减。

题面触发词：

- 给两个日期，求相隔多少天。
- 给日期求星期几。
- 给日期加上/减去若干天。
- 给 UTC 时间和时区偏移，求当地时间。
- 夏令时、生效区间、时钟拨快一小时。
- 儒略历、格里高利历、1582 年 10 月跳日。

什么时候用：

- 日期需要跨月、跨年、跨闰年。
- 需要比较日期先后或求差。
- 题目有时区 offset，例如 `UTC+8`、`-05:30`。
- 题目明确给出夏令时开始/结束日期和偏移规则。
- 历史日期要求区分 Julian / Gregorian。

不要什么时候用：

- 题目只在同一天内算秒数，直接 `h*3600+m*60+s`。
- 题目使用农历、节气、天文历法，本模板不覆盖。
- 夏令时按真实国家历史数据库变化，本模板不内置数据库，必须按题面规则模拟。
- 如果题目没有提 1582 切历，不要自行跳过日期，默认 proleptic Gregorian 更稳。

复杂度：

- 日期转 day number：`O(1)`。
- day number 转日期：`O(1)`。
- 日期差、星期、加减天：`O(1)`。
- 处理 `n` 个日期：`O(n)`。

数据范围参考：

- 年份绝对值很大时用 `long long`。
- 本模板适合普通竞赛日期范围，含公元前需按题面决定是否有 year 0。
- 时区 offset 用分钟保存，避免小数小时。

依赖的标准容器：

- `long long`：day number、秒数、分钟数。
- `string`：解析 `YYYY-MM-DD`、`HH:MM:SS`、时区字符串。
- `array/vector`：月份天数表，月份按 1-index。

输入如何整理：

```cpp
int y, m, d;
char c1, c2;
cin >> y >> c1 >> m >> c2 >> d; // 2026-05-18
```

接口：

```text
days_from_civil(y,m,d) -> Gregorian 日期转 day number，1970-01-01 为 0。
civil_from_days(z) -> day number 转 Gregorian 日期。
julian_day_number_gregorian(y,m,d) -> Gregorian JDN。
julian_day_number_julian(y,m,d) -> Julian JDN。
diff_days(a,b) = days(b) - days(a)。
weekday = (days + 4) mod 7，1970-01-01 是 Thursday。
```

## 最重要思想：日期先转整数

```text
日期 y-m-d -> day number
相差天数 = day2 - day1
加 N 天 = civil_from_days(day + N)
星期几 = (day + offset) % 7
```

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Date {
    ll y;
    int m;
    int d;
};

struct DateTime {
    Date date;
    int hh;
    int mm;
    int ss;
};

ll floor_div(ll a, ll b) {
    assert(b > 0);
    __int128 aa = a, bb = b;
    __int128 q = aa / bb;
    __int128 r = aa % bb;
    if (r < 0) q--;
    assert((__int128)LLONG_MIN <= q && q <= (__int128)LLONG_MAX);
    return (ll)q;
}

bool is_gregorian_leap(ll y) {
    return (y % 400 == 0) || (y % 4 == 0 && y % 100 != 0);
}

bool is_julian_leap(ll y) {
    return y % 4 == 0;
}

int month_days_gregorian(ll y, int m) {
    static int md[13] = {0,31,28,31,30,31,30,31,31,30,31,30,31};
    if (m < 1 || m > 12) throw runtime_error("bad month");
    if (m == 2 && is_gregorian_leap(y)) return 29;
    return md[m];
}

int month_days_julian(ll y, int m) {
    static int md[13] = {0,31,28,31,30,31,30,31,31,30,31,30,31};
    if (m < 1 || m > 12) throw runtime_error("bad month");
    if (m == 2 && is_julian_leap(y)) return 29;
    return md[m];
}

bool valid_date_gregorian(ll y, int m, int d) {
    if (m < 1 || m > 12) return false;
    return 1 <= d && d <= month_days_gregorian(y, m);
}

bool valid_date_julian(ll y, int m, int d) {
    if (m < 1 || m > 12) return false;
    return 1 <= d && d <= month_days_julian(y, m);
}

// Howard Hinnant 算法：Gregorian，返回距离 1970-01-01 的天数。
ll days_from_civil(ll y, int m, int d) {
    if (!valid_date_gregorian(y, m, d)) throw runtime_error("bad Gregorian date");
    y -= m <= 2;
    ll era = floor_div(y, 400);
    unsigned yoe = (unsigned)(y - era * 400);
    unsigned mp = (unsigned)(m + (m > 2 ? -3 : 9));
    unsigned doy = (153 * mp + 2) / 5 + (unsigned)d - 1;
    unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return era * 146097 + (ll)doe - 719468;
}

Date civil_from_days(ll z) {
    z += 719468;
    ll era = floor_div(z, 146097);
    unsigned doe = (unsigned)(z - era * 146097);
    unsigned yoe = (doe - doe / 1460 + doe / 36524 - doe / 146096) / 365;
    ll y = (ll)yoe + era * 400;
    unsigned doy = doe - (365 * yoe + yoe / 4 - yoe / 100);
    unsigned mp = (5 * doy + 2) / 153;
    unsigned d = doy - (153 * mp + 2) / 5 + 1;
    unsigned m = mp + (mp < 10 ? 3 : -9);
    y += m <= 2;
    return {y, (int)m, (int)d};
}

// JDN: 整数儒略日号，适合比较历史日期。Gregorian 版本。
ll julian_day_number_gregorian(ll y, int m, int d) {
    if (!valid_date_gregorian(y, m, d)) throw runtime_error("bad Gregorian date");
    ll a = (14 - m) / 12;
    ll yy = y + 4800 - a;
    ll mm = m + 12 * a - 3;
    return d + (153 * mm + 2) / 5 + 365 * yy + yy / 4 - yy / 100 + yy / 400 - 32045;
}

// JDN: Julian 历版本。
ll julian_day_number_julian(ll y, int m, int d) {
    if (!valid_date_julian(y, m, d)) throw runtime_error("bad Julian date");
    ll a = (14 - m) / 12;
    ll yy = y + 4800 - a;
    ll mm = m + 12 * a - 3;
    return d + (153 * mm + 2) / 5 + 365 * yy + yy / 4 - 32083;
}

bool is_gregorian_gap_1582(ll y, int m, int d) {
    return y == 1582 && m == 10 && 5 <= d && d <= 14;
}

// 1582 罗马/天主教地区切换示例：1582-10-15 及之后 Gregorian，之前 Julian。
ll historical_jdn_1582_switch(ll y, int m, int d) {
    if (is_gregorian_gap_1582(y, m, d)) {
        throw runtime_error("nonexistent date in 1582 switch");
    }
    if (y > 1582 || (y == 1582 && (m > 10 || (m == 10 && d >= 15)))) {
        return julian_day_number_gregorian(y, m, d);
    }
    return julian_day_number_julian(y, m, d);
}

int weekday_1970(Date date) {
    // 0 Sunday, 1 Monday, ..., 6 Saturday. 1970-01-01 is Thursday=4.
    ll z = days_from_civil(date.y, date.m, date.d);
    int w = (int)((z + 4) % 7);
    if (w < 0) w += 7;
    return w;
}

ll datetime_to_utc_seconds(DateTime t, int offset_minutes) {
    ll days = days_from_civil(t.date.y, t.date.m, t.date.d);
    ll local = days * 86400 + t.hh * 3600 + t.mm * 60 + t.ss;
    return local - (ll)offset_minutes * 60;
}

DateTime utc_seconds_to_datetime(ll utc_seconds, int offset_minutes) {
    ll local = utc_seconds + (ll)offset_minutes * 60;
    ll day = floor_div(local, 86400);
    int sec = (int)(local - day * 86400);
    Date date = civil_from_days(day);
    return {date, sec / 3600, sec / 60 % 60, sec % 60};
}

int parse_offset_minutes(const string &s) {
    // 支持 +08:00, -0530, UTC+8, UTC-05:30
    string t = s;
    if (t.rfind("UTC", 0) == 0 || t.rfind("GMT", 0) == 0) {
        t = t.substr(3);
    }
    if (t.empty()) return 0;
    int sign = 1;
    int pos = 0;
    if (t[pos] == '+') {
        sign = 1;
        pos++;
    } else if (t[pos] == '-') {
        sign = -1;
        pos++;
    }
    string rest = t.substr(pos);
    if (rest.empty()) return 0;
    int hour = 0, minute = 0;
    int colon = (int)rest.find(':');
    auto all_digits = [](const string &x) {
        if (x.empty()) return false;
        for (char c : x) {
            if (!isdigit((unsigned char)c)) return false;
        }
        return true;
    };
    if (colon != -1) {
        string hh = rest.substr(0, colon);
        string mm = rest.substr(colon + 1);
        if (!all_digits(hh) || !all_digits(mm)) throw runtime_error("bad timezone");
        hour = stoi(hh);
        minute = stoi(mm);
    } else {
        if (!all_digits(rest)) throw runtime_error("bad timezone");
        if ((int)rest.size() <= 2) {
            hour = stoi(rest);
        } else if ((int)rest.size() == 4) {
            hour = stoi(rest.substr(0, 2));
            minute = stoi(rest.substr(2, 2));
        } else {
            throw runtime_error("bad timezone");
        }
    }
    if (minute < 0 || minute >= 60) throw runtime_error("bad timezone minute");
    return sign * (hour * 60 + minute);
}

void print_date(Date date) {
    cout << date.y << '-';
    cout << setw(2) << setfill('0') << date.m << '-';
    cout << setw(2) << setfill('0') << date.d;
    cout << setfill(' ');
}

void print_datetime(DateTime t) {
    print_date(t.date);
    cout << ' ';
    cout << setw(2) << setfill('0') << t.hh << ':';
    cout << setw(2) << setfill('0') << t.mm << ':';
    cout << setw(2) << setfill('0') << t.ss;
    cout << setfill(' ');
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string op;
    cin >> op;

    if (op == "diff") {
        Date a, b;
        cin >> a.y >> a.m >> a.d >> b.y >> b.m >> b.d;
        cout << days_from_civil(b.y, b.m, b.d) - days_from_civil(a.y, a.m, a.d) << '\n';
    } else if (op == "add") {
        Date a;
        ll delta;
        cin >> a.y >> a.m >> a.d >> delta;
        Date b = civil_from_days(days_from_civil(a.y, a.m, a.d) + delta);
        print_date(b);
        cout << '\n';
    } else if (op == "weekday") {
        Date a;
        cin >> a.y >> a.m >> a.d;
        static string name[7] = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
        cout << name[weekday_1970(a)] << '\n';
    } else if (op == "jdn") {
        string cal;
        Date a;
        cin >> cal >> a.y >> a.m >> a.d;
        if (cal == "gregorian") cout << julian_day_number_gregorian(a.y, a.m, a.d) << '\n';
        else if (cal == "julian") cout << julian_day_number_julian(a.y, a.m, a.d) << '\n';
        else if (is_gregorian_gap_1582(a.y, a.m, a.d)) cout << "INVALID\n";
        else cout << historical_jdn_1582_switch(a.y, a.m, a.d) << '\n';
    } else if (op == "tz") {
        DateTime t;
        string from_zone, to_zone;
        cin >> t.date.y >> t.date.m >> t.date.d >> t.hh >> t.mm >> t.ss >> from_zone >> to_zone;
        ll utc = datetime_to_utc_seconds(t, parse_offset_minutes(from_zone));
        DateTime ans = utc_seconds_to_datetime(utc, parse_offset_minutes(to_zone));
        print_datetime(ans);
        cout << '\n';
    }

    return 0;
}
```

## 夏令时怎么处理

不要内置真实世界数据库。竞赛题通常会给规则，例如：

```text
每年 3 月第二个星期日 02:00 开始 DST，UTC offset +1h
每年 11 月第一个星期日 02:00 结束 DST
```

处理策略：

1. 用日期函数算出规则日期。
2. 把开始/结束时刻转成统一秒数。
3. 判断当前时间是否在 `[start, end)`。
4. 在基础时区 offset 上加 60 分钟。

常用辅助：

```cpp
Date nth_weekday_of_month(ll y, int m, int weekday, int nth) {
    Date first{y, m, 1};
    int w = weekday_1970(first);
    int add = (weekday - w + 7) % 7;
    int day = 1 + add + 7 * (nth - 1);
    return {y, m, day};
}
```

调用示例：

```cpp
ll a = days_from_civil(2024, 2, 28);
ll b = days_from_civil(2024, 3, 1);
cout << b - a << '\n'; // 闰年输出 2
```

常见坑：

- 公历闰年：能被 400 整除，或能被 4 整除但不能被 100 整除。
- 1900 不是公历闰年，2000 是公历闰年。
- 儒略历规则只有“能被 4 整除就是闰年”。
- 题目没说历史切历时，默认不要跳过 1582-10-05 到 1582-10-14。
- 1582 切换不同国家时间不一样；只在题目明确时使用对应规则。
- 时区用分钟，不要用浮点小时。
- 跨日时本地秒数可能为负，必须用 floor_div。
- 夏令时的开始/结束瞬间最容易 off-by-one，统一用半开区间 `[start,end)`。

暴力/部分分替代：

- 日期范围只在同一年：前缀月份天数即可。
- 不跨闰年：按普通年模拟。
- 不会 JDN：对年份不大可从基准日逐日加减，但要小心效率。
- 时区不跨日期：只算小时分钟差先拿部分分。
- 夏令时规则复杂：先忽略 DST，可能拿非 DST 数据分。

最小测试样例：

```text
输入
diff
2024 2 28 2024 3 1

输出
2
```

补充自测：

```text
输入
add
2024 2 28 2

输出
2024-03-01
```

补充自测 2：

```text
输入
weekday
1970 1 1

输出
Thu
```

补充自测 3：

```text
输入
jdn
historical
1582 10 4

输出
2299160
```

补充自测 4：

```text
输入
jdn
historical
1582 10 15

输出
2299161
```

补充自测 5：

```text
输入
tz
2026 5 18 10 0 0 UTC+8 UTC-05:30

输出
2026-05-17 20:30:00
```
