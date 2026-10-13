# 第 9b 讲：双堆——动态维护数据流中位数

## 0. 为什么一个堆不够

单个小顶堆擅长快速得到最小值，单个大顶堆擅长快速得到最大值。中位数位于有序序列中间，需要同时管理较小的一半和较大的一半。

因此把数据分成两部分：

```text
lower：较小的一半，使用大顶堆
upper：较大的一半，使用小顶堆
```

Python 的 `heapq` 是小顶堆，所以 `lower` 保存相反数。

---

## 1. 两个必须始终成立的不变量

### 1.1 顺序不变量

```text
lower 中每个数 <= upper 中每个数
```

只需比较两个堆顶：

```text
lower 的最大值 <= upper 的最小值
```

### 1.2 大小不变量

约定让 `lower` 与 `upper` 大小相同，或者比 `upper` 多一个：

```text
len(lower) == len(upper)
或
len(lower) == len(upper) + 1
```

于是：

- 奇数个元素：中位数是 lower 的最大值；
- 偶数个元素：中位数是两个堆顶的平均值。

---

## 2. 插入一个数字

一种不容易出错的策略：

1. 先把数字加入 `lower`；
2. 把 `lower` 的最大值移动到 `upper`，恢复顺序；
3. 如果 `upper` 更大，再把它的最小值移回 `lower`，恢复大小。

```python
import heapq


class MedianFinder:
    def __init__(self):
        self.lower = []   # 保存负数，相当于大顶堆
        self.upper = []   # 普通小顶堆

    def addNum(self, num):
        heapq.heappush(self.lower, -num)

        moved = -heapq.heappop(self.lower)
        heapq.heappush(self.upper, moved)

        if len(self.upper) > len(self.lower):
            moved_back = heapq.heappop(self.upper)
            heapq.heappush(self.lower, -moved_back)

    def findMedian(self):
        if len(self.lower) > len(self.upper):
            return -self.lower[0]

        return (-self.lower[0] + self.upper[0]) / 2
```

插入最多进行常数次堆操作，时间 `O(log n)`；查询中位数 `O(1)`；保存全部数据需要 `O(n)` 空间。

---

## 3. 手动执行

依次加入：

```text
5, 2, 10, 4
```

过程：

```text
加入 5：lower=[5], upper=[]              中位数 5
加入 2：lower=[2], upper=[5]             中位数 3.5
加入 10：lower=[5,2], upper=[10]          中位数 5
加入 4：lower=[4,2], upper=[5,10]         中位数 4.5
```

这里写的是逻辑内容，不是 Python 堆数组的真实排列。堆只保证堆顶正确，不保证整个列表有序。

---

## 4. 为什么不能只维护一个已排序列表

使用 Python 列表二分找到插入位置需要 `O(log n)`，但在中间插入需要移动元素，仍是 `O(n)`。

双堆不维护完整顺序，只维护中间分界，因此插入降为 `O(log n)`。

如果数据不会动态加入，只需要一次中位数，排序往往更简单。双堆的优势来自“多次插入 + 多次查询”。

---

## 5. 两种常见平衡写法

也可以先根据堆顶决定放入哪一边，再检查大小：

```python
if not lower or num <= -lower[0]:
    heapq.heappush(lower, -num)
else:
    heapq.heappush(upper, num)

if len(lower) > len(upper) + 1:
    heapq.heappush(upper, -heapq.heappop(lower))
elif len(upper) > len(lower):
    heapq.heappush(lower, -heapq.heappop(upper))
```

两种写法都正确。不要混合两套大小约定，否则 `findMedian` 会读取错误的一边。

---

## 6. 常见错误

1. `lower` 存负数，却忘记在读取和移动时恢复符号。
2. 只平衡大小，没有维持两边的顺序。
3. 只维持顺序，没有保证两边大小相差不超过一。
4. 偶数个元素时使用整数除法。
5. 在没有任何元素时调用 `findMedian`。
6. 认为堆内部数组已经完整排序。

## 7. 本讲检查表

1. 哪个堆保存较小一半？
2. 哪个堆允许多一个元素？
3. 两个堆顶分别表示什么？
4. 插入完成后，顺序与大小两个不变量是否都成立？
5. 题目是静态一次查询，还是动态反复查询？

## 8. 本讲总结

- 双堆把中位数两侧的数据分别管理。
- 大顶堆提供较小一半的最大值，小顶堆提供较大一半的最小值。
- 正确性依赖顺序不变量和大小不变量。
- 双堆适合数据流，而不是所有静态中位数问题。

