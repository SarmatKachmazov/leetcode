from typing import List

class Solution:
    def getSneakyNumbers(self, nums: List[int]) -> List[int]:
        """
        Returns the two numbers that appear exactly twice in the given array.

        Problem facts:
            - The array contains integers in the range [0, n - 1].
            - Exactly two distinct numbers appear twice.
            - All other numbers appear exactly once.
            - We only need to return those two duplicated numbers (order does not matter).

        Idea:
            Use a frequency counter. Each time a number reaches a count of 2,
            add it to the result. Since the problem guarantees exactly two such
            numbers, we can stop early once we have both.

        Example:
            nums = [0, 3, 2, 1, 3, 2]
            The numbers 3 and 2 each appear twice → answer = [3, 2]

        Time complexity:  O(n)
            Single pass through the array.
        Space complexity: O(k)
            k = size of the value range. Since the problem bounds are small,
            this is effectively O(1) extra space.

        Returns:
            A list of exactly two integers in any order.
        """
        freq = [0] * (max(nums) + 1)
        res: List[int] = []

        for x in nums:
            freq[x] += 1
            if freq[x] == 2:
                res.append(x)
                if len(res) == 2:  # exactly two duplicated numbers guaranteed
                    break

        return res