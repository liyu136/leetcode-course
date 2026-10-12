# Python 数据结构与 LeetCode 学习日志

这套讲义面向以下学习状态：

- 已经熟悉 Python 的基础语法；
- 能理解一些题目的大致思路，但经常无法独立写成代码；
- 尚未系统学习数据结构与算法；
- 每天可投入约 2 小时；
- 目标是在 1–2 个月后独立完成多数简单题和一部分常见中等题。

课程不会要求你先用 C 手写所有底层结构，也不会把重点放在背模板上。重点是建立这条能力链：

> 题目描述 → 手工步骤 → 状态与变量 → 伪代码 → Python → 测试与复杂度

## 课程入口

1. 阅读 [课程总纲](course-plan.md)。
2. 学习 [第 1 讲：程序执行、复杂度与从思路到代码](lessons/01-complexity-and-execution.md)。
3. 独立完成 [第 1 讲练习](exercises/01-exercises.md)。
4. 完成后再查看 [第 1 讲参考答案](answers/01-answers.md)。

### 第 2 讲：数组与 Python `list`

1. 学习 [第 2 讲：数组、动态数组与原地修改](lessons/02-arrays-and-python-list.md)。
2. 使用 [第 2 讲 Notebook 练习](exercises/02-exercises.ipynb) 编码。
3. 完成并自测后，再查看 [第 2 讲参考答案](answers/02-answers.md)。

### 第 3 讲：哈希表、`set` 与 `dict`

1. 学习 [第 3 讲：哈希思想、哈希表、set 与 dict](lessons/03-hash-tables-set-dict.md)。
2. 使用 [第 3 讲 Notebook 练习](exercises/03-exercises.ipynb) 编码。
3. 完成并自测后，再查看 [第 3 讲参考答案](answers/03-answers.md)。

### 第 4 讲：栈

1. 学习 [第 4 讲：栈——保存尚未完成的工作](lessons/04-stack.md)。
2. 使用 [第 4 讲 Notebook 练习](exercises/04-exercises.ipynb) 编码。
3. 完成并自测后，再查看 [第 4 讲参考答案](answers/04-answers.md)。

### 第 5–8 讲

- 第 5 讲：[队列、双端队列与 BFS](lessons/05-queue-deque-bfs.md) · [Notebook 练习](exercises/05-exercises.ipynb)
- 第 6 讲：[链表——通过引用连接数据](lessons/06-linked-list.md) · [Notebook 练习](exercises/06-exercises.ipynb)
- 第 7 讲：[二叉树与递归遍历](lessons/07-binary-tree-recursion.md) · [Notebook 练习](exercises/07-exercises.ipynb)
- 第 8 讲：[二叉搜索树、层序遍历与树的综合题](lessons/08-bst-level-order.md) · [Notebook 练习](exercises/08-exercises.ipynb)

这些 Notebook 的末尾包含前面章节的累计复习题。参考答案暂不提供，完成后统一批改。

### 第 9–10 讲：堆与图

- 第 9 讲：[堆与优先队列——反复取出当前最重要的元素](lessons/09-heap-priority-queue.md)
- 第 10 讲：[图、DFS 与 BFS——在关系网络中搜索](lessons/10-graph-dfs-bfs.md)

第 9 讲重点是 Python `heapq`、大小为 `k` 的堆、Top K 和多路合并。第 10 讲统一讲解邻接表、DFS、BFS、连通分量、图中环、拓扑排序与克隆图。

### 第 11–12 讲：双指针与滑动窗口

- 第 11 讲：[双指针——用两个位置共同描述搜索范围](lessons/11-two-pointers.md)
- 第 12 讲：[滑动窗口——维护一个连续区间的状态](lessons/12-sliding-window.md)

先掌握左右指针、读写指针和有序序列扫描，再学习固定窗口、可变窗口、频率窗口以及答案更新时机。

### 第 13–15 讲：二分、回溯与动态规划

- 第 13 讲：[二分查找——利用单调性每次排除一半](lessons/13-binary-search.md)
- 第 14 讲：[回溯——在选择树中尝试、撤销与继续](lessons/14-backtracking.md)
- 第 15 讲：[动态规划入门——保存重复子问题的答案](lessons/15-dynamic-programming-intro.md)

这三讲分别建立单调搜索、选择树搜索和重复子问题求解的完整思考流程。完成后，再进入 Hot 100 按模式混合训练。

## 使用规则

- 第一次做题时，可以查单个 Python 语法，但不要搜索整题答案。
- 一道题思考 15–25 分钟后仍无进展，再获取提示。
- 看过答案的题不算完成；关闭答案后从空白重写成功，才算完成。
- 每道核心题在第 1、3、7、14 天重新完成。
- 错题记录“具体卡点”，不要只写“不会”。

例如：

```text
不够具体：这道题我不会。
具体：我知道要用 set，但不知道应该在判断前还是判断后加入元素。
```

## 目录结构

```text
learning-log/
├── README.md
├── course-plan.md
├── lessons/       # 正式讲义
├── exercises/     # 不含答案的练习
└── answers/       # 参考答案与讲解
```
