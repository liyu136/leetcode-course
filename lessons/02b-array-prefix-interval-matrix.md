# 第 2b 讲：数组进阶——前缀信息、区间与矩阵

## 0. 本讲解决什么问题

第 2 讲介绍了数组、下标和原地修改。本讲进一步学习 Hot 100 中常见的数组信息组织方式：

1. 怎样快速得到一段连续区间的信息；
2. 怎样在不使用除法的情况下计算“除自己以外”的乘积；
3. 怎样合并相互重叠的区间；
4. 怎样利用下标本身保存信息；
5. 怎样系统处理矩阵的边界、旋转和搜索。

这些题看起来不同，核心都在于：**不要重复计算已经扫描过的信息。**

---

## 1. 前缀和：把区间求和变成两次查询

给定数组：

```text
nums = [2, -1, 3, 4]
```

定义：

```text
prefix[i] = nums 前 i 个元素的和
```

因此：

```text
prefix = [0, 2, 1, 4, 8]
```

开头额外放一个 `0`，可以统一处理从下标 `0` 开始的区间。

半开区间 `[left, right)` 的和为：

```text
prefix[right] - prefix[left]
```

构造需要 `O(n)`，之后每次查询只需 `O(1)`。

```python
prefix = [0]
for value in nums:
    prefix.append(prefix[-1] + value)

def range_sum(left, right):
    return prefix[right] - prefix[left]
```

### 1.1 和为 K 的子数组

假设当前扫描到位置 `i`，当前前缀和为 `current`。如果更早出现过：

```text
old = current - k
```

那么从那个旧位置之后到当前位置的子数组和就是 `k`。

字典保存：

```text
某个前缀和此前出现过多少次
```

```python
def subarray_sum(nums, k):
    counts = {0: 1}
    current = 0
    answer = 0

    for value in nums:
        current += value
        answer += counts.get(current - k, 0)
        counts[current] = counts.get(current, 0) + 1

    return answer
```

`{0: 1}` 表示扫描开始前已经存在一次前缀和 `0`。缺少它会漏掉从下标 `0` 开始的答案。

它和第 8b 讲“路径总和 III”使用同一个公式。区别是数组扫描不会进入兄弟分支，因此不需要回溯删除计数。

---

## 2. 前缀积与后缀积

问题：对每个位置，返回除它自身以外所有元素的乘积，不能使用除法。

对下标 `i`：

```text
答案 = i 左侧所有数的乘积 × i 右侧所有数的乘积
```

先让 `answer[i]` 保存左侧乘积，再从右向左乘入右侧乘积：

```python
def product_except_self(nums):
    n = len(nums)
    answer = [1] * n

    left_product = 1
    for i in range(n):
        answer[i] = left_product
        left_product *= nums[i]

    right_product = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= right_product
        right_product *= nums[i]

    return answer
```

循环不变量：

- 第一次扫描到 `i` 时，`left_product` 只包含 `[0, i)`；
- 第二次扫描到 `i` 时，`right_product` 只包含 `(i, n-1]`。

时间 `O(n)`；除输出数组外额外空间 `O(1)`。这种写法自然支持数组中存在一个或多个 `0`。

---

## 3. 合并区间：先排序，再维护当前答案

例如：

```text
[[1, 3], [2, 6], [8, 10], [15, 18]]
```

先按起点排序。此后新区间只能与答案中的最后一个区间发生重叠：

```python
def merge(intervals):
    intervals.sort(key=lambda interval: interval[0])
    merged = []

    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return merged
```

状态含义：`merged` 中的区间已经互不重叠，且覆盖了所有已扫描区间。

注意题目对端点相等时是否算重叠。上面使用 `start > last_end` 开启新区间，因此 `[1, 2]` 与 `[2, 3]` 会被合并。

复杂度主要来自排序：`O(n log n)`。

---

## 4. 轮转数组：三次翻转

把数组向右轮转 `k` 步：

```text
[1,2,3,4,5,6,7], k=3
→ [5,6,7,1,2,3,4]
```

令 `k %= n`，然后：

1. 翻转整个数组；
2. 翻转前 `k` 个；
3. 翻转剩余部分。

```python
def rotate(nums, k):
    n = len(nums)
    if n == 0:
        return
    k %= n

    def reverse(left, right):
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)
```

时间 `O(n)`，额外空间 `O(1)`。最常见错误是忘记 `k %= n` 或混淆右端点是否包含。

---

## 5. 把下标当作哈希位置

“缺失的第一个正数”要求 `O(n)` 时间和 `O(1)` 额外空间。

长度为 `n` 的数组，答案一定在 `[1, n+1]` 中。若值 `x` 满足 `1 <= x <= n`，它应该放到下标 `x - 1`。

```python
def first_missing_positive(nums):
    n = len(nums)

    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            target = nums[i] - 1
            nums[i], nums[target] = nums[target], nums[i]

    for i, value in enumerate(nums):
        if value != i + 1:
            return i + 1

    return n + 1
```

为什么使用 `while` 而不是 `if`？交换到 `i` 的新值可能仍然需要被送到另一个位置。

为什么加上 `nums[nums[i] - 1] != nums[i]`？重复值可能让两个相等元素无限交换。

虽然内部有 `while`，每个有效值最多被放到正确位置一次，因此总时间仍为 `O(n)`。

---

## 6. 矩阵的坐标与边界

矩阵通常使用：

```python
rows = len(matrix)
cols = len(matrix[0])
```

访问前先确认矩阵非空。不要默认矩阵一定是正方形；普通矩阵的 `rows` 和 `cols` 可以不同。

### 6.1 螺旋矩阵

维护尚未处理区域的四条边界：

```python
def spiral_order(matrix):
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    answer = []

    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            answer.append(matrix[top][col])
        top += 1

        for row in range(top, bottom + 1):
            answer.append(matrix[row][right])
        right -= 1

        if top <= bottom:
            for col in range(right, left - 1, -1):
                answer.append(matrix[bottom][col])
            bottom -= 1

        if left <= right:
            for row in range(bottom, top - 1, -1):
                answer.append(matrix[row][left])
            left += 1

    return answer
```

后两条边遍历前必须重新检查边界，否则单行或单列中心区域会被重复加入。

### 6.2 原地旋转正方形矩阵

顺时针旋转 90° 可以拆成：

1. 沿主对角线转置；
2. 每一行左右翻转。

```python
def rotate_matrix(matrix):
    n = len(matrix)

    for row in range(n):
        for col in range(row + 1, n):
            matrix[row][col], matrix[col][row] = matrix[col][row], matrix[row][col]

    for row in matrix:
        row.reverse()
```

只遍历主对角线上方。如果遍历整个矩阵，每一对元素会交换两次，等于没有变化。

### 6.3 搜索行列均递增的矩阵

从右上角出发：

- 当前值太大，只能向左；
- 当前值太小，只能向下。

```python
def search_matrix(matrix, target):
    if not matrix or not matrix[0]:
        return False

    row = 0
    col = len(matrix[0]) - 1

    while row < len(matrix) and col >= 0:
        value = matrix[row][col]
        if value == target:
            return True
        if value > target:
            col -= 1
        else:
            row += 1

    return False
```

每一步排除一整行或一整列，时间为 `O(rows + cols)`。

### 6.4 矩阵置零

若某格为 `0`，将对应整行整列置零。不能一看到零就立刻清空，否则新写入的零会继续传播。

一种清晰方法是先用两个集合记录行列；进阶做法使用第一行和第一列作为标记数组，并额外记录它们原本是否含零。

```python
def set_zeroes(matrix):
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][c] == 0 for c in range(cols))
    first_col_zero = any(matrix[r][0] == 0 for r in range(rows))

    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0

    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0

    if first_row_zero:
        for c in range(cols): matrix[0][c] = 0
    if first_col_zero:
        for r in range(rows): matrix[r][0] = 0
```

---

## 7. 本讲检查表

遇到数组或矩阵题时问：

1. 区间信息是否可以由两个前缀状态相减得到？
2. 是否可以从左右两个方向预处理？
3. 排序后，当前对象是否只需与最后一个答案比较？
4. 数值范围是否允许“值映射到下标”？
5. 原地写标记会不会污染尚未读取的信息？
6. 矩阵是按层处理、按方向移动，还是利用行列单调性？
7. 每次缩小边界后是否需要重新检查合法性？

## 8. 本讲总结

- 前缀和把区间计算转换为状态之差。
- 前缀与后缀扫描可以避免除法和重复计算。
- 区间排序后，只需维护最后一个合并结果。
- 数值范围较小时，数组下标本身可以承担哈希位置的作用。
- 矩阵题的关键是明确坐标含义、边界变化和原地修改顺序。

