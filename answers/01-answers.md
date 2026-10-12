# 第 1 讲参考答案

请先独立完成练习，再阅读本文件。答案代码不是背诵材料；阅读后应关闭本文件，从空白重新实现。

## 练习 1

`ans` 的变化：

| 当前 `x` | 循环结束后的 `ans` |
|---:|---:|
| 1 | 1 |
| 4 | 1 |
| 2 | 1 |

最终输出：

```text
1
```

## 练习 2

原代码的 `return False` 位于循环内部，所以检查完第一个非负元素后就结束了，不会继续检查后面的元素。

```python
def has_negative(nums):
    for x in nums:
        if x < 0:
            return True

    return False
```

只有当循环全部执行完、仍未发现负数时，才能确定结果为 `False`。空数组不会进入循环，因此会执行最后的 `return False`。

时间复杂度是 `O(n)`，额外空间复杂度是 `O(1)`。

## 练习 3

```text
状态：已经发现的 target 数量 count
初始化：count = 0
更新条件：当前元素 x == target
更新方式：count += 1
返回值：遍历完成后的 count
```

```python
def count_target(nums, target):
    count = 0

    for x in nums:
        if x == target:
            count += 1

    return count
```

时间复杂度为 `O(n)`，额外空间复杂度为 `O(1)`。

## 练习 4

```python
def find_min(nums):
    ans = nums[0]

    for x in nums[1:]:
        if x < ans:
            ans = x

    return ans
```

时间复杂度为 `O(n)`。

从算法思想上只维护一个 `ans`，额外空间是 `O(1)`。不过需要注意，Python 的 `nums[1:]` 会创建切片副本，严格按这段具体代码计算会产生 `O(n)` 的额外空间。

如果希望具体实现也只使用 `O(1)` 额外空间，可以避免切片：

```python
def find_min(nums):
    ans = nums[0]

    for i in range(1, len(nums)):
        if nums[i] < ans:
            ans = nums[i]

    return ans
```

这是 Python 中容易被忽略的区别：算法思路可能是常量空间，但某些方便语法会额外复制数据。

## 练习 5

```python
def contains_duplicate_brute_force(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True

    return False
```

内层从 `i + 1` 开始有两个作用：

- 不让元素与自己比较；
- 不重复比较已经检查过的元素对。

最坏时间复杂度为 `O(n²)`，额外空间复杂度为 `O(1)`。

## 练习 6

```python
def contains_duplicate(nums):
    seen = set()

    for x in nums:
        if x in seen:
            return True
        seen.add(x)

    return False
```

集合保存已经遍历过的元素。必须先检查后加入，否则当前元素一定会在集合中。只有检查完所有元素仍没有重复，才能返回 `False`。

集合成员查询平均为 `O(1)`，因此平均时间复杂度为 `O(n)`。最坏情况下集合保存 `n` 个元素，所以额外空间为 `O(n)`。

这里说“平均 `O(1)`”是因为 Python 的 `set` 基于哈希表。极端哈希冲突下理论最坏情况会更差，但入门面试分析通常采用平均复杂度。

## 练习 7

- 时间：`O(1)`；
- 额外空间：`O(1)`。

通过下标访问最后一个元素，不需要遍历数组。

## 练习 8

- 时间：`O(n)`；
- 额外空间：`O(1)`。

两个连续循环执行约 `2n` 次，忽略常数后是 `O(n)`。

## 练习 9

- 时间：`O(n²)`；
- 额外空间：`O(1)`。

程序检查不同下标组成的元素对，总数量为 `n(n-1)/2`，保留增长最快的项后是 `O(n²)`。

## 练习 10

- 时间：`O(log n)`；
- 额外空间：`O(1)`。

每轮将 `n` 缩小为原来的一半。

## 练习 11

- 时间：`O(n)`；
- 额外空间：`O(n)`。

每个元素复制一次，新列表最终包含 `n` 个元素。

## 练习 12

```text
外层下标范围：0 到 len(nums) - 1
内层下标为什么从 i + 1 开始：避免使用同一个元素，也避免重复比较
满足条件的布尔表达式：nums[i] + nums[j] == target
返回内容：[i, j]
时间复杂度：O(n²)
额外空间复杂度：O(1)
```

```python
def two_sum_brute_force(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

题目保证存在答案，所以这里可以不写找不到时的返回值。如果题目没有这个保证，可以根据接口要求在末尾返回 `None`、空列表，或者抛出异常。

## 掌握检查

如果你仍然需要看答案才能写出代码，不代表没有进步，但目前处在“能够复现”而不是“能够独立完成”的阶段。

建议在以下时间重新完成练习 2、3、5、6、12：

- 当天稍晚；
- 1 天后；
- 3 天后；
- 7 天后。

每次都从空白开始。连续两次无需提示完成，才可以减少复习频率。

