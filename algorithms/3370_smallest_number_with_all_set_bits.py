class Solution:
    def smallestNumber(self, n: int) -> int:
        """
        Finds the smallest number >= n that has all bits set to 1 in its binary form.

        Examples:
            n = 5  -> binary 101  -> result = 7  (111)
            n = 10 -> binary 1010 -> result = 15 (1111)
            n = 3  -> binary 11   -> result = 3  (already all ones)

        Algorithm:
            1. Start with x = 1 (binary: 1)
            2. While (x - 1) is less than n:
                - Multiply x by 2
            3. When (x - 1) >= n, return (x - 1)
               because it will be the smallest number like 1, 3, 7, 15, etc.

        Time complexity:  O(log n)
            Each iteration doubles x, so the number of steps
            equals the number of bits in n.
        Space complexity: O(1)
            Uses only constant additional memory.
        """
        x = 1
        while x - 1 < n:
            x = x * 2  # multiply by 2 each step
        return x - 1