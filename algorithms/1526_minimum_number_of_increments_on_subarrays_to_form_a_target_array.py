from typing import List

class Solution:
    def minNumberOperations(self, target: List[int]) -> int:
        """
        Returns the minimum number of operations to form `target` starting from an all-zero array,
        where one operation increments all elements in a chosen subarray by 1.

        Key idea:
            Each time target[i] rises above target[i-1], we must pay exactly that positive difference,
            because the only way to raise position i (without lowering anything) is to perform
            increments on a subarray covering i. Summing all positive increases builds the exact
            "new height" we need. Flat or descending steps require no extra cost.

        Formula:
            answer = target[0] + sum(max(0, target[i] - target[i-1]) for i = 1..n-1)

        Examples:
            target = [1,2,3,2,1]
            - diffs: +1, +1, 0, 0  → answer = 1 + 1 + 1 = 3

            target = [3,1,1,2]
            - diffs: -, 0, +1     → answer = 3 (first element) + 1 = 4

            target = [0,0,0]
            - all zeros → answer = 0

        Time complexity:  O(n)
            Single pass over the array to sum positive rises.
        Space complexity: O(1)
            Constant extra space.
        """
        if not target:
            return 0

        ops = target[0]
        for i in range(1, len(target)):
            if target[i] > target[i - 1]:
                ops += target[i] - target[i - 1]
        return ops