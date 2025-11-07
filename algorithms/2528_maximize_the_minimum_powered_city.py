from typing import List

class Solution:
    def maxPower(self, stations: List[int], r: int, k: int) -> int:
        """
        Maximize the minimum city power after adding at most k new stations.

        Definitions:
            - There are n cities on a line, stations[i] is the number of stations at city i.
            - Each station contributes +1 power to every city within distance r (inclusive).
            - You may place up to k additional stations (anywhere, multiple per city).
            - City power = sum of stations located in [i-r, i+r].
            - Goal: maximize min(power[i]) across all cities.

        Approach (Binary search + greedy feasibility):
            1) Precompute base power per city using a sliding window on `stations`.
               Let base[i] = sum(stations[j]) for j in [i-r, i+r] ∩ [0, n-1].
            2) Binary search answer M = the minimum power we try to achieve.
            3) Feasibility check for a candidate M:
               - Sweep cities left→right, maintaining a running "added effect" `add`
                 from previously placed new stations (via a difference array over cities).
               - At city i, current power = base[i] + add. If it's < M, we must add
                 `need = M - current` new stations so that i (and further cities)
                 receive +need coverage.
               - Where to place them? Place at the farthest position that still helps i,
                 which effectively lets their contribution span cities i..end,
                 where end = min(n-1, i + 2*r). We model this *over cities*:
                     add += need; diff[end+1] -= need
                 (This simulates placing each new station within i+r, but tracked
                  as a range add over cities rather than station positions.)
               - If total used stations > k → infeasible.
            4) Return the largest feasible M.

        Why the range i..i+2r:
            If we place the new stations as far right as allowed (at position i+r, or clipped to n-1),
            their coverage over cities starts no later than i and extends at most to i+2r.

        Example:
            stations = [1,2,4,5,0], r = 1, k = 2
            base power (before add):
                city0: stations[0..1] = 1+2 = 3
                city1: stations[0..2] = 1+2+4 = 7
                city2: stations[1..3] = 2+4+5 = 11
                city3: stations[2..4] = 4+5+0 = 9
                city4: stations[3..4] = 5+0 = 5
            Binary search finds the max minimal power after placing at most 2 new stations.

        Time complexity:
            - Building base powers: O(n)
            - Binary search over answer: ~O(log (max(base)+k))
            - Each feasibility check: O(n)
            → Total: O(n log (max(base)+k))

        Space complexity:
            - O(n) for base powers and the temporary difference array in each check.
        """
        n = len(stations)

        # ---- 1) Precompute base power per city with a sliding window ----
        base = [0] * n
        window = 0
        L = 0
        # initial window covers [0 .. min(n-1, r)]
        for i in range(min(n, r + 1)):
            window += stations[i]
        # fill base[0]
        base[0] = window
        # slide the "stations window" center from city 1..n-1
        for i in range(1, n):
            # move window center from i-1 to i:
            # remove stations leaving the left side
            left_out = i - r - 1
            if left_out >= 0:
                window -= stations[left_out]
            # add stations entering on the right side
            right_in = i + r
            if right_in < n:
                window += stations[right_in]
            base[i] = window

        # ---- 2) Binary search on the answer (minimum power) ----
        lo = 0
        hi = max(base) + k  # safe upper bound: one city can be covered by all k new stations

        def feasible(M: int) -> bool:
            """Greedy: can we make every city's power >= M using ≤ k new stations?"""
            used = 0
            add = 0
            # difference array over cities to turn range adds into O(1) updates
            diff = [0] * (n + 1)

            for i in range(n):
                add += diff[i]  # apply previously scheduled increments ending/starting here
                current = base[i] + add
                if current < M:
                    need = M - current
                    used += need
                    if used > k:
                        return False
                    add += need  # starting now, every city gets +need until 'end'
                    end = min(n - 1, i + 2 * r)
                    diff[end + 1] -= need  # stop contributing after 'end'
            return True

        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo