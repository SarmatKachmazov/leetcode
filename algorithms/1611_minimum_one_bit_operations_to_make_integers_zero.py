class Solution:
    def minimumOneBitOperations(self, n: int) -> int:
        """
        Return the minimum number of operations to transform n to 0.

        Operation (from the problem):
            Pick an index i (0-based), and flip bit i and all higher bits (i.e., bits j >= i).

        Key idea (Gray code):
            The shortest sequence of such flips corresponds to walking along a Gray-code path.
            The minimum number of operations equals the value of n converted from Gray to Binary.
            If g is Gray, then binary b is:
                b = g ^ (g >> 1) ^ (g >> 2) ^ ... (until g becomes 0)
            Therefore, answer = gray_to_binary(n).

        Implementation:
            Accumulate XORs while shifting n right.

        Examples:
            n = 0  -> 0
            n = 1 (1)   -> 1
            n = 3 (11)  -> 2
            n = 6 (110) -> 4

        Time complexity:  O(log n)
            We process each bit once.
        Space complexity: O(1)
        """
        ans = 0
        while n:
            ans ^= n
            n >>= 1
        return ans