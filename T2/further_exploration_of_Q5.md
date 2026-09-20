# How to treat the input so that it can naturally fulfill all requirements?

One advantage of rebuilding the result as an integer is that leading zeros disappear naturally. For example:

```text
007 → 7
020 → 20
000 → 0
```

This matches the output requirement of the question.

However, there is an important limitation to this approach: **it works conveniently here because the question tells us that the code always contains exactly three digits.**

If the number of digits were not fixed, writing separate variables such as `h`, `t`, and `u` would no longer be practical. We would normally process the digits using a loop.

## version 1

### Question 1: Do we know in advance how many times we need to loop?

A for loop with a fixed number of repetitions is not the most natural choice.

We need a while loop.

**But a while loop needs a condition.**

### Question 2: How to create a ending condition?

You need a **variable** which stores a value that changes monotonically (in a consistent direction) toward a termination condition.

For example:

789
↓
78
↓
7
↓
0

Once the number becomes 0, there are no digits left to process.

So a natural condition is:

while number > 0:

### The number needs to be updated each turn, which is called "iteration"

```python
digit = number % 10
number = number // 10
```

**Each repetition extracts the last digit and then removes it from the number.** This allows us to process a number with an arbitrary number of digits.

## version 2

Alternatively, we could convert the number to a string and iterate through its characters:

```python
for digit in str(number):
    ...
```

### Can We Simply Ignore Zero?

Suppose we have a sequence of digits and want to remove the leading zeros.

A first attempt might be:

result = ""

for digit in code:
    if digit != "0":
        result += digit

For example:

007 → 7

It seems to work.

But before accepting this solution, we should ask an important question:

### Can we construct a test case that makes this program fail?

Instead of choosing a random input, think about the **assumption made by the program.**

This program assumes that:

Every zero can be removed.

So we should deliberately construct a case **where a zero is important**.

For example:

101

The program produces:

11

which is incorrect.

The zero in 101 is not a leading zero. It is part of the number and must be preserved.

Similarly:

700

must remain:

700

The zeros at the end are trailing zeros, and they cannot be removed either.

### How can we distinguish a leading zero from an important zero?

Think about when a zero **stops being a leading zero**.

Once we have reached the first non-zero digit, any zero that appears afterwards must be kept.

Therefore, we can use a Boolean flag to remember whether the first non-zero digit has already been reached.

```python
result = ""
leading = True

for digit in code:
    if leading and digit == "0":
        continue

    leading = False
    result += digit

Consider:

00102

The process is:

0    leading = True   → skip
0    leading = True   → skip
1    first non-zero   → leading becomes False
0    leading = False  → keep
2    leading = False  → keep

So the result is:

102

The key idea is that **the meaning of 0 depends on where it appears**.
```

### We fixed `101`. Can anyone find another input that still breaks our new solution?




There is still a hidden assumption: there is always nonzero number in the input.

```python
if result == "":
    result = "0"
```

### Designing Better Test Cases

Try to identify the assumptions made by your solution and deliberately construct inputs that challenge them.

For this problem, useful test cases include:

007   # leading zeros
101   # zero in the middle
700   # trailing zeros
123   # no zeros
000   # all zeros

Each test case checks a different situation.

**A good test case is designed to expose a possible mistake, not just to show that the program works on a normal input.**


```python
code = input()

h = int(code[0])
t = int(code[1])
u = int(code[2])
```

### What assumption does this code make?

Code contains at least three characters.

Now ask:

**Does the problem actually guarantee that the input will contain three characters?**

No.

The problem says that the code should be treated as three digits, but the input itself is still given as an integer from 0 to 999.

For example, if the user enters:

7

then:

code = input()

stores:

"7"

not:

"007"

Therefore:

code[0]   # works
code[1]   # IndexError
code[2]   # IndexError

This gives us an important way to construct test cases.

### Does the representation stored in my program actually match the representation required by the problem?

We may need to create them explicitly:

```python
code = input().zfill(3)
```

For example:

"7".zfill(3)

becomes:

"007"

### A Useful Habit

Whenever you use operations such as:

list[index]
string[index]

ask yourself:

Am I sure this index always exists?

# Thinking Deeper About Modulo: From Cycles to State Compression

We often learn modulo `%` as an operation that gives the remainder:

```python
17 % 5
```

gives:

```text
2
```

This is correct, but it is not the most useful way to think about modulo when solving problems.

---

### 1. Start from the rotating lock

For a ten-state lock:

```text
0, 10, 20, 30, ...   behave the same
1, 11, 21, 31, ...   behave the same
2, 12, 22, 32, ...   behave the same
...
9, 19, 29, 39, ...   behave the same
```
> **If several different numbers always behave in the same way, do we really need to distinguish between them?**

---

### 2. Which values are actually different?

but from the lock's point of view, there are only ten meaningful states.

Modulo performs exactly this reduction:

```python
value % 10
```

maps every possible integer into:

```text
0, 1, 2, ..., 9
```

So:

```text
2 % 10  = 2
12 % 10 = 2
22 % 10 = 2
32 % 10 = 2
```

It is saying:

> **These values are different numerically, but they are equivalent for this problem.**

---

## 3. Modulo as State Compression

```text
Many possible values
        ↓
Discard information that does not affect the result
        ↓
Keep only the meaningful state
```

### The important question to ask?
**When do two different values become indistinguishable in this problem?**
**Do not keep information that cannot affect the answer.**
