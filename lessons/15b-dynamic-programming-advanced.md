# 第 15b 讲：进阶动态规划——布尔状态、双状态、区间与双序列

## 0. 从一维 DP 到更丰富的状态

第 15 讲已经掌握 DP 五步法。本讲不改变方法，而是扩展“状态需要保存什么”：

1. 可不可行：布尔 DP；
2. 同时维护最大和最小：双状态 DP；
3. 一段区间是否满足条件：区间 DP；
4. 两条序列的前缀如何匹配：双序列 DP；
5. 由结尾位置定义有效长度。

每一题都必须先用自然语言写清 `dp[...]` 的含义，再写转移。

---

## 1. 杨辉三角：二维递推的最简单形式

每个内部元素来自左上与右上：

```python
def generate(num_rows):
    triangle = []

    for row_index in range(num_rows):
        row = [1] * (row_index + 1)
        for col in range(1, row_index):
            row[col] = triangle[row_index - 1][col - 1] + triangle[row_index - 1][col]
        triangle.append(row)

    return triangle
```

它提醒我们：转移只读取上一层已经计算好的状态，边界位置需要单独初始化。

---

## 2. 完全平方数：零钱兑换的同类问题

把所有不超过 `n` 的平方数当作硬币，问题变成“组成金额 n 的最少硬币数”。

```python
def num_squares(n):
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for total in range(1, n + 1):
        square = 1
        while square * square <= total:
            dp[total] = min(dp[total], dp[total - square * square] + 1)
            square += 1

    return dp[n]
```

状态：`dp[total]` 表示组成 `total` 的最少平方数数量。

---

## 3. 单词拆分：布尔 DP

状态定义：

```text
dp[i] = s[:i] 能否被字典中的单词完整拆分
```

若存在某个 `j < i`，满足：

```text
dp[j] 为真，并且 s[j:i] 在字典中
```

则 `dp[i]` 为真。

```python
def word_break(s, word_dict):
    words = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True

    for end in range(1, len(s) + 1):
        for start in range(end):
            if dp[start] and s[start:end] in words:
                dp[end] = True
                break

    return dp[len(s)]
```

`dp[0] = True` 表示空前缀可以被合法拆分，它是所有第一次匹配的起点。

基础复杂度 `O(n²)` 次切分检查；Python 切片还会创建新字符串。可以用最大单词长度限制 `start` 范围。

---

## 4. 乘积最大子数组：最大值可能来自最小值

负数会翻转大小关系。因此扫描到当前元素时，必须同时维护：

```text
current_max：以当前位置结尾的最大乘积
current_min：以当前位置结尾的最小乘积
```

```python
def max_product(nums):
    current_max = nums[0]
    current_min = nums[0]
    answer = nums[0]

    for value in nums[1:]:
        previous_max = current_max
        previous_min = current_min

        current_max = max(value, value * previous_max, value * previous_min)
        current_min = min(value, value * previous_max, value * previous_min)
        answer = max(answer, current_max)

    return answer
```

为什么保存最小值？一个很小的负数乘以新的负数可能变成最大正数。

必须先保存旧状态，不能更新 `current_max` 后再用新值计算 `current_min`。

---

## 5. 最长有效括号：以位置结尾的长度

定义：

```text
dp[i] = 以 s[i] 结尾的最长有效括号长度
```

只有 `s[i] == ')'` 时答案可能非零。

```python
def longest_valid_parentheses(s):
    dp = [0] * len(s)
    best = 0

    for i in range(1, len(s)):
        if s[i] != ')':
            continue

        if s[i - 1] == '(':
            dp[i] = 2 + (dp[i - 2] if i >= 2 else 0)
        else:
            opening = i - dp[i - 1] - 1
            if opening >= 0 and s[opening] == '(':
                dp[i] = dp[i - 1] + 2
                if opening > 0:
                    dp[i] += dp[opening - 1]

        best = max(best, dp[i])

    return best
```

难点是第二种情况：先跳过前一个有效块，再检查它左侧是否存在可以配对的 `(`。

---

## 6. 最长回文子串：区间状态

定义：

```text
dp[left][right] = s[left:right+1] 是否为回文
```

转移：

```text
s[left] == s[right]
并且内部长度不超过 1，或 dp[left+1][right-1] 为真
```

```python
def longest_palindrome(s):
    n = len(s)
    if n == 0:
        return ''

    dp = [[False] * n for _ in range(n)]
    best_start = 0
    best_length = 1

    for length in range(1, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1

            if s[left] == s[right] and (length <= 2 or dp[left + 1][right - 1]):
                dp[left][right] = True
                if length > best_length:
                    best_start = left
                    best_length = length

    return s[best_start:best_start + best_length]
```

计算顺序必须保证较短的内部区间先完成，所以按区间长度递增。

该题也可以使用中心扩展，以 `O(1)` 额外空间完成；区间 DP 更适合学习状态依赖。

---

## 7. 最长公共子序列：两个前缀

子序列不要求连续，但必须保持相对顺序。

定义：

```text
dp[i][j] = text1 前 i 个字符与 text2 前 j 个字符的 LCS 长度
```

```python
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]
```

多出的第 0 行和第 0 列表示其中一个字符串为空，使边界自然初始化为 0。

---

## 8. 编辑距离：双序列上的操作代价

定义：

```text
dp[i][j] = word1[:i] 转换为 word2[:j] 的最少操作数
```

边界：

```text
dp[i][0] = i   删除 i 个字符
dp[0][j] = j   插入 j 个字符
```

若最后字符相同，不增加操作；否则比较删除、插入和替换：

```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                delete = dp[i - 1][j]
                insert = dp[i][j - 1]
                replace = dp[i - 1][j - 1]
                dp[i][j] = 1 + min(delete, insert, replace)

    return dp[m][n]
```

这里的删除、插入、替换都是从当前状态反向看最后一步。状态定义清晰后，三个来源才不会混乱。

---

## 9. 几类 DP 放在一起

| 题型 | 状态关键词 | 典型依赖 |
|---|---|---|
| 单词拆分 | 前 i 个字符能否拆分 | 更短前缀 |
| 乘积最大子数组 | 以 i 结尾的最大与最小 | 前一位置的双状态 |
| 最长有效括号 | 以 i 结尾的有效长度 | 前块及其左边界 |
| 回文子串 | 区间 `[l, r]` 是否回文 | 内部区间 `[l+1, r-1]` |
| LCS | 两个前缀的最优长度 | 上、左、左上 |
| 编辑距离 | 两个前缀的最小代价 | 删除、插入、替换 |

---

## 10. 常见错误

1. 单词拆分把 `dp[0]` 初始化为 False。
2. 乘积题只保存最大值，忽略负数翻转。
3. 原地更新双状态时使用了已经修改的新值。
4. 区间 DP 的计算顺序早于内部区间。
5. 双序列 DP 混淆“前 i 个字符”和下标 `i`。
6. 编辑距离没有正确初始化空字符串边界。
7. 把子序列误认为必须连续的子串。

## 11. 本讲检查表

1. `dp` 的每个下标表示位置、数量还是区间？
2. 状态表示最大值、最小值、长度、代价还是可行性？
3. 当前状态需要前一状态、内部区间还是两个序列的前缀？
4. 初始化是否严格符合状态定义？
5. 计算顺序是否保证所有依赖已经完成？
6. 答案位于最后一个状态，还是所有状态的最大值？

## 12. 本讲总结

- DP 方法没有改变，变化的是状态中必须包含的信息。
- 布尔 DP 用于判断可行性。
- 负数会翻转大小时，需要同时保存最大和最小状态。
- 区间 DP 必须先计算较短区间。
- 双序列 DP 常用多出一行一列表示空前缀。
- 任何转移都应能用“最后一步发生了什么”解释。

