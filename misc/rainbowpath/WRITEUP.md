# Problem Writeup: Shortest Path to Collect Colours

## Problem Statement
You are given a tree with $N$ nodes and $N - 1$ weighted edges. Each node is also coloured from $1$ to $K$. Interestingly, there is an equal number of nodes of each colour.

On a node of colour $X$, you may choose to pick up colour $X$ or not. Find the shortest path on the tree that picks up all $K$ colours in order from $1$ to $K$, starting and ending at any node. You are allowed to traverse the same node or edge multiple times.

Constraints:
- $N = 3 \cdot 10^6$
- $K = 10^5$

---

## Step 1: Noticing the Funny
A somewhat common problem-solving technique in Competitive Programming is "noticing the funny." The line:

> "Interestingly, there is an equal number of nodes of each colour"

hints that we should consider how many nodes each colour has. Given the constraints, this tells us there are exactly $\frac{N}{K} = 30$ nodes of each colour.

---

## Step 2: Competitive Programming Knowledge Test
Since it's a CP problem, it's expected that you know how to compute the shortest path between two nodes $A$ and $B$ in a tree.

The standard approach:
1. Arbitrarily root the tree (e.g., node 1).
2. Use DFS to compute the distance from the root to every node ($\text{dist}[i]$).
3. Use **binary lifting** (aka $2^k$ decomposition in Singapore) to compute the Lowest Common Ancestor (LCA) of two nodes $A$ and $B$.
4. Then,
   $$\text{dist}(A, B) = \text{dist}[A] + \text{dist}[B] - 2 \cdot \text{dist}[\text{LCA}(A, B)]$$

We'll call this function `findDist(A, B)`. Since binary lifting takes $O(\log N)$ time, each call to `findDist` is efficient.

> Since this is a CTF, you can also just rely on AI to fill in your knowledge — even though the author doesn't like AI :(

---

## Step 3: No, You Can't Do Simple Greedy
A naive greedy might try:
- For each colour $X$, pick the shortest edge to some node of colour $X+1$

But this produces a **disjointed** path, not one full path from start to end. You'll miss required segments, and the total path will be underestimated.

---

## Step 4: Consider All Options
To do this properly, you can bruteforce via recursion:

1. Start at any node of colour 1.
2. Try going to each node of colour 2.
3. Then each node of colour 3.
4. And so on...

Let $f(x)$ be the **minimum distance** to start at node $x$ and pick up all colours from $\text{colour}[x]$ to $K$.
Then,
$$f(x) = \min_{y, \text{colour}[y] = \text{colour}[x]+1} (f(y) + \text{dist}(x, y))$$

Finally, take the minimum of $f(x)$ over all $x$ with colour $1$ to get the answer.

### Time Complexity (Naive Recursion)
- Each call to $f(x)$ makes up to 30 calls to the next level
- So total recursive calls: $30^K$
- Each call takes $O(30 \cdot \log N)$ time
- Total time: $O(30^{K+1} \log N)$

This is around $8.61 \times 10^{47714}$ operations — hilariously huge.
Even if every atom in the observable universe were a supercomputer running since the Big Bang, you wouldn't finish in time.

---

## Step 5: Speedup?
Let’s apply **Dynamic Programming (DP)**!

### Insight:
We’re recalculating $f(x)$ multiple times. We can save (memoize) computed values of $f(x)$ so they’re only calculated once.

This drastically cuts down on work.

### Time Complexity (with DP):
- Number of states = number of nodes $= N$
- For each state, we process ~30 options with $O(\log N)$ per option
- Total: $O(N \cdot 30 \cdot \log N)$ = $O(N \log N)$

This results in about $3 \times 10^9$ operations, and after considering the
constant factor of the operations, will result in a runtime of no more than
one minute.

---


