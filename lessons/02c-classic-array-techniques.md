# 第 2c 讲：经典数组技巧——异或、投票、三色划分与排列

## 0. 为什么单独补这一讲

Hot 100 的“技巧”题通常没有统一的数据结构，但每道题都依赖一个明确的不变量。本讲不要求死背代码，而要理解代码为什么能排除错误答案。

---

## 1. 异或：只出现一次的数字

异或 `^` 有三个关键性质：

```text
x ^ x = 0
x ^ 0 = x
异或满足交换律和结合律
```

如果除一个数字外，其余数字都出现两次：

```python
def single_number(nums):
    answer = 0
    for value in nums:
        answer ^= value
    return answer
```

成对数字不必相邻，因为顺序不影响最终异或结果。时间 `O(n)`，空间 `O(1)`。

异或技巧依赖题目非常具体的出现次数条件，不能用于一般频率统计。

---

## 2. Boyer–Moore 投票：多数元素

多数元素出现次数严格大于 `n // 2`。把多数元素与不同元素两两抵消，最后仍会剩下多数元素。

```python
def majority_element(nums):
    candidate = None
    count = 0

    for value in nums:
        if count == 0:
            candidate = value

        if value == candidate:
            count += 1
        else:
            count -= 1

    return candidate
```

`count` 不是 candidate 的真实出现次数，而是它在当前未抵消部分中的净优势。

若题目不保证多数元素存在，第一次扫描只能得到候选者，还要再扫描一次验证出现次数。

---

## 3. 荷兰国旗：三段循环不变量

颜色分类只有 `0、1、2`，要求原地排序。维护四个区域：

```text
[0, left)       全是 0
[left, current) 全是 1
[current, right] 尚未检查
(right, n-1]    全是 2
```

```python
def sort_colors(nums):
    left = 0
    current = 0
    right = len(nums) - 1

    while current <= right:
        if nums[current] == 0:
            nums[left], nums[current] = nums[current], nums[left]
            left += 1
            current += 1
        elif nums[current] == 1:
            current += 1
        else:
            nums[current], nums[right] = nums[right], nums[current]
            right -= 1
```

遇到 `2` 后为什么不移动 `current`？因为从右侧换来的元素还没有检查。

遇到 `0` 后可以同时移动，是因为 `[left, current)` 本来全是 `1`；交换到 current 的元素已经确定是 `1`，或两个指针原本重合。

---

## 4. 下一个排列

目标是在所有排列的字典序中，找到严格大于当前排列的最小一个。

例如：

```text
[1, 3, 5, 4, 2]
→ [1, 4, 2, 3, 5]
```

推导过程：

1. 从右向左寻找第一个上升位置 `i`，即 `nums[i] < nums[i+1]`；
2. 右侧已经是非递增序列，它是当前前缀下能得到的最大后缀；
3. 从右向左找第一个大于 `nums[i]` 的元素并交换；
4. 将 `i+1` 之后翻转成最小的递增顺序。

```python
def next_permutation(nums):
    n = len(nums)
    i = n - 2

    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]

    left, right = i + 1, n - 1
    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
```

如果整个数组非递增，`i == -1`，翻转整个数组便得到最小排列。

---

## 5. 把数组看成链表：寻找重复数

数组长度为 `n+1`，值都在 `[1, n]`，因此可以把：

```text
下标 i → 下一个下标 nums[i]
```

看成一条隐式链表。因为节点数多于可取值数量，必然有两个下标指向同一个值；这会在隐式链表中形成环，重复数就是环入口。

```python
def find_duplicate(nums):
    slow = nums[0]
    fast = nums[nums[0]]

    while slow != fast:
        slow = nums[slow]
        fast = nums[nums[fast]]

    finder = 0
    while finder != slow:
        finder = nums[finder]
        slow = nums[slow]

    return finder
```

第一阶段只证明两个指针在环内相遇，不保证相遇点是入口。第二阶段让一个指针回到起点，两者都每次走一步，再次相遇的位置才是环入口。

该方法依赖非常严格的值域条件。普通数组出现重复值时不能机械使用 Floyd。

---

## 6. 怎样识别这些技巧

| 题目条件 | 可能的方法 |
|---|---|
| 其余元素全部出现两次 | 异或抵消 |
| 某元素出现次数超过一半 | Boyer–Moore 投票 |
| 只有三类且要求原地分类 | 三段指针 |
| 求字典序中的紧邻排列 | 后缀结构 + 局部交换 |
| 长度 n+1、值域 1..n、不可修改数组 | 隐式链表 + Floyd |

这些方法的共同点不是语法，而是题目给了强约束。先写出约束，再判断它能否形成抵消、分区、单调后缀或隐式指针。

## 7. 常见错误

1. 把异或用于“元素出现任意次数”的题。
2. 忘记 Boyer–Moore 在“不保证答案存在”时需要验证。
3. 颜色分类交换右侧元素后错误地移动 current。
4. 下一个排列找到上升点后，对整个数组排序；虽然可能正确，但不再是 `O(n)`。
5. Floyd 第一阶段相遇后直接返回相遇值。
6. 没检查数组值是否能安全地作为下标。

## 8. 本讲总结

- 技巧题高度依赖输入条件。
- 每段代码都应能用一个循环不变量解释。
- 看懂“为什么这一步不会漏答案”，比记住五段独立代码更重要。

