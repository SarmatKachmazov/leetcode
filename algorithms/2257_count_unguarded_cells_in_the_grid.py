from typing import List, Set, Tuple

class Solution:
    def countUnguarded(self, m: int, n: int, guards: List[List[int]], walls: List[List[int]]) -> int:
        """
        Count cells in an m×n grid that are NOT guarded and NOT occupied (neither guard nor wall).

        Rules:
            - Each guard watches in four directions (up/down/left/right) until a wall or another guard blocks the view.
            - Cells containing walls or guards are not counted as guarded and are not part of the answer.

        Idea (row/column scans):
            1) Put all walls and guards in sets for O(1) membership checks.
            2) For each row, scan left→right and right→left:
               once a guard has been seen, mark all subsequent empty cells as guarded
               until hitting a wall or another guard.
            3) Do the same for each column, top→down and bottom→up.
            4) Count cells that are neither wall nor guard nor marked guarded.

        Example:
            m = 4, n = 6
            guards = [[0,0],[1,1],[2,3]]
            walls  = [[0,1],[2,2],[1,4]]
            → answer = 7

        Time complexity:  O(m * n)
            Four linear passes over rows/columns (two directions each).
        Space complexity: O(g + w + k)
            g = #guards, w = #walls, k = #guarded cells (≤ m*n).
        """
        wall: Set[Tuple[int, int]] = {(r, c) for r, c in walls}
        guard: Set[Tuple[int, int]] = {(r, c) for r, c in guards}
        guarded: Set[Tuple[int, int]] = set()

        # Row scans
        for r in range(m):
            seen_guard = False
            for c in range(n):  # left to right
                cell = (r, c)
                if cell in wall:
                    seen_guard = False
                elif cell in guard:
                    seen_guard = True
                else:
                    if seen_guard:
                        guarded.add(cell)

            seen_guard = False
            for c in range(n - 1, -1, -1):  # right to left
                cell = (r, c)
                if cell in wall:
                    seen_guard = False
                elif cell in guard:
                    seen_guard = True
                else:
                    if seen_guard:
                        guarded.add(cell)

        # Column scans
        for c in range(n):
            seen_guard = False
            for r in range(m):  # top to bottom
                cell = (r, c)
                if cell in wall:
                    seen_guard = False
                elif cell in guard:
                    seen_guard = True
                else:
                    if seen_guard:
                        guarded.add(cell)

            seen_guard = False
            for r in range(m - 1, -1, -1):  # bottom to top
                cell = (r, c)
                if cell in wall:
                    seen_guard = False
                elif cell in guard:
                    seen_guard = True
                else:
                    if seen_guard:
                        guarded.add(cell)

        # Count unguarded & unoccupied cells
        ans = 0
        for r in range(m):
            for c in range(n):
                cell = (r, c)
                if cell not in wall and cell not in guard and cell not in guarded:
                    ans += 1
        return ans