# 第 5 讲批改：队列、`deque` 与 BFS

## 总评

完成度：**很好，约 8.5 / 10**。

Notebook 中原有的全部断言都通过了。你已经能够独立写出：

- `deque` 时间窗口；
- 邻接表 BFS；
- 网格 BFS 的主体结构；
- 多源 BFS；
- 哈希频率统计；
- 栈模拟退格。

额外边界测试发现了一处真实错误：网格最短路在检查目标格是否合法、是否为障碍之前，就直接返回了距离。除这一点外，主要算法均正确。

---

## 1. 概念题

五题基本正确。

### 可以更准确的两处

第 3 题不能只记成“无权图”，更完整的说法是：

> 普通 BFS 能求无权图，或所有边代价相同的图中的最短距离。

第 4 题你的理解正确。保存 `level_size` 的准确含义是：

> 循环开始时，队列里现有的这些节点属于当前层；处理它们时新加入的节点属于下一层。

---

## 2. RecentCounter

结果正确，边界也正确。

```python
while self.data[0] < t - 3000:
    self.data.popleft()
```

这里使用 `<` 而不是 `<=` 很重要，因为区间左端点 `t - 3000` 也包括在窗口内。

复杂度分析：每个请求只入队一次、最多出队一次，因此多次调用的总时间是线性的，单次调用的均摊时间为 `O(1)`。

---

## 3. 无权图最短距离

代码正确而且简洁。

```python
dis = {start: 0}
```

这里的 `dis` 同时承担两个作用：

1. 记录最短距离；
2. 判断节点是否已经被发现。

你也正确地在入队时写入 `dis`，所以一个节点最多入队一次。

时间复杂度为 `O(V + E)`，空间复杂度为 `O(V)`。

---

## 4. 网格最短路

主体思路正确，但存在一处边界错误。

原代码先执行：

```python
if (nr, nc) == target:
    return dis + 1
```

然后才检查坐标是否越界、格子是否为障碍。这会导致下面的输入错误地返回 `1`：

```python
grid_shortest_path([[0, 1]], (0, 0), (0, 1))
```

终点是障碍，应返回 `-1`。

正确顺序应该是：

1. 产生邻居坐标；
2. 检查边界；
3. 检查障碍；
4. 检查是否访问过；
5. 标记并入队；
6. 出队后检查是否到达目标，或在确认邻居合法后再检查目标。

推荐写法：

```python
from collections import deque

def grid_shortest_path(grid, start, target):
    rows = len(grid)
    cols = len(grid[0])
    queue = deque([(start[0], start[1], 0)])
    visited = {start}
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        row, col, distance = queue.popleft()

        if (row, col) == target:
            return distance

        for dr, dc in directions:
            nr = row + dr
            nc = col + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == 1:
                continue
            if (nr, nc) in visited:
                continue

            visited.add((nr, nc))
            queue.append((nr, nc, distance + 1))

    return -1
```

建议记住网格题的固定顺序：

```text
生成坐标 → 检查边界 → 检查格子 → 检查 visited → 标记并入队
```

---

## 5. 腐烂的橘子

你的实现能够通过已有测试和补充测试，多源 BFS 的核心也写对了：所有初始腐烂橘子在第 0 分钟一起入队。

当前版本用 `visit` 防止重复入队，因此虽然没有真的把新鲜橘子改成 `2`，算法仍然正确。

不过可以进一步简化。只让新鲜橘子进入队列，并直接修改网格：

```python
if (
    0 <= nr < rows
    and 0 <= nc < cols
    and grid[nr][nc] == 1
):
    grid[nr][nc] = 2
    fresh -= 1
    queue.append((nr, nc, minute + 1))
```

这样网格本身就充当了 `visited`，不再需要单独的集合。

你在文字中写的：

```python
grid[nr][nc] = 1
```

应该区分为：

```python
grid[nr][nc] == 1   # 判断它是不是新鲜橘子
grid[nr][nc] = 2    # 把它标记为已经腐烂
```

`==` 是比较，`=` 是赋值。

---

## 6. 第一个只出现一次的字符

代码正确，时间复杂度为 `O(n)`。

你写的这句话很好：

> `O(n)` 并不是只能遍历一次，只要不是随着 `n` 增长而进行嵌套的完整遍历，两次线性遍历仍然是 `O(n)`。

严格地说，两个循环的工作量是 `n + n = 2n`，忽略常数后仍为 `O(n)`。

---

## 7. 简化退格字符串

代码正确，空栈时遇到 `#` 也处理正确。

栈中元素的含义可以表述为：

> 栈保存当前已经处理过、并且尚未被退格删除的字符。

时间复杂度为 `O(n)`，额外空间为 `O(n)`。

---

## 8. 总结题修正

第 1、4、5 题正确。

第 2 题回答不完整。可以承担 `visited` 作用的包括：

- 无权图题中的距离字典 `dis`；
- 网格最短路中的 `visited` 集合；
- 腐烂橘子优化版中修改后的 `grid`。

第 3 题中，“方向数组”不是边本身。更准确的说法是：

- 节点：每一个可通行的格子；
- 边：两个上下左右相邻、并且都可通行的格子之间的连接；
- `directions`：用于生成候选邻居的工具。

---

## 代码表达建议

这些不是正确性错误，但改掉后代码会更像标准题解：

1. 不要用 `dir` 作变量名，因为它会遮住 Python 内置函数 `dir()`；建议写 `directions`。
2. 坐标始终使用元组：`(row, col)`，不需要反复写 `tuple([nr, nc])`。
3. 可以直接解包：

   ```python
   row, col, distance = queue.popleft()
   ```

   比 `node[0]`、`node[1]`、`node[2]` 更清晰。

## 建议的复习动作

明天不要看答案，从空白重新写一次 `grid_shortest_path`。写代码前先在纸上写：

```text
queue 中元素：(row, col, distance)
入队条件：合法、可走、未访问
标记时机：入队时
结束条件：目标出队
```

只要这四句能自己写出来，网格 BFS 的代码通常就能顺着写完。
