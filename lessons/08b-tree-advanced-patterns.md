# 第 8.5 讲：二叉树进阶递归模式

## 0. 为什么需要补这一讲

第 7、8 讲已经解决了树题的基础问题：

- DFS 前序、中序、后序；
- 最大深度、翻转、对称、直径；
- BST 搜索、验证、第 K 小；
- 层序遍历与最近公共祖先。

Hot 100 中还有一组题，难点不在“会不会遍历”，而在于怎样设计递归返回值或维护路径状态：

1. 将有序数组转换为平衡二叉搜索树；
2. 二叉树展开为链表；
3. 从前序与中序遍历序列构造二叉树；
4. 路径总和 III；
5. 二叉树中的最大路径和。

本讲还补充“判断平衡二叉树”，因为它集中体现了一个重要技巧：

> 递归返回正常答案，也可以用特殊值同时报告失败。

---

## 1. 平衡二叉树

### 1.1 什么叫平衡

对树中的每一个节点：

```text
左子树高度与右子树高度之差不超过 1
```

并且左右子树本身也必须平衡。

注意是“每一个节点”，不能只检查根节点。

```text
        1
       / \
      2   3
     /
    4
```

这棵树仍然平衡：根节点两侧高度只相差 1。

```text
        1
       /
      2
     /
    3
```

这棵树不平衡：节点 1 的左右高度相差 2。

### 1.2 低效方法：每个节点重新计算高度

可以对每个节点调用一次 `max_depth`：

```python
def is_balanced(root):
    if root is None:
        return True

    left_height = max_depth(root.left)
    right_height = max_depth(root.right)

    return (
        abs(left_height - right_height) <= 1
        and is_balanced(root.left)
        and is_balanced(root.right)
    )
```

这在倾斜树中会反复计算相同子树的高度，最坏达到 `O(n²)`。

### 1.3 一次后序递归：高度或失败标记

定义辅助函数：

> `height(node)`：如果子树平衡，返回它的高度；如果不平衡，返回 `-1`。

```python
def is_balanced(root):
    def height(node):
        if node is None:
            return 0

        left_height = height(node.left)
        if left_height == -1:
            return -1

        right_height = height(node.right)
        if right_height == -1:
            return -1

        if abs(left_height - right_height) > 1:
            return -1

        return 1 + max(left_height, right_height)

    return height(root) != -1
```

每个节点只处理一次：

```text
时间：O(n)
空间：O(h)
```

这里的 `-1` 不是实际高度，而是一种“失败信号”。父节点收到后可以立即停止继续计算。

---

## 2. 将有序数组转换为平衡 BST

有序数组：

```text
[-10, -3, 0, 5, 9]
```

要构造高度平衡的 BST，可以不断选择区间中点作为根：

```text
中点       → 当前根
左半区间   → 左子树
右半区间   → 右子树
```

```python
def sorted_array_to_bst(nums):
    def build(left, right):
        if left > right:
            return None

        middle = (left + right) // 2
        root = TreeNode(nums[middle])

        root.left = build(left, middle - 1)
        root.right = build(middle + 1, right)

        return root

    return build(0, len(nums) - 1)
```

函数契约：

> `build(left, right)` 使用 `nums[left:right+1]` 构造一棵平衡 BST，并返回根节点。

为什么选择中点？

- 左右两边元素数量尽量接近；
- 数组已经有序，所以左半都小于根，右半都大于根；
- 对每个子区间重复同样过程。

每个元素只创建一次：

```text
时间：O(n)
递归空间：O(log n)   # 构造结果本身不计
```

不要使用：

```python
nums[:middle]
nums[middle + 1:]
```

频繁切片会额外复制数组。使用下标区间更稳定。

---

## 3. 从前序与中序遍历构造二叉树

假设节点值互不相同：

```text
preorder = [3, 9, 20, 15, 7]
inorder  = [9, 3, 15, 20, 7]
```

两种遍历分别提供不同信息：

```text
前序第一个元素：当前子树的根
根在中序中的位置：左子树与右子树的分界
```

根是 `3`：

```text
inorder = [9]  3  [15, 20, 7]
           左       右
```

左子树有 1 个节点，所以前序中根后面的 1 个元素属于左子树：

```text
preorder = 3  [9]  [20, 15, 7]
                左       右
```

### 3.1 使用哈希表定位中序下标

如果每次在中序数组中线性搜索根，最坏会达到 `O(n²)`。

先建立：

```python
inorder_index = {
    value: index
    for index, value in enumerate(inorder)
}
```

之后查找根位置平均为 `O(1)`。

### 3.2 使用区间递归

```python
def build_tree(preorder, inorder):
    inorder_index = {
        value: index
        for index, value in enumerate(inorder)
    }

    def build(pre_left, pre_right, in_left, in_right):
        if pre_left > pre_right:
            return None

        root_value = preorder[pre_left]
        root = TreeNode(root_value)

        middle = inorder_index[root_value]
        left_size = middle - in_left

        root.left = build(
            pre_left + 1,
            pre_left + left_size,
            in_left,
            middle - 1,
        )

        root.right = build(
            pre_left + left_size + 1,
            pre_right,
            middle + 1,
            in_right,
        )

        return root

    return build(
        0,
        len(preorder) - 1,
        0,
        len(inorder) - 1,
    )
```

这里最容易错的是四个边界。不要同时在脑中记公式，先计算：

```text
left_size = 中序根下标 - 中序左边界
```

然后前序中根后面的 `left_size` 个元素属于左子树。

复杂度：

```text
时间：O(n)
额外空间：O(n)   # 哈希表和递归栈
```

---

## 4. 二叉树展开为链表

目标：原地把树展开成前序遍历顺序的“右链表”：

```text
原树：
        1
       / \
      2   5
     / \   \
    3   4   6

展开：
1 → 2 → 3 → 4 → 5 → 6
```

所有节点都应满足：

```text
node.left is None
```

### 4.1 为什么普通前序修改容易丢失子树

如果在节点 1 处立刻执行：

```python
root.right = root.left
root.left = None
```

原来的右子树 5 可能失去引用。因此修改指针前必须明确后续节点保存在哪里。

### 4.2 反向前序：右、左、根

如果从前序顺序的末尾向前连接，每个节点只需要指向已经处理好的 `previous`：

```python
def flatten(root):
    previous = None

    def dfs(node):
        nonlocal previous

        if node is None:
            return

        dfs(node.right)
        dfs(node.left)

        node.right = previous
        node.left = None
        previous = node

    dfs(root)
```

处理顺序是：

```text
右子树 → 左子树 → 当前节点
```

但最终形成的链表是：

```text
根 → 左 → 右
```

原因是我们在反向建立链表：当前节点连接到已经完成的后继。

函数没有返回新树，而是原地修改输入节点。

---

## 5. 路径总和 III

这道题与第 7 讲的“路径总和”不同。

### 5.1 两道题的区别

第 7 讲路径总和：

```text
必须从根开始
必须在叶节点结束
```

路径总和 III：

```text
可以从任意节点开始
可以在任意后代节点结束
必须一直向下，不能拐回父节点
统计路径数量，不是只判断是否存在
```

### 5.2 朴素方法

以每个节点为起点，再向下统计：

```text
最坏时间：O(n²)
```

这可以作为第一版思路，但 Hot 100 中更值得掌握的是前缀和方法。

### 5.3 根到当前节点的前缀和

假设当前根到节点的累加和为：

```text
current_sum
```

如果此前路径上出现过：

```text
current_sum - target_sum
```

那么从那个前缀之后到当前节点的路径和正好是 `target_sum`。

数组中的“和为 K 的子数组”也是同一原理，只是树中同时存在多条递归路径。

### 5.4 哈希表只记录当前递归路径

```python
def path_sum(root, target_sum):
    prefix_counts = {0: 1}

    def dfs(node, current_sum):
        if node is None:
            return 0

        current_sum += node.val

        paths = prefix_counts.get(
            current_sum - target_sum,
            0,
        )

        prefix_counts[current_sum] = (
            prefix_counts.get(current_sum, 0) + 1
        )

        paths += dfs(node.left, current_sum)
        paths += dfs(node.right, current_sum)

        prefix_counts[current_sum] -= 1

        return paths

    return dfs(root, 0)
```

初始化：

```python
prefix_counts = {0: 1}
```

表示在路径开始前有一个和为 0 的空前缀，使“从根开始且和为目标”的路径也能被统计。

### 5.5 为什么递归返回前要减一

```python
prefix_counts[current_sum] -= 1
```

哈希表应只表示“当前根到当前节点”这条路径。

从左子树返回、准备进入右子树时，左子树节点不能成为右子树路径的前缀。减一是在撤销当前分支加入的状态，这就是回溯。

复杂度：

```text
平均时间：O(n)
空间：O(h) 到 O(n)
```

---

## 6. 二叉树中的最大路径和

路径可以从任意节点开始，在任意节点结束，但相邻节点必须通过父子边连接，且同一节点不能重复经过。

节点值可能为负数。

### 6.1 与直径题相似，但不是同一个量

直径题：

```text
left_height + right_height
```

最大路径和：

```text
node.val + left_gain + right_gain
```

共同模式是：

- 辅助函数向父节点返回“一条可以继续连接的单边路径”；
- 独立变量记录“左右两边在当前节点汇合”的全局答案。

### 6.2 父节点只能选择一边

如果当前节点同时把左、右两条路径返回给父节点，就会出现分叉，不再是一条简单路径。

所以返回：

```python
node.val + max(left_gain, right_gain)
```

但更新全局答案时，允许左右两边同时经过当前节点：

```python
node.val + left_gain + right_gain
```

### 6.3 负贡献应被舍弃

```python
left_gain = max(gain(node.left), 0)
right_gain = max(gain(node.right), 0)
```

如果一侧路径和为负，连接它只会让答案更小，因此把贡献看作 0。

完整代码：

```python
def max_path_sum(root):
    best = float("-inf")

    def gain(node):
        nonlocal best

        if node is None:
            return 0

        left_gain = max(gain(node.left), 0)
        right_gain = max(gain(node.right), 0)

        through_node = (
            node.val + left_gain + right_gain
        )
        best = max(best, through_node)

        return node.val + max(left_gain, right_gain)

    gain(root)
    return best
```

为什么 `best` 不能初始化为 0？

如果整棵树所有值都是负数，答案仍然必须选择至少一个节点。例如单节点 `-3` 的答案是 `-3`，不是 0。

---

## 7. 六种模式放在一起比较

| 问题 | 递归函数返回什么 | 额外状态 |
|---|---|---|
| 判断平衡 | 高度，或失败标记 `-1` | 无 |
| 有序数组转 BST | 构造好的子树根节点 | 数组区间 |
| 前序和中序构树 | 构造好的子树根节点 | 两组遍历区间、下标表 |
| 展开为链表 | 无，原地修改 | `previous` |
| 路径总和 III | 当前子树中的路径数量 | 当前前缀和、前缀计数字典 |
| 最大路径和 | 可连接给父节点的单边最大贡献 | 全局 `best` |

看到新树题时，不要先猜前序还是后序。先问：

```text
1. 父节点需要从孩子那里得到什么？
2. 当前节点需要向父节点返回什么？
3. 是否还有一个不能直接返回的全局答案？
4. 是否携带了只属于当前根到节点路径的状态？
5. 从递归返回时是否需要撤销状态？
```

---

## 8. 常见错误

### 8.1 判断平衡时重复计算高度

让同一次后序递归同时完成高度计算和平衡判断。

### 8.2 构树时反复切片和搜索

使用下标区间，并提前建立中序值到下标的映射。

### 8.3 展开链表时丢失原右子树

修改引用前必须保存后续结构，或使用反向前序配合 `previous`。

### 8.4 路径总和 III 忘记回溯前缀计数

左右子树是两条不同路径，不能共享只属于另一分支的前缀。

### 8.5 最大路径和把左右两边一起返回

全局候选可以同时使用左右两侧；返回给父节点时只能选择一侧。

### 8.6 最大路径和把 best 初始化为 0

全负树会得到错误答案。应初始化为负无穷。

---

## 9. 本讲检查表

```text
1. 递归函数返回的是高度、节点、数量还是路径贡献？
2. 是否可以用特殊返回值报告失败？
3. 构树时根节点怎样确定？左右区间怎样划分？
4. 原地修改指针前，后续结构是否仍能找到？
5. 路径可以从哪里开始、在哪里结束？
6. 哈希表表示所有历史，还是只表示当前递归路径？
7. 返回上一层前是否需要撤销状态？
8. 当前节点的全局候选与返回给父节点的结果是否相同？
9. 负贡献应该保留还是舍弃？
10. 全部节点为负数时，初始化值是否仍然正确？
```

## 10. 本讲总结

1. 平衡判断可以让高度函数用 `-1` 同时报告失败，避免重复计算。
2. 有序数组取中点，可以递归构造平衡 BST。
3. 前序确定根，中序划分左右子树；哈希表用于快速定位根。
4. 二叉树展开可使用“右、左、根”的反向前序原地连接。
5. 路径总和 III 是树上的前缀和，需要在离开分支时回溯计数。
6. 最大路径和与直径共享“返回单边结果、更新双边全局答案”的模式。

