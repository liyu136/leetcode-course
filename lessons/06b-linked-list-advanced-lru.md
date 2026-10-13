# 第 6b 讲：链表进阶——间隔指针、分段反转、归并与 LRU

## 0. 本讲的核心问题

第 6 讲已经掌握遍历、反转、合并、中点、判断环和相交。本讲补齐 Hot 100 的链表进阶模式：

1. 两个指针保持固定距离；
2. 找到环的入口；
3. 反转一段链表，而不是整条链表；
4. 链表上的归并排序；
5. 复制带随机指针的结构；
6. 哈希表与双向链表组合实现 LRU。

链表题最重要的习惯仍然是：**修改 `.next` 之前，先保存之后还要访问的节点。**

---

## 1. 删除倒数第 N 个节点：保持固定间隔

让 `fast` 比 `slow` 先走 `n` 步。当 `fast` 到达末尾时，`slow` 正好位于目标节点之前。

使用虚拟头节点可以统一删除头节点的情况：

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    slow = dummy
    fast = dummy

    for _ in range(n):
        fast = fast.next

    while fast.next is not None:
        slow = slow.next
        fast = fast.next

    slow.next = slow.next.next
    return dummy.next
```

循环不变量：`fast` 与 `slow` 之间始终相隔 `n` 条边。

为什么循环检查 `fast.next`？因为我们需要让 `slow` 停在被删除节点的前一个位置，而不是目标本身。

---

## 2. 环形链表 II：从相遇点找到入口

第一阶段与判断环相同：慢指针走一步，快指针走两步。若相遇，说明存在环。

第二阶段：

1. 一个指针回到链表头；
2. 另一个留在相遇点；
3. 两者都每次走一步；
4. 再次相遇的位置就是环入口。

```python
def detect_cycle(head):
    slow = head
    fast = head

    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            finder = head
            while finder is not slow:
                finder = finder.next
                slow = slow.next
            return finder

    return None
```

设头到入口距离为 `a`，入口到第一次相遇点距离为 `b`，环长为 `c`。相遇时快指针比慢指针多走若干整圈，可以推出 `a` 与“相遇点继续走到入口”的距离相差整圈，所以两个一步指针会在入口相遇。

判断节点身份必须使用 `is`，不能比较节点值。

---

## 3. 两数相加：链表上的竖式加法

每轮处理两个当前数字和进位：

```python
def add_two_numbers(l1, l2):
    dummy = ListNode()
    tail = dummy
    carry = 0

    while l1 is not None or l2 is not None or carry:
        x = l1.val if l1 is not None else 0
        y = l2.val if l2 is not None else 0
        total = x + y + carry

        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next

        if l1 is not None: l1 = l1.next
        if l2 is not None: l2 = l2.next

    return dummy.next
```

循环条件中的 `or carry` 很重要。例如 `5 + 5` 处理完两个节点后仍需创建进位节点 `1`。

---

## 4. 两两交换：先连接，再移动

每次交换 `first` 和 `second`：

```text
previous → first → second → following
```

变成：

```text
previous → second → first → following
```

```python
def swap_pairs(head):
    dummy = ListNode(0, head)
    previous = dummy

    while previous.next is not None and previous.next.next is not None:
        first = previous.next
        second = first.next

        first.next = second.next
        second.next = first
        previous.next = second

        previous = first

    return dummy.next
```

画引用变量比只画节点更重要。交换后 `first` 变成这一组的尾部，所以下一轮 `previous = first`。

---

## 5. K 个一组反转

这道题可以拆成三个操作：

1. 从 `group_previous` 向后确认是否有完整的 `k` 个节点；
2. 反转 `[group_start, group_next)`；
3. 把反转后的组重新接回主链。

```python
def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_previous = dummy

    def get_kth(start, steps):
        current = start
        for _ in range(steps):
            current = current.next
            if current is None:
                return None
        return current

    while True:
        kth = get_kth(group_previous, k)
        if kth is None:
            break

        group_next = kth.next
        previous = group_next
        current = group_previous.next

        while current is not group_next:
            following = current.next
            current.next = previous
            previous = current
            current = following

        old_group_start = group_previous.next
        group_previous.next = kth
        group_previous = old_group_start

    return dummy.next
```

把 `previous` 初始化为 `group_next`，反转完成时原组头会自动指向下一组，不需要再单独补尾部连接。

不足 `k` 个节点的最后一组保持原顺序。

---

## 6. 复制带随机指针的链表

每个节点除 `next` 外还有 `random`，它可能指向链表中任意节点或 `None`。

难点是：复制节点的 `random` 必须指向另一个复制节点，不能仍指向原节点。

第一遍创建所有副本，建立旧节点到新节点的映射；第二遍连接引用：

```python
def copy_random_list(head):
    if head is None:
        return None

    copies = {}
    current = head
    while current is not None:
        copies[current] = Node(current.val)
        current = current.next

    current = head
    while current is not None:
        copy = copies[current]
        copy.next = copies.get(current.next)
        copy.random = copies.get(current.random)
        current = current.next

    return copies[head]
```

这和“克隆图”的本质相同：哈希表既防止重复创建，也保存旧对象到新对象的对应关系。

---

## 7. 排序链表：链表上的归并排序

链表不支持 `O(1)` 随机访问，因此归并排序比依赖下标的排序更自然：

1. 快慢指针找中点并断开；
2. 递归排序左右两半；
3. 合并两个有序链表。

```python
def sort_list(head):
    if head is None or head.next is None:
        return head

    slow = head
    fast = head.next
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next

    right = slow.next
    slow.next = None

    left_sorted = sort_list(head)
    right_sorted = sort_list(right)
    return merge_two_lists(left_sorted, right_sorted)
```

这里让 `fast = head.next`，偶数长度时 `slow` 停在左半部分最后一个节点，便于断链。

时间 `O(n log n)`；递归调用栈通常为 `O(log n)`。

---

## 8. LRU 缓存：哈希表 + 双向链表

LRU 需要两个操作都为 `O(1)`：

- 按键找到缓存节点：哈希表；
- 删除任意节点、把节点移动到最新位置：双向链表。

约定：

```text
head 后面是最久未使用
tail 前面是最近使用
```

```python
class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.nodes = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _append_recent(self, node):
        previous = self.tail.prev
        previous.next = node
        node.prev = previous
        node.next = self.tail
        self.tail.prev = node

    def _mark_recent(self, node):
        self._remove(node)
        self._append_recent(node)

    def get(self, key):
        if key not in self.nodes:
            return -1
        node = self.nodes[key]
        self._mark_recent(node)
        return node.value

    def put(self, key, value):
        if key in self.nodes:
            node = self.nodes[key]
            node.value = value
            self._mark_recent(node)
            return

        node = Node(key, value)
        self.nodes[key] = node
        self._append_recent(node)

        if len(self.nodes) > self.capacity:
            least_recent = self.head.next
            self._remove(least_recent)
            del self.nodes[least_recent.key]
```

两个哨兵节点让头尾插入删除不需要特殊分支。字典和链表必须同步更新，否则会留下已经驱逐的节点。

---

## 9. 本讲检查表

1. 是否需要虚拟头节点统一删除或重连头部？
2. 两个指针之间的距离应保持多少？
3. 修改 `.next` 前是否保存了后继？
4. 反转的是整条链表还是半开区间？
5. 分组不足 `k` 个时应该怎样处理？
6. 复制结构时，新节点是否仍意外指向原节点？
7. LRU 的哈希表和双向链表是否始终包含同一批真实节点？

## 10. 本讲总结

- 固定间隔指针适合倒数位置问题。
- Floyd 第二阶段用于寻找环入口。
- 分段反转的关键是保存组后继，并重新连接组前驱。
- 链表排序自然使用归并。
- 复制任意引用结构时，旧对象到新对象的哈希映射非常重要。
- LRU 是“哈希定位 + 双向链表维护顺序”的经典组合。

