# 第 4b 讲：单调栈与单调队列——维护仍有可能成为答案的候选

## 0. 从普通栈进一步前进

第 4 讲已经学习“每日温度”：栈保存尚未找到右侧更大元素的下标。本讲补充三类 Hot 100 模式：

1. 为每个元素寻找左右第一个更小边界；
2. 当前元素作为“底部”时计算可确定的贡献；
3. 在滑动窗口中维护当前最大值。

核心思想是：**一旦某个候选确定不可能比另一个候选更有用，就立即删除它。**

---

## 1. 单调栈到底保存什么

单调栈通常保存下标，因为答案往往需要：

- 元素值：`nums[index]`；
- 距离：`current - index`；
- 左右边界位置。

“单调递增栈”通常表示从栈底到栈顶，对应元素值递增。遇到更小值时弹栈，被弹出的元素终于找到了右侧第一个更小元素。

### 1.1 相等元素怎样处理

循环条件用 `<` 还是 `<=` 会影响相等元素归属于哪个边界。没有脱离具体题目的统一答案；关键是左右两侧的规则要能避免重复计算或漏算。

---

## 2. 柱状图中的最大矩形

高度：

```text
[2, 1, 5, 6, 2, 3]
```

如果柱子 `i` 作为矩形高度，需要知道它能向左右延伸到哪里。边界是两侧第一个严格更矮的柱子。

扫描到更矮柱子时，栈顶柱子的右边界确定；弹栈后新的栈顶就是它的左边界。

```python
def largest_rectangle_area(heights):
    extended = [0] + heights + [0]
    stack = []
    best = 0

    for right, height in enumerate(extended):
        while stack and extended[stack[-1]] > height:
            middle = stack.pop()
            left = stack[-1]
            width = right - left - 1
            best = max(best, extended[middle] * width)

        stack.append(right)

    return best
```

两个哨兵 `0` 的作用：

- 左侧哨兵让弹栈后总能找到左边界；
- 右侧哨兵迫使剩余柱子全部结算。

栈内保持高度非递减。每个下标入栈一次、出栈一次，总时间 `O(n)`。

### 2.1 为什么宽度是 `right - left - 1`

弹出的 `middle`：

- `right` 是右侧第一个更矮位置，不能包含；
- `left` 是左侧第一个更矮位置，也不能包含；
- 真正可用区间为 `(left, right)`。

---

## 3. 接雨水：弹出的高度形成凹槽底部

当当前柱子高于栈顶时，栈顶可能是一个凹槽底部：

```python
def trap(height):
    stack = []
    water = 0

    for right, right_height in enumerate(height):
        while stack and height[stack[-1]] < right_height:
            bottom = stack.pop()

            if not stack:
                break

            left = stack[-1]
            width = right - left - 1
            bounded_height = min(height[left], right_height) - height[bottom]
            water += width * bounded_height

        stack.append(right)

    return water
```

一次弹栈只计算从 `height[bottom]` 到较低边界高度的这一层水，不会与之后的弹栈重复。

### 3.1 双指针方法

接雨水也可以维护：

```text
left_max  = 左边见过的最高柱子
right_max = 右边见过的最高柱子
```

较低一侧的水量已经由其本侧最大值确定，因此移动较低一侧。

```python
def trap_two_pointers(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0

    while left < right:
        if height[left] <= height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1

    return water
```

两种方法都为 `O(n)`；双指针额外空间 `O(1)`，单调栈更能迁移到“边界结算”问题。

---

## 4. 单调队列：滑动窗口最大值

窗口不断右移时，需要：

1. 删除已经离开窗口的元素；
2. 快速得到窗口最大值。

使用 `deque` 保存下标，并保持对应值从队首到队尾单调递减。

```python
from collections import deque

def max_sliding_window(nums, k):
    queue = deque()
    answer = []

    for right, value in enumerate(nums):
        left = right - k + 1

        while queue and queue[0] < left:
            queue.popleft()

        while queue and nums[queue[-1]] <= value:
            queue.pop()

        queue.append(right)

        if left >= 0:
            answer.append(nums[queue[0]])

    return answer
```

### 4.1 为什么较小的旧值可以永久删除

假设旧值 `a` 在新值 `b` 左边，而且 `a <= b`：

- 在数值上，`a` 不如 `b`；
- 在有效时间上，`a` 还会比 `b` 更早离开窗口。

因此只要 `b` 存在，`a` 永远不可能成为窗口最大值。

队首是当前最大值；队尾用于删除被新元素淘汰的候选。

---

## 5. 单调栈、单调队列怎样选择

| 问题 | 结构 | 候选何时失效 |
|---|---|---|
| 右侧第一个更大/更小 | 单调栈 | 新元素解决了旧元素 |
| 左右边界、矩形面积 | 单调栈 | 新边界使旧柱子可以结算 |
| 固定窗口最大/最小值 | 单调队列 | 离开窗口，或被更新且更优的元素支配 |

不要只因为题目出现“最大值”就使用单调结构。它通常还需要连续扫描、窗口移动或“第一个边界”等顺序关系。

## 6. 常见错误

1. 栈里保存值，但答案需要下标距离。
2. 忘记结算扫描结束后仍留在栈中的柱子。
3. 柱状图宽度写成 `right - left`，多算一格。
4. 接雨水弹栈后栈为空，却继续读取左边界。
5. 单调队列只维护单调性，却忘记删除窗口外下标。
6. 队列保存值导致无法判断某个重复值是否已经离开窗口。

## 7. 本讲检查表

1. 我寻找的是第一个更大/更小元素，还是窗口中的最大值？
2. 结构中应该保存值还是下标？
3. 栈或队列保持递增还是递减？
4. 相等值使用 `<` 还是 `<=`，会影响谁被保留？
5. 被弹出的元素在这一刻确定了什么答案？
6. 是否需要哨兵结算剩余元素？
7. 每个元素是否最多进入和离开结构一次？

## 8. 本讲总结

- 单调结构保存的是仍可能成为答案的候选。
- 柱状图使用“左右第一个更小边界”。
- 接雨水可以把弹出的柱子视为凹槽底部。
- 单调队列同时维护窗口有效期和候选优先级。
- 看起来存在嵌套 `while`，但每个元素最多进出一次，所以总时间通常是 `O(n)`。

