# 第 10b 讲：Trie 前缀树——按字符路径保存字符串集合

## 0. Trie 解决什么问题

哈希集合可以 `O(1)` 平均判断完整单词是否存在，但不直接支持“是否存在以某前缀开头的单词”。

Trie 将字符串的每个字符看成一条边：

```text
插入 cat、car、dog

root
├─ c ─ a ─ t*
│       └─ r*
└─ d ─ o ─ g*
```

`*` 表示这里是完整单词的结尾。

---

## 1. 节点需要保存什么

每个 Trie 节点保存：

1. 从字符到子节点的映射；
2. 当前节点是否是完整单词结尾。

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False
```

注意：路径存在不代表完整单词存在。例如插入 `apple` 后，前缀 `app` 存在，但单词 `app` 尚未插入。

---

## 2. 插入字符串

从根开始逐字符向下：

```python
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_word = True
```

多个单词共享前缀时会复用同一段路径，这也是 Trie 的主要结构特征。

---

## 3. 搜索完整单词与搜索前缀

把公共遍历提取成辅助函数：

```python
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def _find_node(self, text):
        node = self.root
        for char in text:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def insert(self, word):
        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
        node.is_word = True

    def search(self, word):
        node = self._find_node(word)
        return node is not None and node.is_word

    def startsWith(self, prefix):
        return self._find_node(prefix) is not None
```

区别只有最后一步：

- `search` 必须到达节点且 `is_word == True`；
- `startsWith` 只需路径存在。

---

## 4. 复杂度

设字符串长度为 `L`：

- 插入：`O(L)`；
- 搜索完整单词：`O(L)`；
- 搜索前缀：`O(L)`。

空间与所有新建字符节点数量有关。最坏情况下接近所有字符串总长度；共享前缀越多，复用越明显。

哈希字典子节点适合字符集合不固定的情况。若题目严格限制为小写英文字母，也可使用长度 26 的数组：

```python
index = ord(char) - ord('a')
```

数组访问常数更小，但每个节点都会预留 26 个位置，可能浪费空间。

---

## 5. Trie 与普通树、哈希表的关系

- 从结构看，Trie 是一棵多叉树；
- 从用途看，它是把字符串前缀编码进路径的索引；
- 从实现看，每个节点通常使用哈希表或定长数组保存孩子。

Trie 不是“更高级的哈希表”，而是树与映射的组合。

---

## 6. 常见扩展

### 6.1 记录通过次数

节点增加 `prefix_count`，插入时沿路径加一，可以查询多少单词拥有某前缀。

### 6.2 删除单词

不能简单删除共享节点。通常先减少计数，只有某节点不再被任何单词使用时才安全移除。

### 6.3 通配符搜索

如果查询字符 `.` 可以匹配任意字符，就需要从当前节点递归尝试所有孩子。这时最坏时间不再只是 `O(L)`，因为搜索会产生分支。

---

## 7. 常见错误

1. 只检查路径存在，导致把前缀误认为完整单词。
2. 每次插入都重新创建已有前缀节点，破坏共享结构。
3. 在循环中忘记 `node = node.children[char]`。
4. 使用长度 26 的数组时计算字符下标错误。
5. 删除单词时破坏其他单词共享的前缀。

## 8. 本讲检查表

1. 查询的是完整单词还是前缀？
2. 字符集合固定还是任意？
3. 节点应该使用字典还是定长数组？
4. 是否需要记录单词结束标记？
5. 是否还需要频率、前缀计数或删除功能？

## 9. 本讲总结

- Trie 使用字符路径保存字符串集合。
- 路径存在与完整单词存在是两个不同条件。
- 插入和查询时间都与字符串长度成正比。
- 它特别适合大量前缀查询，是树和哈希映射的组合结构。

