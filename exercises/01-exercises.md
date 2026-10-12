# 第 1 讲练习

建议直接在独立的 `.py` 文件中完成代码。第一次练习可以查单个 Python 语法，但不要查看完整题解。

## 一、代码执行

### 练习 1

不要运行代码，先写出最终输出：

```python
nums = [3, 1, 4, 2]
ans = nums[0]

for x in nums[1:]:
    if x < ans:
        ans = x

print(ans)
```

同时写出每轮循环结束后的 `ans`。

### 练习 2

下面的函数原本想判断数组中是否存在负数。它有什么问题？

```python
def has_negative(nums):
    for x in nums:
        if x < 0:
            return True
        return False
```

请修正它，并说明：

- `return False` 为什么应该放在那个位置？
- 输入为空数组时会返回什么？

## 二、从思路到代码

### 练习 3：统计目标值

实现：

```python
def count_target(nums, target):
    """返回 target 在 nums 中出现的次数。"""
    pass
```

编码前先写：

```text
状态：
初始化：
更新条件：
更新方式：
返回值：
```

测试：

```python
assert count_target([1, 2, 2, 3], 2) == 2
assert count_target([], 2) == 0
assert count_target([1, 3], 2) == 0
```

### 练习 4：寻找最小值

实现：

```python
def find_min(nums):
    """返回非空数组中的最小值。"""
    pass
```

要求：

- 不使用内置的 `min`；
- 能正确处理全部为正、全部为负和只有一个元素的情况；
- 本题假定输入非空；
- 写出时间和额外空间复杂度。

### 练习 5：判断重复——暴力版本

实现：

```python
def contains_duplicate_brute_force(nums):
    pass
```

使用两层循环比较不同位置的元素。要求：

- 同一个位置不能和自己比较；
- 找到重复立即返回 `True`；
- 全部检查完后返回 `False`；
- 写出时间和空间复杂度。

### 练习 6：判断重复——集合版本

使用 `set` 把上一题优化为平均 `O(n)` 时间：

```python
def contains_duplicate(nums):
    pass
```

在写代码前回答：

1. 集合中保存什么？
2. 为什么要先检查、后加入？
3. 为什么 `return False` 应位于循环外？
4. 最坏情况下集合会保存多少个元素？

## 三、复杂度判断

写出以下代码的时间复杂度和额外空间复杂度，并用一句话说明原因。

### 练习 7

```python
def get_last(nums):
    return nums[-1]
```

### 练习 8

```python
def print_twice(nums):
    for x in nums:
        print(x)

    for x in nums:
        print(x)
```

### 练习 9

```python
def print_pairs(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            print(nums[i], nums[j])
```

### 练习 10

```python
def reduce_number(n):
    while n > 1:
        n //= 2
```

### 练习 11

```python
def make_copy(nums):
    result = []
    for x in nums:
        result.append(x)
    return result
```

## 四、综合练习

### 练习 12：两数之和暴力版

给定整数数组 `nums` 和整数 `target`，假设恰好存在一组答案，返回两个元素的下标。

```python
def two_sum_brute_force(nums, target):
    pass
```

示例：

```python
assert two_sum_brute_force([2, 7, 11, 15], 9) == [0, 1]
assert two_sum_brute_force([3, 2, 4], 6) == [1, 2]
assert two_sum_brute_force([3, 3], 6) == [0, 1]
```

编码前写出：

```text
外层下标范围：
内层下标为什么从 i + 1 开始：
满足条件的布尔表达式：
返回内容：
时间复杂度：
额外空间复杂度：
```

## 五、自我检查

完成后确认：

- [ ] 我没有先看参考答案；
- [ ] 我能解释每个变量表示什么；
- [ ] 我测试了空数组或题目允许的最小输入；
- [ ] 我测试了负数或重复值；
- [ ] 我能说明时间和空间复杂度；
- [ ] 我能关闭代码后重新写出至少三个函数。

