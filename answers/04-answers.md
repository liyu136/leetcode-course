# 第 4 讲参考答案

请先完成 Notebook 并运行测试。重点不是背代码，而是说清栈内元素的含义。

## 1. 手动跟踪

```text
stack = []              stack=[]，x 尚不存在
stack.append(3)         stack=[3]
stack.append(5)         stack=[3,5]
x = stack.pop()         stack=[3]，x=5
stack.append(7)         stack=[3,7]，x=5
x = stack[-1]           stack=[3,7]，x=7
```

`stack[-1]` 只读取栈顶；`stack.pop()` 返回并删除栈顶。

## 2. ArrayStack

```python
class ArrayStack:
    def __init__(self):
        self._items = []

    def push(self, value):
        self._items.append(value)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)
```

每个 `ArrayStack()` 对象拥有自己的 `_items`。`self` 是调用该方法的具体对象。

## 3. 有效括号

```python
def is_valid_parentheses(text):
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
    }
    stack = []

    for ch in text:
        if ch in "([{":
            stack.append(ch)
        else:
            if not stack:
                return False

            if stack.pop() != pairs[ch]:
                return False

    return not stack
```

不变量：`stack` 保存此前尚未匹配的左括号，栈顶是下一个右括号必须优先匹配的元素。

时间 `O(n)`，额外空间最坏 `O(n)`。

## 4. 删除相邻重复字符

```python
def remove_adjacent_duplicates(text):
    stack = []

    for ch in text:
        if stack and stack[-1] == ch:
            stack.pop()
        else:
            stack.append(ch)

    return "".join(stack)
```

不变量：处理完一个前缀后，栈是该前缀完全消除相邻重复字符后的结果。

时间 `O(n)`，额外空间 `O(n)`。

## 5. 逆波兰表达式

```python
def evaluate_rpn(tokens):
    stack = []

    for token in tokens:
        if token not in {"+", "-", "*", "/"}:
            stack.append(int(token))
            continue

        right = stack.pop()
        left = stack.pop()

        if token == "+":
            value = left + right
        elif token == "-":
            value = left - right
        elif token == "*":
            value = left * right
        else:
            value = abs(left) // abs(right)
            if (left < 0) != (right < 0):
                value = -value

        stack.append(value)

    return stack[-1]
```

先弹出的是右操作数。若顺序颠倒，减法和除法会得到不同结果。时间 `O(n)`，空间 `O(n)`。

## 6. MinStack

```python
class MinStack:
    def __init__(self):
        self.values = []
        self.minimums = []

    def push(self, value):
        self.values.append(value)

        if not self.minimums:
            current_min = value
        else:
            current_min = min(value, self.minimums[-1])

        self.minimums.append(current_min)

    def pop(self):
        self.minimums.pop()
        return self.values.pop()

    def top(self):
        return self.values[-1]

    def get_min(self):
        return self.minimums[-1]
```

不变量：两个栈长度相同，`minimums[i]` 等于 `values[:i+1]` 的最小值。

所有操作为 `O(1)`，总空间为 `O(n)`。

也可以用一个栈保存二元组：

```python
(value, minimum_so_far)
```

## 7. 每日温度

```python
def daily_temperatures(temperatures):
    answer = [0] * len(temperatures)
    stack = []

    for today, temperature in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temperature:
            previous_day = stack.pop()
            answer[previous_day] = today - previous_day

        stack.append(today)

    return answer
```

栈保存尚未找到更高温度的下标。从栈底到栈顶，对应温度为非递增。

每个下标只入栈一次、最多出栈一次，因此所有 `while` 的总执行次数是 `O(n)`，整个算法时间为 `O(n)`，额外空间为 `O(n)`。

## 复习重点

第一轮要求独立完成：

1. `ArrayStack`；
2. 有效括号；
3. 删除相邻重复字符。

第二轮要求在少量提示后完成：

1. 逆波兰表达式；
2. MinStack；
3. 每日温度。

隔天复习时，不要先背代码，先写“栈里保存什么”和“什么时候弹栈”。
