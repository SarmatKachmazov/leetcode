class Solution:
    def countOperations(self, num1: int, num2: int) -> int:
        """
        Count how many operations are needed to make either number equal to zero.

        Operation:
            While both numbers are > 0, subtract the smaller one from the larger one.
            Each subtraction counts as one operation.

        Optimization insight:
            Repeated subtraction is equivalent to integer division:
                - If a >= b, then instead of subtracting b many times,
                  we can do (a // b) operations at once, and set a %= b.
                - Otherwise we do the symmetric step for b.
            This reduces the process to the logic of the Euclidean algorithm.

        Examples:
            num1 = 2, num2 = 3
                3 - 2 = 1
                2 - 1 = 1
                1 - 1 = 0
                → total operations = 3

            num1 = 10, num2 = 10
                10 - 10 = 0
                → total operations = 1

        Time complexity:  O(log(max(num1, num2)))
            (Same behavior as the Euclidean algorithm)
        Space complexity: O(1)
        """
        ops = 0
        a, b = num1, num2
        while a and b:
            if a >= b:
                ops += a // b
                a %= b
            else:
                ops += b // a
                b %= a
        return ops