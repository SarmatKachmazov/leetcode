from typing import List

class Solution:
    def minOperations(self, nums: List[int]) -> int:
        """
        Return the minimum number of operations to make all elements zero.

        Operation (from the problem):
            Choose a subarray [i, j] and set all occurrences of the minimum
            non-negative value within that subarray to 0.

        Key idea (monotonic stack):
            Scan left to right and maintain a non-decreasing stack of "active levels".
            - Start with sentinel 0 on the stack (so zeros never add operations).
            - For each num:
                * Pop while stack top > num  (higher levels cannot continue).
                * If stack top < num:
                      we are starting a new positive level → ++answer and push num.
                * If stack top == num: nothing to do.
            The number of times we push a new positive level is exactly the minimal
            number of operations.

        Examples:
            nums = [0, 2]              → answer = 1
            nums = [3, 1, 2, 1]        → answer = 3
            nums = [1, 1, 1]           → answer = 1
            nums = [2, 0, 2]           → answer = 2

        Correctness intuition:
            Any time the current height rises above the last active level, you must
            introduce a new operation that can “paint” (and later zero out) that level.
            When the height drops, higher levels end (pop). Equal height continues.

        Time complexity:  O(n)
        Space complexity: O(n)  (stack)
        """
        ans = 0
        stack = [0]  # sentinel avoids counting zeros as new levels

        for num in nums:
            while stack and stack[-1] > num:
                stack.pop()
            if not stack or stack[-1] < num:
                if num > 0:
                    ans += 1
                stack.append(num)

        return ans