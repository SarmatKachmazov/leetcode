from typing import List
from collections import Counter

class Solution:
    def findXSum(self, nums: List[int], k: int, x: int) -> List[int]:
        """
        Return an array answer of length n - k + 1 where answer[i] is the x-sum
        of the subarray nums[i .. i + k - 1].

        Definition (x-sum):
            - Count frequencies of values in the subarray.
            - Keep only the top x most frequent values.
              If frequencies tie, the LARGER value is considered more frequent.
            - The x-sum is the sum of the resulting multiset
              (equivalently: sum_{v in top x} v * freq[v]).

        Simple approach (fits constraints for version I):
            For each window of length k:
              1) build a frequency map,
              2) sort distinct values by (-freq, -value),
              3) take the first x entries and add v * freq[v] to the answer.

        Example:
            nums = [1,1,2,2,3,4,2,3], k = 6, x = 2
            windows:
              [1,1,2,2,3,4] → keep {1 (2x), 2 (2x)} → sum = 1+1+2+2 = 6
              [1,2,2,3,4,2] → keep {2 (3x), 4 (1x)} → sum = 2+2+2+4 = 10
              [2,2,3,4,2,3] → keep {2 (3x), 3 (2x)} → sum = 2+2+2+3+3 = 12
            answer = [6, 10, 12]

        Time complexity:
            For each of (n - k + 1) windows:
              - counting: O(k),
              - sorting distinct values: O(d log d), d ≤ k.
            ⇒ O((n - k + 1) * (k + d log d)) = O(n * k log k) worst case.

        Space complexity:
            O(d) for the frequency map (d ≤ k).
        """
        n = len(nums)
        ans: List[int] = []

        for i in range(n - k + 1):
            window = nums[i:i+k]
            freq = Counter(window)                    # value -> count
            # sort by: highest frequency first, break ties by larger value
            order = sorted(freq.items(), key=lambda p: (-p[1], -p[0]))
            # sum v * freq[v] over top x entries (or all if fewer than x distinct)
            s = 0
            take = min(x, len(order))
            for j in range(take):
                v, c = order[j]
                s += v * c
            ans.append(s)

        return ans