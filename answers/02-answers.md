# 第 2 讲参考答案

请先完成 Notebook 并运行测试，再查看本文件。参考答案不是唯一写法，重点是变量含义和循环不变量是否清楚。

## 1. 概念题

### 1.1 别名与切片

```python
a = [1, 2, 3]
b = a
c = a[:]
b[0] = 9
c[1] = 8
```

最终：

```python
a == [9, 2, 3]
b == [9, 2, 3]
c == [1, 8, 3]
```

`a` 和 `b` 指向同一个列表，`c` 是新的外层列表。

### 1.2 二维列表

```python
grid = [[0] * 2] * 3
grid[0][1] = 7
```

结果：

```python
[[0, 7], [0, 7], [0, 7]]
```

三行引用同一个内部列表。

### 1.3 复杂度

- `nums[-1]`：时间 `O(1)`，额外空间 `O(1)`；
- `nums[1:]`：时间 `O(n)`，额外空间 `O(n)`；
- `nums.pop(0)`：时间 `O(n)`，额外空间通常记作 `O(1)`；
- 连续执行 `n` 次 `append`：总时间 `O(n)`，单次摊还 `O(1)`；
- `x in nums`：最坏时间 `O(n)`。

## 2. 原地反转

```python
def reverse_in_place(nums):
    left = 0
    right = len(nums) - 1

    while left < right:
        nums[left], nums[right] = nums[right], nums[left]
        left += 1
        right -= 1
```

不变量：每轮开始时，`left` 左侧和 `right` 右侧都已经处于反转后的正确位置。

- 时间：`O(n)`；
- 额外空间：`O(1)`。

## 3. 删除指定值

```python
def remove_value(nums, val):
    write = 0

    for read in range(len(nums)):
        if nums[read] != val:
            nums[write] = nums[read]
            write += 1

    return write
```

不变量：处理 `read` 之前，`nums[:write]` 恰好是此前所有不等于 `val` 的元素，并保持原顺序。

- 时间：`O(n)`；
- 额外空间：`O(1)`。

## 4. 移动零

先依次写入所有非零元素，再把剩余位置填成零：

```python
def move_zeroes(nums):
    write = 0

    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write] = nums[read]
            write += 1

    while write < len(nums):
        nums[write] = 0
        write += 1
```

第一段循环结束后：

- `nums[:write]` 是全部非零元素；
- 相对顺序保持不变；
- 后面有 `len(nums)-write` 个位置需要设为零。

- 时间：`O(n)`；
- 额外空间：`O(1)`。

也可以在发现非零元素时与 `write` 位置交换。这种写法同样正确，但需要更仔细地描述不变量。

## 5. 有序数组的平方

输入可能包含负数，因此直接从左到右平方不会保持有序：

```text
[-4, -1, 0, 3, 10]
平方后：[16, 1, 0, 9, 100]
```

最大平方一定来自当前绝对值最大的端点。把较大的平方放到结果末尾：

```python
def sorted_squares(nums):
    result = [0] * len(nums)
    left = 0
    right = len(nums) - 1
    write = len(nums) - 1

    while left <= right:
        left_square = nums[left] * nums[left]
        right_square = nums[right] * nums[right]

        if left_square > right_square:
            result[write] = left_square
            left += 1
        else:
            result[write] = right_square
            right -= 1

        write -= 1

    return result
```

不变量：`result[write+1:]` 已经保存了最大的若干平方，并且处于最终正确位置。

- 时间：`O(n)`；
- 额外空间：`O(n)`，因为题目返回新列表。

简单地平方后排序需要 `O(n log n)` 时间，没有利用输入已经有序的条件。

## 6. 数组右旋

### 使用额外列表

```python
def rotate_right(nums, k):
    if not nums:
        return

    k %= len(nums)
    rotated = nums[-k:] + nums[:-k]
    nums[:] = rotated
```

`nums[:] = rotated` 修改原列表对象；如果写成 `nums = rotated`，调用者持有的原列表不会改变。

- 时间：`O(n)`；
- 额外空间：`O(n)`。

### 挑战：`O(1)` 额外空间

利用三次反转：

```text
[1, 2, 3, 4, 5, 6, 7], k = 3

全部反转：      [7, 6, 5, 4, 3, 2, 1]
反转前 k 个：   [5, 6, 7, 4, 3, 2, 1]
反转剩余部分：  [5, 6, 7, 1, 2, 3, 4]
```

```python
def rotate_right_constant_space(nums, k):
    if not nums:
        return

    def reverse_range(left, right):
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

    n = len(nums)
    k %= n

    reverse_range(0, n - 1)
    reverse_range(0, k - 1)
    reverse_range(k, n - 1)
```

- 时间：`O(n)`；
- 额外空间：`O(1)`。

## 7. 调试题

边遍历边删除会让元素移动，循环却继续向前，因此可能跳过元素。

新列表版本：

```python
def remove_negatives(nums):
    result = []

    for x in nums:
        if x >= 0:
            result.append(x)

    return result
```

原地版本可以使用与 `remove_value` 相同的读写指针：

```python
def remove_negatives_in_place(nums):
    write = 0

    for read in range(len(nums)):
        if nums[read] >= 0:
            nums[write] = nums[read]
            write += 1

    del nums[write:]
```

最后的切片删除会真正缩短原列表。总体时间是 `O(n)`，算法只使用 `O(1)` 额外状态。

## 复习建议

核心题是：

1. `remove_value`；
2. `move_zeroes`；
3. `sorted_squares`。

请在第 1、3、7 天从空白重新完成。复习时先写一句循环不变量，再写代码。

