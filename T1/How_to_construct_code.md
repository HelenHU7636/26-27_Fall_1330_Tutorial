# Comments First

> **Always write the comments first.**

The first time you read this problem description, it is natural to come up with the following framework:

```python
# read in input
# people

# budget

# calculate money needed for those people, 30 per person

# result = budget - total

# output:
# if affordable, print remaining
# otherwise, print need
```

This problem is very simple, so some students may think that writing comments like these is unnecessary.

However, when you start working on more complex problems, 

In general, solving a programming problem involves two major parts.

## Part 1: Solve the Problem in Your Head

Before writing actual code, you first need to understand what the program is supposed to do.

This involves two things:

1. **Precisely catch all the problem requirements.**

   You need to know exactly what the input means, what output is required, and what special cases or details must be handled.

2. **Come up with a solution that the computer can execute step by step.**

   In other words, you need to transform the original problem into a clear sequence of operations.

   Sometimes this is straightforward.

   Sometimes the algorithm itself is the hardest part of the problem.

You can think of this stage as building a **flowchart in your head**:

```text
Input
  ↓
Process the information
  ↓
Make decisions
  ↓
Calculate the result
  ↓
Output
```

At this stage, you are solving the **problem logic**, not worrying about Python syntax yet.

---

## Part 2: Translate the Logic into Code

Once the logic is clear, the second task is to express it correctly in Python.

Now you need to think about things such as:

- variables
- expressions
- `if` / `else`
- indentation
- function calls
- syntax
- output format

> **How do I express what I already know in Python?**

---

## Why Write Comments First?

If you skip the comments and immediately start coding, your brain is forced to do both jobs at the same time:

```text
Understand the problem
        +
Design the solution
        +
Remember all requirements
        +
Write correct Python syntax
        +
Avoid implementation mistakes
```

That creates a lot of unnecessary cognitive load.

When the problem becomes complicated, it is very easy to forget a requirement, lose track of the logic, or get stuck in small coding details.

Writing comments first forces you to separate these tasks. Instead of solving everything at once, you deal with **one problem at a time**.

This is essentially a form of **separation of concerns**.

You can also think of it as **“divide and conquer” at the thinking level**:

> Break one complicated task into several smaller and easier tasks.

# STOP 1: What is the problem with that?

Suppose we translate the comments into code very quickly:

```python
people = input()
budget = input()

total = people * 30
result = budget - total
```

**Answer the question to be marked as active participant. BONUS POINTS ADDED!!**

When we run it, Python gives us an error similar to:

```text
TypeError: unsupported operand type(s) for -: 'str' and 'str'
```

`input()` gives us **raw input data**, which in Python is a string.

For example:

```python
people = input()
```

does not mean:

```text
people = 4
```

in the computer's mind.

It means something closer to:

```text
people = "4"
```

The computer does not automatically know that `"4"` is supposed to be used as a number.

---

## Raw Data → Processed Data

**Before data can be used in a mathematical operation**, we often need a processing step:

```text
Raw input
    ↓
Data processing
    ↓
Usable data
    ↓
Calculation
```

In this problem:

```text
"4"
 ↓
int(...)
 ↓
4
 ↓
use it in calculation
```

---

# Python Makes Type Assumptions Easy

In languages such as C++, the type is usually written explicitly when a variable is declared:

```cpp
int people;
int budget;
```

That makes the programmer think about the data type immediately.

Python does not force you to do this:

```python
people = ...
budget = ...
```

This is convenient, but it also makes one kind of mistake very easy:

> You know that the variable represents an integer, so you unconsciously assume that the computer knows too.

It does not.

The computer only knows what you explicitly give it.

So when planning your solution, it is useful to annotate the expected type of important variables:

```python
# people: int
# budget: int
# total: int
# result: int
```

---

# STOP 2: A Formula Is Not Just a Formula

Now suppose we have correctly processed the input.

The next question is:

```python
# result = ?
```

Should it be:

```python
result = budget - total
```

or:

```python
result = total - budget
```

Mathematically, both are valid expressions.

But in programming, we should not choose an expression only because it produces "some difference".

We should ask:

> **What meaning do we want the result to carry?**

If we define:

```python
result = budget - total
```

then the sign of `result` tells us something:

```text
result > 0
→ money is left

result == 0
→ exactly enough money

result < 0
→ money is missing
```

Now one variable carries both the numerical result and useful logical information.

That makes the later decision much easier.

---
# Look for Constraint Words

The first time we read the problem, we only extracted the general idea. But problem descriptions often contain **small words that impose important restrictions**.

For example:

> "N is the **nonnegative** amount left or missing."

So our comments need to become more precise again.

```python
# result = budget - total

# if result >= 0:
#     print the nonnegative amount remaining

# if result < 0:
#     print the nonnegative amount missing
#     missing amount = -result
```

Restrictions are often adjectives, adverbs, numerical limits, or short phrases such as:

```text
nonnegative
exactly
at most
at least
strictly greater than
no more than
one space
on separate lines
inclusive
exclusive
```
Move them into your comments.

For example:

```python
# people: integer from 1 to 4
# budget: integer from 0 to 500

# lunch costs exactly 30 per person

# output N must be nonnegative

# exactly enough money counts as affordable

# use exactly one space after the colon
```

Now the comments contain not only the general logic, but also the important constraints.

---

# STOP 3: What is the problem with that?

Now look at this condition:

```python
if result > 0:
```
**Answer the question to be marked as active participant. BONUS POINTS ADDED!!**


The problem says that having exactly enough money is still affordable.

Therefore:

```text
result == 0
```

belongs to the same case as:

```text
result > 0
```

So the correct condition is:

```python
result >= 0
```

This is a **boundary condition**.

Boundary conditions are extremely common sources of wrong answers.

Typical examples include:

```text
>  vs >=
<  vs <=
n    vs n - 1
first element
last element
empty input
```

A solution may be logically correct in general and still fail because of one boundary case.

---

# Refine the Comments Before Writing the Code

Our first version was:

```python
# read in input
# people

# budget

# calculate money needed for those people

# result = budget - total

# output:
# if affordable, print remaining
# otherwise, print need
```

After checking data types, constraints, meaning, and boundary conditions, it becomes:

```python
# read people as raw input
# convert people to int

# read budget as raw input
# convert budget to int

# total: int
# lunch costs exactly 30 per person
# total = people * 30

# result: int
# result = budget - total

# if result >= 0:
#     budget is sufficient, including exactly enough
#     print "Remaining:" followed by result
#     result is already nonnegative

# else:
#     budget is insufficient
#     print "Need:" followed by -result
#     -result gives the nonnegative amount missing
```

At this point, the problem is almost solved.

The code is now mostly a translation task.

---

# Final Step: Translate Comments into Code

```python
people = int(input())
budget = int(input())

total = people * 30
result = budget - total

if result >= 0:
    print("Remaining:", result)
else:
    print("Need:", -result)
```

Notice how little thinking is required at this stage.

Most of the difficult work has already been done in the comments.

The final code is simply the executable version of the logic we have already designed.