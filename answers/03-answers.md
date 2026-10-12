# 第 3 讲参考答案

请先完成练习并运行测试。阅读答案后，关闭本文件，从空白重写核心题。

## 1. 概念题

1. 键空间通常大于槽位数量，根据抽屉原理，不同键可能映射到相同槽位。
2. `list` 可变，修改后哈希值和定位关系可能失效，因此不可哈希。
3. `x in my_dict` 检查键。
4. `set(nums)` 平均时间 `O(n)`，额外空间 `O(n)`。
5. 使用可哈希元组：`visited.add((row, col))`。

## 2. 频率统计

```python
def frequency_map(items):
    counts = {}

    for item in items:
        counts[item] = counts.get(item, 0) + 1

    return counts
```

- 键：元素；
- 值：截至当前位置的出现次数；
- 平均时间：`O(n)`；
- 额外空间：`O(k)`，其中 `k` 是不同元素数量，最坏为 `O(n)`。

## 3. 有效的字母异位词

```python
def is_anagram(s, t):
    if len(s) != len(t):
        return False

    counts = {}

    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1

    for ch in t:
        if ch not in counts:
            return False

        counts[ch] -= 1

        if counts[ch] < 0:
            return False

    return True
```

长度相同，并且第二个字符串没有把任何字符的可用数量减到负数，即可确定频率完全相同。

另一种写法会在计数减到零时删除键，最后检查字典是否为空。两种都可以，但必须能说明正确性。

## 4. 两数之和

```python
def two_sum(nums, target):
    positions = {}

    for i, x in enumerate(nums):
        needed = target - x

        if needed in positions:
            return [positions[needed], i]

        positions[x] = i
```

- 键：此前出现的数值；
- 值：该数值的下标；
- 不变量：处理下标 `i` 前，字典保存了 `nums[:i]` 中元素到下标的映射；
- 先查询保证不会把当前元素使用两次。

平均时间 `O(n)`，额外空间 `O(n)`。

## 5. 两个数组的交集

集合运算版本：

```python
def intersection_builtin(nums1, nums2):
    return list(set(nums1) & set(nums2))
```

手写版本：

```python
def intersection_manual(nums1, nums2):
    values1 = set(nums1)
    result = set()

    for x in nums2:
        if x in values1:
            result.add(x)

    return list(result)
```

设两个数组长度为 `m、n`，平均时间 `O(m+n)`，额外空间 `O(m+n)`；更精细的空间上界取决于不同元素数量。

## 6. 分组字母异位词

```python
def group_anagrams(words):
    groups = {}

    for word in words:
        key = "".join(sorted(word))

        if key not in groups:
            groups[key] = []

        groups[key].append(word)

    return list(groups.values())
```

- 键：排序后的规范字符串；
- 值：具有该规范形式的原单词列表。

若有 `n` 个单词，平均长度为 `k`，排序方案时间约为 `O(nk log k)`，保存结果和键需要额外空间。

如果字符集固定为 26 个小写字母，也可以用长度 26 的频率元组作键，把构造键的成本降为 `O(k)`。

## 7. 最长连续序列

```python
def longest_consecutive(nums):
    values = set(nums)
    best = 0

    for x in values:
        if x - 1 not in values:
            current = x
            length = 1

            while current + 1 in values:
                current += 1
                length += 1

            best = max(best, length)

    return best
```

只有没有前驱 `x-1` 的元素才启动搜索，因此每个连续数字只会在某个序列扫描中被访问一次。平均时间 `O(n)`，额外空间 `O(n)`。

## 复习重点

必须能够从空白重写：

1. `frequency_map`；
2. `two_sum`；
3. `is_anagram`。

`group_anagrams` 和 `longest_consecutive` 达到“能解释并在少量提示后写出”即可，随后通过间隔复习提升到独立完成。

