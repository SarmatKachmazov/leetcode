from typing import List
import heapq

class DSU:
    """Disjoint Set Union (Union-Find) with path compression and union by rank."""
    def __init__(self, n: int):
        self.p = list(range(n + 1))
        self.r = [0] * (n + 1)

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1


class Solution:
    def processQueries(self, c: int, connections: List[List[int]], queries: List[List[int]]) -> List[int]:
        """
        Maintain a power grid with `c` stations (IDs 1..c). The graph structure is fixed:
        `connections` are undirected cables. Initially all stations are online.

        Queries:
          - [1, x]: If station x is online → return x.
                     Otherwise, return the smallest online station in the SAME connected component as x.
                     If none exist → return -1.
          - [2, x]: Turn station x offline (idempotent).

        Key idea:
            The topology never changes, so we precompute connected components with DSU (Union-Find).
            For each component, maintain a min-heap of its currently online stations (by ID).
            Turning a station offline is handled by a boolean array `offline[x]` and lazily removing
            it from the heap when it reaches the heap top. For query type [1, x], if x is offline,
            we peek/pop the component heap until we find an online station or the heap becomes empty.

        Example:
            c = 5
            connections = [[1,2],[2,3],[4,5]]
            queries = [[1,3], [2,2], [1,3], [2,1], [1,3], [2,3], [1,3], [1,5]]
            Output   = [3, 1, 3, -1, 5]

        Correctness notes:
            - DSU partitions stations into fixed components.
            - Each component's min-heap stores candidate online IDs; lazy deletion ensures
              every offline ID is removed at most once (when it reaches the top).
            - Query [1, x] uses x directly if online; otherwise uses x's component heap.

        Time complexity (amortized):
            - DSU build:            O((c + |E|) * α(c))
            - Initial heap build:   O(c log c) across all components
            - Each query:           O(log c) amortized (lazy pops occur once per station)
            Overall:                O((c + |E|) α(c) + c log c + |Q| log c)

        Space complexity:
            O(c + |E|) for DSU, heaps, and offline flags.

        Returns:
            A list of integers, one per query of type [1, x].
        """
        # 1) Build DSU to fix components
        dsu = DSU(c)
        for u, v in connections:
            dsu.union(u, v)

        # 2) For each component root, prepare a min-heap of station IDs (all start online)
        comp_heap = {}
        roots = [dsu.find(i) for i in range(1, c + 1)]
        for r in roots:
            if r not in comp_heap:
                comp_heap[r] = []
        for i in range(1, c + 1):
            heapq.heappush(comp_heap[roots[i - 1]], i)

        offline = [False] * (c + 1)
        out: List[int] = []

        def smallest_online(root: int) -> int:
            """Return the smallest online station in component `root`, or -1 if none."""
            h = comp_heap[root]
            while h and offline[h[0]]:
                heapq.heappop(h)
            return h[0] if h else -1

        # 3) Process queries
        for t, x in queries:
            if t == 2:
                if 1 <= x <= c:
                    offline[x] = True  # idempotent
            else:  # t == 1
                if 1 <= x <= c and not offline[x]:
                    out.append(x)
                else:
                    root = dsu.find(x)
                    out.append(smallest_online(root))

        return out